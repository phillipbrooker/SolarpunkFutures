#!/usr/bin/env python

"""
SOLARPUNK FUTURES
Haziasoft

A device/game for thinking through some preposterous problems to do with:

    * the relationship of social research to meaningful positive change
    * the role of technologies in informing the practices of social life
    * the possibility of supporting resistance and activism through design/games
    * ...more?
    
None of this may work, it might all be a dead end, but it's an attempt to
apply some skills and expertises I have to something genuine and important.

¯\_(ツ)_/¯

INDEX:
    1. IMPORTS
    2. CONSTANTS / INITIAL VARIABLES AND GENERAL FUNCTIONS
    3. SPLASH SCREEN
    4. GAMEPLAY
        4. 1. Objects and General Gameplay Functions
        4. 2. Game Loop
"""


"""
#1. IMPORTS
"""

#Hardware Libraries
import fourletterphat as flp
from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw #Python Image Library, for Inky
from font_hanken_grotesk import HankenGroteskMedium 
import scrollphathd as sphd
import touchphat as tp

#Other (generic) stuff
from time import sleep, time
from random import randint, choice, shuffle, uniform
import math
import signal #for blocking the script from terminating when run in terminal
import subprocess #for managing commands to bash


"""
2. CONSTANTS / INITIAL VARIABLES AND GENERAL FUNCTIONS
"""


town = "Atherton" #Change these to locales near the player
nearby_towns = ["Bolton", "Leigh", "Tyldesley",
                "Hindley Green", "Daisy Hill",
                "Westhaughton", "Astley", "Worsley",
                "Over Hulton", "Little Hulton"]

year = 2049
game_index = year - 2049 + 24
temp = 1.5
spinner = ["|", "/", "-", "\\"]
flpsecs = 8 #how many secs do you want the temp/year readout to display for?

def displayTemp(temp, flpsecs): #Single loop of temp reading
    flp.clear()
    flp.print_str("TEMP")
    flp.show()
    sleep(flpsecs/2)
    
    #Reading in digit by digit (inc. decimal)
    flp.clear()
    temp = str(round(temp, 1))
    flp.set_digit(0, "+")
    flp.set_digit(1, str(temp[0]))
    flp.set_decimal(1, True)
    flp.set_digit(2, str(temp[2]))
    flp.set_digit(3, "C")
    flp.show()
    sleep(flpsecs)
    
def displayYear(year, flpsecs): #Single loop of year reading
    flp.clear()
    flp.print_str("YEAR")
    flp.show()
    sleep(flpsecs/2)
    
    flp.clear()
    flp.print_number_str(str(year))
    flp.show()
    sleep(flpsecs)
    
def displaySpinner(spinner, i): #i = number of full cycles
    for iterations in range(i):
        for s in spinner:
            s = s * 4 #Making 4 copies of the same character, one per digital number display
            flp.clear()
            flp.print_str(s)
            flp.show()
            sleep(1/16.0)

def interstitialWaves(cycles): # Wave graphics for SPHD. 
    for iteration in range(0, cycles): #How many times the pattern cycles
        t = time() * 10
        for x in range(17): #17 = x pixels
            for y in range(7): #7 = y pixels
                b = math.sin(x + y + t) + math.cos(x + y + t)
                b = (b + 2) / 4
                sphd.set_pixel(x, y, b)
        sphd.show()

def clearSPHD():
    sphd.clear()
    sphd.show()

def resourcePlusMinus(flux): #For requests (sending)
    global scen
    if scen.resource_requested == "people":
        people.amount = int(people.amount + (people.amount * flux))
    elif scen.resource_requested == "food":
        food.amount = int(food.amount + (food.amount * flux))
    elif scen.resource_requested == "water":
        water.amount = int(water.amount + (water.amount * flux))
    elif scen.resource_requested == "photo voltaics":
        pv.amount = int(pv.amount + (pv.amount * flux))
    elif scen.resource_requested == "electronics":
        electronics.amount = int(electronics.amount + (electronics.amount * flux))
    elif scen.resource_requested == "building materials":
        building_materials.amount = int(building_materials.amount + (building_materials.amount * flux))
    elif scen.resource_requested == "tools":
        tools.amount = int(tools.amount + (tools.amount * flux))
    elif scen.resource_requested == "medical supplies":
        medical_supplies.amount = int(medical_supplies.amount + (medical_supplies.amount * flux))

def resourceAdd(): #For making requests
    global memo
    if memo.item1 == "people" or memo.item2 == "people":
        people.amount = int(people.amount + randint(15, 40))
    elif memo.item1 == "food" or memo.item2 == "food":
        food.amount = int(food.amount + randint(15, 80))
    elif memo.item1 == "water" or memo.item2 == "water":
        water.amount = int(water.amount + randint(10, 25))
    elif memo.item1 == "photo voltaics" or memo.item2 == "photo voltaics":
        pv.amount = int(pv.amount + randint(5, 10))
    elif memo.item1 == "electronics" or memo.item2 == "electronics":
        electronics.amount = int(electronics.amount + randint(2, 8))
    elif memo.item1 == "building materials" or memo.item2 == "building materials":
        building_materials.amount = int(building_materials.amount + randint(1, 5))
    elif memo.item1 == "tools" or memo.item2 == "tools":
        tools.amount = int(tools.amount + randint(2, 10))
    elif memo.item1 == "medical supplies" or memo.item2 == "medical supplies":
        medical_supplies.amount = int(medical_supplies.amount + randint(2, 8))

"""
3. SPLASH SCREEN
"""

inky = auto() 

#Setting up Inky for logo display
inky.set_border(inky.BLACK)
img = Image.open("/home/brooker/Desktop/SolarpunkFutures/sp_logo.png")
inky.set_image(img)
inky.show()

sleep(10) #Gives Inky a chance to catch up.

interstitialWaves(250)
clearSPHD()

title = sphd.write_string("   Solarpunk Futures ") #The leading spaces starts the title off-screen
for scroll_line in range(0, title-3): #The -3 stops the scroll immediately after the last character
    sphd.show()
    sphd.scroll(1)
    sleep(0.05) #Scroll speed (lower for faster)
