# Application Modules

This document provides detailed descriptions of the core modules that constitute the Event-Driven Agent Framework, explaining their responsibilities and interactions.

---

## `main.py`

This is the application's entry point, utilizing the FastAPI framework to expose its functionality as a web service.

* **Functionality**: It initializes the FastAPI application and the `EventOrchestrator`, which serves as the primary orchestrator for the framework.
* **`/event` Endpoint**: Defines a POST endpoint that accepts an `Event` as input. The `EventOrchestrator` handles the incoming event, processes it, and returns the result.
* **Orchestration**: `main.py` acts as the interface, receiving external events and delegating the complete processing flow to the `EventOrchestrator` class.
* **Execution**: The `if __name__ == "__main__"` block allows the service to be run locally using `uvicorn`.

---

## `task_registry.py`

This file manages a central registry for all tasks within the framework.

* **Functionality**: The `TaskRegistry` maintains static lists for `ProcessingTasks` and `ActionTasks`. This allows different parts of the framework, such as the `EventOrchestrator` and `GeminiLLM`, to access the available tasks globally.
* **Methods**: It provides class methods for registering (`register_processing`, `register_action`) and retrieving (`get_processing_tasks`, `get_action_tasks`) tasks, ensuring all tasks are discovered and accessible by the framework.
* **Typing**: It utilizes Python's typing (`List`, `Type`, `types.FunctionDeclaration`) to ensure data consistency for registered tasks.

---

## `planner.py`

The `Planner` is a central component that integrates `ProcessingTasks` with the LLM to determine the response and actions to be executed.

* **Functionality**: It receives an already executed `ProcessingTask` and uses its results to generate a prompt for the LLM. The LLM, in turn, can produce a text response and/or one or more function calls.
* **Flow**:
    1.  The `Planner` creates a prompt for the LLM using the `ProcessingTask`'s result.
    2.  It sends the prompt to the `GeminiLLM` to obtain a response.
    3.  It iterates over any function calls returned by the LLM and executes them using the `ProcessingTask`'s action registry.
    4.  It collects the results of the executed actions.
* **Return Value**: Returns an `AgentResponse`, which includes the LLM's text message, the original event, and a history of the actions that were executed.

---

## `EventOrchestrator.py`

The `EventOrchestrator` is the primary entry point for the framework's business logic.

* **Functionality**: It receives an event and delegates responsibility to the correct `ProcessingTask` based on the task name (`event.task_name`).
* **Flow**:
    1.  The orchestrator checks the list of registered tasks.
    2.  It finds the `ProcessingTask` that matches the `task_name` from the event.
    3.  It instantiates that task with the provided event.
    4.  It invokes the `Planner` to handle the task instance and obtain the final response.
* **Error Handling**: If the requested task in the event is not found in the registry, it returns an error message.

---

## `gemini.py`

This file encapsulates the logic for interacting with the Gemini LLM API.

* **Functionality**: It handles communication with the language model, including setting up tools (Function Calling) based on the registered tasks.
* **Process**:
    1.  It initializes the Gemini client with the model name (`gemini-2.5-flash-lite`).
    2.  It retrieves `ActionTask` declarations from the `TaskRegistry` and configures them as tools for the model. This is essential for the LLM to understand which actions it can call.
    3.  The `generate_response` function accepts a prompt and sends the content to the model.
* **Response Parsing**: It parses the LLM's response, extracting both the text response and any function calls the model has generated. The result is returned as an `LLMResponse` object.