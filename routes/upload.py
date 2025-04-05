from fastapi import APIRouter, File, UploadFile, HTTPException
import os
import shutil

router = APIRouter(prefix="/upload", tags=["Upload"])

STORAGE_PATH = "storage"

os.makedirs(STORAGE_PATH, exist_ok=True)

@router.post("/")
async def upload_video(file: UploadFile = File(...)):
    file_path = os.path.join(STORAGE_PATH, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "Película subida exitosamente", "filename": file.filename}
