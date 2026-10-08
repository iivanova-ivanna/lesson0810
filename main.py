import tkinter as tk
import random
import string

# Выделенная функция генерации пароля
def generate_password(length=12, use_specials=True):
    # Базовый набор: буквы в разном регистре и цифры
    chars = string.ascii_letters + string.digits
    # Добавляем спецсимволы, если флаг True
    if use_specials:
        chars += "!@#$%^&*()"
    # Генерируем случайную строку заданной длины
    return "".join(random.choice(chars) for _ in range(length))


def click():
    # Очищаем текстовое поле перед выводом
    password_entry.delete(0, tk.END)
    # Вызываем функцию генерации (длина 12, со спецсимволами)
    new_password = generate_password(length=12, use_specials=True)
    # Отображаем пароль в интерфейсе
    password_entry.insert(0, new_password)


root = tk.Tk()
root.title("Генератор паролей")
root.geometry("300x150")

button = tk.Button(root, text = "Сгенирировать пароль", command = click)
button.pack()
password_entry = tk.Entry(root, font=("Arial", 12), justify="center")
password_entry.pack()

root.mainloop()