clearSPHD()

interstitialWaves(500)
clearSPHD()

sleep(10) #Gives Inky time to catch up

displaySpinner(spinner, 6)
displayTemp(temp, flpsecs)
displayYear(year, flpsecs)
        
"""
4. GAMEPLAY
"""

    #4. 1. Objects and General Gameplay Functions

def incomingMessageScreen(): #Everything for drawing the screen
    #Setup
    img = Image.new("P", (inky.WIDTH, inky.HEIGHT))
    draw = ImageDraw.Draw(img)
    font1 = ImageFont.truetype(HankenGroteskMedium, 14)
    font2 = ImageFont.truetype(HankenGroteskMedium, 24)
    font3 = ImageFont.truetype(HankenGroteskMedium, 12)
    
    #Individual bits of text and their locations
    message1 = "Mutual Aid Union:"
    w1, h1 = font1.getsize(message1)
    x1 = 2
    y1 = 2

    message2 = town + " Branch"
    w2, h2 = font1.getsize(message2)
    x2 = 4 + w1
    y2 = 2

    message3 = "Incoming Message..."
    w3, h3 = font2.getsize(message3)
    x3 = (inky.WIDTH/2) - (w3/2)
    y3 = (inky.HEIGHT/2) - (h3/2)

    message4 = "[open >>]"
    w4, h4 = font3.getsize(message4)
    x4 = (inky.WIDTH) - w4 - 2
    y4 = (inky.HEIGHT) - h4 - 2

    draw.text((x1, y1), message1, inky.BLACK, font1)
    draw.text((x2, y2), message2, inky.YELLOW, font1)
    draw.text((x3, y3), message3, inky.BLACK, font2)
    draw.text((x4, y4), message4, inky.BLACK, font3)
    inky.set_image(img)
    inky.show()
    
class Resources:
    resource_list = [] #Keeping track of all resources
    def __init__(self, name, LED_index, amount, collective_noun, max_graph_num):
        self.name = name #resource_list position; 0
        self.LED_index = LED_index #1
        self.amount = amount #2
        self.collective_noun = collective_noun #3
        self.max_graph_num = max_graph_num #4
        Resources.resource_list.append([self.name, self.LED_index, self.amount, self.collective_noun, self.max_graph_num])
    def graphCalc(self): #for calculating number of LEDs to switch on per resource
        return int((self[2] / self[4]) * 7) #amount/max_graph_num * 7 (number of LEDs per column)
    
    #Resource data - initialising (though amounts will fluctuate)
people = Resources("people", 0, randint(100, 350), "members", 500)
food = Resources("food", 2, randint(100, 300), "baskets", 500)
water = Resources("water", 4, randint(50, 150), "barrels", 250)
pv = Resources("photo voltaics", 6, randint(40, 80), "panels", 150)
electronics = Resources("electronics", 8, randint(30, 60), "boxes", 80)
building_materials = Resources("building materials", 10, randint(15, 30), "pallets", 50)
tools = Resources("tools", 12, randint(20, 50), "packs", 100)
medical_supplies = Resources("medical supplies", 14, randint(20, 40), "bundles", 100)
morale = Resources("morale", 16, randint(30, 55), "units", 100)

def updateResources(resource_list): #Effectively for converting from class attributes to lists that can be read
    for item in resource_list:
        if item[0] == "people":
            item[2] = people.amount
        elif item[0] == "food":
            item[2] = food.amount
        elif item[0] == "water":
            item[2] = water.amount
        elif item[0] == "photo voltaics":
            item[2] = pv.amount
        elif item[0] == "electronics":
            item[2] = electronics.amount
        elif item[0] == "building materials":
            item[2] = building_materials.amount
        elif item[0] == "tools":
            item[2] = tools.amount
        elif item[0] == "medical supplies":
            item[2] = medical_supplies.amount
        elif item[0] == "morale":
            item[2] = morale.amount

def drawResource(resource): #Drawing the graph
    global game_state
    if resource[2] <= 0: #Clearing a column if a resource amount falls to zero or below
        sphd.clear_rect(resource[1], 0, 1, 7)
        sphd.show()
        game_state = "game over"
    else:
        level = Resources.graphCalc(resource)
        for y in range(0, level):
            sphd.set_pixel(resource[1], abs(6-y), 0.2) #resource[1] is LED index, abs(6-y) begins each bar at the bottom of the graph, 0.2 is brightness
        sphd.show()
      
class Scenario: #Template for writing lines of text to the screen as a scenario
    scenario_list = [] #Keeping track of scenarios
    def __init__(self, resource_requested, l1, l2, l3, l4, l5, l6, l7, l8):
        self.resource_requested = resource_requested
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        self.l4 = l4
        self.l5 = l5
        self.l6 = l6
        self.l7 = l7
        self.l8 = l8
        Scenario.scenario_list.append(self)

    #Scenario data - TODO: modularise this out, it's massive and unecessary here
s1 = Scenario("people",
              "This is big. Just got a tip-off that some",
              "surveyors are coming to scope out some",
              "nearby land for a shale gas extraction facility.",
              "Sending everybody we can spare over to",
              "block the roads; might be fucked either way,",
              "but can anyone send any help?",
              "",
              "")

s2 = Scenario("people",
              "Hey, how's it going in " + town + "? Just",
              "messaging cos we've got a load of new",
              "members this last few months and we could do",
              "with training them up in 3D printing, first aid",
              "& hydroponics. We heard you've got plenty of",
              "good mentors, any chance you could send",
              "them our way please?",
              "")

s3 = Scenario("people",
              "Hey " + town + ", we've had a HUGE yield on",
              "our farms this year, struggling to get",
              "everything picked...any chance you could",
              "send some people our way to help out, so",
              "it doesn't go to waste? Cheers.",
              "",
              "",
              "")

s4 = Scenario("food",
              "Really gutted, some sort of blight has got",
              "most of our vegetable crops this year, we're",
              "now running a bit short on food, can't really",
              "see what else we can do, so I'm putting out",
              "a general request on the MAU network; any",
              "food you can send us would be really helpful,",
              "thank you.",
              "")

