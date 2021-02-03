from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from dependencies import get_query_token, get_token_header
from root import home
from internal import admin
from routers import items, users

import uvicorn

# Tags metadata
tags_metadata = [
    {
        "name": "root",
        "description": "Operations with root.",
    },
    {
        "name": "items",
        "description": "Operations with items.",
    },
    {
        "name": "users",
        "description": "Operations with users.",
    },
    {
        "name": "admin",
        "description": "Operations with admin.",
    }
]

origins = [
    "http://127.0.0.1:8888",
]

# FastAPI initialization app
app = FastAPI(
    title="demoapp2",
    description="This project is a demo project, created to the simple use of learn FastApi",
    dependencies=[Depends(get_query_token)],
    openapi_tags=tags_metadata,
    version="0.0.1"
)

# App static folder {for css files}
app.mount("/static", StaticFiles(directory="static"), name="static")


# App add middleware CORS, allows origins, credentials, methods and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# App include routers {users, items, admin and root}
app.include_router(
    users.routerUsers,
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    items.routerItems,
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    admin.routerAdmin,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)
app.include_router(
    home.routerHome,
    tags=["root"],
    responses={404: {"description": "Not found"}},
)

if __name__ == "__main__":
    uvicorn.run("myapp:app", host="0.0.0.0", port=8888, reload=True)
