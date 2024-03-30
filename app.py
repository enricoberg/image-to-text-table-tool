import pyautogui, time, keyboard, json, sys, win32api, pytesseract
from util import OverlayWidget
from PyQt5 import QtWidgets
import tkinter as tk
from PIL import ImageGrab
from tkinter import filedialog


win32api.MessageBox(0, 'Please select the txt file where you want to save your results', '')
root = tk.Tk()
root.withdraw()
output_path = filedialog.askopenfilename(filetypes=[("TXT Files", "*.txt")])
with open(output_path, "w") as file:
    file.write("")

def track_mouse():
    previous_x, previous_y = pyautogui.position()
    x0,y0 =pyautogui.position()
    
    
    while True:
        if not keyboard.is_pressed('ctrl+q'):
            x1, y1 = pyautogui.position()
            width=x1-x0
            heigth=y1-y0
            return x0, y0, width, heigth
        time.sleep(0.05)
        current_x, current_y = pyautogui.position()
        if current_x != previous_x or current_y != previous_y:
            
            previous_x, previous_y = current_x, current_y
            


def on_key_event(event):
    if event.event_type == keyboard.KEY_DOWN and event.name == 'q' and keyboard.is_pressed('ctrl'):
        with open('rectangles_coordinates.json', 'r') as file:
            existing_data = json.load(file)
            x0, y0, width, height = track_mouse()
            new_data = {"x": x0, "y": y0, "width": width, "height": height}
            existing_data.append(new_data)
            with open('rectangles_coordinates.json', 'w') as file:
                json.dump(existing_data, file, indent=4)
            window.update_rectangles()
    elif event.event_type == keyboard.KEY_DOWN and event.name == 'esc':       
        app.quit()
    elif event.event_type == keyboard.KEY_DOWN and event.name == 'u' and keyboard.is_pressed('ctrl'):
        try:
            extract_images()
        except:
            print("Error conveting images")


def extract_images():
    with open("rectangles_coordinates.json", "r") as file:
        data = json.load(file)
    i=0
    with open(output_path, "r") as file:
        text = file.read()
    for obj in data:  
        i+=1
        img = ImageGrab.grab(bbox=(obj["x"], obj["y"], obj["x"] + obj["width"], obj["y"] + obj["height"]))   
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  
        
        converted_text = pytesseract.image_to_string(img)  
        text_without_newlines = converted_text.replace("\n", "")
        text+=text_without_newlines
        text+="\t"
        
        #img.save(f'capture_{i}.png')
    with open(output_path, "w") as file:
        file.write(text)


    
data = []
with open('rectangles_coordinates.json', 'w') as file:
    json.dump(data, file)


app = QtWidgets.QApplication(sys.argv)
window = OverlayWidget()
window.show()        


keyboard.on_press_key('q', on_key_event)
keyboard.on_press_key('esc', on_key_event)
keyboard.on_press_key('u', on_key_event)


sys.exit(app.exec_())

