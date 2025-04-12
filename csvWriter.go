package main

import (
	"encoding/base64"
	"encoding/csv"
	"fmt"
	"os"
	"strings"
)

// LoadExistingMetadata loads existing metadata from the CSV
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
		if len(record) >= 1 {
			// Just store the filename as key to track which files have been processed
			data[record[0]] = "processed"
		}
	}
	return data, nil
}

func WriteCSVWithExistingMetadata(csvPath string, existingMetadata map[string]string, responses chan []string) error {
	// First, collect all the data we need to write
	var records [][]string

	// Add header
	records = append(records, []string{"Filename", "Title", "Keywords", "Category", "Releases"})

	// Read existing records if the file exists
	existingFile, err := os.Open(csvPath)
	if err == nil {
		defer existingFile.Close()
		reader := csv.NewReader(existingFile)
		existingRecords, err := reader.ReadAll()
		if err == nil && len(existingRecords) > 1 {
			// Skip header row and add all existing records
			records = append(records, existingRecords[1:]...)
		}
	}

	// Add new records from responses
	for terms := range responses {
		if len(terms) >= 5 {
			filename := terms[0]
			// Skip if already wrote existing metadata
			if _, exists := existingMetadata[filename]; !exists {
				records = append(records, terms)
			}
		}
	}

	// Now write all records to the file
	file, err := os.Create(csvPath)
	if err != nil {
		return fmt.Errorf("failed to create CSV file: %w", err)
	}
	defer file.Close()

	// Write each record manually with minimal quoting
	for i, record := range records {
		for j, field := range record {
			// Check if the field needs quoting (contains comma, newline, or quote)
			needsQuoting := strings.ContainsAny(field, ",\"\r\n")

			if needsQuoting {
				// Escape quotes by doubling them and wrap in quotes
				field = strings.ReplaceAll(field, "\"", "\"\"")
				_, err := file.WriteString("\"" + field + "\"")
				if err != nil {
					return fmt.Errorf("failed to write quoted field to CSV: %w", err)
				}
			} else {
				// Write the field without quotes
				_, err := file.WriteString(field)
				if err != nil {
					return fmt.Errorf("failed to write field to CSV: %w", err)
				}
			}

			// Add comma if not the last field
			if j < len(record)-1 {
				_, err := file.WriteString(",")
				if err != nil {
					return fmt.Errorf("failed to write delimiter to CSV: %w", err)
				}
			}
		}

		// Add newline after each record (Windows style for better compatibility)
		if i < len(records)-1 {
			_, err := file.WriteString("\r\n")
			if err != nil {
				return fmt.Errorf("failed to write newline to CSV: %w", err)
			}
		}
	}

	return nil
}

// EncodeImageToBase64 reads an image file and encodes it to a base64 string
func EncodeImageToBase64(filePath string) (string, error) {
	data, err := os.ReadFile(filePath)
	if err != nil {
		return "", fmt.Errorf("error reading file: %w", err)
	}
	return base64.StdEncoding.EncodeToString(data), nil
}
