package main

import (
	"os"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

func main() {
	a := app.NewWithID("com.github.meulindo.autostockutils")
	w := a.NewWindow("AutostockUtils")
	w.Resize(fyne.NewSize(500, 500))

	label := widget.NewLabel("Hello, Fyne! Please select a folder.")
	selectFolderBtn := createSelectFolderButton(label, w)

	// Load and set the icon for the window
	iconPath := "meulindo-ilus-invert.png"
	iconFile, err := os.ReadFile(iconPath)
	if err == nil {
		iconResource := fyne.NewStaticResource("App Icon", iconFile)
		w.SetIcon(iconResource)
	} else {
		// Handle error if icon cannot be loaded
		fyne.LogError("Failed to load icon", err)
	}

	w.SetContent(container.NewVBox(label, selectFolderBtn, createStartQCButton(a, w)))
	w.ShowAndRun()
}
