# AutoStock Utils 🤖

![Autostock Utils](https://github.com/alexandreffaria/AutostockUtils/blob/main/gui-rosa.png?raw=true)
![Autostock Utils](https://github.com/alexandreffaria/AutostockUtils/blob/main/gui-azul.png?raw=true)

## what it do?

This badboi makes images(midjourney) and the CSV metadata(gpt), so you can sell images forever. Of course, robotos are not very smart yet, so you gonna have to do some qc. But that's basically it.

## why it do?

Of course, you could always sell stock images on the internet. But now Adobe Stock is accepting AI-generated images, and you can be the most prolific stock photographer on the planet.

## how we do?

### One time thing

- Schedule **everyDayImHustlin.sh** to run everyday at 8:00, it makes midjourney images until 21:00. **pinocchio.py** has to sleep, and eat for that matter, he takes a lunch break.
- create a .env file with the following:

```.env
OPENAI_API_KEY=
MOUSE_X=
MOUSE_Y=
ICON_PATH=meulindo.ico
```

### Everyday thing

- Download your images from midjourney websitio
- **autostock.py**
- Quality control the images
  - click x to delete and arrows to move between images
- Wait for a while. The metadata will be saved on the same folder as the images.
- Go to adobe and Vecteezy and upload the csv's.
- Set images as AI and send them to approval.
  - You can use **Utils/markAsAi_vecteezy.py** to do it for you.
    - you can use **Utils/getMouseCoordinates.py** to set it up
- Profit! 💰

### Other qualities of life: 🕊

- **Utils/Autostock.atn** - Photoshop action to generate content-aware fill on letter box images.
- **Utils/promptGenerator.py** - Generates a specified amount of prompts based on the strategy
- **Utils/generatePromptsForAllCategories.sh** - Loops the promptGenerator on all categories.
- **Utils/getMouseCoordinates.py** - Grabs mouse coordinates to help set up macros.
- **Utils/pinocchio.py** - Sends the prompts to midjourney during the day and pretends to be a real boi. (midjourney doesn't like robots.)

### 🤝 Contributing

Just clone and install the libs:

- pip install -r requirements.txt

### To-do's

- [x] Integrate upscaling
- [x] GUI
- [x] Connect everything together
- [ ] Integrate inpainting

---

<https://github.com/Sanster/IOPaint/releases/tag/iopaint-1.0.0b2>
