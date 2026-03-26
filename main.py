from fastapi import FastAPI
import uvicorn

# Import routers
from app.api import chat

app = FastAPI(title="Ouroboros Web Chat", description="Web chat interface for Ouroboros agent")

# Include API routers
app.include_router(chat.router)

@app.get("/")
async def root():
    return {"message": "Ouroboros Web Chat API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# For deployment in Colab/Jupyter
app_for_uvicorn = app