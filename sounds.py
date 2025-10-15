import pygame
import os.path

class SoundLibrary:
    def __init__(self):
        def load(file_name):
            full_file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sounds", file_name)
            if os.path.exists(full_file_name):
                print("File %s exists" % full_file_name)
            else:
                print("File %s doesn't exist" % full_file_name)
            sound = pygame.mixer.Sound(full_file_name)
            return sound

        self.gun_fire = load("8bit_gunloop_explosion.wav")
        self.picked_coin = load("Coin 3.wav")
        self.explosion_4 = load("Explosion 4.wav")
        self.explosion_1 = load("Explosion 1.wav")