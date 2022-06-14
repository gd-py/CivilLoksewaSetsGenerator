import pyautogui,sys
import time
pyautogui.click(clicks=4)
time.sleep(5)
for i in range(101):
    pyautogui.hotkey('ctrl','a')
    pyautogui.hotkey('alt','n')
    pyautogui.hotkey('ctrl','shift','m')
    pyautogui.hotkey('ctrl','1')
    pyautogui.hotkey('ctrl','s')
    pyautogui.hotkey('alt','f4')
    time.sleep(3)
    pyautogui.press('down')
    pyautogui.press('enter')
    time.sleep(3)
    

    