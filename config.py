import sys

def load_token():
    try:
        with open("token.txt", "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        print("❌ ОШИБКА: Файл 'token.txt' не найден!")
        print("💡 Создай файл token.txt рядом с main.py и вставь туда токен.")
        sys.exit(1)