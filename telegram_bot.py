import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Voice
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from text_recognition import text_recognition
from openai_api import api_request, speech_to_text

import config

class StatesGroup(StatesGroup):
    photo = State()
    reply = State()



storage = MemoryStorage()
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)


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
async def photo_handler(msg: types.Message, state: FSMContext):
    await StatesGroup.photo.set()
    file_id = msg.photo[-1].file_id
    photo = await bot.get_file(file_id)
    photo_path = "photos/%s.jpg" % (file_id)
    await msg.answer("Please wait\n"
                     "Recognizing the text...")
    await photo.download(destination_file=photo_path)
    recognized_text = text_recognition(photo_path)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Yes, send", callback_data="Yes")
        ],
        [
            InlineKeyboardButton(text="No, edit", callback_data="No")
        ]
    ])
    await bot.send_message(chat_id=msg.chat.id,
                           text="This is your text?\n"
                           + recognized_text,
                           reply_markup=keyboard)
    await StatesGroup.next()
    
    

@dp.callback_query_handler(lambda c: True, state=StatesGroup.reply)
async def process_callback_button(callback_query: CallbackQuery, state: FSMContext):
    # Check which button was pressed by looking at the callback_data
    if callback_query.data == "Yes":
        api_response = api_request(callback_query.message.text)
        #await bot.send_message(chat_id=callback_query.message.chat.id, text="Please wait\nYour request is being processed...")
        await bot.send_message(chat_id=callback_query.message.chat.id,
                               text=api_response)
    elif callback_query.data == "No":
        # Copy the recognized text to user buffer
        await bot.send_message(chat_id=callback_query.message.chat.id, 
                               text="Please, copy and edit this text, and then send it to me:")
        await bot.send_message(chat_id=callback_query.message.chat.id,
                               text="```"+callback_query.message.text[18:]+"```",
                               parse_mode='MarkdownV2')
    # Answer the callback query to remove the "pending" status of the button press
    await bot.answer_callback_query(callback_query.id)
    await state.finish()


@dp.message_handler(content_types="text")
#Sent API request with text from user to OpenAI
async def text_handler(msg: types.Message):
    api_response = api_request(msg.text)
    await msg.answer(api_response)

@dp.message_handler(content_types="voice")
async def handle_voice_message(msg: types.Message):
    # Get the voice message from the message object
    voice_message: Voice = msg.voice
    audio_id = voice_message.file_id
    audio = await bot.get_file(audio_id)
    audio_path = "audio/%s.webm" % (audio_id)
    await audio.download(destination_file=audio_path)
    api_response = speech_to_text(audio_path)
    await msg.answer(api_response)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
