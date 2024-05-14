from fastapi import APIRouter
from pydantic import BaseModel

from app.api.titanic.service.titanic_service import TitanicService


router = APIRouter()

class Request(BaseModel):
    question: str

class Response(BaseModel):
    answer: str

service = TitanicService()

@router.post('/titanic')
async def titanic(req:Request):
    print('타이타닉 딕셔너리 내용')
    hello = 'C:\\Users\\bitcamp\\python-kube\\chat-server\\backend\\app\\api\\titanic\\data\\hello.txt'
    f = open(hello, "r", encoding="utf-8")
    data = f.read()
    print(data)
    f.close()

    # service.process()

    print(req)
    return Response(answer = "생존자는 100명이야")