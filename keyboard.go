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
		currentIndex = len(images) - 1
	}
	activeImage.File = images[currentIndex].Path
	activeImage.Refresh()
	updateWindowTitle(qcWindow, images[currentIndex])
}

func moveNext(activeImage *canvas.Image, qcWindow fyne.Window) {
	if currentIndex < len(images)-1 {
		currentIndex++
	} else {
		currentIndex = 0
	}
	activeImage.File = images[currentIndex].Path
	activeImage.Refresh()
	updateWindowTitle(qcWindow, images[currentIndex])
}

func markAndRemoveFromView(activeImage *canvas.Image, qcWindow fyne.Window) {
	file := activeImage.File
	for _, img := range deletedStack {
		if img.file == file {
			return
		}
	}
	deletedStack = append(deletedStack, DeletedImage{file, currentIndex})
	log.Printf("Image '%s' marked for deletion.", file)

	images = append(images[:currentIndex], images[currentIndex+1:]...)
	if currentIndex >= len(images) {
		currentIndex = 0
	}

	if len(images) > 0 {
		activeImage.File = images[currentIndex].Path
		activeImage.Refresh()
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

	lastDeleted := deletedStack[len(deletedStack)-1]
	deletedStack = deletedStack[:len(deletedStack)-1]

	newImage := Image{Path: lastDeleted.file, URL: ""} // Adjust URL appropriately if required
	images = append(images[:lastDeleted.index], append([]Image{newImage}, images[lastDeleted.index:]...)...)

	log.Printf("Image '%s' restored to index %d.", lastDeleted.file, lastDeleted.index)

	currentIndex = lastDeleted.index
	activeImage.File = images[currentIndex].Path
	activeImage.Refresh()
	updateWindowTitle(qcWindow, images[currentIndex])
}
