from fastapi import FastAPI
from core.config import settings
from api.endpoints import router

app = FastAPI(title="C++ AI Assistant", version="1.0.0")
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)