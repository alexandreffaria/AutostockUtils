package main

import (
	"fmt"
	"os"
	"path/filepath"

	"fyne.io/fyne/theme"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/container/layout"
	"fyne.io/fyne/v2/container/widget"
)

type ImageViewer struct {
	folderPath   string
	files        []string
	currentIndex int
	image        *canvas.Image
}

func NewImageViewer(folderPath string, files []string) *ImageViewer {
	return &ImageViewer{
		folderPath:   folderPath,
		files:        files,
		currentIndex: 0,
		image:        canvas.NewImageFromFile(filepath.Join(folderPath, files[0])),
	}
}

func (viewer *ImageViewer) NextImage() {
	viewer.currentIndex = (viewer.currentIndex + 1) % len(viewer.files)
	viewer.updateImage()
}

func (viewer *ImageViewer) PreviousImage() {
	viewer.currentIndex = (viewer.currentIndex - 1 + len(viewer.files)) % len(viewer.files)
	viewer.updateImage()
}

func (viewer *ImageViewer) updateImage() {
	viewer.image.File = filepath.Join(viewer.folderPath, viewer.files[viewer.currentIndex])
	viewer.image.Refresh()
}

func main() {
	if len(os.Args) != 2 {
		fmt.Println("Usage: go run script.go /path/to/folder")
		os.Exit(1)
	}

	folderPath := os.Args[1]
	if _, err := os.Stat(folderPath); os.IsNotExist(err) {
		fmt.Printf("The specified folder '%s' does not exist.\n", folderPath)
		os.Exit(1)
	}

	files, err := getListOfImageFiles(folderPath)
	if err != nil {
		fmt.Printf("Error getting image files in folder '%s': %v\n", folderPath, err)
		os.Exit(1)
	}

	viewer := NewImageViewer(folderPath, files)

	myApp := app.New()
	myWindow := myApp.NewWindow("Image Viewer")

	myWindow.SetContent(container.NewVBox(
		container.NewHBox(
			layout.NewSpacer(),
			widget.NewButtonWithIcon("", widget.NewIcon(theme.NavigateBackIcon()), func() { viewer.PreviousImage() }),
			layout.NewSpacer(),
			widget.NewButtonWithIcon("", widget.NewIcon(theme.NavigateNextIcon()), func() { viewer.NextImage() }),
			layout.NewSpacer(),
		),
		container.NewCenter(
			container.NewMax(viewer.image),
		),
	))

	myWindow.ShowAndRun()
}

func getListOfImageFiles(folderPath string) ([]string, error) {
	var imageFiles []string

	err := filepath.Walk(folderPath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if info.Mode().IsRegular() {
			ext := filepath.Ext(info.Name())
			switch ext {
			case ".png", ".jpg", ".jpeg", ".gif", ".bmp":
				imageFiles = append(imageFiles, info.Name())
			}
		}
		return nil
	})

	if err != nil {
		return nil, err
	}

	return imageFiles, nil
}
