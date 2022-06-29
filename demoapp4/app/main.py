import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routes.users import routerUsers


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(
        routerUsers,
        prefix="/user",
        tags=["users"]
    )

    return _app


app = get_application()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8888, reload=True)
