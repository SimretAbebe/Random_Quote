from fastapi import FastAPI, HTTPException
import json
import random
from typing import Dict, List, Any

app = FastAPI(
    title="Random Quote API",
    description="A simple API to get random inspirational quotes.",
    version="1.0.0"
)

# Load quotes from JSON file
def load_quotes() -> List[Dict[str, Any]]:
    try:
        with open("quotes.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Quotes file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid quotes file format")

quotes = load_quotes()

@app.get("/quotes/random", response_model=Dict[str, Any])
def get_random_quote():
    if not quotes:
        raise HTTPException(status_code=404, detail="No quotes available")
    return random.choice(quotes)

@app.get("/quotes", response_model=List[Dict[str, Any]])
def get_all_quotes():
    return quotes

@app.get("/quotes/{quote_id}", response_model=Dict[str, Any])
def get_quote_by_id(quote_id: int):
    for quote in quotes:
        if quote["id"] == quote_id:
            return quote
    raise HTTPException(status_code=404, detail="Quote not found")
