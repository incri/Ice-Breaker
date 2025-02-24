from fastapi import FastAPI
from server.api import router

app = FastAPI(title="Wikipedia Summary API", version="1.0")

# Include API routes
app.include_router(router, prefix="/api", tags=["Wikipedia Summary"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Wikipedia Summary API!"}
