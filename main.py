import uvicorn
from fastapi import FastAPI
# Local imports
from constants.general import General

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    if General.RELEASE.value:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        app.debug = True
        uvicorn.run(app, host="127.0.0.1", port=5000)