package main

import (
	"image/color"
	"log"
	"os"

	"gioui.org/app"
	"gioui.org/op"
	"gioui.org/text"
	"gioui.org/widget"
	"gioui.org/widget/material"
	"github.com/sqweek/dialog"
)

func main() {
	go func() {
		window := new(app.Window)
		err := run(window)
		if err != nil {
			log.Fatal(err)
		}
		os.Exit(0)
	}()
	app.Main()
}

func run(window *app.Window) error {
	theme := material.NewTheme()
	var ops op.Ops
	selectBtn := new(widget.Clickable)

	for {
		switch e := window.Event().(type) {
		case app.DestroyEvent:
			return e.Err
		case app.FrameEvent:
			gtx := app.NewContext(&ops, e)

			// Define an illustrative label
			title := material.H1(theme, "Hello, Gio")
			title.Color = color.NRGBA{R: 127, G: 0, B: 0, A: 255}
			title.Alignment = text.Middle

			// Check for button click with the correct context
			if selectBtn.Clicked(gtx) {
				selectedFolder, err := dialog.Directory().Title("Select Folder").Browse()
				if err != nil {
					log.Println("No folder selected:", err)
				} else {
					log.Println("Selected folder:", selectedFolder)
				}
			}

			// Create a button layout
			btnLayout := material.Button(theme, selectBtn, "Select Folder")
			title.Layout(gtx)
			btnLayout.Layout(gtx)

			e.Frame(gtx.Ops)
		}
	}
}
