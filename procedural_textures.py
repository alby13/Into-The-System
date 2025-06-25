import pygame as pg
import random

def generate_circuit_floor_texture(width, height) -> pg.Surface:
    # Main surface for the texture
    texture_surface = pg.Surface((width, height))

    # Colors
    BG_COLOR = (20, 40, 20)  # Dark desaturated green
    TRACE_COLOR_MAIN = (50, 150, 50)  # Brighter green
    TRACE_COLOR_SECONDARY = (40, 120, 120) # Darker Cyan
    PAD_COLOR = (100, 100, 50)  # Dull yellow/gold
    COMPONENT_COLOR = (30, 30, 30) # Dark grey for simple components

    texture_surface.fill(BG_COLOR)

    grid_size = 16  # Draw traces along a conceptual grid
    num_traces_main = (width * height) // (grid_size * 50) # Density control
    num_traces_secondary = (width * height) // (grid_size * 40)

    # --- Helper to draw a single trace segment ---
    def draw_trace_segment(surface, color, start_pos, end_pos, thickness):
        pg.draw.line(surface, color, start_pos, end_pos, thickness)
        # Add small pads at the start/end of main traces
        if color == TRACE_COLOR_MAIN:
            pg.draw.circle(surface, PAD_COLOR, start_pos, thickness + 1)
            pg.draw.circle(surface, PAD_COLOR, end_pos, thickness + 1)

    # --- Generate Main Traces ---
    for _ in range(num_traces_main):
        x = random.randint(0, width // grid_size) * grid_size
        y = random.randint(0, height // grid_size) * grid_size
        trace_len_pixels = random.randint(grid_size * 2, grid_size * 10)
        thickness = random.randint(1, 3)

        if random.choice([True, False]): # Horizontal trace
            end_x = min(width, x + trace_len_pixels)
            draw_trace_segment(texture_surface, TRACE_COLOR_MAIN, (x, y), (end_x, y), thickness)
            # Chance to turn
            if random.random() < 0.4 and y + grid_size < height and y - grid_size > 0:
                next_y_dir = random.choice([-1, 1])
                next_y_len = random.randint(grid_size, grid_size * 3)
                next_y = min(height, max(0, y + next_y_dir * next_y_len))
                draw_trace_segment(texture_surface, TRACE_COLOR_MAIN, (end_x, y), (end_x, next_y), thickness)
        else: # Vertical trace
            end_y = min(height, y + trace_len_pixels)
            draw_trace_segment(texture_surface, TRACE_COLOR_MAIN, (x, y), (x, end_y), thickness)
            # Chance to turn
            if random.random() < 0.4 and x + grid_size < width and x - grid_size > 0:
                next_x_dir = random.choice([-1, 1])
                next_x_len = random.randint(grid_size, grid_size * 3)
                next_x = min(width, max(0, x + next_x_dir * next_x_len))
                draw_trace_segment(texture_surface, TRACE_COLOR_MAIN, (x, end_y), (next_x, end_y), thickness)

    # --- Generate Secondary, thinner traces (more numerous) ---
    for _ in range(num_traces_secondary):
        x = random.randint(0, width // grid_size) * grid_size
        y = random.randint(0, height // grid_size) * grid_size
        trace_len_pixels = random.randint(grid_size, grid_size * 5)
        thickness = 1 # Thinner traces

        if random.choice([True, False]): # Horizontal trace
            end_x = min(width, x + trace_len_pixels)
            pg.draw.line(texture_surface, TRACE_COLOR_SECONDARY, (x,y), (end_x, y), thickness)
        else: # Vertical trace
            end_y = min(height, y + trace_len_pixels)
            pg.draw.line(texture_surface, TRACE_COLOR_SECONDARY, (x,y), (x, end_y), thickness)

    # --- Add some larger "component" pads/areas ---
    num_components = (width * height) // (grid_size * 200)
    for _ in range(num_components):
        comp_w = random.randint(grid_size // 2, grid_size * 2)
        comp_h = random.randint(grid_size // 2, grid_size * 2)
        comp_x = random.randint(0, width - comp_w)
        comp_y = random.randint(0, height - comp_h)
        pg.draw.rect(texture_surface, COMPONENT_COLOR, (comp_x, comp_y, comp_w, comp_h))
        # Add small "pins" or connection pads to components
        for i in range(random.randint(2,4)):
            pin_x, pin_y = 0,0
            edge = random.choice(['top', 'bottom', 'left', 'right'])
            if edge == 'top':
                pin_x = comp_x + random.randint(0, comp_w)
                pin_y = comp_y
            elif edge == 'bottom':
                pin_x = comp_x + random.randint(0, comp_w)
                pin_y = comp_y + comp_h
            elif edge == 'left':
                pin_x = comp_x
                pin_y = comp_y + random.randint(0, comp_h)
            else: # right
                pin_x = comp_x + comp_w
                pin_y = comp_y + random.randint(0, comp_h)
            pg.draw.circle(texture_surface, PAD_COLOR, (pin_x, pin_y), 2)


    return texture_surface

def generate_ceiling_texture(width, height) -> pg.Surface:
    texture_surface = pg.Surface((width, height))

    # Colors
    BG_COLOR = (10, 10, 25)      # Very dark blue
    GRID_LINE_COLOR = (20, 20, 40) # Slightly lighter dark blue for grid
    LIGHT_COLORS = [
        (50, 20, 20, 150),       # Dim red, semi-transparent
        (50, 50, 20, 150),       # Dim yellow, semi-transparent
        (20, 20, 60, 150)        # Dim blue, semi-transparent
    ]

    texture_surface.fill(BG_COLOR)

    # Draw faint grid lines
    grid_spacing = 32
    for x in range(0, width, grid_spacing):
        pg.draw.line(texture_surface, GRID_LINE_COLOR, (x, 0), (x, height), 1)
    for y in range(0, height, grid_spacing):
        pg.draw.line(texture_surface, GRID_LINE_COLOR, (0, y), (width, y), 1)

    # Draw sparse "indicator lights" at some grid intersections
    num_lights = (width * height) // (grid_spacing * grid_spacing * 10) # Density: 1 light per 10 grid cells on avg

    for _ in range(num_lights):
        grid_x = random.randint(0, (width // grid_spacing) -1)
        grid_y = random.randint(0, (height // grid_spacing) -1)

        light_x = grid_x * grid_spacing
        light_y = grid_y * grid_spacing

        # Create a small surface for the light to handle alpha blending correctly
        light_surface = pg.Surface((grid_spacing, grid_spacing), pg.SRCALPHA)
        light_color = random.choice(LIGHT_COLORS)

        # Draw light source (e.g., a small square or circle)
        # Making it slightly offset within the grid cell for variety
        light_size = random.randint(2, 4)
        center_offset_x = grid_spacing // 2 + random.randint(-grid_spacing//4, grid_spacing//4)
        center_offset_y = grid_spacing // 2 + random.randint(-grid_spacing//4, grid_spacing//4)

        pg.draw.rect(light_surface, light_color, (center_offset_x - light_size // 2, center_offset_y - light_size // 2, light_size, light_size))

        texture_surface.blit(light_surface, (light_x, light_y))

    return texture_surface

if __name__ == '__main__':
    # Example usage for testing the texture generation
    pg.init()
    texture_width, texture_height = 256, 256
    # generated_texture = generate_circuit_floor_texture(texture_width, texture_height)
    generated_texture = generate_ceiling_texture(texture_width, texture_height) # Test ceiling

    # Save or display the texture
    # pg.image.save(generated_texture, "procedural_floor_test.png")
    # print("Saved test texture to procedural_floor_test.png")

    # Display in a window for quick visual check
    screen = pg.display.set_mode((texture_width, texture_height))
    screen.blit(generated_texture, (0,0))
    pg.display.flip()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
    pg.quit()
