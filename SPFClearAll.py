#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SOLARPUNK FUTURES: CLEAR ALL DISPLAYS
"""

import buttonshim as bs

import fourletterphat as flp

import argparse
import time
from inky.auto import auto
from PIL import Image

import scrollphathd as sphd

import touchphat as tp

print("Clearing each display in turn:")
print("		1. Button Shim")
print("		2. Four Letter Phat")
print("		3. Inky")
print("		4. Scroll Phat HD")
print("		5. Touch Phat")
print()

"""
1. CLEAR BUTTON SHIM
"""
bs.set_pixel(0, 0, 0)

print("---BUTTON SHIM CLEAR")
print()

"""
2. CLEAR FOUR LETTER PHAT
"""
flp.clear()
flp.show()

print("---FOUR LETTER PHAT CLEAR")
print()

"""
3. CLEAR INKY
"""
inky_display = auto(ask_user=True, verbose=True)

# Command line arguments to determine number of cycles to run
parser = argparse.ArgumentParser()
parser.add_argument('--number', '-n', type=int, required=False, help="number of cycles")
args, _ = parser.parse_known_args()

# The number of red / black / white refreshes to run

if args.number:
    cycles = args.number
else:
    cycles = 3

colours = (inky_display.RED, inky_display.BLACK, inky_display.WHITE)
colour_names = (inky_display.colour, "black", "white")

# Create a new canvas to draw on

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))

# Loop through the specified number of cycles and completely
# fill the display with each colour in turn.

for i in range(cycles):
    print("Inky cleaning cycle %i" % (i + 1))
    for j, c in enumerate(colours):
        inky_display.set_border(c)
        for x in range(inky_display.WIDTH):
            for y in range(inky_display.HEIGHT):
                img.putpixel((x, y), c)
        inky_display.set_image(img)
        inky_display.show()
        time.sleep(1)

print()
print("---INKY CLEAR")
print()

"""
4. CLEAR SCROLL PHAT HD
"""
sphd.clear()
sphd.show()

print("---SCROLL PHAT CLEAR")
print()
    
"""
5. CLEAR TOUCH PHAT
"""
tp.all_off()
print("---TOUCH PHAT CLEAR")
print()

print("---CLEARING COMPLETE")
print()