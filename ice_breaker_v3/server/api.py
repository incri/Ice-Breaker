from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ice_breaker import generate_summary

router = APIRouter()


@router.get("/summary/{person_name}", response_model=Dict[str, Any])
async def get_summary(person_name: str):
    """
    API endpoint to fetch Wikipedia summary and image for a given person.

    Args:
        person_name (str): Name of the person.

    Returns:
        Dict[str, Any]: A dictionary containing structured summary and thumbnail URL.
    """
    summary, thumbnail_url = generate_summary(person_name)

    if summary is None:
        raise HTTPException(status_code=404, detail="Person not found on Wikipedia.")

    return {"details": summary.to_dict(), "thumbnail": thumbnail_url}
