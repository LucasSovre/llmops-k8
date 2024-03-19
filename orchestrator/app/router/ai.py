import asyncio
import datetime
import json
from typing import Any, Dict, Optional
import uuid
from fastapi import Depends, Request, routing
from pydantic import BaseModel
from redis import Redis
from sse_starlette.sse import EventSourceResponse
from ..dependencies.database import get_mongo_dependency, get_redis_dependency

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
async def prompt(input: PromptInput, redisConn:Redis = Depends(get_redis_dependency), mongoConn = Depends(get_mongo_dependency)):
    ticket_id = uuid.uuid4().hex
    error = None
    message = json.dumps({
        "ticket_id": ticket_id,
        "model": input.model,
        "params": input.params,
        "prompt": input.prompt
    })
    try:
        mongoConn.db.ticket.insert_one({
        "ticket_id": ticket_id,
        "model": input.model,
        "params": input.params,
        "prompt": input.prompt,
        "status": "pending",
        "result": None,
        "process_time": None,
        "created_at": datetime.datetime.now(),
        "updated_at": None,
        })
    except Exception as e:
        error = str(e)
    try:
        redisConn.lpush(f"input_queue_{input.model}", message)
    except Exception as e:
        error = str(e)
    return {
        "error": error,
        "ticket_id": ticket_id
        }

@router.get("/stream")
async def stream(channel:str,request: Request,redisConn:Redis = Depends(get_redis_dependency), mongoConn = Depends(get_mongo_dependency)):
    pubsub = redisConn.pubsub()
    pubsub.subscribe(channel)
        
    async def event_generator():
        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break
    
            msg = pubsub.get_message()
            if msg and msg['type'] == 'message':
                data = json.loads(handle_message(msg))
                try:
                    result = mongoConn.db.ticket.find_one_and_update(
                        {"ticket_id": channel},
                        {"$set": {"status": "completed", "result": data.get("result"), "updated_at": datetime.datetime.now(), "process_time": data.get("process_time")}},
                        return_document=True
                    )
                except Exception as e:
                    print(f"Error updating ticket {channel}: {str(e)}")
                yield {
                    "event": "message",
                    "id": channel,
                    "retry": RETRY_TIMEOUT,
                    "data": data.get("result")
                }
            
            await asyncio.sleep(STREAM_DELAY)
    return EventSourceResponse(event_generator())