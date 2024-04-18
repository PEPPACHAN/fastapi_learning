from fastapi import FastAPI, APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer


from typing import Union
from jwt.exceptions import ExpiredSignatureError
from pydantic import BaseModel, HttpUrl

import json
import jwt
from datetime import datetime, timedelta


secret = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJuZXZlcmdldHRoZXNlY3JldCJ9.QbuvU88A57q6oXEq065f54vUCL53lGzPFvYrMzHZqO0"
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/")

bd = {
    "username": "PEPPA",
    "password": "peppa"
}


router = APIRouter(prefix="/route", tags=["router"])

class Item(BaseModel):
    id: int
    name: str
    price: int
    is_offer: Union[bool, None] = False


@router.get("/item/{itemid}", tags=["Get_All"], responses={400: {"detail": "All is OK"}})
async def item(itemid: int, q: Union[str, None] = "some q"):
    return {itemid: q}

@router.put("/items/update/", tags=["put"])
async def update_item(item: Item):
    return {"id": item.id, "name": item.name, "price": item.price}

@router.post("/release/")
async def postik(item: Item):
    return item


auth_router = APIRouter(prefix="/auth", tags=["auth"])

# @auth_router.post("/jwt/get", tags=["auth", "general"])
async def create_jwt(model: dict):
    model.update({"exp":datetime.utcnow()+timedelta(minutes=1)})
    encode_jwt = jwt.encode(model, secret, algorithm="HS256")
    return encode_jwt, jwt.decode(encode_jwt, secret, algorithms="HS256")


@auth_router.post("/")
async def authorize(username: str, password: str):
    if username == bd["username"] or password == bd["password"]:
        return await create_jwt({
            "sub": {
                "username": username,
                "auth": True
                }})
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")


@auth_router.get("/check/")
async def check_jwt(token: str):
    try:
        jwt.decode(token, secret, algorithms="HS256")
    except ExpiredSignatureError:
        return HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Unavailible token")
    return "Availible token"


app = FastAPI()

@app.get("/", tags=["Get_All"])
def greeting():
    return {"hi": "everyone"}

app.include_router(router)
app.include_router(auth_router)

# uvicorn main:app --reload
