package main

import (
	"archive/zip"
	"fmt"
	"image/color"
	"io"
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"
	"sync"
	"time"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/layout"
	"fyne.io/fyne/v2/widget"
	"github.com/joho/godotenv"

	// ✅ Correct import paths for your project
	"autostockutils/internal/metadata"
)

// Global variables
var appIcon fyne.Resource
var images []metadata.Image
var progressBar *widget.ProgressBar
var progressLabel *widget.Label
var folderEntry *widget.Entry
var currentIndex int
var deletedStack []DeletedImage

// DeletedImage represents an image marked for deletion ;* XOXO Cursor
type DeletedImage struct {
	file  string
	index int
}

// updateProgress updates the progress bar and label ;* XOXO Cursor
func updateProgress(value float64, message string) {
	if progressBar != nil {
		progressBar.SetValue(value)
	}
	if progressLabel != nil {
		progressLabel.SetText(message)
	}
}

// loadImagesFromFolder loads images from the specified folder path ;* XOXO Cursor
func loadImagesFromFolder(folderPath string, label *widget.Label) error {
	// Primeiro, verifica se há arquivos ZIP
	zipFiles := checkForZipFiles(folderPath)
	if len(zipFiles) > 0 {
		if err := processZipFilesConcurrently(folderPath, zipFiles); err != nil {
			return fmt.Errorf("error processing ZIP files: %w", err)
		}
		label.SetText("Processed ZIPs successfully")
	}

	// Depois carrega as imagens
	files, err := os.ReadDir(folderPath)
	if err != nil {
		return fmt.Errorf("error reading folder: %v", err)
	}

	images = []metadata.Image{}
	for _, file := range files {
		if !file.IsDir() {
			ext := strings.ToLower(filepath.Ext(file.Name()))
			if ext == ".jpg" || ext == ".jpeg" || ext == ".png" {
				imagePath := filepath.Join(folderPath, file.Name())

				// Tenta abrir o arquivo para verificar se está acessível
				f, err := os.OpenFile(imagePath, os.O_RDONLY, 0)
				if err != nil {
					log.Printf("Aviso: Não foi possível acessar o arquivo %s: %v", imagePath, err)
					continue
				}
				f.Close()

				images = append(images, metadata.Image{Path: imagePath})
			}
		}
	}

	if len(images) == 0 {
		return fmt.Errorf("nenhuma imagem encontrada em %s", folderPath)
	}

	label.SetText(fmt.Sprintf("%d imagens carregadas de %s", len(images), folderPath))
	return nil
}

// checkForZipFiles returns a list of ZIP files in the folder ;* XOXO Cursor
func checkForZipFiles(folderPath string) []string {
	entries, err := os.ReadDir(folderPath)
	if err != nil {
		log.Printf("Erro ao ler pasta para ZIPs: %v", err)
		return nil
	}

	var zipFiles []string
	for _, entry := range entries {
		if !entry.IsDir() && strings.ToLower(filepath.Ext(entry.Name())) == ".zip" {
			zipPath := filepath.Join(folderPath, entry.Name())

			// Tenta abrir o arquivo ZIP para verificar se está acessível
			f, err := os.OpenFile(zipPath, os.O_RDONLY, 0)
			if err != nil {
				log.Printf("Aviso: Não foi possível acessar o arquivo ZIP %s: %v", zipPath, err)
				continue
			}
			f.Close()

			zipFiles = append(zipFiles, zipPath)
		}
	}

	return zipFiles
}

// processZipFilesConcurrently extracts all ZIP files in parallel ;* XOXO Cursor
func processZipFilesConcurrently(folderPath string, zipFiles []string) error {
	var wg sync.WaitGroup
	errors := make(chan error, len(zipFiles))

	for _, zipFilePath := range zipFiles {
		wg.Add(1)
		go func(zipPath string) {
			defer wg.Done()
			if err := unzip(zipPath, folderPath); err != nil {
				errors <- fmt.Errorf("failed to unzip %s: %w", zipPath, err)
				return
			}
			if err := os.Remove(zipPath); err != nil {
				errors <- fmt.Errorf("failed to delete zip file %s: %w", zipPath, err)
				return
			}
		}(zipFilePath)
	}

	wg.Wait()
	close(errors)

	// Collect and return the first error if any
	if len(errors) > 0 {
		return <-errors
	}

	return nil
}

