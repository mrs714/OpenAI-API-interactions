import math
import threading
import tkinter as tk
from tkinter import scrolledtext

import pyperclip
from pynput import mouse

from backend.open_ring import create_button_event_dict
from backend.utils.get_active_window import getSelectedText

click_button_event_dict = None
emoji_label_list, emoji_title_list = [], []
MAX_EMOJI_NUM = 6


def init_button_definition_thread():
    click_button_event_dict = None
    print("INIT button_definition_thread")
    click_button_event_dict = create_button_event_dict()
    print(click_button_event_dict)
    # emoji buttons
    # for button_id, (key, values) in enumerate(click_button_event_dict.items()):
    key_list = list(click_button_event_dict.keys())

    for i in range(MAX_EMOJI_NUM):
        angle = i * 360 / MAX_EMOJI_NUM
        x = right_center_x + radius * math.cos(math.radians(angle))
        y = right_center_y - radius * math.sin(math.radians(angle))
        canvas.create_oval(
            x - button_radius,
            y - button_radius,
            x + button_radius,
            y + button_radius,
            fill="lightblue",
            # outline="black",
        )
        if i < len(key_list):
            emoji, *_ = click_button_event_dict[key_list[i]]
            emoji_label = tk.Label(root, text=emoji, font=("Arial", 30), bg="lightblue")
            emoji_title = tk.Label(
                root, text=key_list[i], font=("Arial", 10), bg="white"
            )
            emoji_label.place(x=x - (button_radius) // 2, y=y - (button_radius) // 2)
            emoji_title.place(
                x=x - (button_radius) // 2, y=y - (button_radius) // 2 + 30
            )
            emoji_label.bind(
                "<Button-1>",
                lambda x=emoji: perform_emoji_func(x, click_button_event_dict),
            )
        else:
            emoji_label = tk.Label(root, text="🚧", font=("Arial", 30), bg="lightblue")
            emoji_title = tk.Label(root, text="None", font=("Arial", 10), bg="white")
            emoji_label.place(x=x - (button_radius) // 2, y=y - (button_radius) // 2)
            emoji_title.place(
                x=x - (button_radius) // 2, y=y - (button_radius) // 2 + 30
            )
        emoji_label_list.append(emoji_label)
        emoji_title_list.append(emoji_title)


def update_button_definition_thread():
    click_button_event_dict = None
    print("update_button_definition_thread")
    click_button_event_dict = create_button_event_dict()
    print(click_button_event_dict)
    # emoji buttons
    key_list = list(click_button_event_dict.keys())
    print(emoji_label_list)
    for i in range(MAX_EMOJI_NUM):
        if i < len(key_list):
            emoji, *_ = click_button_event_dict[key_list[i]]
            emoji_label_list[i]["text"] = emoji
            emoji_title_list[i]["text"] = key_list[i]
            emoji_label_list[i].bind(
                "<Button-1>",
                lambda x=emoji: perform_emoji_func(x, click_button_event_dict),
            )
            # print("pack", emoji_label_list[i])
            # emoji_label_list[i].pack()
        else:
            # print("unpack", emoji_label_list[i])
            # emoji_label_list[i].pack_forget()
            continue

    root.deiconify()

button_thread = threading.Thread(target=init_button_definition_thread)
button_thread.start()

# from shortcut import perform_shortcut

W = 600
H = 300

CLOSE_BUTTON_HEIGHT = 30
CLOSE_BUTTON_WIDTH = 30


def close():
    root.withdraw()


def return_txt(func, txt, text_field):
    output: str = func(txt)
    text_field.insert(tk.END, output)


def perform_emoji_func(x: tk.Event, click_button_event_dict: dict):
    """the result of this function corresponding to each button"""
    id = x.widget._w.split("label")[-1]
    id = 0 if id == "" else int(id) // 2
    emoji, func, need_input, instruction = click_button_event_dict[
        list(click_button_event_dict.keys())[id]
    ]
    if need_input != "need_input":
        func()
        return
    if need_input == "hide_ring":
        root.attributes("-alpha", 0)

    # text box
    f = tk.Frame(root)
    f.place(x=10, y=20)
    txt1 = scrolledtext.ScrolledText(f, width=40, height=25, wrap=tk.WORD)

    selected = getSelectedText()
    print(selected)
    return_txt(func, selected, txt1)
    button_input = tk.Button(
        f,
        text="Copy",
        command=lambda x="copy_to_clipboard": copy_to_clipboard(txt1.get("1.0", tk.END)),
        bg="systemTransparent",
    )

    button_input.pack(side=tk.TOP)
    txt1.pack(fill="both", side=tk.TOP)

def copy_to_clipboard(txt):
    print("IM COPYING SHIT INTO CLIP: " + txt)
    pyperclip.copy(txt)

def dummy(x: tk.Event, click_button_event_dict: dict):
    """the result of this function corresponding to each button"""
    # TODO: there must be some other ways...
    print(f"pressed: {x}")
    id = x.widget._w.split("label")[-1]
    id = 0 if id == "" else int(id) - 1
    print(click_button_event_dict)
    emoji_func = click_button_event_dict[list(click_button_event_dict.keys())[id]]
    print(f"id={id} \t {emoji_func}")

    # cmd = "CMD+N"  # func()
    # perform_shortcut(cmd)
    # if needed
    # root.withdraw()


def send_args(x: str):
    print(x)


root = tk.Tk()
root.title("Smart AI Ring")
root.withdraw()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-transparent", True)
root.config(bg="systemTransparent")


root.geometry(f"{W}x{H}")

# root.attributes("-alpha", 0.1)
# root.overrideredirect(True)
# root.deiconify()
# root.after(1, lambda: root.withdraw())
canvas = tk.Canvas(
    root, width=W, height=H, bg="systemTransparent", borderwidth=0, highlightthickness=0
)
canvas.pack()

right_center_x = (W * 3) // 4
right_center_y = H // 2
left_center_x = W // 4
left_center_y = H // 2
radius = 100
button_radius = 30


# close button
button = tk.Button(canvas, text="x", command=close, bg="systemTransparent")
button.place(
    x=right_center_x - CLOSE_BUTTON_WIDTH / 2,
    y=right_center_y - CLOSE_BUTTON_HEIGHT / 2,
    width=CLOSE_BUTTON_WIDTH,
    height=CLOSE_BUTTON_HEIGHT,
)


def on_click(x, y, button, pressed):
    if button == mouse.Button.middle and pressed:
        update_button_thread = threading.Thread(target=update_button_definition_thread)
        update_button_thread.start()
        print("Ring Opened!!")
        x, y = root.winfo_pointerxy()
        root.geometry(
            f"+{x - right_center_x}+{y - right_center_y - CLOSE_BUTTON_HEIGHT}"
        )


def mouse_listener_thread():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()


# Create a new thread for the mouse listener
listener_thread = threading.Thread(target=mouse_listener_thread)

# Start the thread
listener_thread.start()

root.mainloop()


"""
Right part
- topmost doesn't work once in twice (python/vscode)
- pack_forget() doesn't work
- can't set emojitext
- make it unique for logitech


Left part
- input / output text for the left part
"""
