# Event-Driven Agent Framework

The **Event-Driven Agent Framework** is a Python framework designed to build intelligent agents that process events from sensors, wearable devices, or any external system.  
It combines **ProcessingTasks**, which transform raw events into structured insights, and **ActionTasks**, which allow the agent to trigger external actions (e.g., turning on alarms, sending notifications, or interacting with third-party APIs).

---

## 🔑 Key Concepts

- **Event**  
  The basic unit of information the agent receives.  
  Example: a movement detection event, a low battery event, or a health metric reading.

- **ProcessingTask**  
  A task that analyzes incoming events and produces insights or predictions.  
  Example: detect if a person appears in a camera feed.

- **ActionTask**  
  A callable action that the LLM can execute to respond to an event.  
  Example: trigger an alarm or send a push notification.

- **Planner**  
  Orchestrates how events are processed and decides which actions (if any) should be executed. The planner leverages an LLM to interpret context and select appropriate actions.

- **TaskRegistry**  
  A central registry for all `ProcessingTasks` and `ActionTasks`. Developers extend the framework by registering new tasks.

---

## ⚙️ Architecture Overview

Incoming Event --> EventOrchestrator --> ProcessingTask --> Planner (LLM) --> ActionTask(s)

1. **EventOrchestrator** receives an event and delegates it to the appropriate ProcessingTask.
2. **The ProcessingTask** executes business logic and produces structured results.
3. **The Planner interprets** the result using an LLM and selects one or more ActionTasks.
4. The chosen ActionTasks are executed, producing side effects (e.g., notifications, alarms).

---

## 🚀 Example Flow

1. A movement is detected by the security system.  
2. `MovementDetectionTask` runs and returns:  
   ```json
    {"object_detected": "person"}
3. The Planner interprets this and decides to trigger the alarm:
    ```json
    {
      "function_call": {
        "name": "turn_alarm_on",
        "args": { "alarm_type": "Noise" }
      }
    }
4. The ActionTask executes and turns on the noise alarm.

## 📚 Documentation

- [Installation Guide](install.md)  
- [Creating ActionTasks](actions.md)
- [Creating ProcessingTasks](processing.md)  