s5 = Scenario("food",
              "Hi all, I'm organising a local festival, but",
              "food-wise we've only really got the basics",
              "covered. Wondering if anyone has any",
              "particularly exciting stuff they could send",
              "over maybe, make it as special as we can?",
              "Thanks!",
              "",
              "")

s6 = Scenario("food",
              "Police came, trampled our fields to shit.",
              "",
              "We've got enough in storage to get us by,",
              "but now we're expecting a bit of a tight",
              "food year, anyone fancy throwing some stuff",
              "our way please? More just to cheer us up",
              "than anything else...",
              "")

s7 = Scenario("water",
              "Did you get bitten much by the drought",
              "this year " + town + "? We're pretty dry,",
              "crops reasonably OK but our animals have",
              "suffered a little, any spare water at all",
              "please?",
              "",
              "",
              "")

s8 = Scenario("water",
              "These fucking water butts are the bane of",
              "my life! We've got these pressurised ones",
              "to help with the irrigation, but a valve",
              "on the main feed popped, must have been",
              "weeks ago but only just realised why the",
              "pressure had dropped today...we're short",
              "quite a few gallons to say the least. Help?",
              "")

s9 = Scenario("water",
              "Hey, sending this to all, our cooling",
              "system for the computer network has got",
              "a leak, we're in the process of fixing it",
              "but don't really have any spare water to",
              "keep refilling and testing it. Anyone able",
              "to send any please? Pretty urgent, hardware",
              "overheating fast.",
              "")

s10 = Scenario("photo voltaics",
              "That hailstone last winter absolutely",
              "battered our PVs, we've been limping along",
              "alright since then, but loads of new members",
              "means loads more energy draw...think we",
              "need to replace them, any panels you could",
              "spare would be gratefully received, thanks!",
              "",
              "")

s11 = Scenario("photo voltaics",
              "Some fucking idiot knocked a hole in one",
              "of our water pipes, flooded the battery",
              "store and the water has completely fried",
              "ALL of our PVs. Seriously, any help please?",
              " ",
              "Lots of love, from The Fucking Dark Ages :-/",
              "",
              "")

s12 = Scenario("photo voltaics",
              "Weird one maybe, but we've now got a good",
              "few new members with science training of",
              "one kind or another, hoping to build them",
              "a facility and start a kind of research",
              "institute type thing? BIG energy demand,",
              "says our planners...some extra PVs would be",
              "really helpful please!",
              "")

s13 = Scenario("electronics",
              "Guess who didn't rain-proof their",
              "hydroponics system? Fuck, so annoyed",
              "with myself, sorry to have to ask but",
              "we weren't anticipating needing to use",
              "our electronics supply so heavily, we're",
              "a bit short, anyone got any spares to send",
              "please?",
              "")

s14 = Scenario("electronics",
              "We've got a bit of a dearth of talent in",
              "the electronics department, desperately",
              "need to run some training - we've got the",
              "people, but teaching n00bs is the kind of",
              "thing that leads to lots of fried components,",
              "anticipating we'll need lots of spares - any",
              "help please?",
              "")

s15 = Scenario("electronics",
              "There's a woman here who says she can soup",
              "up our electric fences AND reduce the power",
              "draw. Not sure how, but we could do with",
              "saving the energy and she's confident with it",
              "so thinking if we can get her some components",
              "we could let her have a try, any spares much",
              "appreciated, thanks!",
              "")

s16 = Scenario("building materials",
              "I SAID we should replace the felt in the",
              "storehouse roof, but no, I was being",
              "\"wasteful\". Whatever. Now our wood has",
              "rotted, and our sand is filthy. And I'm",
              "supposed to come cap in hand to the MAU",
              "for help, so...",
              "",
              "")

s17 = Scenario("building materials",
              "Don't know how to say this, all still in",
              "shock. A power node got flooded in a surge",
              "from the brook, shorted the electricity and",
              "caused a fire in connected houses. Two died.",
              "Urgently need to build new houses for the",
              "survivors, any building materials would go",
              "to good use.",
              "")

s18 = Scenario("building materials",
              "We've just taken in a new surgical specialist;",
              "can finally pull the trigger on extending our",
              "clinic, woo! We'll be able to get her to work",
              "as soon as we can get the place built, anybody",
              "able to chip in some materials please?",
              "",
              "",
              "")

s19 = Scenario("tools",
              "Hey " + town + ", do I remember right you",
              "did some work on your housing recently?",
              "Do you have any of the tools left over",
              "still? We're wanting to do something",
              "similar, but could do with some better",
              "kit if there's any spare please? Any tips",
              "on doing the work welcome too!",
              "")

s20 = Scenario("tools",
              "Hey all, we're running a soapbox derby for",
              "our kids, trying to plug that mechanical",
              "engineering gap before it's a gap kind of",
              "thing...can anyone help us putting together",
              "some toolkits for them please?",
              "",
              "",
              "")

s21 = Scenario("tools",
              "We're in touch with a pretty solid new MAU",
              "community just outside " + choice(nearby_towns) + ",",
              "wondering if you might be able to contribute",
              "anything to a welcome pack for them, help",
              "get  them set up? Specifically, if you've got any",
              "tools to send, that'd be really great thanks.",
              "",
              "")

s22 = Scenario("medical supplies",
              "Hey " + town + ", we've had a flood in our clinic",
              "and it's made a mess of more than a few",
              "batches of medical supplies - we're sending",
              "a call round to see if anyone has any to",
              "spare, anything you can send would be really",
              "helpful, thanks.",
              "",
              "")

s23 = Scenario("medical supplies",
              town + ", the police just busted our clinic on",
              "some ridiculous drug dealing charge, we could",
              "do with some help please. We have plenty",
              "materials and people to rebuild things, but",
              "they've took basically all of our medical",
              "supplies, anything you can send our way",
              "maybe?",
              "")

s24 = Scenario("medical supplies",
              "This one's going out to the entire MAU, we've",
              "had a really dire round of COVID and though",
              "we're handling it OK, we're pretty low on",
              "medical supplies with a clinic full still. We ",
              "reckon we can kick it in about three weeks",
              "but does anyone have any spare medical",
              "supplies to get us there please?",
              "")

