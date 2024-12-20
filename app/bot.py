import os

import asyncio
import logging
import sys

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.types import Message
from shared_dict import SharedStrDict, load_dict, save_dict

dp = Dispatcher()
db = load_dict()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}!")


@dp.message(Command("добавить"))
async def add_command(message: Message, command: CommandObject) -> None:
    if command.args is None or command.args.count('|') != 1:
        await message.answer("Не переданы аргументы. Формат: 'Абривиатура | Расшифровка'")
    else:
        exploded = list(map(str.strip, command.args.split("|")))
        (abbr, explanation) = (exploded[0].upper(), exploded[1])
        await db.append(abbr, explanation)
        await message.answer(f"Сохранил расшифровку {abbr} = {explanation}")


@dp.message(Command("получить"))
async def get_command(message: Message, command: CommandObject) -> None:
    if command.args is None:
        await message.answer("Не передан аргумент. Формат: 'Абривиатура'")
    else:
        abbr = command.args.strip().upper()
        explanation = await db.get(abbr)
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
