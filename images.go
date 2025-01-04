package main

import (
	"image"
	"os"

	"path/filepath"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/widget"
)

var images []string
var currentIndex int

func createSelectFolderButton(label *widget.Label, w fyne.Window) *widget.Button {
	return widget.NewButton("Select Folder", func() {
		dialog.ShowFolderOpen(func(uri fyne.ListableURI, err error) {
			if uri != nil {
				entries, err := os.ReadDir(uri.Path())
				if err == nil {
					label.SetText("Folder Selected: " + uri.Path())
					images = nil
					for _, entry := range entries {
						if !entry.IsDir() {
							name := entry.Name()
							if filepath.Ext(name) == ".jpg" || filepath.Ext(name) == ".jpeg" || filepath.Ext(name) == ".png" {
								images = append(images, filepath.Join(uri.Path(), name))
							}
						}
					}
					currentIndex = 0
				}
			}
		}, w)
	})
}

func createStartQCButton(a fyne.App, w fyne.Window) *widget.Button {
	return widget.NewButton("Start QC", func() {
		if len(images) > 0 {
			startQCWindow(a)
		}
	})
}

func startQCWindow(a fyne.App) {
	qcWindow := a.NewWindow("Quality Control")
	qcWindow.Resize(fyne.NewSize(800, 600))

	activeImage := canvas.NewImageFromFile(images[currentIndex])
	activeImage.FillMode = canvas.ImageFillContain
	activeImage.SetMinSize(fyne.NewSize(800, 570)) // Occupying 95% of a 600px window

	thumbnailContainer := container.NewHBox()
	updateThumbnails(thumbnailContainer, activeImage)

	qcWindow.Canvas().SetOnTypedKey(handleKeyPress(activeImage, thumbnailContainer))
	qcWindow.SetContent(container.NewVBox(activeImage, thumbnailContainer))
	qcWindow.Show()
}

func updateThumbnails(thumbnailContainer *fyne.Container, activeImage *canvas.Image) {
	thumbnailContainer.Objects = nil
	start := currentIndex - 5
	if start < 0 {
		start = 0
	}
	end := currentIndex + 5
	if end >= len(images) {
		end = len(images) - 1
	}

	for i := start; i <= end; i++ {
		img, err := loadThumbnail(images[i])
		if err == nil {
			thumbnailContainer.Add(img)
		}
	}
	thumbnailContainer.Refresh()
}

func loadThumbnail(imagePath string) (*canvas.Image, error) {
	file, err := os.Open(imagePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()
	img, _, err := image.Decode(file)
	if err != nil {
		return nil, err
	}
	thumb := canvas.NewImageFromImage(img)
	thumb.SetMinSize(fyne.NewSize(50, 50)) // Adjust size for thumbnail
	return thumb, nil
}
