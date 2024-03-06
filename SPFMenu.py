#!/usr/bin/env python

"""
SOLARPUNK FUTURES MENU

1. ABOUT
2. START NEW GAME
3. UNDEFINED (LOAD GAME)
4. SYSTEM HEALTH CHECK
5. SHUTDOWN
"""
import subprocess
from time import sleep
import argparse
import signal

import buttonshim as bs

import fourletterphat as flp

from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw #Python Image Library, for Inky
from font_hanken_grotesk import HankenGroteskMedium

import scrollphathd as sphd

import touchphat as tp

inky = auto()

def startScreen():
    inky.set_border(inky.BLACK)
    img = Image.new("P", (inky.WIDTH, inky.HEIGHT))
    draw = ImageDraw.Draw(img)
    font1 = ImageFont.truetype(HankenGroteskMedium, 14)
    font2 = ImageFont.truetype(HankenGroteskMedium, 12)

    line1 = "SOLARPUNK FUTURES:"
    w1, h1 = font1.getsize(line1)
    x1 = 2
    y1 = 2

    line2 = "1. About"
    w2, h2 = font2.getsize(line2)
    x2 = 10
    y2 = y1 + h1 + 10

    line3 = "2. Start New Game"
    w3, h3 = font2.getsize(line3)
    x3 = 10
    y3 = y2 + h2 + 2

    line4 = "3. --"
    w4, h4 = font2.getsize(line4)
    x4 = 10
    y4 = y3 + h3 + 2

    line5 = "4. System Health Check"
    w5, h5 = font2.getsize(line5)
    x5 = 10
    y5 = y4 + h4 + 2

    line6 = "5. Shutdown (hold for 2 secs)"
    w6, h6 = font2.getsize(line6)
    x6 = 10
    y6 = y5 + h5 + 2

    draw.text((x1, y1), line1, inky.BLACK, font1)
    draw.text((x2, y2), line2, inky.BLACK, font2)
    draw.text((x3, y3), line3, inky.BLACK, font2)
    draw.text((x4, y4), line4, inky.BLACK, font2)
    draw.text((x5, y5), line5, inky.BLACK, font2)
    draw.text((x6, y6), line6, inky.BLACK, font2)
    inky.set_image(img)
    inky.show()

startScreen()

menu_state = "open" #To manage how commands work when invoking the main game file

"""
1. ABOUT
"""
about_screen_on = False

@bs.on_press(bs.BUTTON_E)
def buttonE(button, pressed):
    global menu_state
    if menu_state == "open":
        bs.set_pixel(100, 100, 0)
        global about_screen_on
        if about_screen_on == False:   
            about_screen_on = True
            inky.set_border(inky.BLACK)
            img = Image.open("/home/brooker/Desktop/SolarpunkFutures/sp_about.png")
            inky.set_image(img)
            inky.show()
        else:
            startScreen()
    else:
        pass
        
@bs.on_release(bs.BUTTON_E)
def buttonE(button, pressed):
    global menu_state
    if menu_state == "open":
        bs.set_pixel(0, 0, 0)
    else:
        pass


"""
2. START NEW GAME
"""
@bs.on_press(bs.BUTTON_D)
def buttonD(button, pressed):
    global menu_state
    if menu_state == "open":
        flp.clear()
        flp.show()
        bs.set_pixel(100, 100, 0)
    else:
        pass

@bs.on_release(bs.BUTTON_D)
def buttonD(button, pressed):
    global menu_state
    if menu_state == "open":
        menu_state = "closed"
        bs.set_pixel(0, 0, 0)
        subprocess.run(["sudo", "python3", "/home/brooker/Desktop/SolarpunkFutures/SPFMain.py"])
        quit()
    else:
        pass



"""
3. UNDEFINED (LOAD GAME) #TODO: SAVE AND LOAD STATES?
"""
@bs.on_press(bs.BUTTON_C)
def buttonC(button, pressed):
    pass

@bs.on_release(bs.BUTTON_C)
def buttonC(button, pressed):
    pass
    
    
    