// unzip extracts a ZIP file to the specified destination ;* XOXO Cursor
func unzip(src string, dest string) error {
	r, err := zip.OpenReader(src)
	if err != nil {
		return err
	}
	defer r.Close()

	for _, f := range r.File {
		fpath := filepath.Join(dest, f.Name)

		if f.FileInfo().IsDir() {
			os.MkdirAll(fpath, os.ModePerm)
			continue
		}

		if err = os.MkdirAll(filepath.Dir(fpath), os.ModePerm); err != nil {
			return err
		}

		outFile, err := os.OpenFile(fpath, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, f.Mode())
		if err != nil {
			return err
		}

		rc, err := f.Open()
		if err != nil {
			outFile.Close()
			return err
		}

		_, err = io.Copy(outFile, rc)
		outFile.Close()
		rc.Close()

		if err != nil {
			return err
		}
	}

	return nil
}

// createSelectFolderButton creates a button to select a folder and load images ;* XOXO Cursor
func createSelectFolderButton(label *widget.Label, w fyne.Window) *widget.Button {
	return widget.NewButton("Browse", func() {
		dialog.ShowFolderOpen(func(uri fyne.ListableURI, err error) {
			if err != nil {
				label.SetText(fmt.Sprintf("Error selecting folder: %v", err))
				return
			}
			if uri == nil {
				label.SetText("No folder selected")
				return
			}

			folderPath := uri.Path()
			folderEntry.SetText(folderPath)
			err = loadImagesFromFolder(folderPath, label)
			if err != nil {
				label.SetText(err.Error())
			}
		}, w)
	})
}

// showImageViewer shows a basic image viewer with navigation controls ;* XOXO Cursor
func showImageViewer(icon fyne.Resource) {
	if len(images) == 0 {
		return
	}

	qcWindow := fyne.CurrentApp().NewWindow("Image Viewer")
	qcWindow.Resize(fyne.NewSize(800, 600))
	qcWindow.SetIcon(icon)

	activeImage := canvas.NewImageFromFile(images[0].Path)
	activeImage.FillMode = canvas.ImageFillContain
	activeImage.Resize(fyne.NewSize(780, 540))

	// Create navigation entry with total count
	navEntry := widget.NewEntry()
	navEntry.Resize(fyne.NewSize(50, navEntry.MinSize().Height))
	totalLabel := widget.NewLabel(fmt.Sprintf("/%d", len(images)))

	// Set initial value
	navEntry.SetText(fmt.Sprintf("%d", currentIndex+1))

	navEntry.OnChanged = func(value string) {
		if value == "" {
			return
		}
		num, err := strconv.Atoi(value)
		if err != nil {
			return
		}
		if num < 1 || num > len(images) {
			return
		}
		currentIndex = num - 1
		activeImage.File = images[currentIndex].Path
		activeImage.Refresh()
		updateWindowTitle(qcWindow, images[currentIndex])
	}

	// Function to update nav entry
	updateNavEntry := func() {
		navEntry.SetText(fmt.Sprintf("%d", currentIndex+1))
	}

	// Create feedback overlay
	feedbackLabel := widget.NewLabel("")
	feedbackLabel.Hide()
	feedbackLabel.TextStyle = fyne.TextStyle{Bold: true}
	feedbackLabel.Alignment = fyne.TextAlignCenter

	// Create semi-transparent rectangle for feedback background
	feedbackBg := canvas.NewRectangle(color.NRGBA{0, 0, 0, 128})
	feedbackBg.Hide()
	feedbackBg.Resize(fyne.NewSize(200, 60))

	// Create feedback container and center it
	feedbackContainer := container.NewStack(feedbackBg, feedbackLabel)
	centeredFeedback := container.NewCenter(feedbackContainer)

	// Create bottom container with centered navigation
	navContainer := container.NewHBox(
		layout.NewSpacer(),
		container.NewHBox(
			navEntry,
			totalLabel,
		),
		layout.NewSpacer(),
	)

	// Create main content with overlay
	mainContent := container.NewStack(
		activeImage,
		centeredFeedback,
	)

	// Create final layout
	content := container.NewBorder(
		nil,          // top
		navContainer, // bottom
		nil,          // left
		nil,          // right
		mainContent,  // center
	)
	qcWindow.SetContent(content)

	updateWindowTitle(qcWindow, images[0])

	qcWindow.Canvas().SetOnTypedKey(handleKeyPress(qcWindow, activeImage, feedbackLabel, feedbackBg, updateNavEntry))

	qcWindow.SetOnClosed(func() {
		deleteMarkedImages()
	})

	qcWindow.Show()
}

