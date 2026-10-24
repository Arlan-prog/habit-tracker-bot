import asyncio
import os
from datetime import date

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from storage import load_habits, save_habits

load_dotenv()

BUTTON_HABITS = "📋 Мои привычки"
BUTTON_ADD = "➕ Добавить привычку"
BUTTON_MARK = "✅ Отметить выполнение"
BUTTON_STATS = "📊 Статистика"

dp = Dispatcher()
user_states: dict[int, str] = {}


def get_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BUTTON_HABITS)],
            [KeyboardButton(text=BUTTON_ADD)],
            [KeyboardButton(text=BUTTON_MARK)],
            [KeyboardButton(text=BUTTON_STATS)],
        ],
        resize_keyboard=True,
    )


def waiting_for_name(message: Message) -> bool:
    return bool(message.from_user and user_states.get(message.from_user.id) == "waiting_name")


@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    await message.answer(
        "👋 Привет! Я помогу отслеживать привычки. Выбери действие:",
        reply_markup=get_keyboard(),
    )


@dp.message(F.text == BUTTON_HABITS)
async def show_habits(message: Message) -> None:
    habits = load_habits(message.from_user.id)
    if not habits:
        await message.answer("📭 Привычек пока нет. Добавь первую кнопкой ниже.")
        return

    lines = ["📋 Твои привычки:", ""]
    for index, habit in enumerate(habits, 1):
        lines.append(f"{index}. {habit['name']} (с {habit['created']})")
    await message.answer("\n".join(lines))


@dp.message(F.text == BUTTON_ADD)
async def ask_habit_name(message: Message) -> None:
    user_states[message.from_user.id] = "waiting_name"
    await message.answer("✏️ Напиши название привычки:")


@dp.message(waiting_for_name)
async def add_habit(message: Message) -> None:
    user_id = message.from_user.id
    name = (message.text or "").strip()
    if not name:
        await message.answer("Название не должно быть пустым. Попробуй ещё раз.")
        return

    habits = load_habits()
    habits.append({"name": name, "created": str(date.today()), "entries": []})
    save_habits(user_id, habits)
    user_states.pop(user_id, None)
    await message.answer(f"✅ Привычка «{name}» добавлена!", reply_markup=get_keyboard())


@dp.message(F.text == BUTTON_MARK)
async def mark_habit(message: Message) -> None:
    habits = load_habits()
    if not habits:
        await message.answer("📭 Привычек пока нет.")
        return

    today = str(date.today())
    lines = ["📋 Выбери номер привычки:", ""]
    for index, habit in enumerate(habits, 1):
        done = "✅" if today in habit["entries"] else "⬜"
        lines.append(f"{done} {index}. {habit['name']}")
    lines.extend(["", "Напиши номер:"])
    user_states[message.from_user.id] = "waiting_mark"
    await message.answer("\n".join(lines))


@dp.message(F.text.regexp(r"^\d+$"))
async def process_mark(message: Message) -> None:
    user_id = message.from_user.id
    if user_states.get(user_id) != "waiting_mark":
        return

    habits = load_habits()
    number = int(message.text)
    if not 1 <= number <= len(habits):
        await message.answer("❌ Такого номера нет. Введи номер из списка.")
        return

    habit = habits[number - 1]
    today = str(date.today())
    if today in habit["entries"]:
        user_states.pop(user_id, None)
        await message.answer(f"👍 «{habit['name']}» уже отмечена сегодня.")
        return

    habit["entries"].append(today)
    save_habits(habits)
    user_states.pop(user_id, None)
    await message.answer(f"🔥 «{habit['name']}» выполнена сегодня!", reply_markup=get_keyboard())


@dp.message(F.text == BUTTON_STATS)
async def show_stats(message: Message) -> None:
    habits = load_habits()
    if not habits:
        await message.answer("📭 Привычек пока нет.")
        return

    lines = ["📊 Статистика:", ""]
    for habit in habits:
        lines.append(f"🏷 {habit['name']}: {len(habit['entries'])} выполнений")
    await message.answer("\n".join(lines))


async def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("Не задан BOT_TOKEN. Добавь токен в переменные окружения.")

    async with Bot(token=token) as bot:
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
