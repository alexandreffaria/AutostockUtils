package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"
)

type Image struct {
	Path        string
	URL         string
	Description string
	Title       string
	Keywords    string
	Category    string
}

// Helper function to make OpenAI API calls
func fetchFromOpenAI(apiURL, apiKey, prompt string) (string, error) {
	requestBody, err := json.Marshal(map[string]interface{}{
		"model": "gpt-4o-mini",
		"messages": []map[string]interface{}{
			{
				"role":    "user",
				"content": prompt,
			},
		},
		"max_tokens": 200,
	})
	if err != nil {
		return "", fmt.Errorf("error creating request body: %w", err)
	}

	req, err := http.NewRequest("POST", apiURL, bytes.NewBuffer(requestBody))
	if err != nil {
		return "", fmt.Errorf("error creating request: %w", err)
	}
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+apiKey)

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return "", fmt.Errorf("error sending request: %w", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("error reading response: %w", err)
	}

	responseData := map[string]interface{}{}
	if err := json.Unmarshal(body, &responseData); err != nil {
		return "", fmt.Errorf("error unmarshalling response: %w", err)
	}

	if choices, ok := responseData["choices"].([]interface{}); ok && len(choices) > 0 {
		choice := choices[0].(map[string]interface{})
		if message, ok := choice["message"].(map[string]interface{}); ok {
			if content, ok := message["content"].(string); ok {
				return content, nil
			}
		}
	}
	return "", fmt.Errorf("error parsing API response")
}

// FetchImageMetadata retrieves titles, keywords, and categories for images based on filenames and writes results to CSV
func FetchImageMetadata(images []Image) error {
	apiKey := os.Getenv("OPENAI_API_KEY")
	if apiKey == "" {
		return fmt.Errorf("OPENAI_API_KEY not set")
	}

	if len(images) == 0 {
		return fmt.Errorf("no images to process")
	}

	// Create CSV filename based on folder name
	folderName := filepath.Base(filepath.Dir(images[0].Path))
	csvPath := filepath.Join(filepath.Dir(images[0].Path), folderName+"_adobe.csv")
	existingMetadata, err := LoadExistingMetadata(csvPath)
	if err != nil {
		return fmt.Errorf("failed to load existing metadata: %w", err)
	}

	apiURL := "https://api.openai.com/v1/chat/completions"
	descriptionChan := make(chan []string, len(images))
	errorChan := make(chan error, len(images))
	rateLimiter := time.NewTicker(time.Second / 80) // Create a ticker for rate limiting
	defer rateLimiter.Stop()
	var wg sync.WaitGroup

	// Number of concurrent workers
	concurrentWorkers := 10
	workChan := make(chan Image, len(images))

	// Worker function
	for i := 0; i < concurrentWorkers; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for img := range workChan {
				<-rateLimiter.C
				fileName := filepath.Base(img.Path)
				if _, exists := existingMetadata[fileName]; exists {
					fmt.Printf("Skipping image %s as it already has metadata\n", fileName)
					continue
				}

				// Get the manipulated filename
				manipulatedName := manipulateFileName(img.Path)

				// First, get an image description based on the manipulated filename
				descriptionPrompt := fmt.Sprintf("Describe in detail a stock photo based on this description: '%s'", manipulatedName)
				imageDescription, err := fetchFromOpenAI(apiURL, apiKey, descriptionPrompt)
				if err != nil {
					errorChan <- fmt.Errorf("error fetching description for %s: %w", img.Path, err)
					return
				}

				// Then, fetch the title based on the image description - request a simple descriptive title without commentary
				titlePrompt := fmt.Sprintf("Create a simple, descriptive title for a stock photo based on this description: '%s'. Respond ONLY with the title - no commentary, no colons, no explanations, just a simple descriptive phrase.", imageDescription)
				title, err := fetchFromOpenAI(apiURL, apiKey, titlePrompt)
				if err != nil {
					errorChan <- fmt.Errorf("error fetching title for %s: %w", img.Path, err)
					return
				}
				// Clean up the title - remove quotes, commas, colons, and extra spaces
				title = cleanupText(title)

				// Remove any commentary or formatting from the title
				title = removeCommentaryFromTitle(title)

				// Then, use the image description to fetch keywords
				keywordsPrompt := fmt.Sprintf("Generate 5-10 SEO-friendly keywords or tags for this stock photo described as: '%s'. Separate keywords with commas.", imageDescription)
				keywords, err := fetchFromOpenAI(apiURL, apiKey, keywordsPrompt)
				if err != nil {
					errorChan <- fmt.Errorf("error fetching keywords for %s: %w", img.Path, err)
					return
				}
				// Clean up the keywords - remove trailing periods and extra spaces
				keywords = cleanupText(keywords)

				// Get category for Adobe
				categoryPrompt := fmt.Sprintf("Categorize this stock photo for Adobe Stock based on this description: '%s'. Choose one of the following categories and respond ONLY with the category name (no numbers, no explanations): Animals, Buildings and Architecture, Business, Drinks, Environment, Feelings, Emotions, and Mental States, Food, Graphic Resources, Hobbies and Leisure, Industry, Landscapes, Lifestyle, People, Plants and Flowers, Religion and Culture, Science, Social Issues, Sports, Technology, Transportation, Travel", imageDescription)
				category, err := fetchFromOpenAI(apiURL, apiKey, categoryPrompt)
				if err != nil {
					errorChan <- fmt.Errorf("error fetching category for %s: %w", img.Path, err)
					return
				}

				// Extract just the category name without numbers or explanations
				category = extractCategoryName(category)

				// Send the data to the channel
				descriptionChan <- []string{fileName, title, keywords, category, ""}
			}
		}()
	}

	// Enqueue images for processing
	for _, image := range images {
		workChan <- image
	}
	close(workChan)
	wg.Wait()
	close(descriptionChan)
	close(errorChan)

	fmt.Printf("Processing complete. CSV file created successfully: %s\n", csvPath)

	// Write descriptions to the CSV
	if err := WriteCSVWithExistingMetadata(csvPath, existingMetadata, descriptionChan); err != nil {
		return err
	}

	for err := range errorChan {
		if err != nil {
			fmt.Println("Error:", err)
		}
	}

	return nil
}

