from typing import Optional, Callable
from fastapi import FastAPI
from pydantic import BaseModel
from .dbconnector import Database
import functools


class Message(BaseModel):
    user_id: str
    user_text: str
    message_from_bot: Optional[str] = None
    stage: Optional[int] = None


YES = ['да', 'конечно', 'ага', 'пожалуй', 'йеп', 'угу']
NO = ['нет', 'нет, конечно', 'ноуп', 'найн', 'не-а', 'фиг там']

app = FastAPI()


def db_logger(func: Callable) -> Callable:
    """
    Decorator which will log every request and answer to DB
    :param func: Callable
    :return: Callable
    """

    @functools.wraps(func)
    async def wrapped_func(message: Message):
        db = Database('history.db')
        db.add(message.user_id, 'REQUEST', message.user_text, str(message.dict()))  # logging users request
        result: dict = await func(message)
        db.add(result['user_id'], 'ANSWER', result['message_from_bot'], str(result))  # logging our answer
        return result
    return wrapped_func


@app.get('/')
@db_logger
async def root(message: Message = Message(user_id='unknown user', user_text='Hello')):
    """
    Default GET endpoint, to be tested from browser
    :param message:
    :return:
    """
    message_dict = message.dict()
    message_dict.update({"message_from_bot": "Отправьте /start для начала диалога"})
    return message_dict


@app.post('/')
@db_logger
async def message_from_user(message: Message):
    """
    Main POST endpoint to receive answers from user
    :param message:
    :return:
    """
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

