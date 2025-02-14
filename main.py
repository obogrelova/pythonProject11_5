import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
import requests

from config import TOKEN, THE_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()


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
    await message.answer('Привет я бот помощник! Напиши мне название лисицы и я пришлю информацию о ней.')

@dp.message(lambda message: True)
async def send_fox_info(message: Message):
    type_name = message.text
    type_info = get_type_info(type_name)
    if type_info:
        info_text = (f"Название - {type_info['name']}\n"
                     f"Описание - {type_info['characteristics']}")
        await message.answer(info_text)
    else:
        await message.answer('Тип не найден. Попробуйте ещё раз.')


async def main():
    await dp.start_polling(bot)


if __name__=="__main__":
    asyncio.run(main())