s25 = Scenario("water",
              "We've been boycotting our water bills on",
              "account of the sewage being pumped into",
              "our brook - being threatened with legal",
              "action, so want to go temporarily",
              "completely non-reliant on water companies",
              "to help our case. Any water you can send",
              "is going to be very helpful, thanks!",
              "")


def drawScenario(scen):
    #Setup
    img = Image.new("P", (inky.WIDTH, inky.HEIGHT))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(HankenGroteskMedium, 12)
    x = 2 #Constant horizontal placement, for left-alignment of text

    #Drawing each line individually because graphics are a pain in the arse
    #Not all lines might get used; this is like a text engine for line placement
    line1 = scen.l1 #the text per line
    w1, h1 = font.getsize(line1) #the size of the specified line
    y1 = 2 #placement on vertical axis, relative to screen and previous lines
    
    line2 = scen.l2
    w2, h2 = font.getsize(line2)
    y2 = 2 + y1 + h1
    
    line3 = scen.l3
    w3, h3 = font.getsize(line3)
    y3 = 2 + y2 + h2
    
    line4 = scen.l4
    w4, h4 = font.getsize(line4)
    y4 = 2 + y3 + h3
    
    line5 = scen.l5
    w5, h5 = font.getsize(line5)
    y5 = 2 + y4 + h4
    
    line6 = scen.l6
    w6, h6 = font.getsize(line6)
    y6 = 2 + y5 + h5
        
    line7 = scen.l7
    w7, h7 = font.getsize(line7)
    y7 = 2 + y6 + h6
    
    line8 = scen.l8
    w8, h8 = font.getsize(line8)
    y8 = 2 + y7 + h7
    
    command = " [next >>]" #UI type stuff
    wc, hc = font.getsize(command)
    xc = (inky.WIDTH) - wc - 2 #right aligning this one
    yc = (inky.HEIGHT) - hc - 1 #just off bottom of screen
    
    signoff = "-- " + choice(nearby_towns) + " Branch"
    ws, hs = font.getsize(signoff)
    xs = (inky.WIDTH) - wc - ws - 2 #right align relative to command above
    ys = yc #pegging y location to command to keep them in line
    
    #drawing each element to the canvas, locking it together, showing it
    draw.text((x, y1), line1, inky.BLACK, font)
    draw.text((x, y2), line2, inky.BLACK, font)
    draw.text((x, y3), line3, inky.BLACK, font)
    draw.text((x, y4), line4, inky.BLACK, font)
    draw.text((x, y5), line5, inky.BLACK, font)
    draw.text((x, y6), line6, inky.BLACK, font)
    draw.text((x, y7), line7, inky.BLACK, font)
    draw.text((x, y8), line8, inky.BLACK, font)
    draw.text((xc, yc), command, inky.BLACK, font)
    draw.text((xs, ys), signoff, inky.YELLOW, font)
    inky.set_image(img)
    inky.show()
    
def drawRequest(scen):
    global res
    for item in Resources.resource_list: #Establishing the thing being requested
        if item[0] == scen.resource_requested:
            res = item
            
    #Setup
    img = Image.new("P", (inky.WIDTH, inky.HEIGHT))
    draw = ImageDraw.Draw(img)
    font1 = ImageFont.truetype(HankenGroteskMedium, 14)
    font2 = ImageFont.truetype(HankenGroteskMedium, 18)
    font3 = ImageFont.truetype(HankenGroteskMedium, 12)
    
    title1 = "STOCK SUMMARY:"
    wt1, ht1 = font1.getsize(title1)
    xt1 = 2
    yt1 = 2
    
    title2 = scen.resource_requested.upper()
    wt2, ht2 = font1.getsize(title2)
    xt2 = 2
    yt2 = yt1 + ht1 + 2
    
    request1 = str(res[2]).upper() + " " + res[3].upper()
    w1, h1 = font2.getsize(request1)
    x1 = (inky.WIDTH/2) - (w1/2)
    y1 = 45
    
    request2 = "[D: " + str(int((res[2]/100) * 75)) + " (75%)]"
    w2, h2 = font3.getsize(request2)
    x2 = inky.WIDTH - w2 - 2
    y2 = inky.HEIGHT - h2 - 1
    
    request3 = "[B: " + str(int((res[2]/100) * 25)) + " (25%)]"
    w3, h3 = font3.getsize(request3)
    x3 = 2
    y3 = y2
    
    request4 = "[C: " + str(int((res[2]/100) * 50)) + " (50%)]"
    w4, h4 = font3.getsize(request4)
    x4 = inky.WIDTH - w4 - 2
    y4 = y2 - h4 - 2
    
    request5 = "[A:  0   (0%)]"
    w5, h5 = font3.getsize(request5)
    x5 = 2
    y5 = y2 - h5 - 2
    
    request6 = "-------------------------------"
    w6, h6 = font2.getsize(request6)
    x6 = 2
    y6 = y5 - h5 - 3
    
    request7 = "[choose amount to send]"
    w7, h7 = font3.getsize(request7)
    x7 = inky.WIDTH - w7 - 2
    y7 = y6 - 3
    
    draw.text((xt1, yt1), title1, inky.BLACK, font1)
    draw.text((xt2, yt2), title2, inky.YELLOW, font1)
    draw.text((x1, y1), request1, inky.YELLOW, font2)
    draw.text((x2, y2), request2, inky.BLACK, font3)
    draw.text((x3, y3), request3, inky.BLACK, font3)
    draw.text((x4, y4), request4, inky.BLACK, font3)
    draw.text((x5, y5), request5, inky.BLACK, font3)
    draw.text((x6, y6), request6, inky.BLACK, font2)
    draw.text((x7, y7), request7, inky.BLACK, font3)

    inky.set_image(img)
    inky.show()

class InternalMemo: #Template for writing lines of text to the screen as an internal memo
    memo_list = [] #Keeping track of internal memos
    def __init__(self, item1, item2, l2, l3, l4, l5, l6, l7): #starts at l2 because there's a title on line 1
        self.item1 = item1
        self.item2 = item2
        self.l2 = l2
        self.l3 = l3
        self.l4 = l4
        self.l5 = l5
        self.l6 = l6
        self.l7 = l7
        InternalMemo.memo_list.append(self)

