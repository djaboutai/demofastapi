from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("/")
async def get_root():
    """
    :param: none.
    :return: json response.
    """
    response = jsonable_encoder({"message": "Hello demo app from zigiiprens!"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)
