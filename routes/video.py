from fastapi import APIRouter, Request, Response
from fastapi.responses import StreamingResponse
import os

router = APIRouter(prefix="/video", tags=["Video"])

STORAGE_PATH = "storage"

@router.get("/{video_name}")
def stream_video(request: Request, video_name: str):
    file_path = os.path.join(STORAGE_PATH, video_name)

    if not os.path.exists(file_path):
        return Response(status_code=404, content="Video no encontrado")

    file_size = os.path.getsize(file_path)
    range_header = request.headers.get("range")
    
    start_byte = 0
    end_byte = file_size - 1  # Por defecto se entrega todo

    if range_header:
        # Ejemplo: "bytes=1000-2000"
        bytes_range = range_header.replace("bytes=", "")
        parts = bytes_range.split("-")
        start_byte = int(parts[0])
        if len(parts) > 1 and parts[1]:
            end_byte = int(parts[1])
        else:
            # Limita la descarga a 1MB por solicitud si no se especifica
            end_byte = min(start_byte + 1024 * 1024 - 1, file_size - 1)

    chunk_size = end_byte - start_byte + 1

    def stream_chunk():
        with open(file_path, "rb") as video:
            video.seek(start_byte)
            yield video.read(chunk_size)

    headers = {
        "Content-Range": f"bytes {start_byte}-{end_byte}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(chunk_size),
        "Content-Type": "video/mp4"
    }

    return StreamingResponse(stream_chunk(), status_code=206, headers=headers)