m1 = InternalMemo("food",
                  "building materials",
                  "Some bugs got into our food stores, made",
                  "a mess of lots of our arable crops. Could",
                  "do with replacing the lost crops and",
                  "repairing the store walls to keep the",
                  "bugs out. Check the inventory, what's our",
                  "priority for an MAU request?")

m2 = InternalMemo("people",
                  "photo voltaics",
                  "We've been quizzing " + choice(nearby_towns) + " branch",
                  "about the possibility of boycotting energy",
                  "companies; they've given us some schematics",
                  "for new PV arrays and have told us to expect",
                  "to have to organise protests - should we send,",
                  "out an MAU request for PVs or people?")

m3 = InternalMemo("medical supplies",
                  "electronics",
                  "Our refrigeration in the clinic got fried by",
                  "a surge from a shonky battery, took out the",
                  "whole power supply to the building and all",
                  "the medicines and blood stuff in the fridges",
                  "is trashed - make an urgent MAU request.",
                  "")

m4 = InternalMemo("tools",
                  "water",
                  "Testing our new central heating system has",
                  "done a real number on our water stores (SO",
                  "MANY LEAKS) and this new coolant has made",
                  "a gloopy mess on loads of the tools we were",
                  "using too - any chance of asking the MAU",
                  "for some help maybe?")

m5 = InternalMemo("photo voltaics",
                  "electronics",
                  "The team building our new solar capture",
                  "array are struggling with the components",
                  "we've got in store, they're a bit old and",
                  "inefficient apparently...does anyone in the",
                  "MAU have any they could spare us?",
                  "")

m6 = InternalMemo("people",
                  "food",
                  "We really need a recruitment drive, we're",
                  "going to start struggling in the next few",
                  "years if we don't have some manufacturing",
                  "specialists coming in - can we see if the",
                  "MAU has anyone to spare, or maybe they can",
                  "contribute some food for a recruitment event?")

m7 = InternalMemo("water",
                  "building materials",
                  "We've had a load of new members asking to",
                  "join us in " + town + " lately; thinking of",
                  "putting them up in the empty houses across",
                  "from Newbrook Road, but would need to fix",
                  "those water pipes and fill their tanks first,",
                  "MAU got anything for us?")

m8 = InternalMemo("tools",
                  "medical supplies",
                  "URGENT. Wall between library and main hall",
                  "collapsed, people trapped in rubble, we have",
                  "plenty of locals digging them out with what's",
                  "to hand, but if we quickly get some tools and",
                  "medical supplies for survivors we would be",
                  "have a better chance - MAKE THE REQUEST.")

m9 = InternalMemo("people",
                  "electronics",
                  "Hey, this robotics hackathon next month, it's",
                  "getting much more interest than we thought,",
                  "so we're gonna really go for it - can we get any",
                  "electronics supplies and recruits from other",
                  "MAU members do you think?",
                  "")

m10 = InternalMemo("food",
                   "water",
                   "I'm not especially hopeful that the MAU would",
                   "be able to help us since it's going to be such",
                   "a dry year all across the area, but we're",
                   "particularly worried about the coming harvest,",
                   "and our capacity to irrigate our way there...",
                   "worth a request do you think?")

m11 = InternalMemo("building materials",
                   "tools",
                   "OK, our five year plan for all these new houses",
                   "is more or less set in stone now, so we need",
                   "to think how to get our hands on tools and",
                   "materials - could we send an MAU request",
                   "out please?",
                   "")

m12 = InternalMemo("photo voltaics",
                   "medical supplies",
                   "Our visit to the new clinic in " + choice(nearby_towns),
                   "was great, plenty of good ideas for research",
                   "collaborations that we'd like to pursue, so",
                   "trying to set up a new lab to support it,",
                   "will need some photo voltaics and medical",
                   "supplies, could MAU help us with that?")

m13 = InternalMemo("medical supplies",
                   "food",
                   "We passed a motion to take in a number",
                   "of refugees from the European war, so in",
                   "anticipation of them arriving (prob within",
                   "the month), we want to make sure we have",
                   "everything we need with regards food and",
                   "medical supplies - request whatever we need.")

m14 = InternalMemo("people",
                   "water",
                   "The extreme heat is starting wildfires between",
                   town + " and " + choice(nearby_towns) + " and we're not",
                   "really able to contain it ourselves, things",
                   "getting out of hand, ask the MAU if they can",
                   "spare any people or water to help with the",
                   "effort, mark it URGENT.")

m15 = InternalMemo("photo voltaics",
                   "tools",
                   "We've voted yes on a project trying to connect",
                   "our power networks to " + choice(nearby_towns) + " as a ",
                   "sort of testbed for a future whole-area power",
                   "sharing linkup. Which is great news, but do",
                   "you think we could get some support with the",
                   "required PVs and tools from the MAU please?")

m16 = InternalMemo("electronics",
                   "building materials",
                   "I don't know why it fell to " + town + " but",
                   "apparently we're fixing the substations that",
                   choice(nearby_towns) + " wrecked with their shitty wiring...",
                   "Was thinking the least MAU could do is help",
                   "out with our electronics and building material",
                   "supplies, what do you reckon?")

m17 = InternalMemo("people",
                   "medical supplies",
                   "Recent events in the European War have been",
                   "on our mind and we want to help if we can.",
                   "We're organising our area MAU's contribution,",
                   "so let's request support with the relief effort;",
                   "any people and/or medical supplies we can",
                   "contribute will make a big difference.")

m18 = InternalMemo("food",
                   "tools",
                   "Hey, the agri-festival next month, we've",
                   "got a group of labourers coming in to help set",
                   "stages and tents up, but would be nice if we",
                   "could lay out the red carpet with some nice",
                   "food for them, and if we could save them",
                   "a job carting all their tools over...?")

m19 = InternalMemo("water",
                   "electronics",
                   "The more we're adding capacity to our",
                   "computing networks, the more we're realising",
                   "our cooling system is a bit out-dated...any",
                   "chance we could ask MAU if they've any",
                   "electronics to spare, or even just some extra",
                   "water for us to test with?")