// extractCategoryName extracts just the category name from the API response
func extractCategoryName(response string) string {
	// First, clean up the response
	response = strings.TrimSpace(response)

	// Try to extract the category using various patterns

	// Clean up common formatting
	re := strings.NewReplacer("**", "", "*", "", "\"", "", "'", "")
	response = re.Replace(response)

	// Pattern 1: Category name after a colon
	if idx := strings.Index(response, ":"); idx != -1 {
		response = strings.TrimSpace(response[idx+1:])
	}

	// Pattern 2: Remove number prefix if present (e.g., "12. Lifestyle")
	if idx := strings.Index(response, "."); idx != -1 && idx < 4 {
		// Check if there's a number before the dot
		prefix := response[:idx]
		if _, err := fmt.Sscanf(prefix, "%d", new(int)); err == nil {
			response = strings.TrimSpace(response[idx+1:])
		}
	}

	// Return the cleaned response
	return response
}

// cleanupText removes quotes, trailing punctuation, and normalizes spaces
func cleanupText(text string) string {
	// Trim spaces first
	text = strings.TrimSpace(text)

	// Remove quotes
	text = strings.ReplaceAll(text, "\"", "")
	text = strings.ReplaceAll(text, "'", "")

	// Remove trailing punctuation
	text = strings.TrimSuffix(text, ".")
	text = strings.TrimSuffix(text, ",")

	// Normalize spaces
	text = strings.TrimSpace(text)

	return text
}

// removeCommentaryFromTitle removes any commentary or formatting from the title
func removeCommentaryFromTitle(title string) string {
	// Remove any text before a colon (common pattern in commentary)
	if idx := strings.Index(title, ":"); idx != -1 {
		title = strings.TrimSpace(title[idx+1:])
	}

	// Remove phrases like "Title:" or "Description:"
	prefixes := []string{"Title:", "Description:", "Photo of", "Image of", "Picture of", "A photo of", "An image of"}
	for _, prefix := range prefixes {
		if strings.HasPrefix(strings.ToLower(title), strings.ToLower(prefix)) {
			title = strings.TrimSpace(title[len(prefix):])
		}
	}

	// Remove quotes if they wrap the entire title
	if strings.HasPrefix(title, "\"") && strings.HasSuffix(title, "\"") {
		title = title[1 : len(title)-1]
	}
	if strings.HasPrefix(title, "'") && strings.HasSuffix(title, "'") {
		title = title[1 : len(title)-1]
	}

	return strings.TrimSpace(title)
}
