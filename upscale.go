package main

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
)

// UpscaleImages processes each image with Real-ESRGAN, skipping those already upscaled
func UpscaleImages(images []Image) error {
	if len(images) == 0 {
		return fmt.Errorf("no images to upscale")
	}

	// Get the directory of the first image to determine the upscaled directory path
	imageDir := filepath.Dir(images[0].Path)
	upscaledDir := filepath.Join(imageDir, "upscaled")
	if _, err := os.Stat(upscaledDir); os.IsNotExist(err) {
		err = os.Mkdir(upscaledDir, os.ModePerm)
		if err != nil {
			return fmt.Errorf("failed to create upscaled directory: %w", err)
		}
	}

	for _, img := range images {
		base := filepath.Base(img.Path)
		outputImage := filepath.Join(upscaledDir, base)

		if _, err := os.Stat(outputImage); os.IsNotExist(err) {
			if err := runUpscaleCommand(img.Path, outputImage); err != nil {
				return fmt.Errorf("failed to upscale %s: %w", base, err)
			}
		}
	}

	return nil
}

func runUpscaleCommand(inputImage, outputImage string) error {
	command := []string{
		"realesrgan_win/realesrgan-ncnn-vulkan.exe",
		"-i", inputImage,
		"-o", outputImage,
		"-n", "realesrgan-x4plus",
	}

	cmd := exec.Command(command[0], command[1:]...)
	if err := cmd.Run(); err != nil {
		return fmt.Errorf("upscaling command failed: %w", err)
	}

	return nil
}
