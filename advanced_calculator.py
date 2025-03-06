import tkinter as t
from tkinter import ttk, messagebox
import pyttsx3
import speech_recognition as sr
import math

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize main application window
win = t.Tk()
win.title("Multi-Mode Calculator")

# Entry widget for calculator display
entry = t.Entry(win, width=40, borderwidth=5, font=('Arial', 16))
entry.grid(row=0, column=0, columnspan=4, padx=5, pady=5)
lb1 = t.Label(win,text="")
lb1.grid(row = 1, column = 0, columnspan = 5 )
# Calculator functions
def button_click(number):
    current = entry.get()
    entry.delete(0, t.END)
    entry.insert(0, current + str(number))
    if mode == "Audio":
        engine.say(str(number))
        engine.runAndWait()

def button_clear():
    entry.delete(0, t.END)

def button_equal():
    try:
        result = eval(entry.get())
        entry.delete(0, t.END)
        entry.insert(0, result)
        if mode == "Audio":
            engine.say("equals")
            engine.say(result)
            engine.runAndWait()
    except:
        entry.delete(0, t.END)
        entry.insert(0, "Error")
        if mode == "Audio":
            engine.say("Error")
            engine.runAndWait()

# Scientific functions
def button_sci_click(func):
    try:
        current = entry.get()
        result = eval(f"math.{func}({current})")
        entry.delete(0, t.END)
        entry.insert(0, result)
        if mode == "Audio":
            engine.say(f"{func} of {current} equals")
            engine.say(result)
            engine.runAndWait()
    except:
        entry.delete(0, t.END)
        entry.insert(0, "Error")
        if mode == "Audio":
            engine.say("Error")
            engine.runAndWait()

# Voice command handling
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        engine.say("Listening for command")
        engine.runAndWait()
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        engine.say(f"You said {command}")
        engine.runAndWait()
        # Replace spoken words with Python operators
        command = command.replace('plus', '+').replace('minus', '-')
        command = command.replace('times', '*').replace('divided by', '/')
        command = command.replace('open bracket', '(').replace('close bracket', ')')
        command = command.replace('point', '.')
        entry.delete(0, t.END)
        entry.insert(0, eval(command))
    except:
        entry.delete(0, t.END)
        entry.insert(0, "Error")
        engine.say("Sorry, I did not understand that")
        engine.runAndWait()

# Modes
mode = "Basic"

def set_mode(new_mode):
    global mode
    mode = new_mode
    engine.say(f"Mode set to {new_mode}")
    engine.runAndWait()

# Buttons
buttons = [
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
    ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
    ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
    ('0', 5, 0), ('.', 5, 1), ('+', 5, 2), ('=', 5, 3),
    ('C', 6, 0)
]

for (text, row, col) in buttons:
    if text == "=":
        button = t.Button(win, text=text, padx=15, pady=15,   command=button_equal)
    elif text == "C":
        button = t.Button(win, text=text, padx=15, pady=15,   command=button_clear)
    else:
        button =t.Button(win, text=text, padx=15, pady=15,   command=lambda txt=text: button_click(txt))
    button.grid(row=row, column=col, pady=5)

# Scientific buttons
sci_buttons = [
    ('sin', 6, 0), ('cos', 6, 1), ('tan', 6, 2),
    ('log', 7, 0), ('sqrt', 7, 1), ('pow', 7, 2)
]

for (text, row, col) in sci_buttons:
    button = t.Button(win, text=text, padx=15, pady=15,   command=lambda func=text: button_sci_click(func))
    button.grid(row=row, column=col, pady=5)

# Mode buttons
modes = [("Basic", 6, 3), ("Scientific", 7, 3), ("Audio", 8, 0)]

for (text, row, col) in modes:
    if text == "Audio":
        button = t.Button(win, text=text, padx=20, pady=20, command=lambda m=text: set_mode(m))
        button.grid(row=row, column=col, columnspan=2)
    else:
        button = t.Button(win, text=text, padx=20, pady=20, command=lambda m=text: set_mode(m))
        button.grid(row=row, column=col)

# Voice command button
voice_button = t.Button(win, text="Voice Command", padx=15, pady=15,   command=listen_command)
voice_button.grid(row=8, column=2, columnspan=2)

# Start the GUI event loop
win.mainloop()
