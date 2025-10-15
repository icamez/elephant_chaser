import pygame
import sys
import random
import colors
import images
import sounds

class GameObject(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.direction_x = 0
        self.direction_y = 0
        self.speed = 0
        self.game = game
        self.game.add_object(self)
        self.color = colors.yellow
        self.image = None
        self.image_left = None
        self.image_right = None
        self.mask = None
        self.mask_left = None
        self.mask_right = None
        self.health = 1

    def draw(self, window):
        if self.image is not None:
            window.blit(self.image, self.get_rect())
        else:
            print("object " + self.__class__.__name__ + " is drawing")

    def set_image(self, image, mask=None, width=None, height=None):
        if width is not None:
            self.set_size(width, height)
            self.image = image.copy()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        else:
            self.set_size(image.get_width(), image.get_height())
            self.image = image
        if mask is not None:
            self.mask = mask
        else:
            self.mask = pygame.mask.from_surface(self.image)
        self.image_left = None
        self.image_right = None
        self.mask_left = None
        self.mask_right = None

    def set_image_right(self, image, mask=None):
        self.set_size(image.get_width(), image.get_height())
        self.image = image
        self.image_right = image
        self.image_left = pygame.transform.flip(image, True, False)
        if mask is not None:
            self.mask = mask
            self.mask_right = mask
        else:
            self.mask = pygame.mask.from_surface(self.image)
            self.mask_right = self.mask
        self.mask_left = pygame.mask.from_surface(self.image_left)


    @property
    def rect(self):
        return self.get_rect()

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def set_directions(self, x, y):
        self.direction_x = x
        self.direction_y = y
        if self.direction_x < 0 and self.image_left is not None:
            self.image = self.image_left
            self.mask = self.mask_left
        if self.direction_x > 0 and self.image_right is not None:
            self.image = self.image_right
            self.mask = self.mask_right

    def set_size(self, width, height):
        self.width = width
        self.height = height

    def set_health(self, health):
        self.health = health

    def bounce(self):
        self.set_directions(-self.direction_x, -self.direction_y)

    def bounce_random(self):
        dir = random.randint(0, 3)
        if dir == 0:
            self.set_directions(0, -1)
        elif dir == 1:
            self.set_directions(1, 0)
        elif dir == 2:
            self.set_directions(0, 1)
        else:
            self.set_directions(-1, 0)

    def move(self):
        # move object
        r = self.get_rect()
        r.left += self.speed * self.direction_x
        r.top += self.speed * self.direction_y
        if self.game.game_rect.contains(r):
            collided_obj = self.game.find_collided_object(r, self)
            if collided_obj is None:
                self.set_pos(r.left, r.top)
            else:
                if collided_obj.hit_by(self, r):
                    self.set_pos(r.left, r.top)
                else:
                    pass
        else:
            if self.hit_boundary(r):
                self.set_pos(r.left, r.top)

    def set_speed(self, speed):
        if speed < 0:
            speed = 0
        if speed > 10:
            speed = 10
        self.speed = speed

    def set_color(self, color):
        self.color = color

    def update(self):
        self.move()

    # hit methods

    def hit_by(self, obj, r):
        """
        obj collided object:
        return: false if move isn't allowed
        """
        return False

    def hit_boundary(self, r):
        self.bounce()
        return False

    def hit_object(self, obj, r):
        return False

    def hit_block(self, block, r):
        return self.hit_object(block, r)

    def hit_man(self, man, r):
        return False

    def hit_giraffe(self, giraffe, r):
        return self.hit_animal(giraffe, r)

    def hit_elephant(self, elephant, r):
        return self.hit_animal(elephant, r)

    def hit_sloth(self, sloth, r):
        return self.hit_animal(sloth, r)

    def hit_animal(self, animal, r):
        return self.hit_object(animal, r)

    def hit_doubloon(self, doubloon, r):
        return self.hit_object(doubloon, r)

    def hit_bullet(self, bullet, r):
        return self.hit_object(bullet, r)

    def hit_enemy(self, enemy, r):
        return self.hit_object(enemy, r)

    def hit_dragon(self, dragon, r):
        return self.hit_enemy(dragon, r)

    def hit_lizard(self, lizard, r):
        return self.hit_enemy(lizard, r)

    def hit_rat(self, rat, r):
        return self.hit_enemy(rat, r)

    def hit_ghost(self, ghost, r):
        return self.hit_enemy(ghost, r)


class Animal(GameObject):
    def __init__(self, game):
        super().__init__(game)
        self.set_speed(1)

    def hit_by(self, obj, r):
        return obj.hit_animal(self, r)

    def hit_doubloon(self, doubloon, r):
        doubloon.kill()
        return True

    def hit_block(self, block, r):
        self.bounce_random()
        return False

    def hit_enemy(self, enemy, r):
        self.kill()
        return False

    def hit_animal(self, animal, r):
        self.bounce_random()
        return False

    def hit_man(self, man, r):
        man.hit_animal(self, r)


class Giraffe(Animal):
    def __init__(self, game):
        super().__init__(game)
        game.giraffes.add(self)
        self.set_image(game.library.giraffe, None, 50, 50)

    def hit_by(self, obj, r):
        return obj.hit_giraffe(self, r)


class Elephant(Animal):
    def __init__(self, game):
        super().__init__(game)
        game.elephants.add(self)
        self.set_image(game.library.elephant, None, 50, 50)

    def hit_by(self, obj, r):
        return obj.hit_elephant(self, r)


class Sloth(Animal):
    def __init__(self, game):
        super().__init__(game)
        game.sloths.add(self)
        self.set_image(game.library.sloth, None, 50, 50)

    def hit_by(self, obj, r):
        return obj.hit_sloth(self, r)


class Enemy(GameObject):
    def __init__(self, game, image):
        super().__init__(game)
        game.enemies.add(self)
        self.set_image_right(image)

    def hit_by(self, obj, r):
        return obj.hit_enemy(self, r)

    def hit_block(self, block, r):
        self.bounce_random()
        return False

    def hit_man(self, man, r):
        return man.hit_enemy(man, r)

    def hit_doubloon(self, doubloon, r):
        doubloon.kill()
        return True

    def hit_animal(self, animal, r):
        animal.kill()
        return True

    def hit_bullet(self, bullet, r):
        self.game.sound_library.explosion_4.play()
        self.game.kill_enemy(self)
        bullet.kill()
        return False


class Dragon(Enemy):
    def __init__(self, game):
        image = game.library.purple_dragon
        super().__init__(game, image)
        game.dragons.add(self)
        self.set_speed(2)

    def hit_by(self, obj, r):
        return obj.hit_dragon(self, r)


class Lizard(Enemy):
    def __init__(self, game):
        image = game.library.red_lizard
        super().__init__(game, image)
        game.lizards.add(self)
        self.set_speed(1)

    def hit_by(self, obj, r):
        return obj.hit_lizard(self, r)


class Rat(Enemy):
    def __init__(self, game):
        image = game.library.brown_rat
        super().__init__(game, image)
        game.rats.add(self)
        self.set_speed(1)

    def hit_by(self, obj, r):
        return obj.hit_rat(self, r)


class Ghost(Enemy):
    def __init__(self, game):
        image = game.library.blue_ghost
        super().__init__(game, image)
        game.ghosts.add(self)
        self.set_speed(1)

    def hit_by(self, obj, r):
        return obj.hit_rat(self, r)


class ManObject(GameObject):
    def __init__(self, game):
        super().__init__(game)
        self.scale = 8
        self.set_size(300 // self.scale, 400 // self.scale)
        self.set_speed(3)
        self.set_image(self.create_man_image())
        #? / /\/\/\"_"\/\/\/\/\/ \ ?#

    def create_man_image(self):
        new_image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        new_image.fill((0, 0, 0, 0))
        self.draw_man(new_image, self.color, 0, 0)
        new_image = new_image.convert_alpha()
        return new_image

    def draw_man(self, window, color, x, y):
        def s(p):
            return int(p / self.scale)

        pygame.draw.line(window, color, (x + s(150), y + s(200)), (x + s(150), y + s(50)), s(25))
        pygame.draw.line(window, color, (x + s(150), y + s(200)), (x + s(25), y + s(400)), s(25))
        pygame.draw.line(window, color, (x + s(150), y + s(200)), (x + s(275), y + s(400)), s(25))
        pygame.draw.line(window, color, (x + s(150), y + s(150)), (x + s(300), y + s(100)), s(25))
        pygame.draw.line(window, color, (x + s(150), y + s(150)), (x + s(0), y + s(100)), s(25))
        pygame.draw.circle(window, color, (x + s(150), y + s(50)), s(50), s(0))

    #def draw(self, window):
    #    self.draw_man(window, self.color, self.x, self.y)

    def hit_by(self, obj, r):
        return obj.hit_man(self, r)

    def hit_doubloon(self, doubloon, r):
        self.game.pick_doubloon(doubloon)
        return True

    def hit_boundary(self, r):
        return False

    def hit_animal(self, animal, r):
        animal.bounce_random()
        return False

    def fire_bullet(self):
        if self.direction_x == 0 and self.direction_y == 0:
            return
        self.game.sound_library.gun_fire.play()
        bullet = Bullet(self.game)
        bullet.set_directions(self.direction_x, self.direction_y)
        bullet.set_speed(self.speed + 5)

        r = self.get_rect()
        bullet_rect = bullet.get_rect()
        bullet_rect.centerx = r.centerx + self.direction_x * (r.width + bullet_rect.width + 1) // 2
        bullet_rect.centery = r.centery + self.direction_y * (r.height + bullet_rect.height + 1) // 2
        bullet.set_pos(bullet_rect.left, bullet_rect.top)

    def hit_enemy(self, enemy, r):
        self.game.sound_library.explosion_1.play()
        self.game.game_over()


class BlockObject(GameObject):
    def __init__(self, game):
        super().__init__(game)
        game.blocks.add(self)
        self.set_image(self.game.library.stone_wall)
        #self.set_size(50, 50)
        #self.set_color(colors.red)
        self.set_health(30)

    #def draw(self, window):
    #    pygame.draw.rect(window, self.color, self.get_rect())

    def hit_by(self, obj, r):
        return obj.hit_block(self, r)

    def hit_bullet(self, bullet, r):
        self.health -= 1
        if self.health <= 0:
            self.kill()
        bullet.kill()


class GoldDoubloon(GameObject):
    def __init__(self, game):
        super().__init__(game)
        game.doubloons.add(self)
        self.set_size(25, 25)
        self.set_color(colors.yellow)
        self.images = game.library.coin_images
        self.cur_image_index = 0
        self.set_image(self.images[0])
        self.update_counter = 0

    #def draw(self, window):
    #    pygame.draw.circle(window, self.color, (self.x + self.width // 2, self.y + self.height // 2), self.width // 2, 0)

    def update(self):
        super().update()
        self.update_counter += 1
        if self.update_counter >= 10:
            self.update_counter = 0
            self.cur_image_index += 1
            if self.cur_image_index >= len(self.images):
                self.cur_image_index = 0
            self.set_image(self.images[self.cur_image_index])

    def hit_by(self, obj, r):
        return obj.hit_doubloon(self, r)


class Bullet(GameObject):
    def __init__(self, game):
        super().__init__(game)
        game.bullets.add(self)
        self.set_image(self.game.library.blue_circle_bullet)
        #self.set_size(5, 5)
        #self.set_color(colors.black)

    #def draw(self, window):
    #    pygame.draw.ellipse(window, self.color, self.get_rect())

    def hit_by(self, obj, r):
        return obj.hit_bullet(self, r)

    def hit_boundary(self, r):
        self.kill()
        return False

    def hit_bullet(self, bullet, r):
        self.kill()
        return False

    def hit_doubloon(self, doubloon, r):
        self.game.pick_doubloon(doubloon)
        self.kill()
        return False

    def hit_enemy(self, enemy, r):
        return enemy.hit_bullet(self, r)

    def hit_block(self, block, r):
        self.kill()
        return False

    def hit_animal(self, animal, r):
        self.kill()
        return False

    def hit_block(self, block, r):
        return block.hit_bullet(self, r)


class Game:
    def __init__(self, title):
        self.clock = pygame.time.Clock()
        self.title = title
        self.objects = pygame.sprite.Group()
        self.doubloons = pygame.sprite.Group()
        self.giraffes = pygame.sprite.Group()
        self.elephants = pygame.sprite.Group()
        self.sloths = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.dragons = pygame.sprite.Group()
        self.lizards = pygame.sprite.Group()
        self.rats = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()

        self.game_rect = pygame.Rect(0, 0, 1000, 800)
        self.info_rect = pygame.Rect(self.game_rect.right, self.game_rect.top, 300, self.game_rect.height)
        self.window_size = (self.info_rect.right, self.info_rect.height)
        self.window = pygame.display.set_mode(self.window_size, 0, 32)
        self.library = images.ImageLibrary()
        self.sound_library = sounds.SoundLibrary()
        pygame.display.set_caption(self.title)
        self.game_background = colors.hi
        self.info_background = colors.aqua
        self.info_color = colors.yellow
        self.info_font = pygame.font.SysFont("Comic Sans MS", 35)

        self.doubloon_counter = 0
        self.enemies_killed = 0
        self.level = 0
        self.man = None
        self.active = True

    def find_collided_object(self, rect, obj):
        for cur_obj in self.objects:
            if cur_obj is not obj:
                r = cur_obj.get_rect()
                if r.colliderect(rect):
                    return cur_obj
        return None

    def place_random(self, obj):
        while True:
            x = random.randint(self.game_rect.left, self.game_rect.right - obj.width)
            y = random.randint(self.game_rect.top, self.game_rect.bottom - obj.height)
            obj.set_pos(x, y)
            collided_obj = self.find_collided_object(obj.get_rect(), obj)
            if collided_obj is None:
                return

    def create_level_objects(self):
        for i in range(0, self.level):
            elephant = Elephant(self)
            elephant.set_directions(1, 0)
            elephant.set_speed(2)
            self.place_random(elephant)

            giraffe = Giraffe(self)
            giraffe.set_directions(0, -1)
            self.place_random(giraffe)

            sloth = Sloth(self)
            sloth.set_directions(1, 0)
            sloth.set_speed(1)
            self.place_random(sloth)

            dragon = Dragon(self)
            dragon.set_directions(1, 0)
            self.place_random(dragon)

            lizard = Lizard(self)
            lizard.bounce_random()
            self.place_random(lizard)

            rat = Rat(self)
            rat.bounce_random()
            self.place_random(rat)

            ghost = Ghost(self)
            ghost.bounce_random()
            self.place_random(ghost)

        # add 10 blocks
        for block_number in range(1, 10):
            block = BlockObject(self)
            self.place_random(block)
        # add 20 doubloons
        for doubloon_number in range(1, 20):
            doubloon = GoldDoubloon(self)
            self.place_random(doubloon)

    def go_to_next_level(self):
        self.level += 1
        self.create_level_objects()

    def check_next_level(self):
        if len(self.enemies) == 0:
            self.go_to_next_level()

    def create_objects(self):
        self.man = ManObject(self)
        self.place_random(self.man)
        self.go_to_next_level()

    def print_line(self, message, line_number):
        text = self.info_font.render(message, True, self.info_color, self.info_background)
        text_r = text.get_rect()
        text_r.left = self.info_rect.left
        text_r.top = (line_number - 1) * text_r.height
        self.window.blit(text, text_r)

    def blank(self):
        self.window.fill(self.game_background)
        pygame.draw.rect(self.window, self.info_background, self.info_rect)
        self.print_line("hello player", 1)
        self.print_line("level: " + str(self.level), 2)
        self.print_line("doubloons: " + str(self.doubloon_counter), 3)
        self.print_line("enemies killed: " + str(self.enemies_killed), 4)

    def process_man_controls(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.man.set_directions(-1, 0)
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.man.set_directions(1, 0)
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.man.set_directions(0, 1)
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.man.set_directions(0, -1)
            if event.key == pygame.K_e:
                self.man.set_directions(0, 0)
                self.man.set_speed(0)
            if event.key == pygame.K_f or event.key == pygame.K_SPACE:
                self.man.fire_bullet()

            if event.key == pygame.K_z:
                self.man.set_speed(self.man.speed - 1)
            if event.key == pygame.K_c:
                self.man.set_speed(self.man.speed + 1)

    def run(self):
        while self.active:
            # handle pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                self.process_man_controls(event)
            self.update_objects()
            self.blank()
            self.draw_objects()
            pygame.display.update()
            self.check_next_level()
            self.clock.tick(60)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

    def update_objects(self):
        for obj in self.objects:
            obj.update()

    def move_objects(self):
        for obj in self.objects:
            obj.move()

    def draw_objects(self):
        for obj in self.objects:
            obj.draw(self.window)

    def add_object(self, obj):
        obj.game = self
        self.objects.add(obj)

    def pick_doubloon(self, doubloon):
        self.sound_library.picked_coin.play()
        self.doubloon_counter += 1
        doubloon.kill()

    def game_over(self):
        self.active = False

    def kill_enemy(self, enemy):
        enemy.kill()
        self.enemies_killed += 1


def run_elephant_chaser_game():
    pygame.init()
    game = Game("Elephant Chaser")
    game.create_objects()
    game.run()
