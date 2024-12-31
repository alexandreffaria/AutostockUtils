package main

import (
	"log"
	"os"

	"gioui.org/app"
	"gioui.org/io/system"
	"gioui.org/layout"
	"gioui.org/op"
	"gioui.org/widget"
	"gioui.org/widget/material"
	"github.com/sqweek/dialog"
)

func main() {
	go func() {
		if err := runApp(); err != nil {
			log.Fatal(err)
		}
		os.Exit(0)
	}()
	app.Main()
}

func runApp() error {
	var ops op.Ops
	window := app.NewWindow()
	theme := material.NewTheme()

	printBtn := new(widget.Clickable)  // Button to print a message
	folderBtn := new(widget.Clickable) // Button to select a folder

	for {
		e := <-window.Events()
		switch e := e.(type) {
		case system.DestroyEvent:
			return e.Err
		case system.FrameEvent:
			gtx := layout.NewContext(&ops, e)

			layout.Flex{
				Axis:    layout.Vertical,
				Spacing: layout.SpaceAround,
			}.Layout(gtx,
				layout.Rigid(func(gtx layout.Context) layout.Dimensions {
					return material.Button(theme, printBtn, "Print Message").Layout(gtx)
				}),
				layout.Rigid(func(gtx layout.Context) layout.Dimensions {
					return material.Button(theme, folderBtn, "Select Folder").Layout(gtx)
				}),
			)

			// Handle Print Button click
			if printBtn.Clicked(gtx) {
				log.Println("Print Message button clicked")
			}

			// Handle Folder Button click
			if folderBtn.Clicked(gtx) {
				selectedFolder, err := dialog.Directory().Title("Select Folder").Browse()
				if err != nil {
					log.Println("No folder selected:", err)
				} else {
					log.Println("Selected folder:", selectedFolder)
				}
			}

			e.Frame(gtx.Ops)
		}
	}
}
