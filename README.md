## Stopwatch with Button and Progress

This project is a simple stopwatch application built using Pygame. It features a user interface with a button to start and stop the stopwatch, displays the elapsed time, and tracks progress compared to the previous session.

### Features
- **Start/Stop Button**: A button to control the stopwatch.
- **Elapsed Time Display**: Shows the time elapsed since the stopwatch was started.
- **Previous Time Display**: Displays the time from the last session.
- **Progress Tracking**: Calculates and displays the percentage change in time compared to the previous session.
- **Data Persistence**: Saves and loads previous results to and from a text file.

### Requirements
- Python 3.x
- Pygame library

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/slovjinika/stopwatch.git
   cd stopwatch
   ```
2. Install Pygame:
   ```bash
   pip install pygame
   ```

### Usage
1. Run the application:
   ```bash
   python stopwatch.py
   ```
2. Click the "Start" button to begin timing. Click it again to stop the timer.
3. The elapsed time will be displayed, along with the previous session's time and the progress percentage.

### Code Overview
- **Initialization**: The Pygame library is initialized, and the main window is set up.
- **Button Handling**: The button changes its state and color based on whether the stopwatch is running or stopped.
- **Time Formatting**: The elapsed time is formatted into a readable string.
- **File Operations**: The application reads from and writes to a text file to store elapsed times.

### File Structure
- `stopwatch.py`: The main application file.
- `data.txt`: A text file that stores the elapsed times.


