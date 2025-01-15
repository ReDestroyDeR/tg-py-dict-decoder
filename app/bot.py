import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
from dotenv import load_dotenv

from shared_dict import load_dict, save_dict

dp = Dispatcher()
db = load_dict()
maintainer = os.getenv("MAINTAINER")

@dp.message()
async def get_command(message: Message) -> None:
    abbr = message.args.strip().upper()
    explanation = await db.get(abbr)
    if explanation is None:
        await message.answer(
            f"Я пока не знаю что такое: {abbr} 😨" +
            f"\nСообщи об этом - {maintainer}" if maintainer is not None else ""
        )
    else:
        await message.answer(f"Получил расшифровку {abbr} = {explanation}")


async def main() -> None:
    try:
        load_dotenv(".env")
        token = str(os.getenv("TOKEN"))

        if len(token.strip()) == 0:
            print("Missing TOKEN Env var")
            exit(1)
        bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

        await dp.start_polling(bot)
    finally:
        pretty = (os.getenv("PRETTY") or "false").lower() == "true"
        await save_dict(db, pretty)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
