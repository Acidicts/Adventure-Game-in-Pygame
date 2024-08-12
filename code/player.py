import pygame
from pygame import Vector2

from settings import *


class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups, obstacle_sprites):
		# noinspection PyTypeChecker
		super().__init__(groups)
		self.image = pygame.image.load(BASE_PATH + 'graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.copy().inflate(0, -26)

		self.direction = Vector2(0, 0)
		self.speed = 5

		self.obstacle_sprites = obstacle_sprites

	def input(self):
		keys = pygame.key.get_pressed()

		self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
		self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

	def move(self, speed):
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

	def update(self):
		self.input()
		self.move(self.speed)
