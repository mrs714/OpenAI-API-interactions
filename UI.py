import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
from time import sleep

import pygetwindow as gw # Used to get the active window
import pyautogui # Used to get the selected text
import pyperclip # Used to copy the generated text to the clipboard

# Interface for the API_handler_V2.py
import API_handler_v2 as API_handler

# Global variables
window_history = []
last_action = []

def show_message(title, message):
    messagebox.showinfo(title, message)

def execute_api_function(api_function):
    global last_action
    # Make sure we know which window we're in
    update_window_list()
    
    # Execute the API function
    try:
        # Get the selected text, the model and the temperature, and the window name
        text, window = get_text_and_info()

        # Update the text box
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Loading... fetching response to {api_function.__name__} for {window}...")
        root.update_idletasks()

        # Save parameters for retry
        last_action = [api_function, model.get(), temperature.get(), text, window, num_tokens.get()]
        result = api_function(model.get(), temperature.get(), text, window, num_tokens.get())
        
        # Update the text box
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)

        show_message("Success", "API function executed successfully!")

    except Exception as e:
        show_message("Error", f"Error executing API function:\n{str(e)}")

def retry_last_action():
    global last_action
    if last_action:
        try:
            # Update the text box
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, f"Loading... fetching response to {last_action[0].__name__} for {last_action[4]}...")
            root.update_idletasks()

            result = last_action[0](last_action[1], last_action[2], last_action[3], last_action[4], last_action[5])
            
            # Update the text box
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, result)

            show_message("Success", "API function executed successfully!")

        except Exception as e:
            show_message("Error", f"Error executing API function:\n{str(e)}")
    else:
        show_message("Error", "No previous action found!")

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
    if not window_history or (window_history and active_window != window_history[-1][0]):
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
        selected_text = root.clipboard_get()

        # Get the active window name
        window_name = get_active_window_name()

        # Switch back to the original window
        switch_to_previous()

        return selected_text, window_name
        
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

# Number of Tokens slider:
num_tokens = tk.IntVar(root)
num_tokens.set(200)

num_tokens_label = ttk.Label(root, text="Number of Tokens:", anchor='e') 
num_tokens_label.grid(row=2, column=0, pady=10, sticky='e')

num_tokens_slider = ttk.Scale(root, variable=num_tokens, from_=1, to=1000, orient='horizontal', length=200, style='Horizontal.TScale')
num_tokens_slider.grid(row=2, column=1, pady=10, padx=(0, 10), sticky='w')

# Retry button:
retry_button = ttk.Button(root, text="Retry Last Action", command=lambda: retry_last_action(), width=20)
retry_button.grid(row=3, column=0, columnspan=2, pady=10)

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

# Text box:
output_text = tk.Text(root, wrap="word", height=20, width=40)
output_text.grid(row=0, column=2, rowspan=4, pady=10, padx=10, sticky='nsew')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

# Center the window
root.update_idletasks()
root.geometry("+%d+%d" % (root.winfo_screenwidth()/2 - root.winfo_reqwidth()/2, root.winfo_screenheight()/2 - root.winfo_reqheight()/2))

#root.overrideredirect(True)
update_window_list()
root.mainloop()
