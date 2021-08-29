#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/8/27 23:53 
# @Author : SuperYong 
# @File : chapter04.py
# @summary :

from fastapi import APIRouter
from typing import List, Optional, Union
from pydantic import BaseModel, EmailStr

app04 = APIRouter()

'''响应模型'''


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    mobile: str = '100086'
    address: str = None
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    mobile: str = '100086'
    address: str = None
    full_name: Optional[str] = None


users = {
    'user01': {'username': 'yyy', 'password': '123', 'email': '111@163.com',
               'address': 'asdadasd', 'full_name': 'yanghaowen'},
    'user02': {'username': 'www', 'password': '123', 'email': '222@163.com',
               'address': 'xczxczx', 'full_name': 'yanghaoxuan'},
}


@app04.post('/response_model', response_model=UserOut, response_model_exclude_unset=True)
async def response_model(user: UserIn):
    print(user.password)
    return users['user01']


@app04.post('/response_model/attributes', response_model=Union[UserOut, UserIn])
async def response_model_attributes(user: UserIn):
    return user
