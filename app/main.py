from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, Request, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import (
    APIKeyCookie,
)
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.concurrency import run_until_first_complete

from loguru import logger

from app import models

# from app.database import async_db
from app.api import api_router
from app.api.deps import get_db
from app.config import settings
# from app import pubsub


app = FastAPI(
)
api = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    # on_startup=[pubsub.broadcast.connect],
    # on_shutdown=[pubsub.broadcast.disconnect],
)
app.mount("/api", api)

templates = Jinja2Templates(directory="templates")
app.mount("/", StaticFiles(directory="web/public", html=True), name="root")

# @app.on_event("startup")
# async def startup():
#     await async_db.connect()


# @app.on_event("shutdown")
# async def shutdown():
#     await async_db.disconnect()

# FIXME: When authentication exception is reaised, this is triggered
# which prevents the client from capturing the error.
# Check again for a solution to 2dba2595a17 since deployment is behind a proxy
# and related to slash stuff
# see https://github.com/tiangolo/fastapi/issues/1208#issuecomment-611227244
# @app.exception_handler(StarletteHTTPException)
# async def custom_http_exception_handler(request, exc):
#     logger.info(f"error {request} {exc}")
#     return RedirectResponse("/cobeds19/")


# @app.get("/")
# def index(request: Request, db: Session = Depends(get_db)):
#     # hospitals = crud.get_hospitals(db)
#     id = 1
#     return templates.TemplateResponse("index.html", {"request": request, "id": id})


@api.websocket("/crowdsource")
async def crowdsource_ws(websocket: WebSocket):
    # https://fastapi.tiangolo.com/advanced/websockets/
    # https://www.gitmemory.com/issue/tiangolo/fastapi/3009/808977195
    await websocket.accept()
    await run_until_first_complete(
        (pubsub.ws_receiver("crowdsource"), {"websocket": websocket}),
        (pubsub.ws_sender("crowdsource"), {"websocket": websocket}),
    )


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

api.include_router(api_router, prefix=settings.API_V1_STR)
