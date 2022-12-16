import pyautogui
from time import sleep

for i in range(30):
    print(pyautogui.position())
    sleep(.1)                 