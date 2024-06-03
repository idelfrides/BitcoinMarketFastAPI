from typing import List
from pydantic import BaseModel

# -----------------------------------------------

class Favorite(BaseModel):
    id: int
    symbol: str
    user_id: int
    
    class Config:
        from_attributes = True

class UserListOutput(BaseModel):
    id: int
    name: str
    favorites: List[Favorite]
    
    class Config:
        from_attributes = True

class UserCreateInput(BaseModel):
    name: str
    
class StandartOutput(BaseModel):
    message: str
    
class ErrorOutput(BaseModel):
    details: str
    
class UserFavoriteAddInput(BaseModel):
    user_id: int
    symbol: str
    
class DaySummaryOutput(BaseModel):
    symbol: str
    highest: float
    lowest: float
    date: str
    details: str