// updateWindowTitle updates the window title with the current image info ;* XOXO Cursor
func updateWindowTitle(qcWindow fyne.Window, image metadata.Image) {
	manipulatedName := manipulateFileName(image.Path)
	title := fmt.Sprintf("%s (%d of %d)", manipulatedName, currentIndex+1, len(images))
	qcWindow.SetTitle(title)
}

// manipulateFileName formats the filename for display ;* XOXO Cursor
func manipulateFileName(fileName string) string {
	parts := strings.Split(fileName, "_")
	if len(parts) > 3 {
		joined := strings.Join(parts[1:len(parts)-2], " ")
		if idx := strings.Index(joined, "--"); idx != -1 {
			joined = joined[:idx]
		}
		return joined
	}
	return fileName
}

// handleKeyPress handles keyboard shortcuts for navigation ;* XOXO Cursor
func handleKeyPress(qcWindow fyne.Window, activeImage *canvas.Image, feedbackLabel *widget.Label, feedbackBg *canvas.Rectangle, updateNavEntry func()) func(*fyne.KeyEvent) {
	return func(key *fyne.KeyEvent) {
		switch key.Name {
		case fyne.KeyLeft, fyne.KeyH:
			movePrev(activeImage, qcWindow)
			updateNavEntry()
		case fyne.KeyRight, fyne.KeyL:
			moveNext(activeImage, qcWindow)
			updateNavEntry()
		case fyne.KeyZ:
			undoLastDeletion(activeImage, qcWindow)
			updateNavEntry()
			showFeedback(feedbackLabel, feedbackBg, "UNDO")
		case fyne.KeyX:
			markAndRemoveFromView(activeImage, qcWindow)
			updateNavEntry()
			showFeedback(feedbackLabel, feedbackBg, "DELETED")
		}
	}
}

// movePrev moves to the previous image ;* XOXO Cursor
func movePrev(activeImage *canvas.Image, qcWindow fyne.Window) {
	if currentIndex > 0 {
		currentIndex--
	} else {
		currentIndex = len(images) - 1
	}
	activeImage.File = images[currentIndex].Path
	activeImage.Refresh()
	updateWindowTitle(qcWindow, images[currentIndex])
}

// moveNext moves to the next image ;* XOXO Cursor
func moveNext(activeImage *canvas.Image, qcWindow fyne.Window) {
	if currentIndex < len(images)-1 {
		currentIndex++
	} else {
		currentIndex = 0
	}
	activeImage.File = images[currentIndex].Path
	activeImage.Refresh()
	updateWindowTitle(qcWindow, images[currentIndex])
}

// markAndRemoveFromView marks the current image for deletion and removes it from view ;* XOXO Cursor
func markAndRemoveFromView(activeImage *canvas.Image, qcWindow fyne.Window) {
	file := activeImage.File
	for _, img := range deletedStack {
		if img.file == file {
			return
		}
	}
	deletedStack = append(deletedStack, DeletedImage{file, currentIndex})
	log.Printf("Image '%s' marked for deletion.", file)

	images = append(images[:currentIndex], images[currentIndex+1:]...)
	if currentIndex >= len(images) {
		currentIndex = 0
	}

	if len(images) > 0 {
		activeImage.File = images[currentIndex].Path
		activeImage.Refresh()
		updateWindowTitle(qcWindow, images[currentIndex])
	} else {
		qcWindow.Close()
	}
}

