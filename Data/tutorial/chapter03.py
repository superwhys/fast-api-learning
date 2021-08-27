#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/8/27 23:53 
# @Author : SuperYong 
# @File : chapter03.py
# @summary :

from enum import Enum
from typing import Optional, List
from fastapi import APIRouter
from fastapi import Path, Query

app03 = APIRouter()

'''路劲参数和数字的验证'''


@app03.get('path/parameters')
def path_params01():
    return {'message': 'This is a message'}


@app03.get('path/{parameters}')
def path_params01(parameters: str):
    return {'message': parameters}


'''
枚举类型
'''


class CityName(str, Enum):
    Beijing = "Beijing China"
    Shanghai = "Shanghai China"


@app03.get('/enum/{city')
async def latest(city: CityName):
    if city == CityName.Shanghai:
        return {'city_name': city, 'confirmed': 1492, 'death': 7}
    if city == CityName.Beijing:
        return {'city_name': city, 'confirmed': 971, 'death': 9}
    return {'city_name': 'unknown'}


# 文件路劲
@app03.get('/files/{file_path:path}')
def filepath(file_path: str):
    return f'the file path is {file_path}'


# 长度和正则表达式
@app03.get('/path/{num}')
def path_params_validate(num: int = Path(None, title='Your number', ge=1, le=10)):
    return num


'''查询参数和字符串验证'''


@app03.get('/query')
def page_limit(page: int = 1, limit: Optional[int] = None):
    if limit:
        return {'page': page, 'limit': limit}
    return {'page': page}


@app03.get('/query/bool/conversion')
def type_conversion(param: bool = False):
    return param


@app03.get('/query/validations')
def query_params_validate(value: str = Query(...,
                                             min_length=8,
                                             max_length=16,
                                             regex='^a'),
                          values: List[str] = Query(default=['v1', 'v2'], alias='alias_name')):
    return value, values