m20 = InternalMemo("photo voltaics",
                   "building materials",
                   "We've had a few worrying power fluctuations",
                   "across the whole of " + town + " lately, and",
                   "as a stitch-in-time we'd like to audit",
                   "and undertake some maintenance on our",
                   "battery store building - if the MAU can support,",
                   "that'd be really useful.")

m21 = InternalMemo("people",
                   "tools",
                   "The expansion of the coal reclaimation facility",
                   "in our area is unacceptable, we're sending",
                   "people in to dismantle the lifters and block",
                   "the roads up there. We have some help from",
                   choice(nearby_towns) + " but any people or tools from",
                   "MAU would give us a better chance.") 

m22 = InternalMemo("food",
                   "photo voltaics",
                   "The hottest summer of all time continues to",
                   "screw us up in a thousand little ways. This",
                   "time it's fridges - the photo voltaics are",
                   "burning to a crisp and our fridges are crapping",
                   "out, food spoiling quicker than normal. MAU?",
                   "")

m23 = InternalMemo("water",
                   "medical supplies",
                   "We're taking in some of the injured from the",
                   "wildfires out East past the MAU, they're",
                   "going to need medical treatment for sure",
                   "but I said I could ask about sourcing them",
                   "some water to help with the firefighting effort",
                   "too - what's possible here?")

m24 = InternalMemo("photo voltaics",
                   "water",
                   "OK, should have anticipated this more fully",
                   "than we did, but the new houses between here",
                   "and " + choice(nearby_towns) + " have dropped the water",
                   "pressure across " + town + ". Need a new",
                   "water pump pretty quickly to level out the",
                   "supply - PVs and additional water from MAU?")

m25 = InternalMemo("tools",
                   "electronics",
                   "Our trip to the kids' makerspace at " + choice(nearby_towns),
                   "was SO good! Learned a lot and we want to get",
                   "something similar going here - we can use",
                   "the old substation building for it, but",
                   "could do with a stock of tools and electronics",
                   "to kick us off, if the MAU can help?")


def drawInternalMemo(memo):
    #Setup
    img = Image.new("P", (inky.WIDTH, inky.HEIGHT))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(HankenGroteskMedium, 12)
    x = 2 #Constant horizontal placement, for left-alignment of text

    #Drawing each line individually because graphics are a pain in the arse
    #Not all lines might get used; this is like a text engine for line placement
    line1 = "INTERNAL MEMO:" #the text per line
    w1, h1 = font.getsize(line1) #the size of the specified line
    y1 = 2 #placement on vertical axis, relative to screen and previous lines
    
    line2 = memo.l2
    w2, h2 = font.getsize(line2)
    y2 = 2 + y1 + h1
    
    line3 = memo.l3
    w3, h3 = font.getsize(line3)
    y3 = 2 + y2 + h2
    
    line4 = memo.l4
    w4, h4 = font.getsize(line4)
    y4 = 2 + y3 + h3
    
    line5 = memo.l5
    w5, h5 = font.getsize(line5)
    y5 = 2 + y4 + h4
    
    line6 = memo.l6
    w6, h6 = font.getsize(line6)
    y6 = 2 + y5 + h5
    
    line7 = memo.l7
    w7, h7 = font.getsize(line7)
    y7 = 2 + y6 + h6
    
    command = " [next >>]" #UI type stuff
    wc, hc = font.getsize(command)
    xc = (inky.WIDTH) - wc - 2 #right aligning this one
    yc = (inky.HEIGHT) - hc - 1 #just off bottom of screen
    
    signoff = "-- " + town + " Branch"
    ws, hs = font.getsize(signoff)
    xs = (inky.WIDTH) - wc - ws - 2 #right align relative to command above
    ys = yc #pegging y location to command to keep them in line
    
    #drawing each element to the canvas, locking it together, showing it
    draw.text((x, y1), line1, inky.BLACK, font)
    draw.text((x, y2), line2, inky.BLACK, font)
    draw.text((x, y3), line3, inky.BLACK, font)
    draw.text((x, y4), line4, inky.BLACK, font)
    draw.text((x, y5), line5, inky.BLACK, font)
    draw.text((x, y6), line6, inky.BLACK, font)
    draw.text((x, y7), line7, inky.BLACK, font)
    draw.text((xc, yc), command, inky.BLACK, font)
    draw.text((xs, ys), signoff, inky.YELLOW, font)
    inky.set_image(img)
    inky.show()
    
def drawMakeRequest(memo):
    for item in Resources.resource_list: #Establishing the two items to choose between
        if item[0] == memo.item1:
            res1 = item
        elif item[0] == memo.item2:
            res2 = item
            
    #Setup
    img = Image.new("P", (inky.WIDTH, inky.HEIGHT))
    draw = ImageDraw.Draw(img)
    font1 = ImageFont.truetype(HankenGroteskMedium, 14)
    font2 = ImageFont.truetype(HankenGroteskMedium, 18)
    font3 = ImageFont.truetype(HankenGroteskMedium, 12)
    
    title = "STOCK SUMMARY:"
    wt, ht = font1.getsize(title)
    xt = 2
    yt = 2
    
    i1 = memo.item1.upper() + ": "
    wi1, hi1 = font1.getsize(i1)
    xi1 = 2
    yi1 = 33
    
    i1_1 = str(res1[2]).upper() + " " + res1[3].upper()
    wi1_1, hi1_1 = font1.getsize(i1_1)
    xi1_1 = xi1 + wi1 + 2
    yi1_1 = yi1

    i2 = memo.item2.upper() + ": "
    wi2, hi2 = font1.getsize(i2)
    xi2 = 2
    yi2 = yi1 + hi1 + 2
    
    i2_1 = str(res2[2]).upper() + " " + res2[3].upper()
    wi2_1, hi2_1 = font1.getsize(i2_1)
    xi2_1 = xi2 + wi2 + 2
    yi2_1 = yi2

    command1 = "[<<: " + memo.item2.upper() + "]"
    wc1, wh1 = font3.getsize(command1)
    xc1 = inky.WIDTH - wc1 - 2
    yc1 = inky.HEIGHT - wh1 - 1
    
    command2 = "[" + memo.item1.upper() + ": >>]"
    wc2, hc2 = font3.getsize(command2)
    xc2 = inky.WIDTH - wc2 - 2
    yc2 = yc1 - hc2 - 2
    
    line = "-------------------------------"
    wl, hl = font2.getsize(line)
    xl = 2
    yl = yc2 - hc2 - 3
    
    command3 = "[choose resource to request]"
    wc3, hc3 = font3.getsize(command3)
    xc3 = inky.WIDTH - wc3 - 2
    yc3 = yl - 3
    
    draw.text((xt, yt), title, inky.BLACK, font1)
    draw.text((xi1, yi1), i1, inky.YELLOW, font1)
    draw.text((xi1_1, yi1_1), i1_1, inky.YELLOW, font1)
    draw.text((xi2, yi2), i2, inky.YELLOW, font1)
    draw.text((xi2_1, yi2_1), i2_1, inky.YELLOW, font1)
    draw.text((xc1, yc1), command1, inky.BLACK, font3)
    draw.text((xc2, yc2), command2, inky.BLACK, font3)
    draw.text((xl, yl), line, inky.BLACK, font2)
    draw.text((xc3, yc3), command3, inky.BLACK, font3)    

    inky.set_image(img)
    inky.show()

