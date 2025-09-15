# Creating ProcessingTasks

ProcessingTasks handle **event input** and output structured results.  
They must not perform external actions directly.

---

## Example: Low battery Task
Create new action inside ```actions/processing```
```python
class LowBatteryTask(ProcessingTask):

    def __init__(self, event: Event):
        super().__init__(event=event, prompt_name="low_battery")

    @property
    def action_registry(self) -> dict:
        return {
            "alert_emergency_contact": alert_emergency_contact,
        }

    def run(self):
        return {
            "battery_levels": self.event.data,
            "user_profile": get_user_profile()
        }
```

When you define a Processing Task, it's mandatory to define a prompt that turns this action in an 
specialized agent. For this, open `resources/config.yml` and add a new prompt label:

```yml
low_battery: |
  You are an intelligent agent for managing connected devices in a smart home. Your role is to monitor device battery 
  levels and alert the user if any device is running low on power.
  A processing task that checks the battery status of connected devices was executed. This is the result execution:
  {processing_task_result}

  You have the current available ActionTasks:
  {action_tasks}

  ---
  Instructions:
  - Analyze the battery levels of all devices.
  - If any device has a battery level below 20%, you must take action.
  - If there are devices with low battery send a 
    push notification to client summarizing which devices are low.
  - If all devices have battery levels above 20%, provide a friendly message confirming that all devices are charged.
  - Always produce a clear and friendly response to the user, summarizing the situation.
  - Personalize the message using the user’s name whenever possible.
  - If ActionTasks are relevant, generate the function calls. Do not just describe the actions in text.
  - If no ActionTask is needed, just return the textual response.
```

## Registering the Task
Go to ```tasks/__init__.py``` and add register for this action.
```python
TaskRegistry.register_processing(HeartRateAnomalyTask)
```