import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from deep_translator import GoogleTranslator
import requests

from config import TOKEN, THE_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

class Form(StatesGroup):
    waiting_for_text = State()
    waiting_for_translation = State()

def get_fox_types():
    url = 'https://api.api-ninjas.com/v1/animals?name=fox'
    headers = {'X-Api-Key': THE_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

def get_type_info(type_name):
    types = get_fox_types()
    for type in types:
        if type['name'].lower() == type_name.lower():
            return type
    return None

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет я бот помощник! Напиши мне название типа лисицы и я пришлю информацию о ней.')

@dp.message(lambda message: True)
async def send_fox_info(message: Message):
    type_name = message.text
    type_info = get_type_info(type_name)
    if type_info:
        info_text = (f"Тип - {type_info['name']}\n"
                    f"Описание - {type_info['characteristics']}")
        await message.answer(info_text)
    else:
        await message.answer('Тип не найден. Попробуйте ещё раз.')

@dp.message(Form.waiting_for_translation)
async def handle_translation(message:Message, state: FSMContext):
    text_to_translate = message.text
    translator = GoogleTranslator(sourse='auto', target='en')
    translated_text = translator.translate(text_to_translate)


async def main():
    await dp.start_polling(bot)


if __name__=="__main__":
    asyncio.run(main())