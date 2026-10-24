from storage import load_habits,save_habits
from datetime import date
from analytics import show_stats

def add_habit():
    name=input("название привычки: ")
    habits=load_habits()
    habit={
        "name":name,
        "created":str(date.today()),
        "entries":[]
        }
    habits.append(habit)
    save_habits(habits)
    print(f"привычка '{name}' добавлена")

def show_habits():
        habits=load_habits()
        if not habits:
            print("у вас нет привычек")
            return
        print("ваши привычки:")
        for i,habit in enumerate(habits,1):
            print(f"{i}. {habit['name']} (создано {habit['created']})")



def mark_habit():
    habits=load_habits()
    if not habits:
        print("у вас нет привычек")
        return
    show_habits()
    try:
        number=int(input("номер привычки для отметки: "))
        habit=habits[number-1]
    except (ValueError,IndexError):
        print ("некорректный номер")
        return
    today=str(date.today())
    if today in habit['entries']:
        print(f"вы уже отметили '{habit['name']}' сегодня")
        return
    habit['entries'].append(today)
    save_habits(habits)
    print(f"привычка '{habit['name']}' выполнено на сегодня")

def menu():
    while True:
        print("\nвыберите действие:")
        print("1. добавить привычку")
        print("2. показать привычки")
        print("3. отметить привычку")
        print("4. показать статистику")
        print("5. выйти")
        choice=input("ваш выбор: ")
        if choice=="1":
            add_habit()
        elif choice=="2":
            show_habits()
        elif choice=="3":
            mark_habit()
        elif choice=="4":
            show_stats()
        elif choice=="5":
            print("до свидания!")
            break
        else:
            print("некорректный выбор")
if __name__ == "__main__":
    menu()
