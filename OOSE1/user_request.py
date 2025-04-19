import json
import os
import time
from tkinter import messagebox

# Folder path for storing request files
SHARED_REQUESTS_FOLDER = "shared/requests"

# Function to request admin permission for restricted actions
def request_admin_permission(user, action_name):
    # Ensure the shared/requests folder exists before writing the file
    os.makedirs(SHARED_REQUESTS_FOLDER, exist_ok=True)

    # Define the path for the request file based on user and action
    request_file = os.path.join(SHARED_REQUESTS_FOLDER, f"request_{user}_{action_name}.json")

    # Request data structure to be written into the file
    request_data = {
        "user": user,
        "action": action_name,
        "status": "pending"  # Initial status is pending until admin approval
    }

    # Create the request file and write the request data to it
    try:
        with open(request_file, "w") as file:
            json.dump(request_data, file)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create request file: {str(e)}")
        return False

    # Inform the user that their request is sent and waiting for admin approval
    messagebox.showinfo("Request Sent", "Waiting for Admin approval...")

    # Wait for admin's approval or denial (timeout after 60 seconds)
    for _ in range(60):
        time.sleep(1)
        if os.path.exists(request_file):  # Check if file exists (it should exist once created)
            try:
                # Read the file to check the status of the request
                with open(request_file, "r") as file:
                    data = json.load(file)
                    status = data.get("status")

                # Check the status of the request
                if status == "approved":
                    return True
                elif status == "denied":
                    messagebox.showwarning("Action Denied", "Admin denied your request.")
                    return False
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read request file: {str(e)}")
                return False

    # If admin does not respond in time, show a timeout error
    messagebox.showerror("Timeout", "Admin did not respond in time.")
    return False
