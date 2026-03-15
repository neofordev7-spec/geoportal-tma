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
    MenuButtonWebApp,
)

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
APP_URL = os.getenv('APP_URL', 'http://localhost:8000')

logging.basicConfig(level=logging.INFO, format='%(asctime)s — %(levelname)s — %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

XUSH_KELIBSIZ = """
Assalomu alaykum, <b>{name}</b>! 👋

<b>Real Holat</b> — fuqarolar monitoring platformasi.

Siz bu yerda:
🔹 Maktab, shifoxona, yo'l muammolarini xabar berasiz
🔹 Yaqiningizdagi ob'yektlarni tekshirasiz
🔹 Boshqa fuqarolar signallarini ko'rasiz
🔹 Statistikani real vaqtda kuzatasiz

👇 <b>Boshlash uchun tugmani bosing:</b>
"""


@dp.message(CommandStart())
async def start_handler(message: Message):
    webapp_url = f"{APP_URL}/tma/feed/"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📲 Ilovani ochish",
                web_app=WebAppInfo(url=webapp_url)
            )
        ],
        [
            InlineKeyboardButton(
                text="🗺 Xarita",
                web_app=WebAppInfo(url=f"{APP_URL}/tma/tahlil/")
            ),
            InlineKeyboardButton(
                text="📢 Signal",
                web_app=WebAppInfo(url=f"{APP_URL}/tma/murojaat/")
            )
        ],
    ])

    user_name = message.from_user.first_name or "foydalanuvchi"
    text = XUSH_KELIBSIZ.format(name=user_name)

    await message.answer(text, parse_mode='HTML', reply_markup=keyboard)
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
                f"{APP_URL}/api/murojaat/",
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
    webapp_url = f"{APP_URL}/tma/feed/"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="📲 Ilovani ochish",
            web_app=WebAppInfo(url=webapp_url)
        )
    ]])
    await message.answer(
        "📲 Ilovadan foydalanish uchun quyidagi tugmani bosing yoki pastdagi <b>Menu</b> tugmasini bosing:",
        parse_mode='HTML',
        reply_markup=keyboard
    )


async def set_menu_button():
    """Chatning pastida doimiy Mini App tugmasini o'rnatish"""
    webapp_url = f"{APP_URL}/tma/feed/"
    try:
        await bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                text="📲 Ilovani ochish",
                web_app=WebAppInfo(url=webapp_url)
            )
        )
        logger.info("Menu button o'rnatildi")
    except Exception as e:
        logger.error(f"Menu button o'rnatishda xatolik: {e}")


async def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN .env faylida topilmadi!")
        return

    await set_menu_button()
    logger.info(f"Bot ishga tushmoqda... NGROK: {APP_URL}")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
