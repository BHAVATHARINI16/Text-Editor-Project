from tkinter import filedialog

file_path = None

def new_file(text_area):
    global file_path
    file_path = None
    text_area.delete("1.0", "end")

def open_file(text_area):
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", ".txt"), ("All Files", ".*")])
    if file_path:
        with open(file_path, "r") as file:
            text_area.delete("1.0", "end")
            text_area.insert("1.0", file.read())

def save_file(text_area):
    global file_path
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_area.get("1.0", "end"))
    else:
        new_path = save_file_as(text_area)  # Update file_path after Save As
        if new_path:
            file_path = new_path  # Assign the new file path

def save_file_as(text_area):
    global file_path
    new_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", ".txt"), ("All Files", ".*")])
    if new_path:
        with open(new_path, "w") as file:
            file.write(text_area.get("1.0", "end"))
        return new_path  # Return the new file path
    return None  # If user cancels Save As, return None