// undoLastDeletion restores the last deleted image ;* XOXO Cursor
func undoLastDeletion(activeImage *canvas.Image, qcWindow fyne.Window) {
	if len(deletedStack) == 0 {
		log.Println("No images to restore.")
		return
	}

	lastDeleted := deletedStack[len(deletedStack)-1]
	deletedStack = deletedStack[:len(deletedStack)-1]

	newImage := metadata.Image{Path: lastDeleted.file}
	images = append(images[:lastDeleted.index], append([]metadata.Image{newImage}, images[lastDeleted.index:]...)...)

	log.Printf("Image '%s' restored to index %d.", lastDeleted.file, lastDeleted.index)

	currentIndex = lastDeleted.index
	activeImage.File = images[currentIndex].Path
	activeImage.Refresh()
	updateWindowTitle(qcWindow, images[currentIndex])
}

// deleteMarkedImages deletes all images marked for deletion ;* XOXO Cursor
func deleteMarkedImages() {
	for _, img := range deletedStack {
		err := os.Remove(img.file)
		if err != nil {
			log.Printf("Failed to delete file %s: %v", img.file, err)
		} else {
			log.Printf("Image '%s' deleted successfully.", img.file)
		}
	}
	deletedStack = nil
}

// runUpscaleCommand executes the Real-ESRGAN command for upscaling ;* XOXO Cursor
func runUpscaleCommand(inputImage, outputImage string) error {
	// Procura o executável em diferentes locais
	executablePaths := []string{
		"realesrgan_win/realesrgan-ncnn-vulkan.exe",       // Na pasta realesrgan_win
		"realesrgan-ncnn-vulkan.exe",                      // No diretório atual
		"./realesrgan-ncnn-vulkan.exe",                    // Caminho explícito
		"../realesrgan_win/realesrgan-ncnn-vulkan.exe",    // Um nível acima
		"../../realesrgan_win/realesrgan-ncnn-vulkan.exe", // Dois níveis acima
	}

	// Mostra o diretório atual para debug
	currentDir, _ := os.Getwd()
	log.Printf("Diretório atual: %s", currentDir)

	var execPath string
	for _, path := range executablePaths {
		log.Printf("Procurando executável em: %s", filepath.Join(currentDir, path))
		if _, err := os.Stat(path); err == nil {
			execPath = path
			log.Printf("Executável encontrado em: %s", path)
			break
		}
	}

	if execPath == "" {
		return fmt.Errorf("realesrgan-ncnn-vulkan.exe não encontrado.\nDiretório atual: %s\nProcurei em:\n- %s",
			currentDir,
			strings.Join(executablePaths, "\n- "))
	}

	command := []string{
		execPath,
		"-i", inputImage,
		"-o", outputImage,
		"-n", "realesrgan-x4plus",
	}

	log.Printf("Executando comando: %v", command)
	cmd := exec.Command(command[0], command[1:]...)
	output, err := cmd.CombinedOutput() // Captura a saída do comando
	if err != nil {
		return fmt.Errorf("erro ao executar upscaling: %v\nSaída: %s\nComando: %v", err, string(output), command)
	}

	return nil
}

