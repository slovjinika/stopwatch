import tkinter as tk
from tkinter import messagebox
import time
import datetime
import os

class StopwatchDialog:
    def __init__(self, root):
        self.root = root
        self.root.title("stopwatch.py")
        self.root.geometry("180x160")
        self.root.resizable(False, False)

        # Переменные
        self.start_time = 0
        self.elapsed_time = 0
        self.previous_time = None
        self.running = False
        self.data_file = "data.txt"

        # Настройка интерфейса
        self.setup_ui()
        self.load_previous_session()

    def setup_ui(self):
        # Кнопка Start/Stop
        self.btn = tk.Button(self.root, text="Start", font=("Arial", 12), 
                              command=self.toggle, bg="#dcdcdc", width=10)
        self.btn.pack(pady=10)

        # Текущее время
        self.lbl_current = tk.Label(self.root, text="00:00.000", font=("Arial", 14, "bold"))
        self.lbl_current.pack()

        # Предыдущее время
        self.lbl_prev = tk.Label(self.root, text="--:--.---", font=("Arial", 10), fg="gray")
        self.lbl_prev.pack()

        # Прогресс (%)
        self.lbl_progress = tk.Label(self.root, text="", font=("Arial", 10))
        self.lbl_progress.pack()

    def format_time(self, seconds):
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        msecs = int((seconds - int(seconds)) * 1000)
        return f"{minutes:02}:{secs:02}.{msecs:03}"

    def toggle(self):
        if not self.running:
            # Запуск
            self.running = True
            self.start_time = time.time() - self.elapsed_time
            self.btn.config(text="Stop", bg="#b20000", fg="white")
            self.update_clock()
        else:
            # Остановка
            self.running = False
            self.btn.config(text="Start", bg="#dcdcdc", fg="black")
            self.save_result(self.elapsed_time)
            
            # Расчет прогресса
            if self.previous_time is not None and self.previous_time > 0:
                diff = ((self.elapsed_time - self.previous_time) / self.previous_time) * 100
                diff = int(diff)
                color = "#00b200" if diff > 0 else "#b20000" # Зеленый если больше, красный если меньше
                self.lbl_progress.config(text=f"{diff}%", fg=color)
            
            self.previous_time = self.elapsed_time
            self.lbl_prev.config(text=self.format_time(self.previous_time))
            self.elapsed_time = 0 # Сброс для следующего круга

    def update_clock(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.lbl_current.config(text=self.format_time(self.elapsed_time))
            self.root.after(50, self.update_clock)

    def save_result(self, elapsed):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with open(self.data_file, "a") as f:
                f.write(f"{now},{elapsed}\n")
        except Exception as e:
            print(f"Error saving: {e}")

    def load_previous_session(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip().split(',')
                        self.previous_time = float(last_line[1])
                        self.lbl_prev.config(text=self.format_time(self.previous_time))
            except:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    app = StopwatchDialog(root)
    root.mainloop()
