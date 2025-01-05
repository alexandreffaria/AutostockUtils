package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"sync"
	"time"
)

type Image struct {
	Path        string
	URL         string
	Description string
}

// FetchImageMetadata retrieves descriptions for images and writes results to CSV
func FetchImageMetadata(images []Image) error {
	apiKey := os.Getenv("OPENAI_API_KEY")
	if apiKey == "" {
		return fmt.Errorf("OPENAI_API_KEY not set")
	}

	if len(images) == 0 {
		return fmt.Errorf("no images to process")
	}

	csvPath := filepath.Join(filepath.Dir(images[0].Path), "metadata.csv")
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

	// Define FetchDescription function
	FetchDescription := func(apiURL, apiKey string, img Image) (string, error) {
		encodedImage, err := EncodeImageToBase64(img.Path)
		if err != nil {
			return "", fmt.Errorf("error encoding image: %w", err)
		}

		requestBody, err := json.Marshal(map[string]interface{}{
			"model": "gpt-4o-mini",
			"messages": []map[string]interface{}{
				{
					"role": "user",
					"content": []map[string]interface{}{
						{"type": "text", "text": "Provide a concise description for this image."},
						{
							"type": "image_url",
							"image_url": map[string]string{
								"url": fmt.Sprintf("data:image/jpeg;base64,%s", encodedImage),
							},
						},
					},
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
		return "", fmt.Errorf("error parsing description response")
	}

	// Worker function
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

				// Fetch Description
				description, err := FetchDescription(apiURL, apiKey, img)
				if err != nil {
					errorChan <- fmt.Errorf("error fetching description for %s: %w", img.Path, err)
					return
				}

				descriptionChan <- []string{fileName, description}
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
