from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel


class Message(BaseModel):
    user_id: str
    user_text: str


app = FastAPI()


@app.get('/')
async def root():
    return {"message": "Hello World"}


@app.post('/')
async def message_from_user(message: Message):
    if message.user_text.lower() == '/start':
        message_dict = message.dict()
        message_dict.update({'message_from_bot': 'Привет! Я помогу отличить кота от хлеба! '
                                                 'Объект перед тобой квадратный?',
                             'stage': 1})
        return message_dict
