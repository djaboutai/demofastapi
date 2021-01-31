from fastapi import FastAPI, APIRouter

from .payment import process


app = FastAPI(
    redoc_url="/redocs",
    title="ProcessPayment demo",
    description="This app control the method of the Payment Process.",
    version="0.0.1"
)


app.include_router(
    process.router
)

