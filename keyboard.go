package main

import (
	"log"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/canvas"
)

type DeletedImage struct {
	file  string
	index int
}

var deletedStack = []DeletedImage{}

func handleKeyPress(qcWindow fyne.Window, activeImage *canvas.Image) func(*fyne.KeyEvent) {
	return func(key *fyne.KeyEvent) {
		switch key.Name {
		case fyne.KeyLeft, fyne.KeyH:
			movePrev(activeImage, qcWindow)
		case fyne.KeyRight, fyne.KeyL:
			moveNext(activeImage, qcWindow)
		case fyne.KeyU:
			undoLastDeletion(activeImage, qcWindow)
		case fyne.KeyX:
			markAndRemoveFromView(activeImage, qcWindow)
		}
	}
}

func movePrev(activeImage *canvas.Image, qcWindow fyne.Window) {
	if currentIndex > 0 {
		currentIndex--
	} else {
		currentIndex = len(images) - 1 // Loop back to the end
	}
	activeImage.File = images[currentIndex]
	activeImage.Refresh()

	// Update the window title with the new image and index
	updateWindowTitle(qcWindow, images[currentIndex])
}

func moveNext(activeImage *canvas.Image, qcWindow fyne.Window) {
	if currentIndex < len(images)-1 {
		currentIndex++
	} else {
		currentIndex = 0 // Loop back to the start
	}
	activeImage.File = images[currentIndex]
	activeImage.Refresh()

	// Update the window title with the new image and index
	updateWindowTitle(qcWindow, images[currentIndex])
}

func markAndRemoveFromView(activeImage *canvas.Image, qcWindow fyne.Window) {
	file := activeImage.File
	// Check if the file is already in the stack
	for _, img := range deletedStack {
		if img.file == file {
			return
		}
	}
	deletedStack = append(deletedStack, DeletedImage{file, currentIndex})
	log.Printf("Image '%s' marked for deletion.", file)

	// Remove from images list
	images = append(images[:currentIndex], images[currentIndex+1:]...)

	// Adjust index safely
	if currentIndex >= len(images) {
		currentIndex = 0 // Loop to start if we go beyond the last element
	}

	if len(images) > 0 {
		activeImage.File = images[currentIndex]
		activeImage.Refresh()

		// Update the window title with the new active image and index
		updateWindowTitle(qcWindow, images[currentIndex])
	} else {
		qcWindow.Close()
	}
}

func undoLastDeletion(activeImage *canvas.Image, qcWindow fyne.Window) {
	if len(deletedStack) == 0 {
		log.Println("No images to restore.")
		return
	}

	// Get the last deleted image
	lastDeleted := deletedStack[len(deletedStack)-1]
	deletedStack = deletedStack[:len(deletedStack)-1] // Remove it from the stack

	// Restore the image back to its original position
	images = append(images[:lastDeleted.index], append([]string{lastDeleted.file}, images[lastDeleted.index:]...)...)
	log.Printf("Image '%s' restored to index %d.", lastDeleted.file, lastDeleted.index)

	// Update the current index and active image
	currentIndex = lastDeleted.index
	activeImage.File = images[currentIndex]
	activeImage.Refresh()

	// Update the window title with the restored image and index
	updateWindowTitle(qcWindow, images[currentIndex])
}
