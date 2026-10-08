import tkinter as tk

def click():
    pass

root = tk.Tk()
root.title("Генератор паролей")
root.geometry("300x150")

button = tk.Button(root, text = "Сгенирировать пароль", command = click)
button.pack()

root.mainloop()