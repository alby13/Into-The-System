import pygame as pg
from settings import *
from procedural_textures import generate_circuit_floor_texture, generate_ceiling_texture


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.win_image = self.get_texture('resources/textures/win.png', RES)
        # self.circuit_texture = self.get_texture('resources/textures/circuit_board.png', (TEXTURE_SIZE, TEXTURE_SIZE))
        self.procedural_floor_texture = generate_circuit_floor_texture(TEXTURE_SIZE * 2, TEXTURE_SIZE * 2)
        self.procedural_ceiling_texture = generate_ceiling_texture(TEXTURE_SIZE * 2, TEXTURE_SIZE * 2)
        self.wall_pattern = self._create_wall_pattern_surface()

    def _create_wall_pattern_surface(self, width=32, height=32):
        pattern_surface = pg.Surface((width, height), pg.SRCALPHA) # Use SRCALPHA for potential transparency
        pattern_surface.fill((0, 0, 0, 0)) # Transparent background initially

        # Define some pattern colors
        line_color = (0, 50, 0, 150) # Dark, semi-transparent green for subtlety
        dot_color = (0, 70, 70, 100) # Dark, semi-transparent cyan for accents

        # Draw a simple pattern (e.g., grid lines and dots)
        for i in range(0, width, 8):
            pg.draw.line(pattern_surface, line_color, (i, 0), (i, height), 1)
        for i in range(0, height, 8):
            pg.draw.line(pattern_surface, line_color, (0, i), (width, i), 1)

        for x_coord in range(4, width, 8): # Renamed x to x_coord to avoid conflict
            for y_coord in range(4, height, 8): # Renamed y to y_coord to avoid conflict
                pg.draw.circle(pattern_surface, dot_color, (x_coord, y_coord), 1)

        return pattern_surface

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()

    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        # Ceiling rendering with procedural texture
        if self.procedural_ceiling_texture: # Check if texture was generated
            texture_width = self.procedural_ceiling_texture.get_width()
            texture_height = self.procedural_ceiling_texture.get_height()

            if texture_width > 0 and texture_height > 0: # Ensure dimensions are valid
                for x in range(0, WIDTH, texture_width):
                    for y in range(0, HALF_HEIGHT, texture_height): # Iterate up to HALF_HEIGHT
                        self.screen.blit(self.procedural_ceiling_texture, (x, y))
            else: # Fallback
                pg.draw.rect(self.screen, (5,5,10), (0, 0, WIDTH, HALF_HEIGHT)) # Dark blue fallback
        else: # Fallback if texture is None
            pg.draw.rect(self.screen, (5,5,10), (0, 0, WIDTH, HALF_HEIGHT)) # Dark blue fallback

        # Floor rendering with procedural texture
        if self.procedural_floor_texture: # Check if the texture was generated successfully
            texture_width = self.procedural_floor_texture.get_width()
            texture_height = self.procedural_floor_texture.get_height()

            if texture_width > 0 and texture_height > 0: # Ensure dimensions are valid
                # Tile the texture across the floor area (bottom half of the screen)
                for x in range(0, WIDTH, texture_width):
                    for y in range(HALF_HEIGHT, HEIGHT, texture_height):
                        self.screen.blit(self.procedural_floor_texture, (x, y))
            else: # Fallback if texture has zero dimensions
                pg.draw.rect(self.screen, (0,10,0), (0, HALF_HEIGHT, WIDTH, HEIGHT)) # Dark green fallback
        else: # Fallback if self.procedural_floor_texture is None
            pg.draw.rect(self.screen, (0,10,0), (0, HALF_HEIGHT, WIDTH, HEIGHT)) # Dark green fallback

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        WIREFRAME_COLOR = (0, 255, 0)  # Green
        for item in list_objects:
            if len(item) == 5:  # Wall segment
                depth, x_screen, y_top, y_bottom, texture_id = item
                wall_height = y_bottom - y_top
                # Draw black filled rectangle for opacity
                pg.draw.rect(self.screen, (0, 0, 0), (x_screen, y_top, SCALE, wall_height))

                # Tile the wall pattern onto the black rectangle
                pattern_w = self.wall_pattern.get_width()
                pattern_h = self.wall_pattern.get_height()

                if pattern_w > 0 and pattern_h > 0: # Ensure pattern is valid
                    for tile_x in range(0, SCALE, pattern_w):
                        for tile_y in range(0, wall_height, pattern_h):
                            # Calculate actual screen position for the tile
                            blit_x = x_screen + tile_x
                            blit_y = y_top + tile_y

                            # Clip the pattern if it goes beyond the wall segment boundaries
                            clip_width = min(pattern_w, SCALE - tile_x)
                            clip_height = min(pattern_h, wall_height - tile_y)

                            if clip_width > 0 and clip_height > 0:
                                 self.screen.blit(self.wall_pattern, (blit_x, blit_y), area=(0, 0, clip_width, clip_height))

                # Draw green wireframe line over the black rectangle and pattern
                pg.draw.line(self.screen, WIREFRAME_COLOR, (x_screen, y_top), (x_screen, y_bottom), 1)
            elif len(item) == 3:  # Sprite
                depth, image, pos = item
                self.screen.blit(image, pos)
            else:
                # Optional: Log unexpected item types, though this should ideally not happen.
                print(f"Warning: Encountered item with unexpected length in rendering list: {len(item)}")

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)