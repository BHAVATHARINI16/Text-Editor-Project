from tkinter import simpledialog

users = {
    "admin": {"password": "adminpass", "access": "admin"},
    "user1": {"password": "user1pass", "access": "full"},
    "user2": {"password": "user2pass", "access": "limited"},
    "user3": {"password": "user3pass", "access": "restricted"},
}

def login(root):
    username = simpledialog.askstring("Login", "Enter username:")
    password = simpledialog.askstring("Login", "Enter password:", show="*")

    if username in users and users[username]["password"] == password:
        return {"username": username, "access": users[username]["access"]}
    else:
        root.destroy()
        exit()