def drawGameOverScreen():
    sleep(15)
    
    #Setup
    img = Image.new("P", (inky.WIDTH, inky.HEIGHT))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(HankenGroteskMedium, 12)
    x = 2 #Constant horizontal placement, for left-alignment of text

    #Drawing each line individually because graphics are a pain in the arse
    #Not all lines might get used; this is like a text engine for line placement
    line1 = "INTERNAL MEMO:" #the text per line
    w1, h1 = font.getsize(line1) #the size of the specified line
    y1 = 2 #placement on vertical axis, relative to screen and previous lines
    
    line2 = "I'm really sorry to have to announce this, but"
    w2, h2 = font.getsize(line2)
    y2 = 2 + y1 + h1
    
    line3 = "unfortunately our resources are depleted to"
    w3, h3 = font.getsize(line3)
    y3 = 2 + y2 + h2
    
    line4 = "the point we cannot sustain a community."
    w4, h4 = font.getsize(line4)
    y4 = 2 + y3 + h3
    
    line5 = "The " + town + " MAU Branch is disbanding, with"
    w5, h5 = font.getsize(line5)
    y5 = 2 + y4 + h4
    
    line6 = "immediate effect. We had something special"
    w6, h6 = font.getsize(line6)
    y6 = 2 + y5 + h5
    
    line7 = "and we let it slip away. We're sorry."
    w7, h7 = font.getsize(line7)
    y7 = 2 + y6 + h6
    
    signoff = "-- " + town + " Branch"
    ws, hs = font.getsize(signoff)
    xs = (inky.WIDTH) - ws - 2 #right align
    ys = (inky.HEIGHT) - hs - 2
    
    #drawing each element to the canvas, locking it together, showing it
    draw.text((x, y1), line1, inky.BLACK, font)
    draw.text((x, y2), line2, inky.BLACK, font)
    draw.text((x, y3), line3, inky.BLACK, font)
    draw.text((x, y4), line4, inky.BLACK, font)
    draw.text((x, y5), line5, inky.BLACK, font)
    draw.text((x, y6), line6, inky.BLACK, font)
    draw.text((x, y7), line7, inky.BLACK, font)
    draw.text((xs, ys), signoff, inky.YELLOW, font)
    inky.set_image(img)
    inky.show()

def drawWinScreen():
    sleep(15)
    
    #Setup
    img = Image.new("P", (inky.WIDTH, inky.HEIGHT))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(HankenGroteskMedium, 12)
    x = 2 #Constant horizontal placement, for left-alignment of text

    #Drawing each line individually because graphics are a pain in the arse
    #Not all lines might get used; this is like a text engine for line placement
    line1 = "SUBJECT: THANK YOU, SO MUCH" #the text per line
    w1, h1 = font.getsize(line1) #the size of the specified line
    y1 = 2 #placement on vertical axis, relative to screen and previous lines
    
    line2 = "Hey, just ahead of your retirement party"
    w2, h2 = font.getsize(line2)
    y2 = 2 + y1 + h1
    
    line3 = "I wanted to send a personal message saying"
    w3, h3 = font.getsize(line3)
    y3 = 2 + y2 + h2
    
    line4 = "just how much the " + town + " MAU Branch"
    w4, h4 = font.getsize(line4)
    y4 = 2 + y3 + h3
    
    line5 = "appreciate your work. Words can't express."
    w5, h5 = font.getsize(line5)
    y5 = 2 + y4 + h4
    
    line6 = "I really hope you can get a break and let"
    w6, h6 = font.getsize(line6)
    y6 = 2 + y5 + h5
    
    line7 = "us look after you for a change :-) Thank you."
    w7, h7 = font.getsize(line7)
    y7 = 2 + y6 + h6
    
    signoff = "-- " + town + " Branch"
    ws, hs = font.getsize(signoff)
    xs = (inky.WIDTH) - ws - 2 #right align
    ys = (inky.HEIGHT) - hs - 2
    
    #drawing each element to the canvas, locking it together, showing it
    draw.text((x, y1), line1, inky.BLACK, font)
    draw.text((x, y2), line2, inky.BLACK, font)
    draw.text((x, y3), line3, inky.BLACK, font)
    draw.text((x, y4), line4, inky.BLACK, font)
    draw.text((x, y5), line5, inky.BLACK, font)
    draw.text((x, y6), line6, inky.BLACK, font)
    draw.text((x, y7), line7, inky.BLACK, font)
    draw.text((xs, ys), signoff, inky.YELLOW, font)
    inky.set_image(img)
    inky.show()

    #4. 2. Game Loop

