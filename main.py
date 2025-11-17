import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Player, Result

app = FastAPI(title="TSV Eisenberg API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "TSV Eisenberg Backend Running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# Seed helper for demo content
@app.post("/api/seed")
def seed_demo():
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")

    # Only seed if empty
    if db["player"].count_documents({}) == 0:
        demo_players = [
            Player(name="Max Müller", nickname="Maxi", position="Spieler", games_played=12, average_pins=540.5, best_game=589, strikes=32, spares=68).model_dump(),
            Player(name="Lena Schmidt", nickname="Leni", position="Spielerin", games_played=10, average_pins=528.3, best_game=575, strikes=28, spares=60).model_dump(),
            Player(name="Paul Wagner", nickname="Pauli", position="Captain", games_played=14, average_pins=552.1, best_game=601, strikes=40, spares=72).model_dump(),
        ]
        db["player"].insert_many(demo_players)

    if db["result"].count_documents({}) == 0:
        demo_results = [
            Result(date="2025-11-09", opponent="KSV Weimar", home=True, location="Eisenberg", league="Thüringenliga", team_score=3320, opponent_score=3255, highlights="Starke Teamleistung, Pauli mit 589 Pins", top_players=[{"player_name":"Paul Wagner","pins":589}]).model_dump(),
            Result(date="2025-11-02", opponent="SV Jena", home=False, location="Jena", league="Thüringenliga", team_score=3278, opponent_score=3301, highlights="Knappes Spiel auswärts", top_players=[{"player_name":"Lena Schmidt","pins":571}]).model_dump(),
        ]
        db["result"].insert_many(demo_results)

    return {"status": "ok"}

# Public API
@app.get("/api/players")
def list_players(limit: int = 10):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    docs = get_documents("player", {}, limit)
    for d in docs:
        d["_id"] = str(d.get("_id"))
    return docs

@app.get("/api/results")
def list_results(limit: int = 5):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    docs = get_documents("result", {}, limit)
    docs.sort(key=lambda x: x.get("date", ""), reverse=True)
    for d in docs:
        d["_id"] = str(d.get("_id"))
    return docs

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
