from fastapi import FastAPI
from app.api.api import router

app = FastAPI(title="PaperLens API")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "PaperLens backend running "}