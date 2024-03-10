from fastapi import FastAPI, Request

app = FastAPI()

from .router.utils import router as api_router
from .router.ai import router as ai_router

app.include_router(api_router, prefix="/utils", tags=["utils"])
app.include_router(ai_router, prefix="/ai", tags=["ai"])