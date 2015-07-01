# Borderlands 1 Mouse Sensitivity

## Warning!

Do **not** use this for the time being.

The contents of the profile.bin file change drastically based on other settings, so this project needs a lot of work.

## Description
Change the mouse sensitivity to values not possible from the in-game menu.

Place set_mouse_sensitivity.py in your Borderlands save location,
(e.g. D:\Users\somebody\Documents\my games\borderlands\savedata),
then open command prompt at this location, and run:

`python set_mouse_sensitivity.py [sensitivity]`


profile.bin will be backed up at the start of the script to the same folder.
If sensitivity is given, it should be a hexadecimal value between
`0` and `ff`, giving the sensitivity that you want to set the mouse to.
If no sensitivity is given, the program will prompt you for one.

## Requirements

`python 2.x`. To ease use, you may wish to select the option to add `python` to your `PATH` during installation.
You must open a new command prompt once python has been added to your path.
