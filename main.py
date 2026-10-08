from datetime import datetime
import json
import os
import random
import string
import tkinter as tk

# Файл для сохранения локального лимита
LIMIT_FILE = "usage_limit.json"
MAX_GENERATIONS = 5


def load_usage_data():
  """Загружает данные об использовании из файла."""
  if os.path.exists(LIMIT_FILE):
    try:
      with open(LIMIT_FILE, "r") as f:
        return json.load(f)
    except Exception:
      pass
  # Значения по умолчанию, если файла нет или он поврежден
  return {"last_date": str(datetime.today().date()), "count": 0}


def save_usage_data(data):
  """Сохраняет данные об использовании в файл."""
  with open(LIMIT_FILE, "w") as f:
    json.dump(data, f)


def check_and_update_limit():
  """Проверяет лимит. Возвращает True, если генерация разрешена."""
  data = load_usage_data()
  current_date = str(datetime.today().date())

  # Если наступил новый день, сбрасываем счетчик
  if data["last_date"] != current_date:
    data["last_date"] = current_date
    data["count"] = 0

  # Проверяем, не превышен ли лимит
  if data["count"] >= MAX_GENERATIONS:
    return False

  # Увеличиваем счетчик и сохраняем
  data["count"] += 1
  save_usage_data(data)
  return True


def generate_password(length=12, use_specials=True):
  chars = string.ascii_letters + string.digits
  if use_specials:
    chars += "!@#$%^&*()"
  return "".join(random.choice(chars) for _ in range(length))


def click():
  password_entry.delete(0, tk.END)

  # Проверяем лимит перед генерацией
  if not check_and_update_limit():
    password_entry.insert(0, "Лимит исчерпан (5 в день)!")
    button.config(state=tk.DISABLED)  # Блокируем кнопку
    return

  new_password = generate_password(length=12, use_specials=True)
  password_entry.insert(0, new_password)

  # Обновляем текст на кнопке, показывая остаток
  data = load_usage_data()
  remains = MAX_GENERATIONS - data["count"]
  button.config(text=f"Сгенерировать пароль (Осталось: {remains})")


root = tk.Tk()
root.title("Генератор паролей")
root.geometry("350x150")

# При запуске проверяем, нужно ли сразу заблокировать кнопку
usage_data = load_usage_data()
if usage_data["last_date"] == str(datetime.today().date()):
  initial_count = usage_data["count"]
else:
  initial_count = 0

remains = MAX_GENERATIONS - initial_count

# Настройка кнопки в зависимости от остатка лимита
if remains <= 0:
  button_text = "Лимит на сегодня исчерпан"
  button_state = tk.DISABLED
else:
  button_text = f"Сгенерировать пароль (Осталось: {remains})"
  button_state = tk.NORMAL

button = tk.Button(
    root, text=button_text, command=click, state=button_state, padx=10, pady=5
)
button.pack(pady=20)

password_entry = tk.Entry(root, font=("Arial", 12), justify="center")
password_entry.pack(pady=5, fill="x", padx=20)

root.mainloop()
