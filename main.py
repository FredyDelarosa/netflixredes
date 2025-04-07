from fastapi import FastAPI
from routes import video, upload
from fastapi.middleware.cors import CORSMiddleware
from auth import routes, models
from auth.database import engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)
app.include_router(routes.router)
app.include_router(video.router)
app.include_router(upload.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
