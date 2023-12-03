#!/usr/bin/env python

import re
import subprocess

import pyperclip

cmd = """osascript -e 'tell application "Google Chrome" to return URL of active tab of front window'"""
cmd2 = """osascript -e 'tell application "System Events"
  tell (first process whose frontmost is true) to return properties
end tell'"""
cmd3 = """osascript -e 'tell application "System Events"
    delay 0.01
    key down command
    keystroke tab
    delay 0.01
    key up command
end tell'"""

selected_text = None

def getChromeActiveUrl():
    return subprocess.check_output(cmd, shell=True, text=True)


def getPreviousWindowName():
    goBackFocus()
    global selected_text
    selected_text = copySelectedText()
    properties = subprocess.check_output(cmd2, shell=True, text=True)
    # Use regular expression to find the value of "displayed name"
    match = re.search(r'displayed name:(.*?),', properties)

    if match:
        displayed_name = match.group(1).strip()
        return displayed_name
    else:
        return "Display name not found"


def goBackFocus():
    return subprocess.check_output(cmd3, shell=True, text=True)

# print("Chrome URL: " + getChromeActiveUrl())
# print("Active Window: " + getPreviousWindowName())


cmd_copy_selected_text = """osascript -e 'tell application "System Events"
    keystroke "c" using command down
end tell'"""

def copySelectedText():
    subprocess.check_output(cmd_copy_selected_text, shell=True, text=True)
    return pyperclip.paste()

def getSelectedText():
    global selected_text
    return selected_text
