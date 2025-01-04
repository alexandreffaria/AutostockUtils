package main

import (
	"fmt"
	"log"
	"os"
	"strings"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/dialog"
)

func showImageViewer(w fyne.Window, icon fyne.Resource) {
	if currentIndex < 0 || len(images) == 0 {
		dialog.ShowInformation("No Images", "There are no images to display.", w)
		return
	}

	qcWindow := fyne.CurrentApp().NewWindow("Image Viewer")
	qcWindow.Resize(fyne.NewSize(800, 600))
	qcWindow.SetIcon(icon)

	activeImage := canvas.NewImageFromFile(images[currentIndex])
	activeImage.FillMode = canvas.ImageFillContain
	content := container.NewStack(activeImage)
	qcWindow.SetContent(content)

	updateWindowTitle(qcWindow, images[currentIndex])

	qcWindow.Canvas().SetOnTypedKey(handleKeyPress(qcWindow, activeImage))

	// Handle closing the image viewer window to delete marked files
	qcWindow.SetOnClosed(func() {
		deleteMarkedImages()
	})

	qcWindow.Show()
}
func updateWindowTitle(qcWindow fyne.Window, imageFile string) {
	manipulatedName := manipulateFileName(imageFile)
	title := fmt.Sprintf("%s (%d of %d)", manipulatedName, currentIndex+1, len(images))
	qcWindow.SetTitle(title)
}

func manipulateFileName(fileName string) string {
	parts := strings.Split(fileName, "_")
	if len(parts) > 3 {
		joined := strings.Join(parts[1:len(parts)-2], " ")
		if idx := strings.Index(joined, "--"); idx != -1 {
			joined = joined[:idx]
		}
		return joined
	}
	return fileName // Return the original if it's too short
}

func deleteMarkedImages() {
	for _, img := range deletedStack {
		err := os.Remove(img.file)
		if err != nil {
			log.Printf("Failed to delete file %s: %v", img.file, err)
		} else {
			log.Printf("Image '%s' deleted successfully.", img.file)
		}
	}
	deletedStack = nil // Clear the stack after deletion
}