def initialSetup():
    global game_state #A way of syncing commands with screens appropriately
    global year #To be used with digital number display
    global game_index #To keep a track of "rounds" in the game
    
    game_state = "incoming message"
    
    shuffle(Scenario.scenario_list) #A one-time randomisation of the order of scenarios
    shuffle(InternalMemo.memo_list) #A one-time randomisation of the order of memos

    for resource in Resources.resource_list: #Draws the initial graph
        drawResource(resource)

initialSetup()
incomingMessageScreen()

while game_state != "game over": #i.e. stop the game when game over
   
    while game_state == "incoming message":
        @tp.on_touch(["Back", "A", "B", "C", "D", "Enter"])
        def handleTouch(event):
            global game_state
            global game_index
            global scen
            if event.name != "Enter":
                pass
            else:
                scen = Scenario.scenario_list[game_index]
                drawScenario(scen)
                game_state = "scenario"
        break

    while game_state == "scenario":
        @tp.on_touch(["Back", "A", "B", "C", "D", "Enter"])
        def handleTouch(event):
            global game_state
            global game_index
            global scen
            global res
            if event.name != "Enter":
                pass
            else:
                drawRequest(scen)
                game_state = "request"
        break
    
    while game_state == "request":
        @tp.on_touch(["Back", "A", "B", "C", "D", "Enter"])
        def handleTouch(event):
            global res
            global game_state
            global game_index
            global memo
            
            for item in Resources.resource_list:
                if item[0] == scen.resource_requested:
                    res = item
            
            if event.name == "Back" or event.name == "Enter":
                pass
            
            elif event.name == "A": #Gives 0% of resource
                morale.amount = morale.amount - 10
                updateResources(Resources.resource_list)
                clearSPHD()
                for resource in Resources.resource_list: #Draws the graph
                    drawResource(resource)
                
                memo = InternalMemo.memo_list[game_index]
                drawInternalMemo(memo)
                if morale.amount <= 0:
                    game_state = "game over"
                else:
                    game_state = "internal memo"
            
            elif event.name == "B": #Gives 25% of resource
                morale.amount = morale.amount + 2
                flux = int((res[2]/100) * 25)
                resourcePlusMinus(-0.25)
                updateResources(Resources.resource_list)
                clearSPHD()
                for resource in Resources.resource_list: #Draws the graph
                    drawResource(resource)
                
                memo = InternalMemo.memo_list[game_index]
                drawInternalMemo(memo)
                game_state = "internal memo"
            
            elif event.name == "C": #Gives 50% of resource
                morale.amount = morale.amount + 5
                flux = int((res[2]/100) * 50)
                resourcePlusMinus(-0.5)
                updateResources(Resources.resource_list)
                clearSPHD()
                for resource in Resources.resource_list: #Draws the graph
                    drawResource(resource)
                
                memo = InternalMemo.memo_list[game_index]
                drawInternalMemo(memo)
                game_state = "internal memo"
                
            elif event.name == "D": #Gives 75% of resource
                morale.amount = morale.amount + 8
                flux = int((res[2]/100) * 75)
                resourcePlusMinus(-0.75)
                updateResources(Resources.resource_list)
                clearSPHD()
                for resource in Resources.resource_list: #Draws the graph
                    drawResource(resource)
                
                memo = InternalMemo.memo_list[game_index]
                drawInternalMemo(memo)
                game_state = "internal memo"
                
        break
    
    while game_state == "internal memo":
        @tp.on_touch(["Back", "A", "B", "C", "D", "Enter"])
        def handleTouch(event):
            global game_state
            global game_index
            global memo
            global res
            if event.name != "Enter":
                pass
            else:
                drawMakeRequest(memo)
                game_state = "make request"
        break
    
    while game_state == "make request":
        @tp.on_touch(["Back", "A", "B", "C", "D", "Enter"])
        def handleTouch(event):
            global game_state
            global game_index
            global memo
            if event.name == "A" or event.name == "B" or event.name == "C" or event.name == "D":
                pass
            elif event.name == "Enter":
                resourceAdd()
                updateResources(Resources.resource_list)
                
                clearSPHD()
                for resource in Resources.resource_list: #Draws the graph
                    drawResource(resource)
                    
                inky.set_border(inky.BLACK)
                img = Image.open("/home/brooker/Desktop/SolarpunkFutures/sp_logo.png")
                inky.set_image(img)
                inky.show()
                game_state = "idle"
                    
            elif event.name == "Back":
                resourceAdd()
                updateResources(Resources.resource_list)
                
                clearSPHD()
                for resource in Resources.resource_list: #Draws the graph
                    drawResource(resource)
                    
                inky.set_border(inky.BLACK)
                img = Image.open("/home/brooker/Desktop/SolarpunkFutures/sp_logo.png")
                inky.set_image(img)
                inky.show()
                game_state = "idle"
        break
    
    while game_state == "idle":
        year = year + 1
        game_index = game_index + 1
        if game_index == 25: #Win criteria - you made it 25 years, break out of game loop
            game_state = "game over"
            break
        temp = temp + round(uniform(0.005, 0.05), 2) #like randint but for floats, to 2 dec places.
        displaySpinner(spinner, 6)
        sleep_time = 60 #One minute, plus rounding up - for testing/demonstration purposes
        #sleep_time = 57600 #16 hours
        for time in range(0, int(sleep_time / flpsecs)): #Cycling through YEAR/TEMP for sleep_time
            displayTemp(temp, flpsecs)
            displayYear(year, flpsecs)
        incomingMessageScreen()
        game_state = "incoming message"
        break

if game_state == "game over":
    if morale.amount <= 0:
        drawGameOverScreen()
    elif morale.amount > 0 and game_index == 25:
        drawWinScreen()
    
    sleep(60) #Gives time for players to read before auto-shutdown
    
    #Display logo
    inky.set_border(inky.BLACK)
    img = Image.open("/home/brooker/Desktop/SolarpunkFutures/sp_logo.png")
    inky.set_image(img)
    inky.show()

    interstitialWaves(250)

    sleep(20) #Let inky catch up 
    
    flp.clear()
    flp.show()
    
    clearSPHD()
    
    tp.all_off()
    
    
    subprocess.run(["sudo", "shutdown"])
    quit()
    #Bye bye MAU :-(

signal.pause()