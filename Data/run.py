#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/8/27 23:53 
# @Author : SuperYong 
# @File : run.py
# @summary : FastApi run

import uvicorn
from fastapi import FastAPI
from tutorial import app03, app04, app05

app = FastAPI()
app.include_router(app03, prefix='/chapter03', tags=['请求参数和验证'])
app.include_router(app04, prefix='/chapter04', tags=['相应处理和FastAPI配置'])
app.include_router(app05, prefix='/chapter05', tags=['FastAPI的依赖注入系统'])

if __name__ == '__main__':
    uvicorn.run('run:app', host='0.0.0.0', port=8000, reload=True, debug=True, workers=1)

'''
/
/coronavirus
/tutorial
'''
