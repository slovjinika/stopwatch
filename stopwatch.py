import pygame
import time
import datetime

# Initialize Pygame
pygame.init()

# Window dimensions
width, height = 150, 130
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("stopwatch.py")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)
red = (178, 0, 0)
green = (0, 178, 0)
light_gray = (220, 220, 220)
#dark_gray = (80, 80, 80)

# Font (Smaller size)
#font = pygame.font.Font(None, 18)
#font = pygame.font.SysFont('Unifont Smooth', 18)
font = pygame.font.Font(None, 22)

# Button
button_rect = pygame.Rect(25, 13, 100, 30)
button_color = light_gray
button_text_color = black
button_text_str = "Start"

# Stopwatch variables
start_time = 0
elapsed_time = 0
running = False
previous_time = None
progress = None
data_file = "data.txt"

# Function to format time
def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{minutes:02}:{int(seconds):02}.{milliseconds:03}"

def draw_time(screen, time_value, y_position, color, font):
    time_text = font.render(f"{format_time(time_value)}", True, color)
    time_rect = time_text.get_rect(center=(width // 2, y_position))
    screen.blit(time_text, time_rect)

# Function to load previous results from the file
def load_results():
    results = []
    try:
        with open(data_file, "r") as f:
            for line in f:
                try:
                    date_str, time_str = line.strip().split(',')
                    date_time = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                    elapsed_time = float(time_str)
                    results.append((date_time, elapsed_time))
                except ValueError as e:
                    print(f"Error reading line: {line.strip()}. Error: {e}")
                except OSError as e:
                    print(f"Error opening file {data_file}: {e}")

    except FileNotFoundError:
        print(f"File not found: {data_file}")

    return results

# Function to save a result to the file
def save_result(elapsed_time):
    now = datetime.datetime.now()
    try:
        with open(data_file, "a") as f:
            f.write(f"{now.strftime('%Y-%m-%d %H:%M:%S')},{elapsed_time}\n")
    except OSError as e:
        print(f"Error writing to file {data_file}: {e}")


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
                    if not running:
                        # Start the stopwatch
                        button_color = red
                        button_text_str = "Stop"
                        button_text_color = white
                        if previous_time is not None:
                            progress = None

                        running = True
                        start_time = time.time()
                    else:
                        # Stop the stopwatch
                        button_text_color = black
                        button_color = light_gray
                        button_text_str = "Start"
                        elapsed_time = time.time() - start_time
                        save_result(elapsed_time)

                        if previous_time is not None:
                            if previous_time == 0:
                                progress = 0
                            else:
                                progress = ((elapsed_time - previous_time) / previous_time) * 100
                            progress = int(progress)  # Remove decimal places
                            #progress = round(progress, 0) # Alternative rounding
                            #progress = int(round(progress)) # Alternative rounding

                        previous_time = elapsed_time
                        running = False



    # Update time
    if running:
        elapsed_time = time.time() - start_time

    # Drawing
    screen.fill(white)

    # Button Shadows 
    #pygame.draw.line(screen, light_gray, (button_rect.x, button_rect.y), (button_rect.x + button_rect.width, button_rect.y), 3)
    #pygame.draw.line(screen, light_gray, (button_rect.x, button_rect.y), (button_rect.x, button_rect.y + button_rect.height), 3)
    #pygame.draw.line(screen, dark_gray, (button_rect.x, button_rect.y + button_rect.height), (button_rect.x + button_rect.width, button_rect.y + button_rect.height), 3)
    #pygame.draw.line(screen, dark_gray, (button_rect.x + button_rect.width, button_rect.y), (button_rect.x + button_rect.width, button_rect.y + button_rect.height), 3)

    # Button
    pygame.draw.rect(screen, button_color, button_rect)
    button_text = font.render(button_text_str, True, button_text_color)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)

    # Stopwatch
    draw_time(screen, elapsed_time, 60, black, font)

    # Previous time
    if previous_time is not None:
        draw_time(screen, previous_time, 80, gray, font)


    # Progress
    progress_color = black
    if progress is not None:
        if progress > 0:
            progress_color = green # Show red for worsening
        else:
            progress_color = red # Show green for improvement

        progress_text = font.render(f"{progress}%", True, progress_color) # Removed {:.2f}
        progress_rect = progress_text.get_rect(center=(width // 2, 100))
        screen.blit(progress_text, progress_rect)

    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
