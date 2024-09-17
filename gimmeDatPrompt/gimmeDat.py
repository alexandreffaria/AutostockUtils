from PIL import Image
import image_interrogator

# Path to your image
image_path = "gimmeDatPrompt/test.png"

# Load the image and run the model
image = Image.open(image_path)
prompt = image_interrogator.image_to_prompt(image, mode='best')

# Print the result prompt
print(prompt)
