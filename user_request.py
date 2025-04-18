# user_request.py
import json
import os
import time
from tkinter import messagebox

SHARED_REQUESTS_FOLDER = "shared/requests"

def request_admin_permission(user, action_name):
    request_file = os.path.join(SHARED_REQUESTS_FOLDER, f"request_{user}_{action_name}.json")

    request_data = {
        "user": user,
        "action": action_name,
        "status": "pending"
    }

    with open(request_file, "w") as file:
        json.dump(request_data, file)

    messagebox.showinfo("Request Sent", "Waiting for Admin approval...")

    for _ in range(60):
        time.sleep(1)
        if os.path.exists(request_file):
            with open(request_file, "r") as file:
                data = json.load(file)
                status = data.get("status")

            if status == "approved":
                return True
            elif status == "denied":
                messagebox.showwarning("Action Denied", "Admin denied your request.")
                return False

    messagebox.showerror("Timeout", "Admin did not respond in time.")
    return False
