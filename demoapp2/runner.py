import uvicorn

# Problem here
from myapp import app

# TODO: The import myapp does not work well, this need a review
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
