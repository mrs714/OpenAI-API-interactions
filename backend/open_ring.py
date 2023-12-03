from API_handler import generate_wheel_elements, generate_response_shortcuts_information
from backend.utils.const import CLICK_BUTTON_EVENT_DICT
from backend.utils.get_active_window import (getChromeActiveUrl,
                                             getPreviousWindowName)


def get_active_window():
    """Return the active window."""
    active_window = getPreviousWindowName()
    active_url = getChromeActiveUrl()
    # print(active_window, active_url)
    return active_window, active_url


def get_active_window_type():
    active_window, url = get_active_window()
    if "swissquote" in url:
        return "stock"
    print(active_window)
    window_type = generate_wheel_elements(active_window)
    print(window_type)
    return window_type


def get_response_shortcuts_information():
    """Return the response shortcuts information based on the active window."""
    active_window, url = get_active_window()
    short_cuts = generate_response_shortcuts_information(active_window)
    return short_cuts


def create_button_event_dict():
    """Create a button event dict based on the active window.
    Available actions:
        - "New file/tab"
        - "brain storm"
        - "brain storm image"
        - "program"
        - "feedback"
        - "feedback image"
        - "stocks information"
        - "stocks advice"
        - "stock insight"
    """

    window_type = get_active_window_type()
    if window_type == "text":
        button_list = ["New file", "brain storm", "feedback", "feedback image"]
    elif window_type == "code":
        button_list = ["New file", "brain storm", "feedback", "program"]
    elif window_type == "web":
        button_list = ["New tab", "brain storm", "feedback", "program"]
    elif window_type == "image_editor":
        button_list = ["feedback image", "New file", "brain storm", "brain storm image"]
    elif window_type == "stock":
        button_list = [
            "New tab",
            "stocks information",
            "stocks advice",
            "stock insight",
        ]
    else:
        button_list = ["New file", "brain storm", "feedback", "program"]
    click_button_event_dict = {key: CLICK_BUTTON_EVENT_DICT[key] for key in button_list}
    shortcut_dict = get_response_shortcuts_information()
    for key in shortcut_dict:
        click_button_event_dict[key] = shortcut_dict[key]
    return click_button_event_dict


if __name__ == "__main__":
    print(create_button_event_dict())
