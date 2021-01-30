from typing import Optional

from fastapi import APIRouter, status, Body
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder

from .process_controller import *

import datetime

router = APIRouter(
    prefix="/paymentprocess",
    tags=["tag-paymentprocess"]
)


@router.post(
    "/",
    responses={
        200: {"message": "Payment is redirected"},
        400: {"message": "The request is invalid"},
        500: {"message": "Any error"}
    }
)
async def payment_process(
        creditcardnumber: str = Body(...,
                                     alias="creditcardnumber",
                                     description="CreditCardNumber is the credit card number",
                                     min_length=16,
                                     max_length=16),
        cardholder: str = Body(...,
                               alias="cardholder",
                               description="CardHolder is the name of the holder"),
        securitycode: str = Body(...,
                                 alias="securitycode",
                                 description="Security code is the CVC code of the card",
                                 min_length=3,
                                 max_length=3),
        amount: float = Body(...,
                             alias="amount",
                             description="The amount field must be better than 0",
                             gt=0),
        expirationdate: Optional[str] = Body(...,
                                             alias="expirationdate",
                                             description="ExpirationDate is the expiration date of the card")
):
    ctrl_amount = ControlAmount()
    ctrl_datetime = ControlDatetime()
    current_date = str(datetime.date.today())
    inputs = {
        "creditcardnumber": creditcardnumber,
        "cardholder": cardholder,
        "expirationdate": expirationdate,
        "securitycode": securitycode,
        "amount": amount,
        "message_amount": ctrl_amount(amount),
        "message_date": ctrl_datetime(current_date, expirationdate)
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(inputs))
