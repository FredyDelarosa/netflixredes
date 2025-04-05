from fastapi import FastAPI
from routes import video, upload

app = FastAPI()

app.include_router(video.router)
app.include_router(upload.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
