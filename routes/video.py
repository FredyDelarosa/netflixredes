from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse
import os

router = APIRouter(prefix="/video", tags=["Video"])

STORAGE_PATH = "storage"

def video_streamer(file_path: str, start: int = 0):
    with open(file_path, "rb") as video:
        video.seek(start)
        while chunk := video.read(1024 * 1024): 
            yield chunk

@router.get("/{video_name}")
def stream_video(video_name: str, range: str = None):
    file_path = os.path.join(STORAGE_PATH, video_name)
    
    if not os.path.exists(file_path):
        return Response(status_code=404, content="Video no encontrado")
    
    start_byte = 0
    if range:
        start_byte = int(range.replace("bytes=", "").split("-")[0])
    
    return StreamingResponse(video_streamer(file_path, start_byte), media_type="video/mp4")
