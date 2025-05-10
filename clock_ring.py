import pygame
from pygame import gfxdraw
import math
from datetime import datetime
from constants import *

# Function to draw a circular ring representing time units (seconds, minutes, hours)
def draw_ring(surface, center, radius, value, max_value, color, thickness):
    """Draw a circular ring for a given value using pygame."""
    start_angle = -90  # Start from the top (12 o'clock position)
    end_angle = start_angle + (360 * value / max_value)  # Calculate the end angle based on the time unit value
    
    # Draw background ring (gray ring for reference)
    pygame.draw.circle(surface, GRAY_RING, center, radius, thickness)
    
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

# Function to continuously update and display the clock
def update_clock():
    """Update the clock display in a loop using pygame."""
    pygame.init()  # Initialize pygame
    width, height = 800, 800  # Set the initial window size
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)  # Create a resizable window
    clock = pygame.time.Clock()  # Initialize a clock object to control frame rate
    fullscreen = False  # Track fullscreen mode
    
    running = True  # Main loop flag
    while running:
        width, height = screen.get_width(), screen.get_height()  # Get the current window size
        
        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check if the user closes the window
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press ESC to exit
                    running = False
                elif event.key == pygame.K_f:  # Press F to toggle fullscreen
                    fullscreen = not fullscreen
                    if fullscreen:
                        display_index = 0  # Change this index if needed for another monitor
                        display_mode = pygame.display.list_modes(display_index)[0]  # Get best resolution for monitor
                        screen = pygame.display.set_mode(display_mode, pygame.FULLSCREEN, display=display_index)
                    else:
                        screen = pygame.display.set_mode((800, 800), pygame.RESIZABLE)  # Restore windowed mode
        
        screen.fill((0, 0, 0))  # Clear the screen with black background
        now = datetime.now()  # Get the current time
        seconds = now.second
        minutes = now.minute
        hours = now.hour  # Use 24-hour format
        
        # Calculate dynamic center based on resized window
        center = (width // 2, height // 2)
        base_radius = min(width, height) // 3  # Scale the ring size dynamically based on window size
        thickness = max(5, base_radius // 15)  # Adjust ring thickness dynamically
        font_size = max(20, base_radius // 5)  # Scale font size dynamically
        
        # Draw rings in correct order (seconds at bottom, then minutes, then hours on top)
        draw_ring(screen, center, base_radius, seconds, 60, COLOR_RING_SECONDS, thickness)  # Ring for seconds
        draw_ring(screen, center, int(base_radius * 0.8), minutes, 60, COLOR_RING_MINUTES, thickness + 2)  # Ring for minutes
        draw_ring(screen, center, int(base_radius * 0.6), hours, 24, COLOR_RING_HOURS, thickness + 4)  # Ring for hours
        
        # Draw digital clock in center with current time
        time_str = f"{hours:02}:{minutes:02}:{seconds:02}"  # Format time in HH:MM:SS
        draw_digital_clock(screen, center, time_str, (255, 255, 255), font_size)  # White text
        
        pygame.display.flip()  # Refresh the display
        clock.tick(5)  # Lower refresh rate to reduce resource usage
    
    pygame.quit()  # Quit pygame when loop exits

# Start the clock update loop
update_clock()
