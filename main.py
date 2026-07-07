import os
import sys
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from db import SessionLocal, engine
import models
import schemas

if os.path.dirname(__file__) not in sys.path:
    sys.path.insert(0, os.path.dirname(__file__))

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hero Clash Backend")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "change_this_secret_for_production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_account_by_username(db: Session, username: str):
    return db.query(models.Account).filter(models.Account.username == username).first()


def authenticate_account(db: Session, username: str, password: str):
    account = get_account_by_username(db, username)
    if not account or not verify_password(password, account.password_hash):
        return None
    return account


def get_current_account(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Ungültiges Token.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    account = get_account_by_username(db, username)
    if account is None:
        raise credentials_exception
    return account


@app.get("/")
def root():
    return {"status": "ok", "service": "hero-clash-backend"}


@app.post("/register", response_model=schemas.AccountResponse)
def register(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    existing = get_account_by_username(db, account.username)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Benutzername existiert bereits.")
    hashed_password = get_password_hash(account.password)
    db_account = models.Account(
        username=account.username.strip(),
        password_hash=hashed_password,
        coins=100,
        wins=0,
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


@app.post("/token", response_model=schemas.Token)
def login_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    account = authenticate_account(db, form_data.username, form_data.password)
    if not account:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Ungültiger Benutzername oder Passwort.", headers={"WWW-Authenticate": "Bearer"})
    access_token = create_access_token(data={"sub": account.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me", response_model=schemas.AccountResponse)
def read_current_account(current_account: models.Account = Depends(get_current_account)):
    return current_account


@app.get("/store", response_model=List[schemas.StoreItem])
def get_store():
    return [
        schemas.StoreItem(name="Starter-Paket", price=50, description="+50 Coins"),
        schemas.StoreItem(name="Premium-Skin", price=120, description="Exklusiver Look"),
        schemas.StoreItem(name="Bonus-Boost", price=180, description="Mehr Startenergie"),
    ]


@app.post("/buy")
def buy_item(request: schemas.BuyItem, current_account: models.Account = Depends(get_current_account), db: Session = Depends(get_db)):
    item_prices = {"Starter-Paket": 50, "Premium-Skin": 120, "Bonus-Boost": 180}
    if request.item not in item_prices:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item nicht gefunden.")
    price = item_prices[request.item]
    if current_account.coins < price:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nicht genügend Coins.")
    current_account.coins -= price
    unlocks = current_account.store_unlocks
    if request.item not in unlocks:
        unlocks.append(request.item)
    current_account.store_unlocks = unlocks
    db.add(current_account)
    db.commit()
    db.refresh(current_account)
    return {"message": f"{request.item} gekauft", "coins": current_account.coins, "store_unlocks": current_account.store_unlocks}
