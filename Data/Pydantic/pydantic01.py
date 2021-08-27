#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/8/27 21:34 
# @Author : SuperYong 
# @File : pydantic01.py
# @summary :

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class User(BaseModel):
    id: int  # 必填类型
    name: str = 'John'  # 选填类型
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


external_data = {
    'id': '123',
    'signup_ts': '2021-08-27 12:22',
    'friends': [1, 2, 3]
}

user = User(**external_data)
print(user)
print(user.id, user.name)
print(repr(user.signup_ts))
print(user.dict())
print(user.json())

print(User.parse_obj(obj=external_data))
print(User.parse_raw('{"id": "123","signup_ts": "2021-08-27 12:22","friends": [1, 2, 3]}'))
# print(User.parse_file(file_path))

print(user.schema())
print(user.schema_json())

# print(User.from_orm(orm_model))
