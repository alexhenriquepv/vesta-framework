turn_alarm_on_declaration = {
    "name": "turn_alarm_on",
    "description": "Turn on the alarm"
}

def turn_alarm_on() -> dict[str, str]:
    """
        Turns on an alarm.

        Returns:
            A dictionary indicating the alarm type.
    """
    print("Turning on the alarm!")
    return { "activated": "True" }