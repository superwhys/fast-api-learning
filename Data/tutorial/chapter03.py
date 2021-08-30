#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/8/27 23:53 
# @Author : SuperYong 
# @File : chapter03.py
# @summary :

from enum import Enum
from datetime import date
from typing import Optional, List
from fastapi import APIRouter, Cookie, Header

'''
使用pydantic定义请求体数据的时候
对字段进行校验使用Field类
对路径参数进行校验使用Path类
对查询参数进行校验使用Query类
'''
from fastapi import Path, Query
from pydantic import BaseModel, Field

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


'''请求体和混合参数的使用'''
'''请求参数和字段'''


class CityInfo(BaseModel):
    name: str = Field(..., example='BeiJing')
    country: str
    country_code: str = None
    country_population: int = Field(default=800, title='人口数量', description='国家的人口数量')

    class Config:
        # 示例 在localhost:8000/docs上的端口文档可以看到示例
        schema_extra = {
            'example': {
                'name': 'ShangHai',
                'country': 'Chain',
                'country_code': 'CN',
                'country_population': 1400000000
            }
        }


@app03.post('/request_body/city')
def city_info(city: CityInfo):
    print(city.name, city.country)
    return city.dict()


'''请求体 路径参数 查询参数 多参数混合'''


@app03.put('/request_body/city/{name}')
def mix_city_info(
        name: str,
        city01: CityInfo,
        city02: CityInfo,  # body可以定义多个
        confirmed: int = Query(ge=0, description='确诊数', default=0),
        death: int = Query(ge=0, description='死亡数', default=0)
):
    if name == 'Shanghai':
        return {'Shanghai': {'confirmed': confirmed, 'death': death}}
    return city01.dict(), city02.dict()


'''数据格式嵌套的请求体'''


class Data(BaseModel):
    city: List[CityInfo] = None
    date: date
    confirmed: int = Query(ge=0, description='确诊数', default=0)
    death: int = Query(ge=0, description='死亡数', default=0)
    recovered: int = Field(ge=0, description='痊愈数', default=0)


@app03.put('/request_body/nested')
def nested_models(data: Data):
    return data.json()


'''Cookie 和 Header参数'''


@app03.get('/cookie')
def cookie(cookie_id: Optional[str] = Cookie(None)):
    return {'cookie_id': cookie_id}


@app03.get('/header')
def header(user_agent: Optional[str] = Header(None, convert_underscores=True), x_token: List[str] = Header(None)):
    # convert_underscores 自动转换下划线
    # user_agent -> user-agent
    return {'User-Agent': user_agent, 'x_token': x_token}

