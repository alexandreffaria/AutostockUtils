package metadata

import (
	"encoding/base64"
	"encoding/csv"
	"fmt"
	"os"
)

// LoadExistingMetadata loads existing metadata from the CSV ;* XOXO Cursor
func LoadExistingMetadata(csvPath string) (map[string]string, error) {
	file, err := os.Open(csvPath)
	if err != nil {
		if os.IsNotExist(err) {
			return make(map[string]string), nil
		}
		return nil, err
	}
	defer file.Close()

	reader := csv.NewReader(file)
	records, err := reader.ReadAll()
	if err != nil {
		return nil, err
	}

	data := make(map[string]string)
	for _, record := range records[1:] {
		if len(record) >= 2 {
			data[record[0]] = record[1]
		}
	}
	return data, nil
}

// WriteCSVWithExistingMetadata writes metadata to CSV while preserving existing entries ;* XOXO Cursor
func WriteCSVWithExistingMetadata(csvPath string, existingMetadata map[string]string, responses chan []string) error {
	file, err := os.Create(csvPath)
	if err != nil {
		return fmt.Errorf("failed to create CSV file: %w", err)
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	// Write header
	if err := writer.Write([]string{"Filename", "Description"}); err != nil {
		return fmt.Errorf("failed to write CSV header: %w", err)
	}

	// Write existing metadata first
	for filename, description := range existingMetadata {
		if err := writer.Write([]string{filename, description}); err != nil {
			return fmt.Errorf("failed to write existing record to CSV: %w", err)
		}
	}

	// Write new metadata
	for terms := range responses {
		filename := terms[0]
		description := terms[1]
		// Skip if already wrote existing metadata
		if _, exists := existingMetadata[filename]; !exists {
			if err := writer.Write([]string{filename, description}); err != nil {
				return fmt.Errorf("failed to write record to CSV: %w", err)
			}
		}
	}

	return nil
}

// EncodeImageToBase64 reads an image file and encodes it to a base64 string ;* XOXO Cursor
func EncodeImageToBase64(filePath string) (string, error) {
	data, err := os.ReadFile(filePath)
	if err != nil {
		return "", fmt.Errorf("error reading file: %w", err)
	}
	return base64.StdEncoding.EncodeToString(data), nil
}
