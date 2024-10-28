import jwt
from script import process_data, get_database
from fastapi import Depends, FastAPI, HTTPException, status
from dotenv import load_dotenv
from os import getenv
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from pydantic import BaseModel
from passlib.hash import bcrypt

load_dotenv()


PORT = int(getenv("PORT"))
JWT_SECRET = getenv("JWT_SECRET")
URI = getenv("DB_URI")

client = AsyncIOMotorClient(URI)
db = client.get_default_database("test")
collection = client.test.users
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


class User(BaseModel):
    id: int
    username: str
    password_hash: str

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    @classmethod
    async def get(self, username=None, id=None):
        user = None
        if username != None:
            user = await collection.find_one({"username": username})
        if id != None:
            user = await collection.find_one({"id": id})
        if user:
            del user['_id']
        return user


def start():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_headers=['*'],
        allow_methods=['*'],
        allow_origins=['*'],
    )

    async def authenticate_user(username: str, password: str):
        tmp = await User.get(username=username)
        if not tmp:
            return False
        user = User(**tmp)
        if not user.verify_password(password):
            return False
        return user

    @app.post("/token")
    async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
        user = await authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Username or Password")
        token = jwt.encode(user.model_dump(), JWT_SECRET)

        return {'access_token': token, 'token_type': 'bearer'}

    @app.post('/users')
    async def create_user(user: User):
        data = user.model_dump()
        data["password_hash"] = bcrypt.hash(data['password_hash'])
        tmp = await User.get(username=data['username'])
        if tmp:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists!")

        user_obj = User(**data)
        await collection.insert_one(data)
        return HTTPException(status_code=status.HTTP_200_OK, detail="User Successfully Created!")

    async def get_current_user(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            user = await User.get(id=payload["id"])
        except:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password'
            )

        return user

    @app.get('/users/me', response_model=User)
    async def get_user(user: User = Depends(get_current_user)):
        return user

    @app.get("/")
    async def homepage():
        return {"Hello": "World"}

    @app.post("/")
    async def check_for_link(User = Depends(get_current_user)):
        print("Running the script...")
        data = get_database()
        process_data(data)
        return "Success!"
    return app


application = start()
if __name__ == "__main__":
    uvicorn.run("main:application", host="0.0.0.0", port=PORT, reload=True)
