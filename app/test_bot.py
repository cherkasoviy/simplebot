from unittest import IsolatedAsyncioTestCase, main
from main import Message, YES, NO, root, message_from_user

# Test messages
empty_message = Message(user_id='31337', user_text='Hello')
stage_1_message = Message(user_id='31337', user_text='', stage=1)
stage_2_message = Message(user_id='31337', user_text='', stage=2)


# Expected answers
smth_wrong_answer = 'Я вас не понимаю, ответьте да или нет на последний вопрос или /start для начала диалога'
initial_answer = 'Привет! Я помогу отличить кота от хлеба! Объект перед тобой квадратный?'
stage_1_yes_answer = 'У него есть уши?'
stage_1_no_answer = 'Это кот, а не хлеб! Не ешь его!'
stage_2_yes_answer = 'Это кот, а не хлеб! Не ешь его!'
stage_2_no_answer = 'Это хлеб, а не кот! Ешь его!'


class MyTestCase(IsolatedAsyncioTestCase):
    async def test_root(self):  # testing default route function
        result = await root()
        self.assertEqual(result, {"message_from_bot": "Отправьте /start для начала диалога"})

    async def test_message_from_user(self):  # tests for main endpoint with wrong(unexpected) input from user
        result = await message_from_user(empty_message)
        self.assertEqual(result['message_from_bot'], smth_wrong_answer, msg='Wrong JSON body or user_text test failed')

    async def test_start_message(self):  # test for initialising the bot with /start
        empty_message.user_text = '/start'
        result = await message_from_user(empty_message)
        self.assertEqual(result['message_from_bot'], initial_answer)

    async def test_stage_1_yes(self):  # Test for yes messages from user for first question
        for answer in YES:
            stage_1_message.user_text = answer
            result = await message_from_user(stage_1_message)
            self.assertEqual(result['message_from_bot'], stage_1_yes_answer)  # checking for next stage question
            self.assertEqual(result['stage'], 2)  # checking for next stage number

    async def test_stage_1_no(self):  # Test for no messages from user for first question
        for answer in NO:
            stage_1_message.user_text = answer
            result = await message_from_user(stage_1_message)
            self.assertEqual(result['message_from_bot'], stage_1_no_answer)  # checking for next stage question
            self.assertEqual(result['stage'], 0)  # checking for next stage number

    async def test_stage_2_yes(self):  # Test for yes messages from user for second question
        for answer in YES:
            stage_2_message.user_text = answer
            result = await message_from_user(stage_2_message)
            self.assertEqual(result['message_from_bot'], stage_2_yes_answer)  # checking for next stage question
            self.assertEqual(result['stage'], 0)  # checking for next stage number

    async def test_stage_2_no(self):  # Test for no messages from user for second question
        for answer in NO:
            stage_2_message.user_text = answer
            result = await message_from_user(stage_2_message)
            self.assertEqual(result['message_from_bot'], stage_2_no_answer)  # checking for next stage question
            self.assertEqual(result['stage'], 0)  # checking for next stage number


if __name__ == '__main__':
    main()
