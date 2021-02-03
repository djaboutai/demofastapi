from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


# APIRouter control for users
routerUsers = APIRouter()


@routerUsers.get("/", tags=["users"], summary="Returns all usernames.")
async def get_all_users():
    response = jsonable_encoder([{"username": "Rick"}, {"username": "Morty"}])
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)


@routerUsers.get("/me", tags=["users"], summary="Returns logged username.")
async def get_user_me():
    response = jsonable_encoder({"username": "fakecurrentuser"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)


@routerUsers.get("/{username}", tags=["users"], summary="Returns desired username.")
async def get_user_by_username(username: str):
    response = jsonable_encoder({"username": username + " settings are ready to use."})
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)
