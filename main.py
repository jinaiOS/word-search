from fastapi import FastAPI, UploadFile, Form, Depends
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from pydantic import BaseModel
from typing import Annotated
import hashlib
import sqlite3

import sqlite3

con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()

cur.execute(f"""
            CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            score INTEGER DEFAULT 0
            );
            """)

app = FastAPI()

SECRET = "jina-key"
manager = LoginManager(SECRET,'/login')

@manager.user_loader()
def query_user(data):
    WHERE_STATEMENTS = f'''id="{data}"'''
    if type(data) == dict:
        WHERE_STATEMENTS = f'''id="{data['id']}"'''
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    user = cur.execute(f"""
                       SELECT * from users WHERE {WHERE_STATEMENTS}
                       """).fetchone()
    return user

@app.post('/login')
def login(id:Annotated[str,Form()], 
           password:Annotated[str,Form()]):
    user = query_user(id)
    hashPassword = hashlib.sha256(password.encode()).hexdigest()
    if not user:
        raise InvalidCredentialsException
    elif hashPassword != user['password']:
        raise InvalidCredentialsException
    
    access_token = manager.create_access_token(data={
        'sub': {
            'id': user['id'],
            'score': user['score']
        }
    })
    
    return {'access_token':access_token}

@app.post('/signup')
def signup(id:Annotated[str,Form()], 
           password:Annotated[str,Form()]):
    hashPassword = hashlib.sha256(password.encode()).hexdigest()
    cur.execute(f"""
                INSERT INTO users(id,password)
                VALUES ('{id}','{hashPassword}')
                """)
    con.commit()
    return '200'

@app.get('/profile')
def get_profile(user=Depends(manager)):
    return {
        "id": user['id'],
        "score": user['score']
    }

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")