from fastapi import FastAPI, APIRouter
from views import user_router, assets_router
from views_sync import sync_router

app = FastAPI()
router = APIRouter()

@router.get("/")
def home():
    return {"greeting": "Hello World! Welcome HOME."}

app.include_router(prefix='/home', router=router)
app.include_router(router=user_router)
app.include_router(router=assets_router)
app.include_router(router=sync_router)