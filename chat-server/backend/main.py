from fastapi import FastAPI
from langchain.llms import OpenAI
from langchain.chat_models.openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from app.api.titanic.model.titanic_model import TitanicModel
from app.main_router import router


class Request(BaseModel):
    question: str

class Response(BaseModel):
    answer: str

app = FastAPI()

app.include_router(router, prefix="/api")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

@app.get("/")
def read_root():
    return {"Hello":"World"}


origins = [
   "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    question: str


llm = OpenAI(openai_api_key="...")



#@app.post("/chat")
def chatting(req:Request):
    print('딕셔너리 내용')
    print(req)

    #객체 생성
    chat_model = ChatOpenAI(
        openai_api_key=os.environ["API_KEY"],
        temperature=0.1,                   #창의성 (0.0 ~ 2.0 )
        max_tokens=2048,                 #최대 토큰수
        model_name='gpt-3.5-turbo-0613' #모델명
        )
    # 질의내용
    #question = '대한민국의 수도는 뭐야?'
    
    #질의
   # print(f'[답변]: {chat_model.predict(question)}')
   
   # message = [
   #    SystemMessage(content=""" You are a traveler. I know the capitals of every country in the world.""",type="system"),
   #    HumanMessage(content="한국의 수도는 어디야?",type="human"),
   #    AIMessage(content= "서울 입니다", type="ai")
   # 
   #    
   # ]
    #print(chat_model.predict_messages(message))


   
    return Response(answer=chat_model.predict(req.question))

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