// UpscaleImages processes each image with Real-ESRGAN ;* XOXO Cursor
func UpscaleImages(images []metadata.Image, w fyne.Window) error {
	if len(images) == 0 {
		return fmt.Errorf("nenhuma imagem para upscale")
	}

	// Get the directory of the first image to determine the upscaled directory path
	imageDir := filepath.Dir(images[0].Path)
	upscaledDir := filepath.Join(imageDir, "upscaled")
	if _, err := os.Stat(upscaledDir); os.IsNotExist(err) {
		err = os.Mkdir(upscaledDir, os.ModePerm)
		if err != nil {
			return fmt.Errorf("erro ao criar pasta 'upscaled': %w", err)
		}
	}

	totalImages := len(images)
	for i, img := range images {
		progress := float64(i) / float64(totalImages)
		updateProgress(progress, fmt.Sprintf("Upscaling imagem %d de %d...", i+1, totalImages))

		base := filepath.Base(img.Path)
		outputImage := filepath.Join(upscaledDir, base)

		// Skip if already upscaled
		if _, err := os.Stat(outputImage); os.IsNotExist(err) {
			if err := runUpscaleCommand(img.Path, outputImage); err != nil {
				dialog.ShowError(err, w) // Mostra o erro em um popup
				return fmt.Errorf("erro ao fazer upscale de %s: %w", base, err)
			}
		}
	}

	// Update progress to 100%
	updateProgress(1.0, "Upscaling concluído!")
	dialog.ShowInformation("Concluído", fmt.Sprintf("Upscaling finalizado com sucesso!\nImagens salvas em: %s", upscaledDir), w)
	return nil
}

// showFeedback shows a temporary feedback message ;* XOXO Cursor
func showFeedback(label *widget.Label, bg *canvas.Rectangle, message string) {
	label.SetText(message)
	label.Show()
	bg.Show()
	go func() {
		time.Sleep(1 * time.Second)
		label.Hide()
		bg.Hide()
	}()
}

func main() {
	// Load .env file
	err := godotenv.Load(".env")
	if err != nil {
		log.Fatalf("Error loading .env file: %v", err)
	}

	// Create the Fyne application window
	a := app.NewWithID("com.github.meulindo.autostockutils")
	w := a.NewWindow("Image Viewer")
	w.Resize(fyne.NewSize(800, 600))

	label := widget.NewLabel("Hey! Where are the images?")

	// Create folder selection UI
	folderEntry = widget.NewEntry()
	folderEntry.SetPlaceHolder("Enter folder path or click Browse... (Ctrl+V to paste)")
	folderEntry.OnChanged = func(path string) {
		if path != "" {
			err := loadImagesFromFolder(path, label)
			if err != nil {
				label.SetText(err.Error())
			}
		}
	}

	selectFolderBtn := createSelectFolderButton(label, w)
	folderContainer := container.NewBorder(nil, nil, selectFolderBtn, nil, folderEntry)

	viewImagesBtn := widget.NewButton("Quality Control", func() {
		if len(images) > 0 {
			showImageViewer(appIcon)
		} else {
			label.SetText("No images to display. Please select a folder first.")
		}
	})
	magicBtn := widget.NewButton("Upscale", func() {
		label.SetText("Performing magic...")
		err := UpscaleImages(images, w)
		if err != nil {
			label.SetText(fmt.Sprintf("Error during magic: %v", err))
		} else {
			label.SetText("Magic completed!")
		}
	})
	descriptionBtn := widget.NewButton("Generate Metadata", func() {
		label.SetText("Generating titles and keywords from filenames...")
		// Call the FetchImageMetadata function from the metadata package
		err := metadata.FetchImageMetadata(images)
		if err != nil {
			label.SetText(fmt.Sprintf("Error generating metadata: %v", err))
		} else {
			label.SetText("Metadata generated successfully!")
			dialog.ShowInformation("Concluído", "Metadata gerada com sucesso!", w)
		}
	})

	// Create progress bar and label
	progressBar = widget.NewProgressBar()
	progressLabel = widget.NewLabel("Ready")
	progressContainer := container.NewVBox(progressBar, progressLabel)

	// Load application icon if available
	iconPath := "meulindo-ilus-invert.png"
	iconFile, err := os.ReadFile(iconPath)
	if err == nil {
		appIcon = fyne.NewStaticResource("App Icon", iconFile)
		w.SetIcon(appIcon)
	} else {
		fyne.LogError("Failed to load icon", err)
	}

	// Set up the UI layout
	w.SetContent(container.NewVBox(
		label,
		folderContainer,
		viewImagesBtn,
		magicBtn,
		descriptionBtn,
		progressContainer,
	))
	w.ShowAndRun()
}
