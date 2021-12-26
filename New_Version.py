import pyautogui
import time
from pynput.keyboard import Key, Controller

keyboard = Controller()

time.sleep(3)

# Variables:
quest_status = "Quest_Done"
# RGB
hedgehog = (189, 138, 66)
gardener = (49, 73, 49)
gardener_eye = (132, 219, 144)
flower_rgb = (247, 214, )
# Cords
next_click = (830, 620)
let_me_hear = (300, 485)
flower_cords = (1120, 600)
# Regions
region_screen = (15, 55, 1885, 630)
region_sword = (35, 720, 125, 280)
region_marks = (25, 625, 220, 50)   # confidence=0.6
region_quest_finished = (300, 900, 830, 35)
region_action = (285, 985, 730, 30)
region_spell = (285, 985, 500, 30)
region_gardener_quest = (180, 300, 770, 40)

# Functions
def key_hold(key, hold_time):
    start = time.time()
    while time.time() - start < hold_time:
        keyboard.press(key)
    keyboard.release(key)

def region_scan_click(region_tuple, rgb_tuple, key, key_hold_time):
    key_hold(key, key_hold_time)
    time.sleep(key_hold_time)

    screen = pyautogui.screenshot(region=region_tuple)
    start_x = region_tuple[0]
    start_y = region_tuple[1]
    lenght_x = region_tuple[0] + region_tuple[2]
    lenght_y = region_tuple[1] + region_tuple[3]
    for x in range(start_x, lenght_x, 5):
        for y in range(start_y, lenght_y, 5):
            pixel_color = screen.getpixel((x - start_x, y - start_y))
            if rgb_tuple == pixel_color:
                pyautogui.click((x, y))
                break
        else:
            continue
        break

def region_scan_image_key(region_tuple, rgb_tuple, key_click, key_hold_time, image, image_region, quest_part):
    global quest_status
    screen = pyautogui.screenshot(region=region_tuple)
    start_x = region_tuple[0]
    start_y = region_tuple[1]
    lenght_x = region_tuple[0] + region_tuple[2]
    lenght_y = region_tuple[1] + region_tuple[3]
    for x in range(start_x, lenght_x, 5):
        for y in range(start_y, lenght_y, 5):
            pixel_color = screen.getpixel((x - start_x, y - start_y))
            if rgb_tuple == pixel_color:
                pyautogui.click((x, y))
                quest_status = quest_part
                screen = pyautogui.screenshot(region=region_tuple)
                if pyautogui.locateCenterOnScreen(image, region=image_region, confidence=0.8):
                    break
                else:
                    time.sleep(0.5)
                    continue
        else:
            continue
        break
    if quest_status != quest_part:
        time.sleep(0.5)
        key_hold(key_click, key_hold_time)

def check_rgb_move(region_tuple, rgb_tuple, rgb_cords, key_click, key_hold_time):
    start_x = region_tuple[0]
    start_y = region_tuple[1]
    real_rgb_x = rgb_cords[0] - start_x
    real_rgb_y = rgb_cords[1] - start_y
    while True:
        screen = pyautogui.screenshot(region=region_tuple)
        pixel_color = screen.getpixel((real_rgb_x, real_rgb_y))
        time.sleep(0.5)
        if rgb_tuple == pixel_color:
            break
        else:
            key_hold(key_click, key_hold_time)


while True:
# Sword Check
    if pyautogui.locateCenterOnScreen(
            'SWORD.png',
            region=region_sword,
            confidence=0.8):
        print("INFO: Sword Found")
# Look For Mob
        if quest_status == "Quest_Ready":
            region_scan_click(
                region_screen,
                hedgehog,
                Key.f3,
                0.1)
            print("INFO: Spell Used")
# Quest Done
            if pyautogui.locateCenterOnScreen(
                    'QUEST.png',
                    region=region_quest_finished,
                    confidence=0.8):
                quest_status = "Quest_Done"
                print("INFO: Quest Done")
                time.sleep(2)
# Returning to NPC
        elif quest_status == "Quest_Done":
            print("Returning to NPC")
            region_scan_image_key(region_screen,
                                  gardener,
                                  Key.up,
                                  0.1,
                                  "GARDENER_QUEST_START.png",
                                  region_gardener_quest,
                                  "NPC_Found")
# Finishing Quest
        elif quest_status == "NPC_Found":
            # next_click
            pyautogui.click(next_click)
            time.sleep(0.5)
            # Okay
            pyautogui.click(next_click)
            time.sleep(0.5)
            quest_status = "Quest_Completed"
# Taking Quest
        elif quest_status == "Quest_Completed":
            region_scan_image_key(region_screen,
                                  gardener,
                                  Key.up,
                                  0.1,
                                  "GARDENER_QUEST_START.png",
                                  region_gardener_quest,
                                  "Quest_Started")
            # next_click 1
            pyautogui.click(next_click)
            time.sleep(0.5)
            # next_click 2
            pyautogui.click(next_click)
            time.sleep(1)
            # Option
            pyautogui.click(let_me_hear)
            time.sleep(0.5)
            # next_click 3
            pyautogui.click(next_click)
            time.sleep(0.5)
            # next_click 4
            pyautogui.click(next_click)
            time.sleep(0.5)
            # Okay
            pyautogui.click(next_click)
            time.sleep(0.5)
# Returning to Position
        elif quest_status == "Quest_Started":
            check_rgb_move(region_screen,
                           flower_rgb,
                           flower_cords,
                           Key.down,
                           0.1)
            time.sleep(0.5)
            quest_status = "Quest_Ready"
    else:
        time.sleep(2)
        print("WARNING: Sword Not Found")