from .settings import *


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        # noinspection PyTypeChecker
        super().__init__(groups)
        direction = player.status.split('_')[0]

        self.player = player

        full_path = f'{BASE_PATH}graphics/weapons/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        if direction == 'down':
            self.rect = self.image.get_rect(midtop=self.player.rect.midbottom + Vector2())
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom=self.player.rect.midtop + Vector2())
        elif direction == 'left':
            self.rect = self.image.get_rect(midright=self.player.rect.midleft + Vector2(0, 16))
        elif direction == 'right':
            self.rect = self.image.get_rect(midleft=self.player.rect.midright + Vector2(0, 16))

        self.cooldown = None
        self.damage = None

        self.graphic = None
