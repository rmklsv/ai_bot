from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message

import config


bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
#Bot description
async def start_command(message: types.Message):
    await message.answer('This bot gives the answers to tasks '
                         'using GPT chat. Just send a photo with '
                         'your task to recognize text.')

@dp.message_handler(content_types=['photo'])
#Photo from user call the function to recognize text
async def photo_handler(message: Message):
    recognized_text = recognize_text(message.photo)
    await message.answer(recognized_text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

