import pygame
import time
import datetime

# Initialize Pygame
pygame.init()

# Window dimensions
width, height = 150, 130 # Slightly reduced height
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Stopwatch with Button and Progress")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)
red = (255, 0, 0)
green = (0, 255, 0)

# Font (Smaller size)
font = pygame.font.Font(None, 20)

# Button
button_rect = pygame.Rect(25, 20, 100, 30)
button_color = gray

# Stopwatch variables
start_time = 0
elapsed_time = 0
running = False
previous_time = None
progress = None

# Function to format time
def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{minutes:02}:{int(seconds):02}.{milliseconds:03}"

# Function to load previous results from the file
def load_results():
    results = []
    try:
        with open("data.txt", "r") as f:
            for line in f:
                try:
                    date_str, time_str = line.strip().split(',')
                    date_time = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                    elapsed_time = float(time_str)
                    results.append((date_time, elapsed_time))
                except ValueError:
                    print(f"Error reading line: {line.strip()}")
                    continue
    except FileNotFoundError:
        pass
    return results

# Function to save a result to the file
def save_result(elapsed_time):
    now = datetime.datetime.now()
    with open("data.txt", "a") as f:
        f.write(f"{now.strftime('%Y-%m-%d %H:%M:%S')},{elapsed_time}\n")

# Load previous results at startup
results = load_results()

# Game loop
running_game = True
while running_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_game = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if button_rect.collidepoint(event.pos):
                    # Button press
                    button_color = red
                    if not running:
                        if previous_time is not None:
                            progress = None

                        running = True
                        start_time = time.time()
                    else:
                        elapsed_time = time.time() - start_time
                        save_result(elapsed_time)
                        if previous_time is not None:
                            progress = ((previous_time - elapsed_time) / previous_time) * 100
                            progress = round(progress, 2)

                        previous_time = elapsed_time
                        running = False

        if event.type == pygame.MOUSEBUTTONUP:
            button_color = gray

    # Update time
    if running:
        elapsed_time = time.time() - start_time

    # Drawing
    screen.fill(white)

    # Button
    pygame.draw.rect(screen, button_color, button_rect)
    button_text = font.render("Click", True, black)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)

    # Stopwatch
    #time_text = font.render(f"Time: {elapsed_time:.2f}", True, black)
    time_text = font.render(f"Time: {format_time(elapsed_time)}", True, black)  # Use formatted time
    time_rect = time_text.get_rect(center=(width // 2, 60))
    screen.blit(time_text, time_rect)

    # Previous time
    if previous_time is not None:
        #previous_time_text = font.render(f"Previous: {previous_time:.2f}", True, black)
        previous_time_text = font.render(f"Previous: {format_time(previous_time)}", True, black) # Use formatted time
        previous_time_rect = previous_time_text.get_rect(center=(width // 2, 80))
        screen.blit(previous_time_text, previous_time_rect)

    # Progress
    progress_color = black
    if progress is not None:
        if progress > 0:
            progress_color = green
        else:
            progress_color = red

        progress_text = font.render(f"Progress: {progress:.2f}%", True, progress_color)
        progress_rect = progress_text.get_rect(center=(width // 2, 100))
        screen.blit(progress_text, progress_rect)

    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()