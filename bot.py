import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from storage import load_habits, save_habits
from datetime import date

TOKEN = "8579369363:AAH0Nm0IFFvyPF_isniiAI5qx0WGKMW3AQY"

bot = Bot(token=TOKEN)
dp = Dispatcher()
user_states = {}
def get_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Мои привычки")],
            [KeyboardButton(text="➕ Добавить привычку")],
            [KeyboardButton(text="✅ Отметить выполнение")],
            [KeyboardButton(text="📊 Статистика")],
        ],
        resize_keyboard=True
    )
    return keyboard
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет я созданный бот через Ардак! Я твой трекер привычек!\n\nВыбери действие:",
        reply_markup=get_keyboard()
    )
@dp.message(F.text == "📋 Мои привычки")
async def show_habits(message: Message):
    habits = load_habits()

    if not habits:
        await message.answer("📭 Привычек пока нет!\nДобавь первую через кнопку ➕")
        return

    text = "📋 Твои привычки:\n\n"
    for i, habit in enumerate(habits, 1):
        text += f"{i}. {habit['name']} (с {habit['created']})\n"

    await message.answer(text)


@dp.message(F.text == "➕ Добавить привычку")
async def ask_habit_name(message: Message):
    user_states[message.from_user.id] = "waiting_name"
    await message.answer("✏️ Напиши название привычки:")

@dp.message(F.text.startswith("") )
async def add_habit(message: Message):
    user_id = message.from_user.id

    if user_states.get(user_id) != "waiting_name":
        return

    name = message.text
    habits = load_habits()

    habit = {
        "name": name,
        "created": str(date.today()),
        "entries": []
    }

    habits.append(habit)
    save_habits(habits)
    user_states[user_id] = None

    await message.answer(
        f"✅ Привычка '{name}' добавлена!",
        reply_markup=get_keyboard()
    )
@dp.message(F.text == "✅ Отметить выполнение")
async def mark_habit(message: Message):
    habits = load_habits()

    if not habits:
        await message.answer("📭 Привычек пока нет!")
        return

    today = str(date.today())
    text = "📋 Выбери номер привычки:\n\n"
    for i, habit in enumerate(habits, 1):
        done = "✅" if today in habit["entries"] else "⬜"
        text += f"{done} {i}. {habit['name']}\n"

    text += "\nНапиши номер:"
    user_states[message.from_user.id] = "waiting_mark"
    await message.answer(text)

@dp.message(F.text.regexp(r"^\d+$"))
async def process_mark(message: Message):
    user_id = message.from_user.id

    if user_states.get(user_id) != "waiting_mark":
        return

    habits = load_habits()
    today = str(date.today())

    try:
        number = int(message.text)
        habit = habits[number - 1]
    except (ValueError, IndexError):
        await message.answer("❌ Неверный номер!")
        return

    if today in habit["entries"]:
        await message.answer(f"👍 '{habit['name']}' уже отмечена сегодня!")
        return

    habit["entries"].append(today)
    save_habits(habits)
    user_states[user_id] = None

    await message.answer(
        f"🔥 '{habit['name']}' выполнена сегодня!",
        reply_markup=get_keyboard()
    )
@dp.message(F.text == "📊 Статистика")
async def show_stats(message: Message):
    habits = load_habits()

    if not habits:
        await message.answer("📭 Привычек пока нет!")
        return

    text = "📊 Статистика:\n\n"
    for habit in habits:
        total = len(habit["entries"])
        text += f"🏷 {habit['name']}\n"
        text += f"   Всего выполнений: {total}\n\n"

    await message.answer(text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())