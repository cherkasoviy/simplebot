from unittest import IsolatedAsyncioTestCase, main
from main import Message, YES, NO, root, message_from_user

empty_message = Message(user_id='31337', user_text='Hello')

smth_wrong_answer = 'Я вас не понимаю, ответьте да или нет на последний вопрос или /start для начала диалога'


class MyTestCase(IsolatedAsyncioTestCase):
    async def test_root(self):  # testing default route function
        result = await root()
        self.assertEqual(result, {"message_from_bot": "Отправьте /start для начала диалога"})

    async def test_message_from_user(self):  # tests for main endpoint
        result = await message_from_user(empty_message)
        self.assertEqual(result['message_from_bot'], smth_wrong_answer, msg='Wrong JSON body or user_text test failed')


if __name__ == '__main__':
    main()
