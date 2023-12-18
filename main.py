import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
# Local imports
from constants.general import General
from routes import authentication, passwords

# Local .env
load_dotenv('.env')

origins = [
    'http://127.0.0.1:3000', 'http://localhost:3000'
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,
)

app.include_router(authentication.router)
app.include_router(passwords.router)

def run_server():
    if General.RELEASE.value:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        app.debug = True
        uvicorn.run(app, host="127.0.0.1", port=5000)

if __name__ == "__main__":
    run_server()