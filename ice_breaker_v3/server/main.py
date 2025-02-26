from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from server.api import router  # Keep API routes if needed

app = FastAPI(title="Wikipedia Summary App", version="1.0")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="server/templates")

# Include API routes (optional)
app.include_router(router, prefix="/api", tags=["Wikipedia Summary"])


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
