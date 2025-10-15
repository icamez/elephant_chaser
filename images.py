import pygame
import os.path
import sys
import colors


class ImageLibrary:
    def __init__(self):
        def load(file_name):
            full_file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images", file_name)
            image = pygame.image.load(full_file_name).convert_alpha()
            #image.set_colorkey(colors.white, pygame.RLEACCEL)
            return image

        def clip(source_image, rect):
            image = source_image.subsurface(rect)
            return image

        self.giraffe  = load("giraffe.png")
        self.elephant = load("elephant.png")
        self.sloth    = load("sloth.png")

        self.enemies  = load("enemies.png").convert()
        self.enemies.set_colorkey((127, 127, 127))

        def get_enemy(rect):
            image = clip(self.enemies, rect)
            return image

        self.beams = load("beams.png")
        self.beams.set_colorkey((0, 0, 0))

        def get_beam(rect):
            image = clip(self.beams, rect)
            return image

        self.green_slime = get_enemy((5 , 110, 29, 22))
        self.red_slime   = get_enemy((42, 110, 29, 22))
        self.blue_slime  = get_enemy((79, 110, 29, 22))

        self.green_snake  = get_enemy((7  , 160, 48, 59))
        self.brown_snake  = get_enemy((66 , 160, 48, 59))
        self.yellow_snake = get_enemy((130, 160, 48, 59))

        self.green_goblin = get_enemy((8,  243, 51, 59))
        self.blue_goblin  = get_enemy((63, 243, 51, 59))
        self.brown_goblin = get_enemy((121, 243, 51, 59))

        self.white_cocatrice  = get_enemy((12,  327, 48, 70))
        self.purple_cocatrice = get_enemy((70,  327, 48, 70))
        self.yellow_cocatrice = get_enemy((127, 327, 48, 70))

        self.green_lizard  = get_enemy((2  , 420, 61, 49))
        self.red_lizard    = get_enemy((68 , 420, 61, 49))
        self.orange_lizard = get_enemy((137, 420, 61, 49))

        self.grey_rat  = get_enemy((5  , 496, 65, 57))
        self.brown_rat = get_enemy((74 , 496, 65, 57))
        self.white_rat = get_enemy((144, 496, 65, 57))

        self.red_scorpion    = get_enemy((8  , 583, 49, 68))
        self.yellow_scorpion = get_enemy((66 , 583, 49, 68))
        self.black_scorpion  = get_enemy((123, 583, 49, 68))

        self.grey_wolf  = get_enemy((5  , 683, 49, 58))
        self.brown_wolf = get_enemy((62 , 683, 49, 58))
        self.blue_wolf  = get_enemy((117, 683, 49, 58))

        self.blue_ghost  = get_enemy((3  , 769, 57, 56))
        self.brown_ghost = get_enemy((63 , 769, 57, 56))
        self.green_ghost = get_enemy((123, 769, 57, 56))

        self.green_dragon  = get_enemy((3  , 847, 100, 73))
        self.red_dragon    = get_enemy((106, 847, 100, 73))
        self.purple_dragon = get_enemy((211, 847, 100, 73))

        self.blue_circle_bullet = get_beam((205, 110, 14, 14))
        self.stone_wall = load("stone_wall.png")

        def load_star_coin(num):
            file_name = os.path.join("star coin rotate", "star coin rotate " + str(num) + ".png")
            image = load(file_name)
            image = pygame.transform.scale(image, (image.get_width() // 50, image.get_height() // 50))
            return image

        self.coin_images = []
        for counter in range(1, 7):
            self.coin_images.append(load_star_coin(counter))
        coin_width = self.coin_images[0].get_width()
        coin_height = self.coin_images[0].get_height()
        coin_rect = self.coin_images[0].get_rect()
        for i in range(1, 6):
            new_image = pygame.Surface((coin_width, coin_height), pygame.SRCALPHA)
            new_image.fill((0, 0, 0, 0))
            image = self.coin_images[i]
            new_image.blit(image, ( (coin_width - image.get_width()) // 2, 0 ))
            self.coin_images[i] = new_image.convert_alpha()


