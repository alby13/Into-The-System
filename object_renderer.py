import pygame as pg
from settings import *


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
        try:
            self.circuit_texture = self.get_texture('resources/textures/circuit_board.png', (TEXTURE_SIZE, TEXTURE_SIZE))
        except pg.error as e:
            print(f"Warning: Could not load circuit_board.png: {e}")
            self.circuit_texture = None

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
        # Sky
        pg.draw.rect(self.screen, (0, 0, 0), (0, 0, WIDTH, HALF_HEIGHT))
        # Floor - Tiled circuit board
        if self.circuit_texture: # Check if the texture was loaded successfully
            texture_width = self.circuit_texture.get_width()
            texture_height = self.circuit_texture.get_height()

            if texture_width > 0 and texture_height > 0: # Ensure dimensions are valid
                for x in range(0, WIDTH, texture_width):
                    for y in range(HALF_HEIGHT, HEIGHT, texture_height):
                        self.screen.blit(self.circuit_texture, (x, y))
            else: # Fallback if texture has zero dimensions
                pg.draw.rect(self.screen, (0,0,0), (0, HALF_HEIGHT, WIDTH, HEIGHT))
        else: # Fallback if self.circuit_texture is None (failed to load)
            pg.draw.rect(self.screen, (0,0,0), (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        WIREFRAME_COLOR = (0, 255, 0)  # Green
        for item in list_objects:
            if len(item) == 5:  # Wall segment
                depth, x_screen, y_top, y_bottom, texture_id = item
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