from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import HTTPException

from agent.factory import create_agent
from model.models import UserPrompt

load_dotenv()

app = FastAPI(
    title="Conversational Agent",
    description="Agente tha uses LLMs for user interaction.",
)

try:
    agent = create_agent()
except Exception as e:
    print(f"Failed to create agent: {e}")


@app.post("/chat")
def chat_with_agent(user_prompt: UserPrompt):
    try:
        return agent.handle_prompt(user_prompt)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
