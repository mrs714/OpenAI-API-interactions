import tkinter as tk
from tkinter import ttk, messagebox

import pygetwindow as gw # Used to get the active window
import pyautogui # Used to get the selected text
import pyperclip # Used to copy the generated text to the clipboard

# Interface for the API_handler_V2.py
import API_handler_v2 as API_handler

def show_message(title, message):
    messagebox.showinfo(title, message)

def execute_api_function(api_function):
    text = capture_selected_text()
    print("Selected Text:", text)
    try:
        api_function(model.get(), temperature.get())
        show_message("Success", "API function executed successfully!")
    except Exception as e:
        show_message("Error", f"Error executing API function:\n{str(e)}")

def capture_selected_text():
    try:
        # Activate the active window
        active_window = gw.getWindowsWithTitle(gw.getActiveWindow().title)
        # Get the name of the process of the window
        
        print (active_window)
        if active_window:
            active_window = active_window[0]
            active_window.activate()

            # Copy the selected text to the clipboard
            pyautogui.hotkey("ctrl", "c")

            # Retrieve the text from the clipboard
            selected_text = root.clipboard_get()
            return selected_text
    except tk.TclError as e:
        print("Error capturing text:", e)

# Create the root window
root = tk.Tk()
root.title("GPT Service")

# Style
style = ttk.Style()
style.configure('TButton', padding=(10, 5), font='Helvetica 10 bold')
style.configure('TEntry', padding=(5, 5), font='Helvetica 10')
style.configure('TCombobox', padding=(5, 5), font='Helvetica 10')
style.configure('Horizontal.TScale', padding=(10, 5), font='Helvetica 10')

# Models:
model = tk.StringVar(root)
model.set("gpt-3.5-turbo")
model_label = ttk.Label(root, text="Model:")
model_label.grid(row=0, column=0, pady=10)
model_selector = ttk.Combobox(root, textvariable=model, values=["gpt-3.5-turbo", "gpt-4", "gpt-4-1106-preview"], state="readonly")
model_selector.grid(row=0, column=1, pady=10, padx=(0, 10))

# Temperature (0 to 1):
temperature = tk.DoubleVar(root)
temperature.set(0.7)

temperature_label = ttk.Label(root, text="Temperature (0 to 1):", anchor='e') 
temperature_label.grid(row=1, column=0, pady=10, sticky='e')

temperature_slider = ttk.Scale(root, variable=temperature, from_=0, to=1, orient='horizontal', length=200, style='Horizontal.TScale')
temperature_slider.grid(row=1, column=1, pady=10, padx=(0, 10), sticky='w')

# Buttons:
buttons_frame = ttk.Frame(root)
buttons_frame.grid(row=2, column=0, columnspan=2, pady=20)

button_width = 15

text_generator_button = ttk.Button(buttons_frame, text="Text generator", command=lambda: execute_api_function(API_handler.text_generator), width=button_width)
text_generator_button.grid(row=0, column=0, padx=10)

text_feedback_button = ttk.Button(buttons_frame, text="Text feedback", command=lambda: execute_api_function(API_handler.text_feedback), width=button_width)
text_feedback_button.grid(row=0, column=1, padx=10)

image_generator_button = ttk.Button(buttons_frame, text="Image generator", command=lambda: execute_api_function(API_handler.image_generator), width=button_width)
image_generator_button.grid(row=1, column=0, padx=10)

image_feedback_button = ttk.Button(buttons_frame, text="Image feedback", command=lambda: execute_api_function(API_handler.image_feedback), width=button_width)
image_feedback_button.grid(row=1, column=1, padx=10)

code_generator_button = ttk.Button(buttons_frame, text="Code generator", command=lambda: execute_api_function(API_handler.code_generator), width=button_width)
code_generator_button.grid(row=2, column=0, padx=10)

code_feedback_button = ttk.Button(buttons_frame, text="Code feedback", command=lambda: execute_api_function(API_handler.code_feedback), width=button_width)
code_feedback_button.grid(row=2, column=1, padx=10)

shortcuts_button = ttk.Button(buttons_frame, text="Shortcuts", command=lambda: execute_api_function(API_handler.shortcuts), width=button_width)
shortcuts_button.grid(row=3, column=0, padx=10)

use_cases_button = ttk.Button(buttons_frame, text="Use cases", command=lambda: execute_api_function(API_handler.use_cases), width=button_width)
use_cases_button.grid(row=3, column=1, padx=10)

# Center the window
root.update_idletasks()
root.geometry("+%d+%d" % (root.winfo_screenwidth()/2 - root.winfo_reqwidth()/2, root.winfo_screenheight()/2 - root.winfo_reqheight()/2))

#root.overrideredirect(True)
root.mainloop()
