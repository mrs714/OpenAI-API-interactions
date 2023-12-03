import time

import pyautogui

from API_handler import (generate_response_brainstorm,
                         generate_response_brainstorm_image,
                         generate_response_feedback,
                         generate_response_feedback_image,
                         generate_response_program,
                         generate_response_shortcuts)
from backend.utils.get_active_window import getPreviousWindowName, goBackFocus
from backend.utils.get_screenshot import capture_and_encode_screenshot


def create_new_file():  # No input
    print("New file created")
    active_window = getPreviousWindowName()
    print(active_window)
    output = generate_response_shortcuts(f"create new file in {active_window}")
    print(output)
    perform_shortcut(output)
    return output


def create_new_tab():  # No input
    print("New tab created")
    active_window = getPreviousWindowName()
    print(active_window)
    output = generate_response_shortcuts(f"create new tab in {active_window}")
    print(output)
    perform_shortcut(output)
    return output

def generate_brain_storm(
    keywords,
):  # Text input - Give some keywords or ideas to get an abstract of your project
    print("Generating abstract from keywords")
    output = generate_response_brainstorm(keywords)
    print(output)
    return output


def generate_brain_storm_image(
    keywords,
):  # Text input - Give some keywords or ideas into what you want your reference image to have
    print("Creating reference image")
    output = generate_response_brainstorm_image(keywords)
    print("Image generated and saved")
    return output


def generate_program(
    program_description,
):  # Text input - Describe what you want the program to do, and in what language
    print("Generating program from input text")
    output = generate_response_program(program_description)
    print(output)
    return output


def generate_feedback(
    text_or_code,
):  # Text input - Input the text/code you want to get feedback on
    print("Generate feedback to the text or code")
    output = generate_response_feedback(text_or_code)
    print(output)
    return output


def generate_feedback_image():  # Image input - 64 encoded
    print("Generate artistic feedback for the image")
    # Change the focus to the other app, take a screenshot, and then change the focus back
    # goBackFocus()
    image_64_encoded = capture_and_encode_screenshot()
    # goBackFocus()
    output = generate_response_feedback_image(image_64_encoded)
    print(output)
    return output


def generate_stocks_information():  # No input
    print("Generate information about the stocks, searching for it")
    output = generate_response_feedback(
        "What are the highest stocks right now?",  # search=True
    )  # True by default, when True it uses the search API
    print(output)
    return output


def generate_stocks_advice(
    investing_questions,
):  # Text input - What advice do you need?
    print("Generate advice about the stocks, withouth a serper query")
    output = generate_response_feedback(investing_questions, search=False)
    print(output)
    return output


def generate_stock_insight(
    stock_name,
):  # Text input - What stock do you want to know about?
    print("Give the information for a certain stock, given the name")
    output = generate_response_feedback(
        f"What is the price for the stock {stock_name}", search=True
    )
    print(output)


def perform_shortcut(shortcut):
    keys = shortcut.split('+')

    for key in keys:
        key = key.replace(" ", "").lower()  # Ensure uppercase
        if key == 'ctrl':
            pyautogui.keyDown('ctrl')
        elif key == 'cmd':
            pyautogui.keyDown('command')
        elif key == 'command':
            pyautogui.keyDown('command')
        else:
            pyautogui.keyDown(key)

    time.sleep(1)  # Adjust this delay if needed

    # Release all keys
    for key in keys:
        key = key.replace(" ", "").lower()
        if key == 'ctrl':
            pyautogui.keyUp('ctrl')
        elif key == 'cmd':
            pyautogui.keyUp('command')
        elif key == 'command':
            pyautogui.keyUp('command')
        else:
            pyautogui.keyUp(key)
