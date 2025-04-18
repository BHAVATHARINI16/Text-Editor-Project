
import os
import json
import tkinter as tk
from tkinter import messagebox

SHARED_REQUESTS_FOLDER = "shared/requests"

def open_admin_panel():
    """Open the admin panel to approve/deny user requests."""
    panel = tk.Toplevel()
    panel.title("Admin Panel - Pending Requests")
    panel.geometry("400x300")

    tk.Label(panel, text="Pending Requests:", font=("Arial", 12, "bold")).pack(pady=10)

    listbox = tk.Listbox(panel, width=50)
    listbox.pack(pady=10)

    approve_button = tk.Button(panel, text="Approve", command=lambda: respond("approved"))
    approve_button.pack(pady=5)

    deny_button = tk.Button(panel, text="Deny", command=lambda: respond("denied"))
    deny_button.pack(pady=5)

    request_files = {}  # To track currently displayed requests

    def refresh_requests():
        nonlocal request_files
        current_requests = load_pending_requests()

        if current_requests.keys() != request_files.keys():
            listbox.delete(0, tk.END)
            request_files = current_requests
            for req_file in request_files:
                info = request_files[req_file]
                listbox.insert(tk.END, f"{info['user']} → {info['action']}")

        panel.after(5000, refresh_requests)  # Auto-refresh every 5 seconds

    def respond(status):
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a request.")
            return

        index = selected[0]
        file_name = list(request_files.keys())[index]
        file_path = os.path.join(SHARED_REQUESTS_FOLDER, file_name)

        with open(file_path, "r") as f:
            data = json.load(f)

        data["status"] = status

        with open(file_path, "w") as f:
            json.dump(data, f)

        messagebox.showinfo("Response Sent", f"Request '{data['action']}' has been {status}.")
        listbox.delete(index)
        del request_files[file_name]

    refresh_requests()

def load_pending_requests():
    """Load all pending requests from the shared folder."""
    requests = {}

    if not os.path.exists(SHARED_REQUESTS_FOLDER):
        os.makedirs(SHARED_REQUESTS_FOLDER)

    for file in os.listdir(SHARED_REQUESTS_FOLDER):
        if file.endswith(".json"):
            file_path = os.path.join(SHARED_REQUESTS_FOLDER, file)
            with open(file_path, "r") as f:
                try:
                    data = json.load(f)
                    if data.get("status") == "pending":
                        requests[file] = data
                except:
                    continue
    return requests
