from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel


class Message(BaseModel):
    user_id: str
    user_text: str
    message_from_bot: Optional[str] = None
    stage: Optional[int] = None


YES = ['да', 'конечно', 'ага', 'пожалуй', 'йеп', 'угу']
NO = ['нет', 'нет, конечно', 'ноуп', 'найн', 'не-а', 'фиг там']

app = FastAPI()


@app.get('/')
async def root():
    return {"message_from_bot": "Отправьте /start для начала диалога"}


@app.post('/')
async def message_from_user(message: Message):
    message_dict = message.dict()
    if message.user_text.lower() == '/start':
        message_dict.update({'message_from_bot': 'Привет! Я помогу отличить кота от хлеба! '
                                                 'Объект перед тобой квадратный?',
                             'stage': 1})
        return message_dict
    elif message.stage == 1:
        if message.user_text.lower() in YES:
            message_dict.update({'message_from_bot': 'У него есть уши?',
                                 'stage': 2})
            return message_dict
        elif message.user_text.lower() in NO:
            message_dict.update({'message_from_bot': 'Это кот, а не хлеб! Не ешь его!',
                                 'stage': 0})
            return message_dict
    elif message.stage == 2:
        if message.user_text.lower() in YES:
            message_dict.update({'message_from_bot': 'Это кот, а не хлеб! Не ешь его!',
                                 'stage': 0})
            return message_dict
        elif message.user_text.lower() in NO:
            message_dict.update({'message_from_bot': 'Это хлеб, а не кот! Ешь его!',
                                 'stage': 0})
            return message_dict
    else:
        message_dict.update({'message_from_bot': 'Я вас не понимаю, ответьте да или нет на последний вопрос '
                                                 'или /start для начала диалога'})
        return message_dict

