import time
import datetime
import os
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Label, Static
from textual.containers import Vertical, Center
from textual.reactive import reactive

class StopwatchApp(App):
    CSS = """
    Screen {
        align: center middle;
    }

    #container {
        width: 30;
        height: auto;
        border: heavy white;
        padding: 1;
        background: $surface;
    }

    .display {
        text-align: center;
        width: 100%;
        margin: 1 0;
    }

    #current_time {
        text-style: bold;
        height: 1;
        color: $accent;
    }

    #prev_time {
        color: $text-muted;
    }

    #progress {
        margin-bottom: 1;
    }

    .start { background: green; }
    .stop { background: maroon; }
    
    .text-green { color: green; }
    .text-red { color: red; }
    """

    # Реактивные переменные (автоматически обновляют UI при изменении)
    elapsed_time = reactive(0.0)
    running = reactive(False)
    previous_time = reactive(None)
    progress_text = reactive("")
    progress_class = reactive("")

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(id="container"):
            yield Center(Button("Start", id="toggle_btn", variant="success"))
            yield Label("00:00.000", id="current_time", classes="display")
            yield Label("--:--.---", id="prev_time", classes="display")
            yield Label("", id="progress", classes="display")
        yield Footer()

    def on_mount(self) -> None:
        """Инициализация при запуске."""
        self.data_file = "data.txt"
        self.start_moment = 0
        self.load_previous_session()
        # Обновляем экран 20 раз в секунду
        self.set_interval(0.05, self.update_clock)

    def format_time(self, seconds: float) -> str:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        msecs = int((seconds - int(seconds)) * 1000)
        return f"{minutes:02}:{secs:02}.{msecs:03}"

    def update_clock(self) -> None:
        if self.running:
            self.elapsed_time = time.time() - self.start_moment
            self.query_one("#current_time", Label).update(self.format_time(self.elapsed_time))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "toggle_btn":
            if not self.running:
                # START
                self.running = True
                self.start_moment = time.time() - self.elapsed_time
                event.button.label = "Stop"
                event.button.variant = "error"
            else:
                # STOP
                self.running = False
                event.button.label = "Start"
                event.button.variant = "success"
                
                self.save_result(self.elapsed_time)
                self.calculate_diff()
                
                self.previous_time = self.elapsed_time
                self.query_one("#prev_time", Label).update(self.format_time(self.previous_time))
                self.elapsed_time = 0.0
                self.query_one("#current_time", Label).update("00:00.000")

    def calculate_diff(self):
        if self.previous_time and self.previous_time > 0:
            diff = int(((self.elapsed_time - self.previous_time) / self.previous_time) * 100)
            color_class = "text-green" if diff > 0 else "text-red"
            progress_widget = self.query_one("#progress", Label)
            progress_widget.update(f"{diff}%")
            # Сбрасываем старые классы цвета и ставим новый
            progress_widget.remove_class("text-green", "text-red")
            progress_widget.add_class(color_class)

    def save_result(self, elapsed: float):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with open(self.data_file, "a") as f:
                f.write(f"{now},{elapsed}\n")
        except Exception as e:
            self.log(f"Error saving: {e}")

    def load_previous_session(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip().split(',')
                        self.previous_time = float(last_line[1])
                        self.query_one("#prev_time", Label).update(self.format_time(self.previous_time))
            except:
                pass

if __name__ == "__main__":
    app = StopwatchApp()
    app.run()

