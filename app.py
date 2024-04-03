import pyautogui, time, keyboard, json, sys, win32api, pytesseract
from util import OverlayWidget
from PyQt5 import QtWidgets
import tkinter as tk
from PIL import ImageGrab
from tkinter import filedialog



def replace_last_object(x0,y0,width,height):
    with open('rectangles_coordinates.json', 'r') as file:
            json_data = json.load(file)
    try:
        json_data.pop()    
    except:
        pass
    object = {"x": x0, "y": y0, "width": width, "height": height}
    json_data.append(object)
    with open('rectangles_coordinates.json', 'w') as file:
        json.dump(json_data, file, indent=4)

#FUNCTION THAT GENERATES COORDINATES OF THE RECTANGLE DRAWN WITH THE MOUSE
def track_mouse():
    with open('rectangles_coordinates.json', 'r') as file:
        json_data = json.load(file)
    json_data.append({"x": 1, "y": 1, "width": 1, "height": 1})
    with open('rectangles_coordinates.json', 'w') as file:
        json.dump(json_data, file, indent=4)
    previous_x, previous_y = pyautogui.position()
    x0,y0 =pyautogui.position()   
    
    while True:
        if not keyboard.is_pressed('ctrl+g'):
            x1, y1 = pyautogui.position()
            width=x1-x0
            heigth=y1-y0
            if not heigth<10 or width<10:
                return x0, y0, width, heigth
            else:
                return 0,0,0,0
        time.sleep(0.05)
        current_x, current_y = pyautogui.position()
        if current_x != previous_x or current_y != previous_y:
            replace_last_object(x0,y0,current_x-x0,current_y-y0)
            window.update_rectangles()
            previous_x, previous_y = current_x, current_y
            

#ROUTER FUNCTION THAT HANDLES THE USER'S KEYBOARD INPUT 
def on_key_event(event):
    if event.event_type == keyboard.KEY_DOWN and event.name == 'g' and keyboard.is_pressed('ctrl'):
        with open('rectangles_coordinates.json', 'r') as file:
            existing_data = json.load(file)
            x0, y0, width, height = track_mouse()
            if x0>0 and y0>0 and width>10 and height>10:
                new_data = {"x": x0, "y": y0, "width": width, "height": height}
                existing_data.append(new_data)
                with open('rectangles_coordinates.json', 'w') as file:
                    json.dump(existing_data, file, indent=4)
                window.update_rectangles()
    elif event.event_type == keyboard.KEY_DOWN and event.name == 'esc':       
        app.quit()
    elif event.event_type == keyboard.KEY_DOWN and event.name == 'enter' and keyboard.is_pressed('ctrl'):
        reset_rectangles()
    elif event.event_type == keyboard.KEY_DOWN and event.name == 'u' and keyboard.is_pressed('ctrl'):
        try:
            extract_images()
        except:
            win32api.MessageBox(0, 'Something unexpected happened converting image to text', 'Error' ,0x00001000)

#CLEARS THE JSON FROM UNWANTED RECTANGLES
def clean_json():
    with open("rectangles_coordinates.json", "r") as file:
        data = json.load(file)   
    filtered_objects = [obj for obj in data if obj.get("width") != 1 and  obj.get("height") != 1]
    with open('rectangles_coordinates.json', 'w') as file:
        json.dump(filtered_objects, file)

#RESETS THE RECTANGLES JSON FILE
def reset_rectangles():
    empty_json=[]
    with open('rectangles_coordinates.json', 'w') as file:
        json.dump(empty_json, file, indent=4)  
    window.update_rectangles()


#FUNCTION TO TAKE SNAPSHOTS IN SELECTED AREAS, CONVERT THEM TO TEXT AND SAVE THE RESULTS IN OUTPUT FILE
def extract_images():   
    clean_json() 
    with open("rectangles_coordinates.json", "r") as file:
        data = json.load(file)    
    with open(output_path, "r") as file:
        text = file.read()
    if text!="":
        text+="\n"
    for obj in data:  
        img = ImageGrab.grab(bbox=(obj["x"], obj["y"], obj["x"] + obj["width"], obj["y"] + obj["height"]))   
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'          
        converted_text = pytesseract.image_to_string(img)  
        text_without_newlines = converted_text.replace("\n", "")
        text+=text_without_newlines
        text+="\t"        
    with open(output_path, "w") as file:
        file.write(text)   

#SHOW A PROMPT TO SELECT THE OUTPUT FILE (CSV OR TXT ARE ALLOWED)
win32api.MessageBox(0, 'Please select the txt file where you want to save your results', '')
root = tk.Tk()
root.withdraw()
output_path = filedialog.askopenfilename(filetypes=[("TXT Files", "*.txt"),("CSV", "*.csv")])
with open(output_path, "w") as file:
    file.write("")

#RESET THE FILE WITH THE RECTANGLES COORDINATES
data = []
with open('rectangles_coordinates.json', 'w') as file:
    json.dump(data, file)
#INITIALIZE THE APP
app = QtWidgets.QApplication(sys.argv)
window = OverlayWidget()
window.show()       

#SET THE LISTENERS FOR THE SHORTCUTS
keyboard.on_press_key('g', on_key_event)
keyboard.on_press_key('esc', on_key_event)
keyboard.on_press_key('u', on_key_event)
keyboard.on_press_key('enter', on_key_event)


sys.exit(app.exec_())