"""
4. SYSTEM HEALTH CHECK
"""
def getSysHealthData():
    ut = subprocess.run("uptime", capture_output=True) #running uptime in bash, capturing output
    lut = len(ut.stdout) #length of output for purposes of string formatting to pull relevant info
    uptime = str(ut.stdout)[15:lut-41]
    cpu_load = str(ut.stdout)[lut-15:lut-11]

    t = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True)
    lt = len(t.stdout)
    temp = str(t.stdout)[7:lt-1]

    s = subprocess.run(["vcgencmd", "measure_clock", "arm"], capture_output=True)
    ls = len(s.stdout)
    cpu_speed = int(str(s.stdout)[16:ls+1])
    return uptime, temp, cpu_load, cpu_speed

@bs.on_press(bs.BUTTON_B)
def buttonB(button, pressed):
    global menu_state
    if menu_state == "open":
        bs.set_pixel(100, 100, 0)
    else:
        pass
    
@bs.on_release(bs.BUTTON_B)
def buttonB(button, pressed):
    global menu_state
    if menu_state == "open":
        bs.set_pixel(0, 0, 0)

        data = getSysHealthData() #reading in system health data to function

        flp.clear()
        flp.show()
        
        flp.scroll_print("-- UPTIME    ") #trailing space to make text scroll off screen
        flp.clear()
        ut_msg = data[0]
        msg = ut_msg.replace(":", " hr ") #if uptime is in order of hours, text formatting for readability
        if msg[-3::] != "min": #if uptime in order of hours, adding "min" for readability
            msg = msg + " min"
        else:
            pass
        flp.scroll_print(msg + "    ")
        flp.clear()

        flp.scroll_print("-- CPU/GPU TEMP    ")
        flp.clear()
        flp.print_number_str(data[1][0:2] + data[1][3] + "C") #removing . as text
        flp.set_decimal(1, 1) #inserting . as decimal point on flp display
        flp.show()
        sleep(3) #to make the time the info is being displayed approx. same as scrolling text
        flp.clear()
        flp.show()
        sleep(1) #having a clear display for a beat
        
        flp.scroll_print("-- CPU LOAD    ")
        flp.clear()
        flp.print_number_str(data[2][0] + data[2][2:4]) #removing . as text
        flp.set_decimal(1, 1) #inserting . as decimal point on flp display
        flp.show()
        sleep(3) #to make the time the info is being displayed approx. same as scrolling text 
        flp.clear()
        flp.show()
        sleep(1) #having a clear display for a beat
        
        flp.scroll_print("-- CPU SPEED    ")
        flp.clear()
        cpu_speed_MHz = int(data[3] / 1000000) #converting from KHz to MHz
        flp.scroll_print(str(cpu_speed_MHz) + "MHz    ")
        flp.clear()
        sleep(1)
        flp.show()
    
    

"""
5. SHUTDOWN
"""
buttonA_held = False

@bs.on_press(bs.BUTTON_A)
def buttonA(button, pressed):
    global buttonA_held
    flp.clear()
    flp.show()
    buttonA_held = False #To reset button held state
    bs.set_pixel(200, 000, 0)

@bs.on_hold(bs.BUTTON_A, hold_time=2)
def buttonA(button):
    global buttonA_held
    buttonA_held = True
    
@bs.on_release(bs.BUTTON_A)
def buttonA(button, pressed):
    bs.set_pixel(0, 0, 0)
    if buttonA_held == False:
        pass
    else:
        bs.set_pixel(0, 0, 0) #CLEARING BUTTON SHIM
    
        flp.clear() #CLEARING FOUR LETTER PHAT
        flp.show()
        
        #CLEARING INKY
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
                sleep(1)
        
        sphd.clear() #CLEAR SCROLL PHAT HD
        sphd.show()
        
        tp.all_off() #CLEAR TOUCH PHAT
            
        subprocess.run(["sudo", "shutdown"])
        quit()
        
signal.pause()
    
    
    
    
    
    
    
    