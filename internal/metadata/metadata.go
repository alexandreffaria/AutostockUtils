package metadata

import (
	"bytes"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"sync"
	"time"
)

// Image represents an image with associated metadata ;* XOXO Cursor
type Image struct {
	Path        string
	Title       string
	Description string
	Keywords    string
	Country     string
}

// fetchFromOpenAI makes an API call to OpenAI to generate text based on the given prompt ;* XOXO Cursor
func fetchFromOpenAI(apiURL, apiKey, prompt string) (string, error) {
	requestBody, err := json.Marshal(map[string]interface{}{
		"model": "gpt-4o-mini",
		"messages": []map[string]interface{}{
			{"role": "user", "content": prompt},
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

	var responseData map[string]interface{}
	if err := json.Unmarshal(body, &responseData); err != nil {
		return "", fmt.Errorf("error unmarshalling response: %w", err)
	}

	if choices, ok := responseData["choices"].([]interface{}); ok && len(choices) > 0 {
		if choice, ok := choices[0].(map[string]interface{}); ok {
			if message, ok := choice["message"].(map[string]interface{}); ok {
				if content, ok := message["content"].(string); ok {
					return content, nil
				}
			}
		}
	}
	return "", fmt.Errorf("error parsing API response")
}

// FetchImageMetadata processes the provided images, fetching metadata for each image via OpenAI,
// and then writes the results to a CSV file in Adobe's format ;* XOXO Cursor
func FetchImageMetadata(images []Image) error {
	apiKey := os.Getenv("OPENAI_API_KEY")
	if apiKey == "" {
		return fmt.Errorf("OPENAI_API_KEY not set")
	}

	if len(images) == 0 {
		return fmt.Errorf("no images to process")
	}

	// Define CSV path (in the same folder as the first image)
	csvPath := filepath.Join(filepath.Dir(images[0].Path), "metadata_adobe.csv")
	outputFile, err := os.OpenFile(csvPath, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
	if err != nil {
		return fmt.Errorf("failed to open CSV file: %w", err)
	}
	defer outputFile.Close()

	writer := csv.NewWriter(outputFile)
	defer writer.Flush()

	// If the CSV file is empty, write the header row.
	fileStat, err := outputFile.Stat()
	if err != nil {
		return err
	}
	if fileStat.Size() == 0 {
		header := []string{
			"Filename", "Image Name", "Description", "Category 1", "Category 2",
			"Category 3", "Keywords", "Free", "W-EL", "P-EL", "SR-EL", "SR-Pice",
			"Editorial", "MR doc Ids", "Pr Docs",
		}
		if err := writer.Write(header); err != nil {
			return err
		}
	}

	apiURL := "https://api.openai.com/v1/chat/completions"
	descriptionChan := make(chan []string, len(images))
	errorChan := make(chan error, len(images))
	rateLimiter := time.NewTicker(time.Second / 80) // Rate limiting: adjust as needed
	defer rateLimiter.Stop()

	var wg sync.WaitGroup
	concurrentWorkers := 10
	workChan := make(chan Image, len(images))

	// Worker goroutines: fetch title and keywords, then send a CSV row to descriptionChan.
	for i := 0; i < concurrentWorkers; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for img := range workChan {
				<-rateLimiter.C

				// Create a title prompt using the image filename.
				titlePrompt := fmt.Sprintf("Create a concise, marketable title for a stock photo based on its filename: '%s'", filepath.Base(img.Path))
				title, err := fetchFromOpenAI(apiURL, apiKey, titlePrompt)
				if err != nil {
					errorChan <- fmt.Errorf("error fetching title for %s: %w", img.Path, err)
					continue
				}

				// Create a keywords prompt based on the generated title.
				keywordsPrompt := fmt.Sprintf("Generate 5-10 SEO-friendly keywords for this stock photo titled: '%s'. Separate with commas.", title)
				keywords, err := fetchFromOpenAI(apiURL, apiKey, keywordsPrompt)
				if err != nil {
					errorChan <- fmt.Errorf("error fetching keywords for %s: %w", img.Path, err)
					continue
				}

				// For demonstration, we assign a fixed category.
				category := "Stock Photography"

				// Combine title and keywords into a description.
				description := fmt.Sprintf("Title: %s\nKeywords: %s", title, keywords)

				// Build the CSV row according to Adobe's required format.
				row := []string{
					filepath.Base(img.Path), // Filename
					title,                   // Image Name
					description,             // Description
					category,                // Category 1
					"212",                   // Category 2 (example fixed code)
					"",                      // Category 3
					keywords,                // Keywords
					"0",                     // Free
					"1",                     // W-EL
					"1",                     // P-EL
					"0",                     // SR-EL
					"0",                     // SR-Pice
					"0",                     // Editorial
					"",                      // MR doc Ids
					"",                      // Pr Docs
				}
				descriptionChan <- row
			}
		}()
	}

	// Enqueue images for processing.
	for _, image := range images {
		workChan <- image
	}
	close(workChan)

	wg.Wait()
	close(descriptionChan)
	close(errorChan)

	// Write rows from descriptionChan to CSV.
	for row := range descriptionChan {
		if err := writer.Write(row); err != nil {
			return fmt.Errorf("error writing to CSV: %w", err)
		}
	}

	// Print any errors encountered during processing.
	for err := range errorChan {
		if err != nil {
			fmt.Println("Error:", err)
		}
	}

	return nil
}
