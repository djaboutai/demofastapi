from fastapi import Header, status
from fastapi.responses import JSONResponse


# Token header controller
async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        invalid_x_token = "X-Token header invalid"
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=invalid_x_token)


# Token query controller
async def get_query_token(token: str):
    if token != "jessica":
        invalid_token = "No Jessica token provided"
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=invalid_token)
