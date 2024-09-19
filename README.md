# AutoStock Utils 🤖
## what it do?
This badboi makes images(midjourney) and the CSV metadata(gpt), so you can sell images forever. Of course, robotos are not very smart yet, so you gonna have to do some qc. But that's basically it.

## why it do?
Of course, you could always sell stock images on the internet. But now Adobe Stock is accepting AI-generated images, and you can be the most prolific stock photographer on the planet. 

## how we do?

### One time thing

* Schedule __everyDayImHustlin.sh__ to run everyday at 8:00, it makes midjourney images until 21:00. __pinocchio.py__ has to sleep, and eat for that matter, he takes a lunch break.
* create a .env file with the following:

```.env
OPENAI_API_KEY=
SFTP_USERNAME_adobe=
SFTP_PASSWORD_adobe=
SFTP_HOST_adobe=sftp.contributor.adobestock.com
SFTP_USERNAME_freepik=
SFTP_PASSWORD_freepik=
SFTP_HOST_freepik=
SFTP_PORT=22
MOUSE_X=
MOUSE_Y=
ICON_PATH=meulindo.ico
```

### Everyday thing

* Download your images from midjourney websitio
* __autostock.py__
* Quality control the images
  - click x to delete and arrows to move between images
* Wait for a while. The metadata will be saved on the same folder as the images.
* Go to adobe and Vecteezy and upload the csv's.
* Set images as AI and send them to approval.
  - You can use __Utils/markAsAi_vecteezy.py__ to do it for you.
    - you can use __Utils/getMouseCoordinates.py__ to set it up
* Profit! 💰

### Other qualities of life: 🕊

* __Utils/Autostock.atn__ - Photoshop action to generate content-aware fill on letter box images.
* __Utils/promptGenerator.py__ - Generates a specified amount of prompts based on the strategy
* __Utils/generatePromptsForAllCategories.sh__ - Loops the promptGenerator on all categories.
* __Utils/getMouseCoordinates.py__ - Grabs mouse coordinates to help set up macros.
* __Utils/pinocchio.py__ - Sends the prompts to midjourney during the day and pretends to be a real boi. (midjourney doesn't like robots.)

### 🤝 Contributing

Just clone and install the libs:
- pip install -r requirements.txt

### To-do's
- [x] Integrate upscaling 
- [x] GUI
- [x] Connect everything together
- [ ] Integrate inpainting

---
https://github.com/Sanster/IOPaint/releases/tag/iopaint-1.0.0b2

Ja tamo usando visao, vamo tira a categoria de uma vez, deixa gpt escolher a que ele achar melhor
Convert to jpg não ta pulando imagens convertidas
image description ta morrendo as vezes
podia remover todas as images processadas da lista de uma vez, só pra ficar mais clean memo
já tamo com ai local, porque continuar pagando gpt?
add region to inpaint via qc (drag rect for each area)