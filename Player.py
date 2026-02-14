import pygame
import time
import Bullet

class Player(pygame.sprite.Sprite):
    
    def __init__(self, position, speed, bullet_manager, audio_manager):
        super().__init__()
        # Use a Vector2 for precise position arithmetic.
        self.position = pygame.math.Vector2(position)
        self.default_speed = speed
        self.speed = speed
        self.direction = "down"
        self.bulletCount = 20
        self.shootingCooldown = 0.4  # seconds between shots
        self.lastShotTime = 0
        self.bullet_manager = bullet_manager
        self.audio_manager = audio_manager
        self.shooting_anim = True

        # Define key bindings using Pygame key constants.
        self.keyBindings = {
            "UP": pygame.K_w,
            "DOWN": pygame.K_s,
            "LEFT": pygame.K_a,
            "RIGHT": pygame.K_d,
            "SHOOT": pygame.K_SPACE
        }

        # Load animations. For simplicity, we assume each animation is a list of images.
        self.animations = {
            "idle": [
                pygame.image.load("Sprites/Player/Idle/down_1.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Idle/down_2.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Idle/down_3.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Idle/down_4.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Idle/down_5.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Idle/down_6.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Idle/down_7.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Idle/down_8.png").convert_alpha(),
            ],
            "walking_up": [
                pygame.image.load("Sprites/Player/Walking/up_1.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/up_2.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/up_3.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/up_4.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/up_5.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/up_6.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/up_7.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/up_8.png").convert_alpha(),
            ],
            "walking_down": [
                pygame.image.load("Sprites/Player/Walking/down_1.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/down_2.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/down_3.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/down_4.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/down_5.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/down_6.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/down_7.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/down_8.png").convert_alpha(),
            ],
            "walking_left": [
                pygame.image.load("Sprites/Player/Walking/left_1.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/left_2.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/left_3.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/left_4.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/left_5.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/left_6.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/left_7.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/left_8.png").convert_alpha(),
            ],
            "walking_right": [
                pygame.image.load("Sprites/Player/Walking/right_1.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/right_2.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/right_3.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/right_4.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/right_5.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/right_6.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/right_7.png").convert_alpha(),
                pygame.image.load("Sprites/Player/Walking/right_8.png").convert_alpha(),
            ],
            "shooting_up": [
                pygame.image.load("Sprites/Player/Shooting/up.png").convert_alpha(),
            ],
            "shooting_down": [
                pygame.image.load("Sprites/Player/Shooting/down.png").convert_alpha(),
            ],
            "shooting_left": [
                pygame.image.load("Sprites/Player/Shooting/left.png").convert_alpha(),
            ],
            "shooting_right": [
                pygame.image.load("Sprites/Player/Shooting/right.png").convert_alpha()
            ],
        }

        # Start with the idle animation image.
        self.image = self.animations["idle"][0]
        self.rect = self.image.get_rect(topleft=self.position)
        # The bounding box for collisions can be the same as the sprite's rect.
        self.collision_rect = pygame.Rect(
            self.position.x + 10,
            self.position.y + 6,
            self.rect.width - 20,
            self.rect.height - 10
        )
        
        # Variables for animation control
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.08  # seconds per frame
        
        # Whether player has reached the door
        self.door_reached = False
        
        # Variables to check if a power up needs to be applied
        self.speed_powerup = False
        self.speed_powerup_timer = 0
        self.collected_powerups = []
        self.powerup_duration = 10
        self.speed_boost_coeff = 1.35
        self.hp_boost_amount = 10
        
        # If player is inside the safe spot
        self.inside_safe_spot = False
        self.safe_spot_sound_played = False
        
        # Variable for puzzle management
        self.solving_puzzle = None


    def update(self, dt, collision_manager, enemy_sprites, health_system, audio_manager, puzzle_manager, current_level):
        self.collision_manager = collision_manager
        self.enemy_sprites = enemy_sprites
        """Update is called every frame."""
        self.updateMovement(health_system, audio_manager, puzzle_manager, current_level, dt)
        self.updateAnimation(dt)
        # Update the sprite's rect based on the new position.
        self.rect.topleft = self.position
        self.collision_rect = pygame.Rect(
            self.position.x + 10,
            self.position.y + 6,
            self.rect.width - 20,
            self.rect.height - 10
        )
 
 
    def get_grid_position(self):
        tile_position_x = int((self.position.x + 16) // 32)
        tile_position_y = int((self.position.y + 16 - 48) // 32)
        return (tile_position_x, tile_position_y)
    
    def teleport(self, teleport_position):
        self.position = pygame.math.Vector2(teleport_position)
        self.rect.topleft = self.position
        self.collision_rect = pygame.Rect(
            self.position.x + 10,
            self.position.y + 6,
            self.rect.width - 20,
            self.rect.height - 10
        )


    def updateMovement(self, health_system, audio_manager, puzzle_manager, current_level, dt):
        """Reads user input, updates the player's position, and prevents movement into walls."""
        keys = pygame.key.get_pressed()
        
        if self.solving_puzzle is not None:
            # do not move the player because a puzzle is being solved
            pass
        else:
            # Save the current position for collision resolution.
            prev_x = self.position.x
            prev_y = self.position.y

            # --- Process horizontal movement ---
            if keys[self.keyBindings["LEFT"]]:
                self.position.x -= self.speed * dt
                self.direction = "left"
            if keys[self.keyBindings["RIGHT"]]:
                self.position.x += self.speed * dt
                self.direction = "right"

            # Update the sprite's rect and collision rectangle.
            self.rect.topleft = self.position
            self.collision_rect = pygame.Rect(
                self.position.x + 10,
                self.position.y + 6,
                self.rect.width - 20,
                self.rect.height - 10
            )

            # Check for horizontal collisions with walls.
            wall_collisions = self.collision_manager.check_wall_collisions(self)
            enemy_collisions = []
            for enemy in self.enemy_sprites.copy():
                if self.collision_manager.check_sprite_collision(self, enemy):
                    enemy_collisions.append(1)
            
            if wall_collisions or enemy_collisions:
                # Revert horizontal movement by restoring the previous x value.
                self.position.x = prev_x
                self.rect.topleft = self.position
                self.collision_rect = pygame.Rect(
                self.position.x + 10,
                self.position.y + 6,
                self.rect.width - 20,
                self.rect.height - 10
                )

            # --- Process vertical movement ---
            # Save the y position after horizontal resolution.
            prev_y = self.position.y
            if keys[self.keyBindings["UP"]]:
                self.position.y -= self.speed * dt
                self.direction = "up"
            if keys[self.keyBindings["DOWN"]]:
                self.position.y += self.speed * dt
                self.direction = "down"

            # Update the rects again.
            self.rect.topleft = self.position
            self.collision_rect = pygame.Rect(
                self.position.x + 10,
                self.position.y + 6,
                self.rect.width - 20,
                self.rect.height - 10
            )

            # Check for vertical collisions with walls.
            wall_collisions = self.collision_manager.check_wall_collisions(self)
            enemy_collisions = []
            for enemy in self.enemy_sprites.copy():
                if self.collision_manager.check_sprite_collision(self, enemy):
                    enemy_collisions.append(1)
                    
            if wall_collisions or enemy_collisions:
                # Revert vertical movement by restoring the previous y value.
                self.position.y = prev_y
                self.rect.topleft = self.position
                self.collision_rect = pygame.Rect(
                self.position.x + 10,
                self.position.y + 6,
                self.rect.width - 20,
                self.rect.height - 10
                ) 
            
            # Update the power up timer if the power up is active. HP does not need one
            if self.speed_powerup == True:
                self.speed_powerup_timer += dt

            # Check if the power up duration has expired. HP does not need one
            if self.speed_powerup_timer > self.powerup_duration:
                self.speed_powerup = False
                self.speed_powerup_timer = 0
                self.speed = self.default_speed
                audio_manager.playSoundEffect("power_down")
                
            # Check if the player reached a power-up. Verify that it is new and not collected before.
            speed_powerup_collisions = self.collision_manager.check_speed_powerup_collisions(self)
            if speed_powerup_collisions:
                for rect in speed_powerup_collisions:
                    if rect not in self.collected_powerups:
                        self.collected_powerups.append(rect)
                        self.speed_powerup = True
                        self.speed_powerup_timer = 0
                        self.speed = self.default_speed * self.speed_boost_coeff
                        audio_manager.playSoundEffect("power_up_speed")
                
            hp_powerup_collisions = self.collision_manager.check_hp_powerup_collisions(self)
            if hp_powerup_collisions:
                for rect in hp_powerup_collisions:
                    if rect not in self.collected_powerups:
                        self.collected_powerups.append(rect)
                        health_system.heal(self.hp_boost_amount)
                        audio_manager.playSoundEffect("power_up_hp")
                        
                        
            # Check if the player reached a safe spot. It will return a list of rects (will be an empty list if no collision).
            safe_spot_collisions = self.collision_manager.check_safe_spot_collisions(self)
            if safe_spot_collisions:
                if self.safe_spot_sound_played == False:
                    audio_manager.playSoundEffect("safe_spot")
                    self.safe_spot_sound_played = True
                self.inside_safe_spot = True
            else:
                self.inside_safe_spot = False
                self.safe_spot_sound_played = False
                
                
            # Check if a puzzle needs to be opened
            puzzle_tiles = list(puzzle_manager.puzzle_details[f'level_{current_level}'].keys())
            for puzzle_coord in puzzle_tiles:
                collision_rect = pygame.Rect(puzzle_coord[0], puzzle_coord[1], 32, 32)
                if pygame.Rect.colliderect(self.collision_rect, collision_rect):
                    if puzzle_manager.puzzle_details[f'level_{current_level}'][puzzle_coord]['attempts_left'] == 0:
                        continue
                    self.solving_puzzle = puzzle_coord
                    puzzle_manager.load_puzzle(puzzle_coord, current_level)
                    audio_manager.playSoundEffect("puzzle_enter")
                
                
            # Check if the player reached the door. It will return a list of rects (will be an empty list if no collision).
            if self.collision_manager.check_door_collision(self):
                self.door_reached = True

            if keys[self.keyBindings["SHOOT"]]:
                self.shoot()         
            
            
    def shoot(self):
        current_time = time.time() # Alternatively, I can use pygame.time.get_ticks()/1000.
        if self.bulletCount == 0 and (current_time - self.lastShotTime) > self.shootingCooldown:
            self.shooting_anim = False
        if self.bulletCount > 0 and (current_time - self.lastShotTime) > self.shootingCooldown:
            self.bulletCount -= 1
            # Initialise a bullet at the player's position moving in self.direction.
            bullet = Bullet.Bullet(self.position, self.direction, speed=250, damage=25, max_range=500)
            self.bullet_manager.add_bullet(bullet)
            self.lastShotTime = current_time
            # Play shooting sound which lasts ~0.5 second
            self.audio_manager.playSoundEffect("shoot")


    def updateAnimation(self, dt):
        """ Update the player's animation based on movement and direction."""
        keys = pygame.key.get_pressed()
        # A flag variable useful for later
        space_pressed = False
        # If Space was pressed and animation can be played (validation)
        if keys[self.keyBindings["SHOOT"]] and self.shooting_anim > 0:
            space_pressed = True
            if self.direction == "up":
                anim = self.animations["shooting_up"]
            elif self.direction == "down":
                anim = self.animations["shooting_down"]
            elif self.direction == "left":
                anim = self.animations["shooting_left"]
            elif self.direction == "right":
                anim = self.animations["shooting_right"]
                
        # Determine if the player is moving.
        elif (keys[self.keyBindings["UP"]] or keys[self.keyBindings["DOWN"]] or 
            keys[self.keyBindings["LEFT"]] or keys[self.keyBindings["RIGHT"]]):
            if self.direction == "up":
                anim = self.animations["walking_up"]
            elif self.direction == "down":
                anim = self.animations["walking_down"]
            elif self.direction == "left":
                anim = self.animations["walking_left"]
            elif self.direction == "right":
                anim = self.animations["walking_right"]
            else:
                anim = self.animations["idle"]
            # TODO: Add shooting animation check.
        else:
            # If not moving, show the idle animation
            anim = self.animations["idle"]
            
        # If space was pressed, just display the single animation
        if space_pressed == True:
            self.image = anim[0]
        else:
            # Update animation timer and frame.
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % len(anim)
            self.image = anim[self.animation_frame]


    def reset(self, starting_pos):
        self.position = pygame.math.Vector2(starting_pos)
        self.direction = "down"
        self.lastShotTime = 0
        self.shooting_anim = True
        self.door_reached = False
        self.speed_powerup = False
        self.collected_powerups = []
        self.speed_powerup_timer = 0
        self.solving_puzzle = None
        self.image = self.animations["idle"][0]
        self.rect = self.image.get_rect(topleft=self.position)
        # The bounding box for collisions can be the same as the sprite's rect.
        self.collision_rect = pygame.Rect(
            self.position.x + 10,
            self.position.y + 6,
            self.rect.width - 20,
            self.rect.height - 10
        )
        self.bulletCount = 20