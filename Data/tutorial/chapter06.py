#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/8/27 23:53 
# @Author : SuperYong 
# @File : chapter06.py
# @summary :
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app06 = APIRouter()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/chapter06/token")  # 请求Token的URL地址 http://127.0.0.1:8000/chapter06/token


@app06.get("/oauth2_password_bearer")
async def oauth2_password_bearer(token: str = Depends(oauth2_schema)):
    return {'token': token}


'''基于 password 和 bearer token 的 OAuth2 认证'''

fake_users_db = {
    "john snow": {
        "username": "john snow",
        "full_name": "John Snow",
        "email": "johnsnow@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


def fake_hash_password(password: str):
    return 'fakehashed' + password


class User(BaseModel):
    username: str
    email: Optional[str] = None
    fullname: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


def fake_decode_token(token: str):
    user = get_user(fake_users_db, token)
    return user


@app06.post('/token')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400,
                            detail='Incorrect Username or password')
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400)
    return {'access_token': user.username, 'type': 'bearer'}


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def get_current_user(token: str = Depends(oauth2_schema)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(status_code=401,
                            detail='invalid authentication credentials')
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400,
                            detail='inactivate user')
    return current_user


@app06.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


"""基于JSON Web Tokens的认证"""

from passlib.context import CryptContext
from datetime import datetime, time, timedelta
from jose import JWTError, jwt

fake_users_db.update({
    "john snow": {
        "username": "john snow",
        "full_name": "John Snow",
        "email": "johnsnow@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
})

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # 生成密钥 openssl rand -hex 32
ALGORITHM = "HS256"  # 算法
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 访问令牌过期分钟


class Token(BaseModel):
    '''返回给用户的token'''
    access_token: str
    token_type: str


# schemes 加密算法
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/chapter06/jwt/token")


def verify_password(plain_password: str, hashed_password: str):
    """对密码进行校验  True or False"""
    print(f'{plain_password}:{hashed_password}')
    return pwd_context.verify(plain_password, hashed_password)


def jwt_get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def jwt_authenticate_user(db, username: str, password: str):
    user = jwt_get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def created_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY,
                             algorithm=ALGORITHM)
    return encoded_jwt


@app06.post('/jwt/token', response_model=Token)
async def login_jwt(form_data: OAuth2PasswordRequestForm = Depends()):
    print('111')
    user = jwt_authenticate_user(db=fake_users_db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400,
                            detail='Incorrect username or password')
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = created_access_token(data={'sub': user.username}, expires_delta=access_token_expires)
    return {'access_token': access_token,
            'token_type': 'bearer'}


async def jwt_get_current_user(token: str = Depends(oauth2_schema)):
    print(f'2: {token}')
    credentials_exception = HTTPException(
        status_code=401,
        detail='could not validate credentials'
    )
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        print(username)
        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = jwt_get_user(fake_users_db, username)
    if user is None:
        raise credentials_exception
    return user


async def jwt_get_current_active_user(current_user: User = Depends(jwt_get_current_user)):
    print('1: ', current_user)
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='inactive user')
    print(current_user)
    return current_user


@app06.get("/jwt/users/me")
async def jwt_read_users_me(current_user: User = Depends(jwt_get_current_active_user)):
    return current_user
