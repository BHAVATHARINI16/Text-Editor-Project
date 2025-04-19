import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import threading
import os
import json

from file_operations import new_file, open_file, save_file, save_file_as
from themes import apply_theme
from fonts import change_font, change_size
from admin_panel import open_admin_panel
from user_auth import login
from restricted_actions import execute_restricted_action

# Initialize main application window
root = tk.Tk()
root.title("Custom Text Editor")
root.geometry("800x600")

current_font_family = "Arial"
current_font_size = 12
current_file = None

text_area = tk.Text(root, wrap="word", undo=True, font=(current_font_family, current_font_size))
text_area.pack(expand=True, fill="both")

# --- Word Counter ---
status_bar = tk.Label(root, text="Words: 0", anchor="w")
status_bar.pack(side="bottom", fill="x")

def update_word_count(event=None):
    words = text_area.get("1.0", "end-1c").split()
    status_bar.config(text=f"Words: {len(words)}")

text_area.bind("<KeyRelease>", update_word_count)

# --- Search and Replace ---
def find_and_replace(text_area):
    find_text = simpledialog.askstring("Find", "Enter text to find:")
    replace_text = simpledialog.askstring("Replace", "Enter replacement text:")
    if find_text and replace_text:
        content = text_area.get("1.0", "end")
        new_content = content.replace(find_text, replace_text)
        text_area.delete("1.0", "end")
        text_area.insert("1.0", new_content)

def search_text(text_area):
    search_query = simpledialog.askstring("Search", "Enter text to search:")
    if search_query:
        text_area.tag_remove("highlight", "1.0", "end")
        start_index = "1.0"
        while True:
            start_index = text_area.search(search_query, start_index, stopindex="end")
            if not start_index:
                break
            end_index = f"{start_index}+{len(search_query)}c"
            text_area.tag_add("highlight", start_index, end_index)
            start_index = end_index
        text_area.tag_config("highlight", background="yellow", foreground="black")

# --- Restricted Action Wrapper ---
def execute_action(action_name, text_area):
    if action_name == "delete":
        try:
            text_area.delete("sel.first", "sel.last")
        except:
            pass
    elif action_name == "find_replace":
        find_and_replace(text_area)
    elif action_name == "search":
        search_text(text_area)

# --- Auto Save Logic ---
def auto_save():
    if current_file:
        with open(current_file, "w") as file:
            file.write(text_area.get("1.0", tk.END))
    root.after(60000, auto_save)  # every 60 seconds

auto_save()

# --- Login System ---
current_user = login(root)

# --- Menu Bar ---
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=lambda: new_file(text_area))
file_menu.add_command(label="Open", command=lambda: open_file(text_area))
file_menu.add_command(label="Save", command=lambda: save_file(text_area))
file_menu.add_command(label="Save As", command=lambda: save_file_as(text_area))
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Edit Menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=lambda: text_area.event_generate("<<Cut>>"))
edit_menu.add_command(label="Copy", command=lambda: text_area.event_generate("<<Copy>>"))
edit_menu.add_command(label="Paste", command=lambda: text_area.event_generate("<<Paste>>"))
edit_menu.add_separator()
edit_menu.add_command(label="Find & Replace", command=lambda: execute_restricted_action(current_user["username"], "find_replace", text_area, execute_action))
edit_menu.add_command(label="Delete", command=lambda: execute_restricted_action(current_user["username"], "delete", text_area, execute_action))
edit_menu.add_command(label="Search", command=lambda: execute_restricted_action(current_user["username"], "search", text_area, execute_action))

# Theme Menu
theme_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Theme", menu=theme_menu)
theme_menu.add_command(label="Light Mode", command=lambda: apply_theme(text_area, "light"))
theme_menu.add_command(label="Dark Mode", command=lambda: apply_theme(text_area, "dark"))

# Font Menu
font_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Font", menu=font_menu)
font_menu.add_command(label="Arial", command=lambda: change_font(text_area, "Arial"))
font_menu.add_command(label="Courier", command=lambda: change_font(text_area, "Courier"))
font_menu.add_command(label="Times New Roman", command=lambda: change_font(text_area, "Times New Roman"))
font_menu.add_separator()
font_menu.add_command(label="Size 12", command=lambda: change_size(text_area, 12))
font_menu.add_command(label="Size 16", command=lambda: change_size(text_area, 16))
font_menu.add_command(label="Size 20", command=lambda: change_size(text_area, 20))

# --- Admin Panel and Request Notification ---
if current_user["access"] == "admin":
    admin_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Admin", menu=admin_menu)

    # This label text will be updated with notification
    admin_label = tk.StringVar()
    admin_label.set("Admin Panel")
    admin_menu.add_command(labelvariable=admin_label, command=open_admin_panel)

    def check_pending_requests():
        while True:
            has_pending = False
            if os.path.exists("shared/requests"):
                for file in os.listdir("shared/requests"):
                    if file.endswith(".json"):
                        try:
                            with open(os.path.join("shared/requests", file), "r") as f:
                                data = json.load(f)
                                if data.get("status") == "pending":
                                    has_pending = True
                                    break
                        except:
                            continue
            admin_label.set("Admin Panel (New)" if has_pending else "Admin Panel")
            threading.Event().wait(5)

    threading.Thread(target=check_pending_requests, daemon=True).start()

# --- Mainloop ---
root.mainloop()
