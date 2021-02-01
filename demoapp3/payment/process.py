from typing import Optional

from fastapi import APIRouter, status, Body, Request, Query
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder

from .process_controller import RequestExternalApiControllingAmount, ControlDatetime

import datetime

router = APIRouter(
    prefix="/paymentprocess",
    tags=["tag-paymentprocess"]
)


@router.post(
    "",
    responses={
        200: {"message": "Payment is redirected"},
        400: {"message": "The request is invalid"},
        404: {"message": "Not found"},
        406: {"message": "Not acceptable"},
        500: {"message": "Any error"}
    }
)
async def payment_process(
        request: Request,
        creditcardnumber: str = Query(...,
                                      alias="creditcardnumber",
                                      description="CreditCardNumber is the credit card number.",
                                      min_length=16,
                                      max_length=16),
        cardholder: str = Query(...,
                                alias="cardholder",
                                description="CardHolder is the name of the holder."),
        securitycode: str = Query(...,
                                  alias="securitycode",
                                  description="Security code is the CVC code of the card."
                                              "Need to be 3 digits.",
                                  min_length=3,
                                  max_length=3),
        amount: float = Query(...,
                              alias="amount",
                              description="The amount field must be better than 0.",
                              gt=0),
        expirationdate: Optional[str] = Query(...,
                                              alias="expirationdate",
                                              description="ExpirationDate is the expiration date of the card."
                                                          "Cannot be in the past.")
):
    # Initialize controllers
    ctrl_amount_extapi_result = RequestExternalApiControllingAmount()
    ctrl_datetime = ControlDatetime()

    # Get request datetime
    params = request.query_params
    print(f'ProcessPayment activated {str(params)}')

    # First control -> datetime
    ret_date = ctrl_datetime(str(datetime.date.today()), str(expirationdate))

    if ret_date:
        # Second control -> amount & payment gateway
        ret_amount = ctrl_amount_extapi_result(creditcardnumber, cardholder, securitycode, amount, expirationdate, params)
        response = {
            "creditcardnumber": creditcardnumber,
            "cardholder": cardholder,
            "expirationdate": expirationdate,
            "securitycode": securitycode,
            "amount": amount,
            "message_date": ret_date,
            "message_external_api": ret_amount
        }
        return JSONResponse(status_code=int(ret_amount['status']), content=jsonable_encoder(response))
    else:
        response = {
            "creditcardnumber": creditcardnumber,
            "cardholder": cardholder,
            "expirationdate": expirationdate,
            "securitycode": securitycode,
            "amount": amount,
            "message_date": ret_date
        }
        return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE, content=jsonable_encoder(response))
