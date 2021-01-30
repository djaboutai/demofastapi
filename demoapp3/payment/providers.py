from typing import Optional

from fastapi import APIRouter, status, Body
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder


from datetime import datetime


router = APIRouter(
    prefix="/providers",
    tags=["tag-providers"]
)


@router.post(
    "/cheappaymentgateway/",
    responses={
            200: {"message": "Payment is processed"},
            400: {"message": "The request is invalid"},
            500: {"message": "Any error"}
        }
)
async def cheap_payment_gateway_process():
    pass


@router.post(
    "/expensivepaymentgateway/",
    responses={
            200: {"message": "Payment is processed"},
            400: {"message": "The request is invalid"},
            500: {"message": "Any error"}
        }
)
async def expensive_payment_gateway_process():
    pass


@router.post(
    "/premiumpaymentgateway/",
    responses={
            200: {"message": "Payment is processed"},
            400: {"message": "The request is invalid"},
            500: {"message": "Any error"}
        }
)
async def premium_payment_gateway_process():
    pass
