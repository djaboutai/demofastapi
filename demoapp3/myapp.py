from fastapi import FastAPI, APIRouter

from .payment import process


app = FastAPI(
    title="ProcessPayment demo",
    description="This app control the method of the Payment Process.",
    docs_url="/docs",
    redoc_url=None,
    version="0.0.1"
)


app.include_router(
    process.router
)

