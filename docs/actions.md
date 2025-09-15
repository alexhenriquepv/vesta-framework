# Creating ActionTasks

ActionTasks are functions the LLM may call to perform **side effects** (alarms, notifications, API calls).
Instead of producing a natural language response, the model generates a formatted string (e.g., JSON) that the framework
knows to interprets and executes.
It`s following the definition of Function calling method that connects the LLM Models to external tools and systems.
A better definition of Function calling can be found in the [Gemini API docs](https://ai.google.dev/gemini-api/docs/function-calling) and [OpenAI docs](https://help.openai.com/en/articles/8555517-function-calling-in-the-openai-api).

---

## Example: Alert emergency contact

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

The declaration variable is defined using a select subset of the [OpenAPI schema](https://spec.openapis.org/oas/v3.0.3#schemaw) format.
A single function declaration can include the following parameters:

1. `name` (string): A unique name for the function (get_weather_forecast, send_email). Use descriptive names without spaces or special characters (use underscores or camelCase).
2. `description` (string): A clear and detailed explanation of the function's purpose and capabilities. 
This is crucial for the model to understand when to use the function. 
Be specific and provide examples if helpful ("Finds theaters based on location and optionally movie title which is currently playing in theaters.").

3. `parameters` (object): Defines the input parameters the function expects.
    1. `type` (string): Specifies the overall data type, such as object.
    2. `properties` (object): Lists individual parameters, each with:
        1. `type` (string): The data type of the parameter, such as string, integer, boolean, array.
        2. `description` (string): A description of the parameter's purpose and format. Provide examples and constraints ("The city and state, e.g., 'San Francisco, CA' or a zip code e.g., '95616'.").
        3. `enum` (array, optional): If the parameter values are from a fixed set, use "enum" to list the allowed values instead of just describing them in the description. This improves accuracy ("enum": ["daylight", "cool", "warm"]).
        4. `required` (array): An array of strings listing the parameter names that are mandatory for the function to operate.

### Step 3 - Register the Action
Go to file ```tasks/__init__.py``` and add a register for this action.
```python
TaskRegistry.register_action(alert_emergency_contact)
```