send_push_notification_declaration = {
    "name": "send_push_notification",
    "description": "Send a push notification"
}

def send_push_notification(username: str, content: str) -> dict:
    """
    Send a push notification.
    Args:
        username: The username or store name or business name.
        content: The content of the push notification.
    Returns:
        A dictionary indicating if notification was sent.
    """
    print(f"Sending push notification => {content} to: {username}")
    return { "username": username, "content": content }