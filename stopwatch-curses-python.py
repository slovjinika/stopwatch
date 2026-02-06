import curses
import time
import datetime
import os

class CursesStopwatch:
    def __init__(self):
        self.data_file = "data.txt"
        self.start_time = 0
        self.elapsed_time = 0
        self.previous_time = None
        self.running = False
        self.diff_text = ""
        self.diff_color_pair = 1 # По умолчанию белый

    def format_time(self, seconds):
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        msecs = int((seconds - int(seconds)) * 1000)
        return f"{minutes:02}:{secs:02}.{msecs:03}"

    def save_result(self, elapsed):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with open(self.data_file, "a") as f:
                f.write(f"{now},{elapsed}\n")
        except Exception:
            pass

    def load_previous_session(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip().split(',')
                        self.previous_time = float(last_line[1])
            except:
                self.previous_time = None

    def toggle(self):
        if not self.running:
            # СТАРТ
            self.running = True
            self.start_time = time.time() - self.elapsed_time
        else:
            # СТОП
            self.running = False
            self.save_result(self.elapsed_time)
            
            if self.previous_time is not None and self.previous_time > 0:
                diff = ((self.elapsed_time - self.previous_time) / self.previous_time) * 100
                self.diff_text = f"{int(diff)}%"
                # Зеленый если > 0, Красный если < 0
                self.diff_color_pair = 2 if diff > 0 else 3
            
            self.previous_time = self.elapsed_time
            self.elapsed_time = 0

    def main(self, stdscr):
        # Настройки curses
        curses.curs_set(0) # Скрыть курсор
        stdscr.nodelay(True) # Не ждать нажатия клавиши
        stdscr.timeout(50) # Частота обновления в мс
        
        # Настройка цветов
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK) # Прогресс +
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)   # Прогресс -

        self.load_previous_session()

        while True:
            stdscr.erase()
            
            # Логика времени
            if self.running:
                self.elapsed_time = time.time() - self.start_time

            # Отрисовка интерфейса
            #stdscr.addstr(1, 2, "STOPWATCH.PY", curses.A_BOLD)
            
            status = "[ STOPPED ]" if not self.running else "[ RUNNING ]"
            stdscr.addstr(2, 2, status)

            # Текущее время
            stdscr.addstr(4, 2, self.format_time(self.elapsed_time), curses.A_BOLD | curses.color_pair(1))

            # Предыдущее время
            prev_str = self.format_time(self.previous_time) if self.previous_time else "--:--.---"
            stdscr.addstr(5, 2, f"Prev: {prev_str}", curses.color_pair(1))

            # Процент разницы
            if self.diff_text:
                stdscr.addstr(6, 2, f"Diff: {self.diff_text}", curses.color_pair(self.diff_color_pair))

            stdscr.addstr(8, 2, "Space: Start/Stop | Q: Quit")

            # Обработка ввода
            try:
                key = stdscr.getch()
                if key == ord(' '):
                    self.toggle()
                elif key in (ord('q'), ord('Q')):
                    break
            except EOFError:
                break

            stdscr.refresh()

if __name__ == "__main__":
    app = CursesStopwatch()
    curses.wrapper(app.main)
