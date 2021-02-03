from fastapi import FastAPI

from payment import process

import uvicorn

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

if __name__ == "__main__":
    uvicorn.run("myapp:app", host="0.0.0.0", port=8888, reload=True)
