
import tkinter as tk
from tkinter import font

# Store current font settings for new text
current_font_family = "Arial"
current_font_size = 12

def apply_font_style(text_area):
    """Apply the current font settings to selected text or set it as default."""
    global current_font_family, current_font_size

    try:
        selected_text = text_area.tag_ranges("sel")  # Check if text is selected
        new_font = font.Font(family=current_font_family, size=current_font_size)

        if selected_text:
            # Apply the font settings to the selected text
            text_area.tag_add("custom_style", "sel.first", "sel.last")
            text_area.tag_configure("custom_style", font=new_font)
        else:
            # Apply for new text after the cursor
            text_area.configure(font=(current_font_family, current_font_size))
    except Exception as e:
        print("Error applying font style:", e)

def change_font(text_area, font_name):
    """Change the font and apply the new style."""
    global current_font_family
    current_font_family = font_name
    apply_font_style(text_area)

def change_size(text_area, size):
    """Change the font size and apply the new style."""
    global current_font_size
    current_font_size = size
    apply_font_style(text_area)
