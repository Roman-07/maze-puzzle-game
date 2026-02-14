import pygame

class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, position, direction, speed, damage, max_range):
        super().__init__()
        # Set the position as a vector, with position being the centre of the player image
        self.position = pygame.math.Vector2((position.x + 16, position.y + 16))
        self.speed = speed
        self.damage = damage
        self.max_range = max_range
        self.distance_traveled = 0
        self.is_active = True

        # Set the direction vector based on direction.
        if direction == "up":
            self.unit_direction_vector = pygame.math.Vector2(0, -1)
        elif direction == "down":
            self.unit_direction_vector = pygame.math.Vector2(0, 1)
        elif direction == "left":
            self.unit_direction_vector = pygame.math.Vector2(-1, 0)
        elif direction == "right":
            self.unit_direction_vector = pygame.math.Vector2(1, 0)
        else:
            self.unit_direction_vector = pygame.math.Vector2(0, 0)

        # Load the bullet image and set up its rect.
        self.image = pygame.image.load("Sprites\\Bullet.png").convert_alpha()
        self.rect = self.image.get_rect(center=self.position)
        self.collision_rect = self.rect


    def update(self, dt, collision_manager, audio_manager, enemy_sprites):
        # Update bullet position, check range, and handle collisions.
        # Calculate displacement based on direction vector, speed, and elapsed time.
        displacement = self.unit_direction_vector * self.speed * dt
        self.position += displacement
        self.distance_traveled += displacement.length()
        self.rect.center = self.position
        self.collision_rect = self.rect

        # Check if bullet exceeded its maximum range.
        if self.distance_traveled >= self.max_range:
            self.is_active = False

        # Check collision with walls (if provided).
        collisions = collision_manager.check_wall_collisions(self)
        if collisions:
            self.is_active = False
        
        # Check collisions with enemies
        for enemy in enemy_sprites.copy():
            if collision_manager.check_sprite_collision(self, enemy):
                enemy.takeDamage(self.damage)
                audio_manager.playSoundEffect("bullet_hit")
                self.is_active = False