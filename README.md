# AutoStock Utils 🤖
## what it do?
This badboi makes images(midjourney) and the CSV metadata(gpt), so you can sell images forever. Of course, robotos are not very smart yet, so you gonna have to do some qc. But that's basically it.

## why it do?
Of course, you could always sell stock images on the internet. But now Adobe Stock is accepting AI-generated images, and you can be the most prolific stock photographer on the planet. 

## how we do?

* Schedule __everyDayImHustlin.sh__ to run everyday at 8:00, it makes midjourney images until 21:00. __pinocchio.py__ has to sleep, and eat for that matter, he takes a lunch break.
* Download your images from midjourney websitio
* __qc.py__ the images to delete and fix the insanity
* upscale them using upscayl (native implementation coming soon!)
* __sendSFTP.py__ to send them to Adobe. (put your info into a .env)
* __generateCSV.py__ to create the metadata
* Profit! 💰

### Other qualities of life: 🕊

* __Utils/Autostock.atn__ - Photoshop action to generate content-aware fill on letter box images.
* __Utils/promptGenerator.py__ - Generates a specified amount of prompts based on the strategy
* __Utils/generatePromptsForAllCategories.sh__ - Loops the promptGenerator on all categories.
* __Utils/getMouseCoordinates.py__ - Grabs mouse coordinates to help set up macros.
* __Utils/pinocchio.py__ - Sends the prompts to midjourney during the day and pretends to be a real boi. (midjourney doesn't like robots.)

### 🤝 Contributing

Just clone and install the libs:
- tkinter
- openai
- dotenv
- pyautogui
- pyperclip
- argparse
- paramiko
- tqdm
- keyboard (gerMouseCoordinates.py)

### To-do's
- [ ] Integrate upscaling 
- [ ] Integrate inpainting
- [ ] GUI
- [ ] Connect everything together


---
https://github.com/Sanster/IOPaint/releases/tag/iopaint-1.0.0b2
