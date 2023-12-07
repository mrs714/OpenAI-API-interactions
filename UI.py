import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
from time import sleep

import pygetwindow as gw # Used to get the active window
import pyautogui # Used to get the selected text

# Images and showing
from PIL import Image, ImageTk
from io import BytesIO

import win32clipboard # Used to copy the generated image to the clipboard
import io # Used to convert the image to the clipboard format

# Interface for the API_handler_V2.py
import API_handler_v2 as API_handler

# Encoding to base64
import base64

# Global variables
window_history = []
last_action = []

def show_message(title, message):
    messagebox.showinfo(title, message)

def execute_api_function(api_function, retry=False):
    global last_action
    # Make sure we know which window we're in
    update_window_list()
    
    # Execute the API function
    try:

        if retry:
            # Get the selected text, the model and the temperature, and the window name
            text, window, screenshot, api_function = last_action[1], last_action[2], last_action[3], last_action[0]
        else:
            # Get the selected text, the model and the temperature, and the window name
            text, window, screenshot = get_text_and_info()

        # Update the text box
        show_text_box()
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Loading... fetching response to \n\n    {api_function.__name__} \n\nfor program\n\n    {window}\n\nand prompt\n\n    {text}...")
        root.update_idletasks()

        if not retry:
            # Save parameters for retry
            last_action = [api_function, text, screenshot, window]

        result = api_function(model.get(), temperature.get(), text, window, screenshot, num_tokens.get(), quality.get())
        
        # Update the text box if text, otherwise show the image
        if api_function.__name__ == "image_generator":
            print(result)

            def send_to_clipboard(image):
                output = io.BytesIO()
                image.convert('RGB').save(output, 'BMP')
                data = output.getvalue()[14:]
                output.close()
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
                win32clipboard.CloseClipboard()

            if result is not None:
                image = result
                print(image)
                send_to_clipboard(image)

                # Load image in correct format
                photo = ImageTk.PhotoImage(image)
                
                # Update the image
                image_label.configure(image=photo)
                image_label.image = photo

                show_image_box()
            
            else:
                output_text.delete("1.0", tk.END)
                output_text.insert(tk.END, "No image generated!")
                return

        else:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, result)

    except Exception as e:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"An error has occurred: {e}")

def get_active_window_name():
    # Switch to the previous window
    active_window = gw.getActiveWindow()
    if active_window:
        return active_window.title
    
def update_window_list():
    # This should be called before clicking on anything
    global window_history
    # Get actual window:
    active_window = gw.getActiveWindow()
    if active_window and (not window_history or (window_history and active_window != window_history[-1][0])):
        window_history.append((active_window, active_window.title))
    if len(window_history) > 2:
        window_history.pop(0)
    for window in window_history:
        if window[1] == "":
            window_history.remove(window)
    root.after(250, update_window_list)

def switch_to_previous():
    global window_history
    if len(window_history) > 1:
        window_history[0][0].activate()
        # Sleep half a second
        sleep(0.25)
        # Update the window history
        update_window_list()
    else:
        show_message("Error", "No previous window found!")

def get_text_and_info():
    try:
        # Switch to the previous window
        switch_to_previous()

        # Copy the selected text to the clipboard
        pyautogui.hotkey("ctrl", "c")

        # Retrieve the text from the clipboard
        try:
            selected_text = root.clipboard_get()
        except tk.TclError as e:
            selected_text = ""

        # Take a screenshot of the window and encode in base64
        screenshot = pyautogui.screenshot()
        screenshot_bytesio = BytesIO()
        screenshot.save(screenshot_bytesio, format='PNG')

        # Convert the screenshot image data to base64
        screenshot_base64 = base64.b64encode(screenshot_bytesio.getvalue()).decode("utf-8")

        # Get the active window name
        window_name = get_active_window_name()

        # Switch back to the original window
        switch_to_previous()

        return selected_text, window_name, screenshot_base64
        
    except tk.TclError as e:
        print("Error capturing text:", e)

def show_text_box():
    image_label.grid_remove()
    output_text.grid()

def show_image_box():
    output_text.grid_remove()
    image_label.grid()

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

# Quality of the image
quality = tk.StringVar(root)
quality.set("medium")
quality_label = ttk.Label(root, text="Quality:")
quality_label.grid(row=1, column=0, pady=10)
quality_selector = ttk.Combobox(root, textvariable=quality, values=["low", "medium", "high"], state="readonly")
quality_selector.grid(row=1, column=1, pady=10, padx=(0, 10))

# Temperature (0 to 1):
temperature = tk.DoubleVar(root)
temperature.set(0.7)

temperature_label = ttk.Label(root, text="Temperature (0 to 1):", anchor='e') 
temperature_label.grid(row=2, column=0, pady=10, sticky='e')

temperature_slider = ttk.Scale(root, variable=temperature, from_=0, to=1, orient='horizontal', length=200, style='Horizontal.TScale')
temperature_slider.grid(row=2, column=1, pady=10, padx=(0, 10), sticky='w')

# Number of Tokens slider:
num_tokens = tk.IntVar(root)
num_tokens.set(200)

num_tokens_label = ttk.Label(root, text="Number of Tokens:", anchor='e') 
num_tokens_label.grid(row=3, column=0, pady=10, sticky='e')

num_tokens_slider = ttk.Scale(root, variable=num_tokens, from_=1, to=1000, orient='horizontal', length=200, style='Horizontal.TScale')
num_tokens_slider.grid(row=3, column=1, pady=10, padx=(0, 10), sticky='w')


# Buttons:
buttons_frame = ttk.Frame(root)
buttons_frame.grid(row=4, column=0, columnspan=2, pady=20)

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

# Retry button:
retry_button = ttk.Button(root, text="Retry Last Action", command=lambda: execute_api_function(None, True), width=20)
retry_button.grid(row=5, column=0, columnspan=2, pady=10)

# Text box
output_text = tk.Text(root, wrap="word", height=20, width=40)
output_text.grid(row=0, column=2, rowspan=6, pady=10, padx=10, sticky='nsew')

# Image box
image_path = "reference.png"  # Replace with the path to your image
image = Image.open(image_path)
image = image.resize((200, 200), Image.LANCZOS)  # Adjust the size as needed
photo = ImageTk.PhotoImage(image)

image_label = tk.Label(root, image=photo)
image_label.grid(row=0, column=2, rowspan=6, pady=10, padx=10, sticky='nsew')

# Initially show the text box
show_text_box()

# Center the window
root.update_idletasks()
root.geometry("+%d+%d" % (root.winfo_screenwidth()/2 - root.winfo_reqwidth()/2, root.winfo_screenheight()/2 - root.winfo_reqheight()/2))

#root.overrideredirect(True) pit roig muntanya canigó
update_window_list()
root.mainloop()

