# Creating ProcessingTasks

ProcessingTasks handle **event input** and output structured results.  
They must not perform external actions directly.

---

## Example: Heart Rate Anomaly Detection
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

## Registering the Task
Go to ```tasks/__init__.py``` and add register for this action.
```python
TaskRegistry.register_processing(HeartRateAnomalyTask)
```