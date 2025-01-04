package main

import (
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
	qcWindow.SetIcon(icon) // Set the icon here

	activeImage := canvas.NewImageFromFile(images[currentIndex])
	activeImage.FillMode = canvas.ImageFillContain
	content := container.NewStack(activeImage)
	qcWindow.SetContent(content)

	qcWindow.Canvas().SetOnTypedKey(handleKeyPress(qcWindow, activeImage))
	qcWindow.Show()
}
