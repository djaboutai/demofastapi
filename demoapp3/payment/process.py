import datetime
from typing import Optional

from fastapi import APIRouter, status, Request, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .process_controller import RequestExternalApiControllingAmount, ControlDatetime


router = APIRouter(
    prefix="/paymentprocess",
    tags=["tag-paymentprocess"]
)

# Initialize controllers
ctrl_amount_external_api_result = RequestExternalApiControllingAmount()
ctrl_datetime = ControlDatetime()


@router.get(
    "",
    responses={
        200: {"message": "Payment is accepted"},
        400: {"message": "The request is invalid"},
        404: {"message": "Not found"},
        406: {"message": "Not acceptable, expiration date of card in the past"},
        500: {"message": "Any internal error"}
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
    """

    :param request: The request captured by router. \n
    :param creditcardnumber: The request first query given as string. \n
    :param cardholder: The request second query given as string. \n
    :param securitycode: The request third query given as string. \n
    :param amount: The request fourth query given as float. \n
    :param expirationdate: The request fifth query given as string. \n
    :return: Return JSONResponse with information related to the request. \n
    """
    # Get request queries
    params = request.query_params

    # First control -> datetime
    ret_date = ctrl_datetime(str(datetime.date.today()), str(expirationdate))

    if ret_date:
        # Second control -> amount & payment gateway
        ret_external_api = ctrl_amount_external_api_result(creditcardnumber, cardholder, securitycode,
                                                           amount, expirationdate, str(params))
        response = {
            "creditcardnumber": creditcardnumber,
            "cardholder": cardholder,
            "expirationdate": expirationdate,
            "securitycode": securitycode,
            "amount": amount,
            "message_date": ret_date,
            "message_external_api": ret_external_api
        }
        return JSONResponse(status_code=ret_external_api['status'], content=jsonable_encoder(response))
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
