import pygame
from pygame import Vector2

from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack):
        # noinspection PyTypeChecker
        super().__init__(groups)

        self.animations = None
        self.animation_speed = 0.15

        self.import_player_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        self.image = pygame.image.load(BASE_PATH + 'graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy().inflate(0, -26)

        self.direction = Vector2(0, 0)
        self.speed = 5

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

        self.create_attack = create_attack
        self.destroy_attack = destroy_attack

        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]

        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.weapon_switch_cooldown = 200

        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 6}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 123
        self.speed = self.stats['speed']

    def import_player_assets(self):
        character_path = BASE_PATH + 'graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': [],
                           'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': []}

        for animation in self.animations.keys():
            full_path = character_path + animation + '/'

            self.animations[animation] = import_folder(full_path)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.attacking:
            self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
            self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

        if keys[pygame.K_SPACE] and not self.attacking:
            self.attack_time = pygame.time.get_ticks()
            self.attacking = True
            self.create_attack()

        if keys[pygame.K_LCTRL] and not self.attacking:
            self.attack_time = pygame.time.get_ticks()
            self.attacking = True

        if keys[pygame.K_q] and self.can_switch_weapon and not self.attacking:
            self.weapon_index += 1
            self.weapon = list(weapon_data.keys())[self.weapon_index % len(weapon_data.keys()) -1]

            self.can_switch_weapon = False
            self.weapon_switch_time = pygame.time.get_ticks()

    def get_status(self):
        if self.direction.magnitude() == 0 and not 'idle' in self.status and not self.attacking:
            dire = self.status.split('_')[0]
            self.status = dire + '_idle'

        if self.attacking and not 'attack' in self.status:
            self.direction.x = 0
            self.direction.y = 0
            dire = self.status.split('_')[0]
            self.status = dire + '_attack'

        if self.direction.x > 0 and self.direction.y == 0:
            self.status = 'right'
        elif self.direction.x < 0 and self.direction.y == 0:
            self.status = 'left'

        if self.direction.y > 0 and self.direction.x == 0:
            self.status = 'down'
        elif self.direction.y < 0 and self.direction.x == 0:
            self.status = 'up'

    def move(self, speed):
        if not self.attacking:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            self.hitbox.x += self.direction.x * speed
            self.collision('x')

            self.hitbox.y += self.direction.y * speed
            self.collision('y')

            self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'x':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left

                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'y':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top

                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        if self.weapon_switch_time:
            if current_time - self.weapon_switch_time >= self.weapon_switch_cooldown:
                self.can_switch_weapon = True
                self.weapon_switch_time = None

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.input()
        self.animate()

        self.get_status()
        self.cooldowns()

        self.move(self.speed)
