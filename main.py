from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
from jose import JWTError, jwt
from datetime import datetime, timedelta
import mysql.connector
from conexion.conexion import conn
from modulos.schema import Usuario, Token

SECRET_KEY = "DI@n@P@diII@280319#%"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 50

app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(username: str, password: str):
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE usuario = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    if user and user['password'] == password:
        return user
    return None

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["usuario"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
