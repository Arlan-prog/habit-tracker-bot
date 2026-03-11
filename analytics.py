from datetime import date, timedelta
from storage import load_habits

def get_streak(habit):
    entries = habit["entries"]
    
    if not entries:
        return 0

    streak = 0
    check_date = date.today()

    while str(check_date) in entries:
        streak += 1
        check_date -= timedelta(days=1)

    return streak

def show_stats():
    habits = load_habits()

    if not habits:
        print("📭 Привычек пока нет!")
        return

    print("\n📊 Статистика:")
    for habit in habits:
        total = len(habit["entries"])
        streak = get_streak(habit)
        print(f"  🏷️  {habit['name']}")
        print(f"      Всего выполнений: {total}")
        print(f"      Текущая серия:    {streak} дней подряд")
        print()