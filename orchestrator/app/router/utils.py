from fastapi import routing

router = routing.APIRouter()

@router.get("/")
async def ping():
    return "OK"