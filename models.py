import json

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func

from db import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(32), unique=True, index=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    coins = Column(Integer, default=100, nullable=False)
    wins = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_login = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    _store_unlocks = Column("store_unlocks", Text, default="[]", nullable=False)

    @property
    def store_unlocks(self):
        try:
            return json.loads(self._store_unlocks or "[]")
        except ValueError:
            return []

    @store_unlocks.setter
    def store_unlocks(self, value):
        self._store_unlocks = json.dumps(value or [])
