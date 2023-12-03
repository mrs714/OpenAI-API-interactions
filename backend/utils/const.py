from backend.click_button import (create_new_file, create_new_tab,
                                  generate_brain_storm,
                                  generate_brain_storm_image,
                                  generate_feedback, generate_feedback_image,
                                  generate_program, generate_stock_insight,
                                  generate_stocks_advice,
                                  generate_stocks_information)

CLICK_BUTTON_EVENT_DICT = {
    "New file": ["📄", create_new_file, "", ""],
    "New tab": ["📄", create_new_tab, "", ""],
    "brain storm": ["🧠", generate_brain_storm, "need_input", "Give some keywords or ideas to get an abstract of your project"],
    "brain storm image": ["🧠", generate_brain_storm_image, "need_input", "Give some keywords or ideas into what you want your reference image to have"],
    "program": ["🖥️", generate_program, "need_input", "Describe what you want the program to do, and in what language"],
    "feedback": ["📝", generate_feedback, "need_input", "Input the text/code you want to get feedback on"],
    "feedback image": ["📝", generate_feedback_image, "hide_ring", "64 encoded"],
    "stocks information": ["📈", generate_stocks_information, "", ""],
    "stocks advice": ["📈", generate_stocks_advice, "need_input", "What advice do you need?"],
    "stock insight": ["📈", generate_stock_insight, "need_input", "What stock do you want to know about?"],
    "dummy": [" ", lambda: eval(2+4)] #
}
