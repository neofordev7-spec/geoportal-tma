import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
)

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
NGROK_URL = os.getenv('NGROK_URL', 'http://localhost:8000')

logging.basicConfig(level=logging.INFO, format='%(asctime)s — %(levelname)s — %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

XUSH_KELIBSIZ = """
Assalomu alaykum! 👋

*GEOPORTAL* — O'zbekiston infratuzilmasi monitoringi platformasiga xush kelibsiz.

Bu yerda siz:
• Singan maktab, shifoxona, yo'l, bog'cha haqida xabar berishingiz
• Barcha murojaatlarni kuzatishingiz
• Respublika bo'yicha statistikani ko'rishingiz mumkin.

Quyidagi tugmani bosib, ilovani oching 👇
"""


@dp.message(CommandStart())
async def start_handler(message: Message):
    webapp_url = f"{NGROK_URL}/tma/"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🌍 GEOPORTAL ochish",
                web_app=WebAppInfo(url=webapp_url)
            )
        ],
        [
            InlineKeyboardButton(
                text="📋 Mening murojaatlarim",
                web_app=WebAppInfo(url=webapp_url)
            )
        ]
    ])

    await message.answer(
        XUSH_KELIBSIZ,
        parse_mode='Markdown',
        reply_markup=keyboard
    )
    logger.info(f"User {message.from_user.id} (@{message.from_user.username}) started bot")


@dp.message(F.web_app_data)
async def web_app_data_handler(message: Message):
    """Mini App dan kelgan ma'lumotni qayta ishlash"""
    import json
    import aiohttp

    try:
        data = json.loads(message.web_app_data.data)
        logger.info(f"WebApp data received from {message.from_user.id}: {data}")

        async with aiohttp.ClientSession() as session:
            payload = {
                **data,
                'telegram_user_id': message.from_user.id,
                'telegram_username': message.from_user.username or '',
                'telegram_full_name': message.from_user.full_name or '',
            }
            async with session.post(
                f"{NGROK_URL}/api/murojaat/",
                json=payload
            ) as resp:
                result = await resp.json()
                if resp.status == 201:
                    await message.answer(
                        f"✅ Murojaatingiz qabul qilindi!\n"
                        f"ID: #{result.get('id')}\n"
                        f"24 soat ichida ko'rib chiqiladi."
                    )
                else:
                    await message.answer("❌ Xatolik yuz berdi. Qayta urinib ko'ring.")
    except Exception as e:
        logger.error(f"WebApp data error: {e}")
        await message.answer("❌ Ma'lumotni qayta ishlashda xatolik yuz berdi.")


@dp.message()
async def fallback_handler(message: Message):
    webapp_url = f"{NGROK_URL}/tma/"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="🌍 GEOPORTAL ochish",
            web_app=WebAppInfo(url=webapp_url)
        )
    ]])
    await message.answer(
        "Botdan foydalanish uchun quyidagi tugmani bosing:",
        reply_markup=keyboard
    )


async def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN .env faylida topilmadi!")
        return

    logger.info(f"Bot ishga tushmoqda... NGROK: {NGROK_URL}")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
