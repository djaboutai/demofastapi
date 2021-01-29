from fastapi import APIRouter, status, Request, Form
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/", summary="Get admin name")
async def get_admin():
    response = jsonable_encoder({"message": "Admin getting zigiiprens"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)


@router.get("/redirect", summary="Redirect to admin root path")
async def get_admin_redirect(request: Request):
    client_host = request.client.host
    client_port = request.client.port
    client_query = request.query_params
    print(f'Request host params, data-host:{client_host} data-port:{client_port}')
    print(f'Request query params, data:{client_query.get("token")} type:{type(client_query)} len:{len(client_query)}')
    return RedirectResponse(url=f"/admin/?{client_query}")


@router.post("/login", summary="Login form for admin")
async def post_admin_login(request: Request, username: str = Form(...), password: str = Form(...)):
    client_host = request.client.host
    client_port = request.client.port
    client_query = request.query_params
    print(f'Request host params, data-host:{client_host} data-port:{client_port}')
    print(f'Request query params, data:{client_query.get("token")}')

    response = jsonable_encoder({"username": username, "password": password})
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)
