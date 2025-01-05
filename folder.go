package main

import (
	"archive/zip"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"sync"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/widget"
)

var images []Image
var currentIndex int

func createSelectFolderButton(label *widget.Label, w fyne.Window) *widget.Button {
	return widget.NewButton("Select Folder", func() {
		dialog.ShowFolderOpen(func(uri fyne.ListableURI, err error) {
			if uri != nil {
				folderPath := uri.Path()
				zipFiles := checkForZipFiles(folderPath)

				if len(zipFiles) > 0 {
					err := processZipFilesConcurrently(folderPath, zipFiles)
					if err != nil {
						dialog.ShowError(err, w)
						label.SetText("Error during extraction.")
						return
					}
					label.SetText(fmt.Sprintf("Processed ZIPs and found %d images.", len(images)))
				} else {
					processImagesInFolder(folderPath)
					label.SetText(fmt.Sprintf("Found %d images in folder.", len(images)))
				}
			}
		}, w)
	})
}

func checkForZipFiles(folderPath string) []string {
	entries, _ := os.ReadDir(folderPath)
	var zipFiles []string

	for _, entry := range entries {
		if !entry.IsDir() && filepath.Ext(entry.Name()) == ".zip" {
			zipFiles = append(zipFiles, filepath.Join(folderPath, entry.Name()))
		}
	}

	return zipFiles
}

func processZipFilesConcurrently(folderPath string, zipFiles []string) error {
	var wg sync.WaitGroup
	errors := make(chan error, len(zipFiles))

	for _, zipFilePath := range zipFiles {
		wg.Add(1)
		go func(zipPath string) {
			defer wg.Done()
			if err := unzip(zipPath, folderPath); err != nil {
				errors <- fmt.Errorf("failed to unzip %s: %w", zipPath, err)
				return
			}
			if err := os.Remove(zipPath); err != nil {
				errors <- fmt.Errorf("failed to delete zip file %s: %w", zipPath, err)
				return
			}
		}(zipFilePath)
	}

	wg.Wait()
	close(errors)

	// Collect and return the first error if any
	if len(errors) > 0 {
		return <-errors
	}

	processImagesInFolder(folderPath)
	return nil
}

func processImagesInFolder(folderPath string) {
	entries, _ := os.ReadDir(folderPath)
	images = nil

	for _, entry := range entries {
		if !entry.IsDir() {
			name := entry.Name()
			if ext := filepath.Ext(name); ext == ".jpg" || ext == ".jpeg" || ext == ".png" {
				fullPath := filepath.Join(folderPath, name)
				images = append(images, Image{Path: fullPath, URL: "file://" + fullPath})
			}
		}
	}

	currentIndex = 0
}

func unzip(src string, dest string) error {
	r, err := zip.OpenReader(src)
	if err != nil {
		return err
	}
	defer r.Close()

	for _, f := range r.File {
		fpath := filepath.Join(dest, f.Name)

		if f.FileInfo().IsDir() {
			if err := os.MkdirAll(fpath, os.ModePerm); err != nil {
				return err
			}
			continue
		}

		if err := os.MkdirAll(filepath.Dir(fpath), os.ModePerm); err != nil {
			return err
		}

		outFile, err := os.OpenFile(fpath, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, f.Mode())
		if err != nil {
			return err
		}
		defer outFile.Close()

		rc, err := f.Open()
		if err != nil {
			return err
		}
		defer rc.Close()

		if _, err := io.Copy(outFile, rc); err != nil {
			return err
		}
	}

	return nil
}
