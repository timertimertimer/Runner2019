import pygame
from const import *


class AnimatedSprite(pygame.sprite.Sprite):
    modes = {
        0: (pygame.image.load('sprites/anim1.png'), pygame.image.load('sprites/anim1_1.png'), 8, 1),
        1: (pygame.image.load('sprites/anim2.png'), pygame.image.load('sprites/anim2_2.png'), 9, 1),
        2: (pygame.image.load('sprites/anim3.png'), pygame.image.load('sprites/anim3_3.png'), 7, 1)
    }

    def __init__(self, x, y, all_sprites, all_blocks):
        super().__init__(all_sprites)
        self.heightMode = 0
        self.mode = 0
        self.frames = []
        self.cur_frame = 0
        self.all_blocks = all_blocks
        self.HP = 3
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.changeMode(0)
        self.image = self.frames[self.cur_frame]
        self.rect.x = x
        self.rect.y = y - self.rect.h + CELL_SIZE + 3

    def cut_sheet(self, sheet, columns, rows):
        self.rect.h = sheet.get_height() // rows
        self.rect.w = sheet.get_width() // columns
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.rect.y += 10
        if pygame.sprite.spritecollideany(self, self.all_blocks) is not None:
            self.rect.y -= 10

    def changeMode(self, mode):
        self.frames = []
        self.cut_sheet(AnimatedSprite.modes[mode][self.heightMode], AnimatedSprite.modes[mode][2], AnimatedSprite.modes[mode][3])
        self.mode = mode

    def forward(self):
        if self.mode == 0:
            self.changeMode(1)
        self.rect.x += PLAYER_SPEED
        blocks = pygame.sprite.spritecollide(self, self.all_blocks, False)
        for block in blocks:
            if block.rect.y < self.rect.y + self.rect.h - 10:
                self.rect.x -= PLAYER_SPEED
                return False
        return True

    def stop(self):
        self.changeMode(0)
