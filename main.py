from typing import Union
from script import process_data, get_database
from fastapi import FastAPI
from dotenv import load_dotenv
from os import getenv
from starlette.middleware.cors import CORSMiddleware
import uvicorn

load_dotenv()


token = getenv("TOKEN_ID")
database_id = getenv("DATABASE_ID")


def start():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_headers=['*'],
        allow_methods=['*'],
        allow_origins=['*'],
    )

    @app.get("/")
    async def homepage():
        return {"Hello": "World"}

    @app.post("/")
    async def check_for_link():
        print("Running the script...")
        data = get_database(database_id)
        process_data(data)
        return "Success!"
    return app


application = start()
if __name__ == "__main__":
    uvicorn.run("main:application", host="0.0.0.0", port=8000, reload=True)
