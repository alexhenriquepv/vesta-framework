alert_emergency_contact_declaration = {
    "name": "alert_emergency_contact",
    "description": "Alerts an emergency contact with a specific message.",
    "parameters": {
        "type": "object",
        "properties": {
            "contact_name": {
                "type": "string",
                "description": "The name of the emergency contact to notify."
            },
            "message": {
                "type": "string",
                "description": "The message to send to the emergency contact."
            }
        },
        "required": ["contact_name", "message"]
    }
}

def alert_emergency_contact(contact_name: str, message: str):
    """
    Alerts an emergency contact with a message.
    Args
        contact_name: The name of the emergency contact to notify.
        message: The message to send to the emergency contact.
    Returns
        A dictionary with status and contact information.
    """
    print(f"--- ALERTING EMERGENCY CONTACT ---")
    print(f"Contact: {contact_name}")
    print(f"Message: {message}")
    print(f"--------------------------------")
    return { "contact": contact_name, "message": message }