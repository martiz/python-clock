import pygame
import math
from datetime import datetime

# Default colors for time rings (seconds, minutes, hours)
ring_colors = {
    "seconds": "#0000FF",   # Blue
    "minutes": "#00FF00",   # Green
    "hours": "#FF0000"      # Red
}

# Convert hex color to RGB tuple
def hex_to_rgb(hex_color):
    """Convert hex color string to an RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Function to draw a circular ring representing time units (seconds, minutes, hours)
def draw_ring(surface, center, radius, value, max_value, color, thickness):
    """Draw a circular ring for a given value using pygame."""
    start_angle = -90  # Start from the top (12 o'clock position)
    end_angle = start_angle + (360 * value / max_value)  # Calculate the end angle based on the time unit value
    
    # Draw background ring (gray ring for reference)
    pygame.draw.circle(surface, (50, 50, 50), center, radius, thickness)
    
    # Draw the progress arc representing the current value
    for angle in range(start_angle, int(end_angle)):
        rad = math.radians(angle)  # Convert angle to radians
        x = int(center[0] + radius * math.cos(rad))  # Calculate x-coordinate
        y = int(center[1] + radius * math.sin(rad))  # Calculate y-coordinate
        pygame.draw.circle(surface, color, (x, y), thickness // 2)  # Draw a small circle to form the arc

# Function to display the digital clock time in the center of the rings
def draw_digital_clock(surface, center, time_str, color, font_size):
    """Draw the digital clock time at the center of the rings."""
    font = pygame.font.SysFont("monospace", font_size, bold=True)  # Use a dynamically sized monospace font
    text = font.render(time_str, True, color)  # Render the text
    text_rect = text.get_rect(center=center)  # Center the text inside the clock
    surface.blit(text, text_rect)  # Draw the text on the screen

# Function to open a settings menu in the GUI
def settings_menu(screen):
    """Display a settings menu to change colors within the Pygame window."""
    menu_active = True
    font = pygame.font.SysFont("monospace", 20, bold=True)
    menu_rect = pygame.Rect(50, 50, 400, 300)  # Increased size for better layout
    input_fields = {"seconds": "", "minutes": "", "hours": ""}
    selected_field = "seconds"
    
    while menu_active:
        screen.fill((0, 0, 0), menu_rect)  # Keep the clock running in the background
        pygame.draw.rect(screen, (30, 30, 30), menu_rect)  # Dark background for settings
        pygame.draw.rect(screen, (255, 255, 255), menu_rect, 2)  # Draw white border
        
        labels = ["Enter hex color code (e.g., #FF0000):"]
        for key in input_fields:
            highlight = " <- Editing" if selected_field == key else ""
            labels.append(f"{key.capitalize()}: {input_fields[key]}{highlight}")
        labels.append("Press S to save, ESC to discard")
        
        for i, label in enumerate(labels):
            color = (255, 255, 0) if "Editing" in label else (255, 255, 255)
            text = font.render(label, True, color)
            screen.blit(text, (menu_rect.x + 10, menu_rect.y + 20 + i * 30))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_active = False  # Exit settings menu without saving
                elif event.key == pygame.K_s:
                    for key in input_fields:
                        if len(input_fields[key]) == 7 and input_fields[key][0] == '#':
                            ring_colors[key] = input_fields[key]
                    menu_active = False
                elif event.key == pygame.K_TAB:
                    selected_keys = list(input_fields.keys())
                    idx = (selected_keys.index(selected_field) + 1) % len(selected_keys)
                    selected_field = selected_keys[idx]
                elif event.unicode.isalnum() or event.unicode == '#':
                    input_fields[selected_field] += event.unicode

# Function to continuously update and display the clock
def update_clock():
    """Update the clock display in a loop using pygame."""
    pygame.init()
    width, height = 800, 800
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    
    running = True
    while running:
        width, height = screen.get_width(), screen.get_height()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_s:
                    settings_menu(screen)
        
        screen.fill((0, 0, 0))
        now = datetime.now()
        seconds, minutes, hours = now.second, now.minute, now.hour
        
        center = (width // 2, height // 2)
        base_radius = min(width, height) // 3
        thickness = max(5, base_radius // 15)
        font_size = max(20, base_radius // 5)
        
        draw_ring(screen, center, base_radius, seconds, 60, hex_to_rgb(ring_colors["seconds"]), thickness)
        draw_ring(screen, center, int(base_radius * 0.8), minutes, 60, hex_to_rgb(ring_colors["minutes"]), thickness + 2)
        draw_ring(screen, center, int(base_radius * 0.6), hours, 24, hex_to_rgb(ring_colors["hours"]), thickness + 4)
        
        time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
        draw_digital_clock(screen, center, time_str, (255, 255, 255), font_size)
        
        pygame.display.flip()
        clock.tick(5)
    
    pygame.quit()

update_clock()
