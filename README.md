# AutoStock Utils 🤖
## what it do?
This badboi makes images(midjourney) and the csv metadata(gpt), so you can sell images forever. Of course robotos are not very smart yet, so you gonna have to do some qc. But that's basically it.

## why it do?
Of course you could always sell stock images on the internet. But now Adobe Stock is accepting AI generated images, and you can be the most prolific stock photographer in the planet. 

## how we do?

* Schedule everyDayImHustlin.sh to run everyday at 8:00
it makes midjourney images until 21:00, pinocchio.py has to sleep, and eat for that matter, he takes a lunch break.
* Download your images from midjourney websitio
* qc.py the images to delete the insanity
* upscale them using upscayl (native implementation coming soon!)
* sendSFTP.py to send them to adobe. (put your info into a .env)
* generateCSV.py to create the metadata
* Profit! 💰


---
https://github.com/Sanster/IOPaint/releases/tag/iopaint-1.0.0b2