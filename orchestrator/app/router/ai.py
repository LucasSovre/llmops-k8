import asyncio
import json
from typing import Any, Dict, Optional
import uuid
from fastapi import Depends, Request, routing
from pydantic import BaseModel
from redis import Redis
from sse_starlette.sse import EventSourceResponse
from ..dependencies.database import get_redis_dependency

STREAM_DELAY = 1  # second
RETRY_TIMEOUT = 15000  # milisecond

class PromptInput(BaseModel):
    model: str
    params: Optional[Dict[str, Any]]
    prompt: str

class PromptOutput(BaseModel):
    error : str|None = None
    ticket_id: str

router = routing.APIRouter()

def handle_message(message):
    """Handle messages received from the subscription."""
    decoded_message = message['data'].decode('utf-8')
    return decoded_message

@router.post("/prompt")
async def prompt(input: PromptInput, redisConn:Redis = Depends(get_redis_dependency)):
    ticket_id = uuid.uuid4().hex
    error = None
    message = json.dumps({
        "ticket_id": ticket_id,
        "model": input.model,
        "params": input.params,
        "prompt": input.prompt
    })
    try:
        redisConn.lpush("input_queue", message)
    except Exception as e:
        error = str(e)
    return {
        "error": error,
        "ticket_id": ticket_id
        }

@router.get("/stream")
async def stream(channel:str,request: Request,redisConn:Redis = Depends(get_redis_dependency)):
    pubsub = redisConn.pubsub()
    pubsub.subscribe(channel)
        
    async def event_generator():
        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break
    
            msg = pubsub.get_message()
            if msg and msg['type'] == 'message':
                data = handle_message(msg)
                yield {
                    "event": "message",
                    "id": channel,
                    "retry": RETRY_TIMEOUT,
                    "data": data
                }
            
            await asyncio.sleep(STREAM_DELAY)
    return EventSourceResponse(event_generator())