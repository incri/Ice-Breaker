from fastapi import APIRouter, HTTPException, Request, Query
from fastapi.templating import Jinja2Templates
from ice_breaker import generate_summary

router = APIRouter()
templates = Jinja2Templates(directory="server/templates")


@router.get("/summary")
async def get_summary(
    request: Request, person_name: str = Query(..., description="Name of the person")
):
    """
    Fetch Wikipedia summary and render it in a template.
    """
    summary, thumbnail_url = generate_summary(person_name)

    if summary is None:
        raise HTTPException(status_code=404, detail="Person not found on Wikipedia.")

    return templates.TemplateResponse(
        "summary.html",
        {"request": request, "details": summary.to_dict(), "thumbnail": thumbnail_url},
    )
