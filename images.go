package main

import (
	"image"
	"image/color"
	"os"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/data/binding"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/layout"
	"fyne.io/fyne/v2/widget"
)

var WindowSizeHeight = binding.NewFloat()
var WindowSizeWidth = binding.NewFloat()

type ResizeDetection struct {
	widget.BaseWidget
	qcWindow           fyne.Window
	thumbnailContainer *fyne.Container
	activeImage        *canvas.Image
}

func NewResizeDetection(qcWindow fyne.Window, thumbnailContainer *fyne.Container, activeImage *canvas.Image) *ResizeDetection {
	wg := &ResizeDetection{
		qcWindow:           qcWindow,
		thumbnailContainer: thumbnailContainer,
		activeImage:        activeImage,
	}
	wg.ExtendBaseWidget(wg)
	return wg
}

func (wg *ResizeDetection) CreateRenderer() fyne.WidgetRenderer {
	el := canvas.NewRectangle(color.Transparent)
	return &resizeDetectionRenderer{widget: wg, el: el}
}

type resizeDetectionRenderer struct {
	widget *ResizeDetection
	el     *canvas.Rectangle
}

func (r *resizeDetectionRenderer) Layout(size fyne.Size) {
	WindowSizeHeight.Set(float64(size.Height))
	WindowSizeWidth.Set(float64(size.Width))
	r.el.Resize(size)
	updateThumbnails(r.widget.qcWindow, r.widget.thumbnailContainer, r.widget.activeImage)
}

func (r *resizeDetectionRenderer) MinSize() fyne.Size {
	return r.el.MinSize()
}

func (r *resizeDetectionRenderer) Refresh() {
	r.el.Refresh()
}

func (r *resizeDetectionRenderer) Objects() []fyne.CanvasObject {
	return []fyne.CanvasObject{r.el}
}

func (r *resizeDetectionRenderer) Destroy() {}

func createStartQCButton(a fyne.App, w fyne.Window) *widget.Button {
	return widget.NewButton("Start QC", func() {
		if len(images) > 0 {
			startQCWindow(a)
		} else {
			dialog.ShowInformation("No Images", "There are no images to process. Please select a folder with images.", w)
		}
	})
}

func startQCWindow(a fyne.App) {
	qcWindow := a.NewWindow("Quality Control")
	qcWindow.Resize(fyne.NewSize(800, 600))

	activeImage := canvas.NewImageFromFile(images[currentIndex])
	activeImage.FillMode = canvas.ImageFillContain

	thumbnailContainer := container.NewGridWrap(fyne.NewSize(75, 75))
	updateThumbnails(qcWindow, thumbnailContainer, activeImage)

	thumbnailScroll := container.NewVScroll(thumbnailContainer)
	thumbnailScroll.SetMinSize(fyne.NewSize(0, 100))

	resizeDetector := NewResizeDetection(qcWindow, thumbnailContainer, activeImage)
	content := container.New(layout.NewBorderLayout(nil, thumbnailScroll, nil, nil), resizeDetector, activeImage, thumbnailScroll)
	qcWindow.SetContent(content)

	qcWindow.Canvas().SetOnTypedKey(handleKeyPress(qcWindow, activeImage, thumbnailContainer))
	qcWindow.Show()
}

func updateThumbnails(qcWindow fyne.Window, thumbnailContainer *fyne.Container, activeImage *canvas.Image) {
	thumbnailContainer.Objects = nil

	windowWidth := qcWindow.Canvas().Size().Width
	thumbnailSize := 75
	// Reduce visibleCount by one to display fewer images
	visibleCount := (int(windowWidth) / thumbnailSize) - 1
	if visibleCount < 1 {
		visibleCount = 1 // Ensure at least one thumbnail is visible
	}
	halfVisibleCount := visibleCount / 2

	start := currentIndex - halfVisibleCount
	if start < 0 {
		start = 0
	}
	end := start + visibleCount - 1
	if end >= len(images) {
		end = len(images) - 1
		start = end - visibleCount + 1
		if start < 0 {
			start = 0
		}
	}

	for i := start; i <= end; i++ {
		img, err := loadThumbnail(images[i])
		if err == nil {
			img.SetMinSize(fyne.NewSize(float32(thumbnailSize), float32(thumbnailSize)))

			if i == currentIndex {
				// Highlight current thumbnail by wrapping it in a border
				thumbnailContainer.Add(container.NewBorder(
					canvas.NewRectangle(color.RGBA{255, 0, 0, 255}),
					nil, nil, nil, img,
				))
			} else {
				thumbnailContainer.Add(img)
			}
		}
	}
	thumbnailContainer.Refresh()
}

func loadThumbnail(imagePath string) (*canvas.Image, error) {
	file, err := os.Open(imagePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()
	img, _, err := image.Decode(file)
	if err != nil {
		return nil, err
	}
	thumb := canvas.NewImageFromImage(img)
	thumb.FillMode = canvas.ImageFillContain
	return thumb, nil
}
