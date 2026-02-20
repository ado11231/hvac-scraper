from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from configs import MANUFACTURERS
from scraper import scrape
import asyncio

app = FastAPI()

class ScrapeRequest(BaseModel):
    manufacturer: str
    model_number: str

@app.post("/scrape")
async def scrape_endpoint(request: ScrapeRequest):
    if request.manufacturer not in MANUFACTURERS:
        raise HTTPException(status_code=404, detail="Manufacterer Not Found")
    
    config = MANUFACTURERS[request.manufacturer]
    await scrape(config, request.model_number, request.manufacturer)
    

    return {"status": "success", "manufacterer": request.manufacturer, "model_number": request.model_number}

