import pygame

class BulletManager:
    
    def __init__(self):
        # Create a sprite group for bullets.
        self.bullets = pygame.sprite.Group()

    def add_bullet(self, bullet):
        self.bullets.add(bullet)

    def update(self, dt, collision_manager, audio_manager, enemy_sprites):
        # Update all bullets and remove the ones that are no longer active.
        self.bullets.update(dt, collision_manager, audio_manager, enemy_sprites)
        for bullet in self.bullets.copy():
            if not bullet.is_active:
                self.bullets.remove(bullet)

    def draw(self, screen):
        self.bullets.draw(screen)