from tkinter import messagebox
from user_request import request_admin_permission  # Import file-based request

# Define restricted operations per user
restricted_operations = {
    "user2": ["find_replace", "delete", "undo_redo", "print", "search"],
    "user3": ["find_replace", "search"]  # These require approval
}

# Completely blocked operations for User3 (no admin approval allowed)
blocked_operations_user3 = ["delete", "undo_redo", "print"]

def execute_restricted_action(user, action_name, text_area, execute_action):
    """Handles restricted actions for User2 and User3 with file-based admin approval."""

    user = user.lower()

    # Admin and User1 have full access
    if user not in restricted_operations:
        execute_action(action_name, text_area)
        return

    # Blocked actions for User3 — No approval possible
    if user == "user3" and action_name in blocked_operations_user3:
        messagebox.showerror("Access Denied", f"{action_name} is not allowed for User3.")
        return

    # Restricted actions that need admin approval
    if action_name in restricted_operations[user]:
        approved = request_admin_permission(user, action_name)
        if approved:
            execute_action(action_name, text_area)
        # If not approved, request_admin_permission already shows message
    else:
        # Allowed action
        execute_action(action_name, text_area)
