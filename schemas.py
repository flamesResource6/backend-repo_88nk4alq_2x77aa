"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# TSV Eisenberg - Kegeln (Nine-pin) Schemas

class Player(BaseModel):
    """
    Players collection schema
    Collection name: "player"
    """
    name: str = Field(..., description="Player full name")
    nickname: Optional[str] = Field(None, description="Player nickname")
    position: Optional[str] = Field(None, description="Team position/role")
    games_played: int = Field(0, ge=0, description="Total games played")
    average_pins: float = Field(0.0, ge=0, description="Average pins per game (Schnitt)")
    best_game: int = Field(0, ge=0, description="Best pins in a single game")
    strikes: int = Field(0, ge=0, description="Total strikes (Neuner)")
    spares: int = Field(0, ge=0, description="Total spares")
    photo_url: Optional[str] = Field(None, description="Avatar or photo URL")

class PlayerScore(BaseModel):
    player_name: str
    pins: int

class Result(BaseModel):
    """
    Match results schema
    Collection name: "result"
    """
    date: str = Field(..., description="Match date ISO string")
    opponent: str = Field(..., description="Opponent team name")
    home: bool = Field(True, description="Home (True) or Away (False)")
    location: Optional[str] = Field(None, description="Venue or city")
    league: Optional[str] = Field("Thüringenliga", description="League name")
    team_score: int = Field(..., ge=0, description="TSV Eisenberg total pins")
    opponent_score: int = Field(..., ge=0, description="Opponent total pins")
    highlights: Optional[str] = Field(None, description="Short match summary")
    top_players: Optional[List[PlayerScore]] = Field(default_factory=list, description="Top player scores")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
