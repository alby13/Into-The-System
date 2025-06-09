import pygame as pg


class Sound:
    def __init__(self, game):
        self.game = game
        try:
            pg.mixer.init()
        except pg.error as e:
            print(f"Warning: Could not initialize sound mixer: {e}")
            # Optionally, disable sound functionality
            self.game.sound_enabled = False
            return

        self.game.sound_enabled = True
        self.path = 'resources/sound/'
        self.shotgun = pg.mixer.Sound(self.path + 'shotgun.wav')
        self.npc_pain = pg.mixer.Sound(self.path + 'npc_pain.wav')
        self.npc_death = pg.mixer.Sound(self.path + 'npc_death.wav')
        self.npc_shot = pg.mixer.Sound(self.path + 'npc_attack.wav')
        self.npc_shot.set_volume(0.2)
        self.player_pain = pg.mixer.Sound(self.path + 'player_pain.wav')
        self.theme = pg.mixer.music.load(self.path + 'theme.mp3')
        pg.mixer.music.set_volume(0.3)

    def play_theme(self):
        if self.game.sound_enabled:
            pg.mixer.music.play(-1)
        else:
            print("Sound disabled, not playing theme.")

# It's good practice to ensure methods that use pg.mixer are also conditional
# For example, if you had a method like:
# def play_shotgun_sound(self):
#    if self.game.sound_enabled:
#        self.shotgun.play()

# And in Game class or wherever Sound methods are called:
# if self.sound.game.sound_enabled: # or just self.sound_enabled if Game tracks it
#    self.sound.play_theme()
#    self.sound.shotgun.play() # etc.
# This is a more robust way but for now, just preventing init crash is enough.