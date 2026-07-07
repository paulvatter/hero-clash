from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class AccountCreate(BaseModel):
    username: str
    password: str


class AccountLogin(BaseModel):
    username: str
    password: str


class AccountResponse(BaseModel):
    username: str
    coins: int
    wins: int
    store_unlocks: List[str]
    created_at: datetime
    last_login: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class StoreItem(BaseModel):
    name: str
    price: int
    description: str


class BuyItem(BaseModel):
    item: str
