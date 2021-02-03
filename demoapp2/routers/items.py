from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


# APIRouter control for items
routerItems = APIRouter()


fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"},
                 "glock": {"name": "Glock"}, "awp": {"name": "AWP"}}


@routerItems.get("/", summary="Returns all items.")
async def get_all_items():
    return JSONResponse(status_code=status.HTTP_200_OK, content=fake_items_db)


@routerItems.get("/{item_id}", summary="Returns name of chosen item_id.")
async def get_item_by_id(item_id: str):
    if item_id not in fake_items_db:
        response = jsonable_encoder({"response": "Not Found"})
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response)
    else:
        response = jsonable_encoder({"name": fake_items_db[item_id]["name"], "item_id": item_id})
        return JSONResponse(status_code=status.HTTP_200_OK, content=response)


@routerItems.put(
    "/{item_id}",
    responses={403: {"description": "Operation forbidden"}},
    summary="Returns updated name of chosen item_id."
)
async def put_item_by_id(item_id: str):
    if item_id != "plumbus":
        response = jsonable_encoder({"response": "You can only update the item: plumbus"})
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=response)
    else:
        response = jsonable_encoder({"item_id": item_id, "name": "The great Plumbus"})
        return JSONResponse(status_code=status.HTTP_200_OK, content=response)
