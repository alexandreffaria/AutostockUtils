package main

import (
	"archive/zip"
	"fmt"
	"io"
	"os"
	"path/filepath"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/widget"
)

var images []string
var currentIndex int

func createSelectFolderButton(label *widget.Label, w fyne.Window) *widget.Button {
	return widget.NewButton("Select Folder", func() {
		dialog.ShowFolderOpen(func(uri fyne.ListableURI, err error) {
			if uri != nil {
				folderPath := uri.Path()
				zipFiles := checkForZipFiles(folderPath)

				if len(zipFiles) > 0 {
					err := processZipFiles(folderPath, zipFiles)
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

func processZipFiles(folderPath string, zipFiles []string) error {
	for _, zipFilePath := range zipFiles {
		if err := unzip(zipFilePath, folderPath); err != nil {
			return fmt.Errorf("failed to unzip %s: %w", zipFilePath, err)
		}
		if err := os.Remove(zipFilePath); err != nil {
			return fmt.Errorf("failed to delete zip file %s: %w", zipFilePath, err)
		}
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
			if filepath.Ext(name) == ".jpg" || filepath.Ext(name) == ".jpeg" || filepath.Ext(name) == ".png" {
				images = append(images, filepath.Join(folderPath, name))
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
			os.MkdirAll(fpath, os.ModePerm)
			continue
		}

		if err := os.MkdirAll(filepath.Dir(fpath), os.ModePerm); err != nil {
			return err
		}

		outFile, err := os.OpenFile(fpath, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, f.Mode())
		if err != nil {
			return err
		}

		rc, err := f.Open()
		if err != nil {
			outFile.Close()
			return err
		}

		_, err = io.Copy(outFile, rc)
		outFile.Close()
		rc.Close()

		if err != nil {
			return err
		}
	}

	return nil
}
