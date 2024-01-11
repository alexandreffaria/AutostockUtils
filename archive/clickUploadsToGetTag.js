// Function to click on each image with a 100ms delay
function clickImagesWithDelay() {
    // Get all elements with the specified class
    const images = document.querySelectorAll('.upload-tile__thumbnail.upload-tile__thumbnail--landscape');

    // Check if there are images
    if (images.length === 0) {
        console.log('No more images with the specified class.');
        return;
    }

    // Loop through each image
    images.forEach((image, index) => {
        // Set a timeout to click each image with a 100ms delay
        setTimeout(() => {
            image.click();

            // Check if it's the last image
            if (index === images.length - 1) {
                console.log('No more images with the specified class.');
            }
        }, index * 300); // 100 milliseconds delay for each image
    });
}

// Execute the function
clickImagesWithDelay();
