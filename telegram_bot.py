from aiogram import Bot, Dispatcher, executor, types
from text_recognition import text_recognition

import config


bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
#Welcome message
async def start_command(msg: types.Message):
    await msg.answer("Hello!\nHow can I help you today?")

@dp.message_handler(commands=["help"])
#Bot functional description
async def help_command(msg: types.Message):
    await msg.answer("This bot gives the answers to tasks "
                         "using GPT chat. Just send a photo with "
                         "your task to recognize text.")

@dp.message_handler(content_types=["photo"])
#Photo from user call the function to recognize text
async def photo_handler(msg: types.Message):
    file_id = msg.photo[-1].file_id
    photo = await bot.get_file(file_id)
    photo_path = "photos/%s.jpg" % (file_id)
    await photo.download(destination_file=photo_path)
    recognized_text = text_recognition(photo_path)
    await msg.answer(recognized_text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

