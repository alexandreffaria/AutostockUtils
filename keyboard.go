package main

import (
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/canvas"
)

func handleKeyPress(qcWindow fyne.Window, activeImage *canvas.Image) func(*fyne.KeyEvent) {
	return func(key *fyne.KeyEvent) {
		switch key.Name {
		case fyne.KeyLeft, fyne.KeyH:
			movePrev(activeImage)
		case fyne.KeyRight, fyne.KeyL:
			moveNext(activeImage)
		}
	}
}

func movePrev(activeImage *canvas.Image) {
	if currentIndex > 0 {
		currentIndex--
		activeImage.File = images[currentIndex]
		activeImage.Refresh()
	}
}

func moveNext(activeImage *canvas.Image) {
	if currentIndex < len(images)-1 {
		currentIndex++
		activeImage.File = images[currentIndex]
		activeImage.Refresh()
	}
}
