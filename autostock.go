package main

import (
	"fmt"
	"os"

	"github.com/therecipe/qt/widgets"
)

func main() {
	app := widgets.NewQApplication(len(os.Args), os.Args)
	window := widgets.NewQMainWindow(nil, 0)
	window.SetWindowTitle("Autostock")
	window.SetMinimumSize2(300, 900)

	mainWidget := widgets.NewQWidget(nil, 0)
	mainWidget.SetStyleSheet("background-color: #202123; color: #FCFCFC;")
	window.SetCentralWidget(mainWidget)

	layout := widgets.NewQVBoxLayout()

	// Create a QLineEdit for the folder path
	folderPathInput := widgets.NewQLineEdit(nil)
	folderPathInput.SetPlaceholderText("Enter folder path...")
	layout.AddWidget(folderPathInput, 0, 0)

	// Create a QPushButton to browse for a folder
	browseButton := widgets.NewQPushButton2("Browse", nil)
	layout.AddWidget(browseButton, 0, 0)

	// Connect the button's click event to open a file dialog
	browseButton.ConnectClicked(func(bool) {
		dialog := widgets.NewQFileDialog2(nil, "Select Folder", "", "")
		dialog.SetFileMode(widgets.QFileDialog__Directory)
		dialog.SetOption(widgets.QFileDialog__ShowDirsOnly, true)

		if dialog.Exec() != 0 {
			selectedFiles := dialog.SelectedFiles()
			if len(selectedFiles) > 0 {
				// No type assertion needed - selectedFiles is already []string
				selectedDir := selectedFiles[0]
				folderPathInput.SetText(selectedDir)
				fmt.Println("Selected directory:", selectedDir)
			}
		}
	})

	// Set layout for the main widget
	mainWidget.SetLayout(layout)
	window.Show()
	app.Exec()
}
