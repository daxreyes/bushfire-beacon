"""
endpoint for handling filepond file upload
https://pqina.nl/filepond/docs/api/server/#url
"""
from datetime import datetime
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import PlainTextResponse
from loguru import logger

router = APIRouter()

@router.post("/", response_class=PlainTextResponse)
async def process(filepond: UploadFile = File(...)):
    logger.info(f'filepond {filepond.__dict__}')
    return f"{filepond.filename}_{int(datetime.now().timestamp())}"