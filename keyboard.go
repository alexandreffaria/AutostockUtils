package main

import (
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/canvas"
)

func handleKeyPress(activeImage *canvas.Image, thumbnailContainer *fyne.Container) func(*fyne.KeyEvent) {
	return func(key *fyne.KeyEvent) {
		switch key.Name {
		case fyne.KeyLeft, fyne.KeyH:
			movePrev(activeImage, thumbnailContainer)
		case fyne.KeyRight, fyne.KeyL:
			moveNext(activeImage, thumbnailContainer)
		}
	}
}

func movePrev(activeImage *canvas.Image, thumbnailContainer *fyne.Container) {
	if currentIndex > 0 {
		currentIndex--
		activeImage.File = images[currentIndex]
		activeImage.Refresh()
		updateThumbnails(thumbnailContainer, activeImage)
	}
}

func moveNext(activeImage *canvas.Image, thumbnailContainer *fyne.Container) {
	if currentIndex < len(images)-1 {
		currentIndex++
		activeImage.File = images[currentIndex]
		activeImage.Refresh()
		updateThumbnails(thumbnailContainer, activeImage)
	}
}
