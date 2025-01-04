package main

import (
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/canvas"
)

func handleKeyPress(qcWindow fyne.Window, activeImage *canvas.Image, thumbnailContainer *fyne.Container) func(*fyne.KeyEvent) {
	return func(key *fyne.KeyEvent) {
		switch key.Name {
		case fyne.KeyLeft, fyne.KeyH:
			movePrev(qcWindow, activeImage, thumbnailContainer)
		case fyne.KeyRight, fyne.KeyL:
			moveNext(qcWindow, activeImage, thumbnailContainer)
		}
	}
}

func movePrev(qcWindow fyne.Window, activeImage *canvas.Image, thumbnailContainer *fyne.Container) {
	if currentIndex > 0 {
		currentIndex--
		activeImage.File = images[currentIndex]
		activeImage.Refresh()
		updateThumbnails(qcWindow, thumbnailContainer, activeImage)
	}
}

func moveNext(qcWindow fyne.Window, activeImage *canvas.Image, thumbnailContainer *fyne.Container) {
	if currentIndex < len(images)-1 {
		currentIndex++
		activeImage.File = images[currentIndex]
		activeImage.Refresh()
		updateThumbnails(qcWindow, thumbnailContainer, activeImage)
	}
}
