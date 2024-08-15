import pygame.font

from .settings import *


class UI:
    def __init__(self):

        self.weapons = []
        for weapons in weapon_data.values():
            path = weapons['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapons.append(weapon)

        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(f'Exp: {str(int(exp))}', False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(10, 10))

        self.display_surface.blit(text_surf, text_rect)

        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(10, 10), 3)

    def selection_box(self, left, top, has):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        if has:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 2)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 2)

        return bg_rect

    def weapon_box(self, weapon_index):
        player = weapon_index
        weapon_index = player.weapon_index

        rect = self.selection_box(10, 630, not player.can_switch_weapon)

        surf = self.weapons[weapon_index % len(self.weapons)]
        rect = surf.get_rect(center=rect.center)

        self.display_surface.blit(surf, rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        self.show_exp(player.exp)

        self.weapon_box(player)
