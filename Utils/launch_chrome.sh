#!/bin/bash

# Launch Chrome with Profile 1 and position on the left third
chromium-browser --profile-directory="Profile 1" &
sleep 15  # Wait for the browser to start
wmctrl -r "Geppetto" -e 0,0,0,853,1080  # Left third

# Launch Chrome with Profile 2 and position in the center third
chromium-browser --profile-directory="Profile 2" &
sleep 15
wmctrl -r "ishmael" -e 0,853,0,853,1080  # Center third

# Launch Chrome with Default Profile and position on the right third
chromium-browser --profile-directory="Default" &
sleep 15
wmctrl -r "pinocchio" -e 0,1706,0,853,1080  # Right third
