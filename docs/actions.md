# Creating ActionTasks

ActionTasks are functions the LLM can call to perform **side effects** (alarms, notifications, API calls).

---

## Example: Turning On an Alarm

### Step 1 — Define the Function
Create a new action task inside ```tasks/actions```.
```python
def alert_emergency_contact(contact_name: str, message: str) -> dict[str, str]:
    return {
        "contact_name": contact_name,
        "message": message
    }
```

### Step 2 - Create the declaration
In the same file, put the declaration variable.
```python
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
```

### Step 3 - Register the Action
Go to file ```tasks/__init__.py``` and add a register for this action.
```python
TaskRegistry.register_action(alert_emergency_contact)
```