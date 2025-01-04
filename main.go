package main

import (
	"os"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

var appIcon fyne.Resource

func main() {
	a := app.NewWithID("com.github.meulindo.autostockutils")
	w := a.NewWindow("Image Viewer")
	w.Resize(fyne.NewSize(800, 600))

	label := widget.NewLabel("Hey! Where are the images?")
	selectFolderBtn := createSelectFolderButton(label, w)
	viewImagesBtn := widget.NewButton("Quality Control", func() {
		if len(images) > 0 {
			showImageViewer(w, appIcon)
		} else {
			label.SetText("No images to display. Please select a folder first.")
		}
	})

	// Define the "Magic" button and its action
	magicBtn := widget.NewButton("Magic", func() {
		// Define what should happen when "Magic" is pressed
		label.SetText("Abracadabra! The magic is done.")
	})

	// Load and set the icon for the application window
	iconPath := "meulindo-ilus-invert.png"
	iconFile, err := os.ReadFile(iconPath)
	if err == nil {
		appIcon = fyne.NewStaticResource("App Icon", iconFile)
		w.SetIcon(appIcon)
	} else {
		// Handle error if icon cannot be loaded
		fyne.LogError("Failed to load icon", err)
	}

	w.SetContent(container.NewVBox(label, selectFolderBtn, viewImagesBtn, magicBtn))
	w.ShowAndRun()
}
