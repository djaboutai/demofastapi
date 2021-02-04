from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from ..database import db
from ..models.userModel import *

# APIRouter control for users
routerUsers = APIRouter()


@routerUsers.get("", summary="Get all users.", response_model=UserOut)
async def get_all_users():
    users_fetch = db.fetch({"email?contains": "@gmail.com"})
    if users_fetch is None:
        return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            content=jsonable_encoder({"user": users_fetch, "msg": "not found users"}))
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(
        {"user": next(users_fetch), "msg": "found users"}))


@routerUsers.post("",
                  response_model=UserOut,
                  responses={
                      200: {"msg": "User is saved"},
                      400: {"msg": "The request is invalid"},
                      404: {"msg": "User not found"},
                      406: {"msg": "Not acceptable, user already exist"},
                      500: {"msg": "Any internal error"}
                  },
                  summary="Create user")
async def create_user(user_in: UserIn):
    user_fetch = next(db.fetch({"email": user_in.email}))
    print(user_fetch)
    if user_fetch:
        return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            content=jsonable_encoder({"user": user_in, "msg": "user already exist"}))
    try:
        user_saved = db.insert(jsonable_encoder(fake_save_user(user_in)))
    except AttributeError:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=jsonable_encoder({"user": user_in, "msg": "user could not be saved"}))
    if user_saved is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=jsonable_encoder({"user": user_in, "msg": "user could not be saved"}))
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder({"user": user_saved, "msg": "user saved"}))


@routerUsers.delete("", summary="Delete all users", response_model=UserOut)
async def delete_all_users():
    users_items = db.fetch()
    for i in next(users_items):
        print(f'[X/X]Deleting key {i["key"]} username {i["username"]}')
        db.delete(i["key"])
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder({"msg": "deleted all users"}))


@routerUsers.get("/{key}", summary="Returns user by key", response_model=UserOut)
async def get_user_by_key(key: str):
    user = db.get(key)
    if user is None:
        return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            content=jsonable_encoder({"msg": "not found key"}))
    return JSONResponse(status_code=status.HTTP_200_OK, content=user)


@routerUsers.put("/{key}", summary="Update user by key", response_model=UserOut)
async def update_user_by_email(upsub: UserUpdateSub, key: str):
    sub = db.get(key)
    if sub is None:
        return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            content=jsonable_encoder({"msg": "not found user to update"}))

    updates = {}
    if upsub.full_name:
        updates["full_name"] = upsub.full_name

    if upsub.email:
        updates["email"] = upsub.email

    if upsub.username:
        updates["username"] = upsub.username

    db.update(updates, key=sub["key"])

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder({"msg": "user updated"}))

    # try:
    #     user = db.update(jsonable_encoder(fake_save_user(user_in)), key)
    # except AttributeError:
    #     return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE,
    #                         content=jsonable_encoder({"msg": "not found key"}))
    # if user is None:
    #     return JSONResponse(status_code=status.HTTP_200_OK,
    #                         content=jsonable_encoder({"msg": "user updated"}))


@routerUsers.delete("/{key}", summary="Delete a user", response_model=UserOut)
async def delete_user(key: str, user_in: UserIn):
    user_item = next(db.fetch({"email": user_in.email}, buffer=1))
    print(f'[X/X]Deleting key {key} username {user_item[0]["username"]}')
    db.delete(key=key)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder({"msg": "user deleted"}))
