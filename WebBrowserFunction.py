#This snippet of code details the functions related to collecting a screenshot to assess genome fitness within the game QWOP using screenshots taken.

from selenium import webdriver
import time
import keyboard
import pytesseract
import os
from PIL import Image
import random
import threading
from io import BytesIO
import re

#Get screenshot of the game QWOP.
#Parse the id and find game content and then collect width and height and take a screenshot.
def getscreenshot(driver):
    # Def gets image
    link = driver.find_element_by_id("gameContent")
    location = link.location
    size = link.size
    png = driver.get_screenshot_as_png()
    im = Image.open(BytesIO(png))  # uses PIL library to open image in memory

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    im = im.crop((left, top, right, bottom))  # defines crop points
    im.save('screenshot.png')  # saves new cropped image


var = 0

#Read screenshot using tessaract then check for meters
def fitness_check(image):
    img = Image.open(image)
    text_on_screen = pytesseract.image_to_string(img)
    fitness = re.findall("(\-?[0-9]+\.[0-9]+) metres", text_on_screen) #using regular expression to continually collect the score off a screenshot
    if not fitness:
        return 0
    else:
        fitness = fitness[0]
        return fitness

#Read screenshot using tessaract to if game is done by checking for the words national hero or participant
def done(image):
    img = Image.open(image)
    text_on_screen = pytesseract.image_to_string(img)
    text = re.findall("PARTICIPANT", text_on_screen) 
    National_Hero = re.findall("NATIONAL HERO", text_on_screen)
    if National_Hero == "NATIONAL HERO":
        return National_Hero
    if not text:
        return None
    else:
        text = text[0]
        return text
