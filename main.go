package main

import (
	"fmt"
	"log"
	"os"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
	"github.com/joho/godotenv"
)

var appIcon fyne.Resource

func main() {
	// Load .env file
	err := godotenv.Load(".env")
	if err != nil {
		log.Fatalf("Error loading .env file")
	}

	a := app.NewWithID("com.github.meulindo.autostockutils")
	w := a.NewWindow("Image Viewer")
	w.Resize(fyne.NewSize(800, 600))

	label := widget.NewLabel("Hey! Where are the images?")
	selectFolderBtn := createSelectFolderButton(label, w)
	viewImagesBtn := widget.NewButton("Quality Control", func() {
		if len(images)s > 0 {
			showImageViewer(w, appIcon)
		} else {
			label.SetText("No images to display. Please select a folder first.")
		}
	})

	magicBtn := widget.NewButton("Upscale", func() {
		label.SetText("Performing magic...")

		err := UpscaleImages(images)
		if err != nil {
			label.SetText(fmt.Sprintf("Error during magic: %v", err))
		} else {
			label.SetText("Magic completed!")
		}
	})

	descriptionBtn := widget.NewButton("Generate Metadata", func() {
		label.SetText("Generating titles and keywords from filenames...")

		// We don't need to encode the images anymore
		err := FetchImageMetadata(images)
		if err != nil {
			label.SetText(fmt.Sprintf("Error generating metadata: %v", err))
		} else {
			label.SetText("Metadata generated successfully!")
		}
	})

	iconPath := "meulindo-ilus-invert.png"
	iconFile, err := os.ReadFile(iconPath)
	if err == nil {
		appIcon = fyne.NewStaticResource("App Icon", iconFile)
		w.SetIcon(appIcon)
	} else {
		fyne.LogError("Failed to load icon", err)
	}
	// Ending of this dude
	w.SetContent(container.NewVBox(label, selectFolderBtn, viewImagesBtn, magicBtn, descriptionBtn))
	w.ShowAndRun()
}
