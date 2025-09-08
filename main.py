from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import HTTPException

from core.EventOrchestrator import EventOrchestrator
from model.event import Event

load_dotenv()

app = FastAPI(
    title="Event Driven Agent",
    description="Agent that uses sensor data input and LLMs for response",
)

event_orchestrator = EventOrchestrator()

@app.post("/event")
def app_handle_event(event: Event):
    try:
        return event_orchestrator.handle_event(event)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
