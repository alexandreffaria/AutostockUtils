 .\realesrgan-ncnn-vulkan.exe -i ..\Utils\teste\2.png -o .\output.png -n realesrgan-x4plus
  wsl.exe powershell.exe ???
##  Workflow:
  - Utils/qc.py
  - Upscale realesrgan
  - convert to jpeg
  - sendSFPT.py
    - Adobe
    - Vecteezy (broken)
  - generateCSV.py
    - Adobe 
    - Vecteezy
