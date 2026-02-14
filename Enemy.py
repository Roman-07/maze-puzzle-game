import pygame
import time
import AStar_PathFinder
import Dijkstra_PathFinder

class Enemy(pygame.sprite.Sprite):
    # Define enemy type attributes
    enemyTypes = {
        "zombie": {"HP": 75, "speed": 72, "damage_amount": 10, "damage_frequency": 3, "detection_radius": 12},
        "skeleton": {"HP": 50, "speed": 56, "damage_amount": 15, "damage_frequency": 2, "detection_radius": 15},
    }
    
    def __init__(self, position, enemy_type="zombie"):
        super().__init__()
        # Validate enemy type; default to "zombie" if unknown.
        if enemy_type not in Enemy.enemyTypes:
            enemy_type = "zombie"
        self.enemy_type = enemy_type
        # Position as a vector for smooth movement.
        self.position = pygame.math.Vector2(position)   # Tuple (x, y) for spawn location.
        self.direction = "down"  # starting facing direction
        
        # Set attributes based on enemy type.
        attributes = Enemy.enemyTypes[self.enemy_type]
        self.HP = attributes["HP"]
        self.speed = attributes["speed"]
        self.damage_amount = attributes["damage_amount"]
        self.damage_frequency = attributes["damage_frequency"]
        self.detection_radius = attributes["detection_radius"]  # in tiles
        
        # Define all the animations for zombie and skeleton
        zombie_animations = {
            "idle_left": [
                pygame.image.load("Sprites/Zombie/Idle/left_1.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Idle/left_2.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Idle/left_3.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Idle/left_4.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Idle/left_5.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Idle/left_6.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Idle/left_7.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Idle/left_8.png").convert_alpha(),
            ],
            "idle_right": [
                pygame.image.load("Sprites/Zombie/Idle/right_1.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Idle/right_2.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Idle/right_3.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Idle/right_4.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Idle/right_5.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Idle/right_6.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Idle/right_7.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Idle/right_8.png").convert_alpha(),
            ],
            "walking_left": [
                pygame.image.load("Sprites/Zombie/Walking/left_1.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Walking/left_2.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Walking/left_3.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Walking/left_4.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Walking/left_5.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Walking/left_6.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Walking/left_7.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Walking/left_8.png").convert_alpha(),
            ],
            "walking_right": [
                pygame.image.load("Sprites/Zombie/Walking/right_1.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Walking/right_2.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Walking/right_3.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Walking/right_4.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Walking/right_5.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Walking/right_6.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Walking/right_7.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Walking/right_8.png").convert_alpha(),
            ],
            "attacking_left": [
                pygame.image.load("Sprites/Zombie/Attacking/left_1.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Attacking/left_2.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Attacking/left_3.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Attacking/left_4.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Attacking/left_5.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Attacking/left_6.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Attacking/left_7.png").convert_alpha(),
            ],
            "attacking_right": [
                pygame.image.load("Sprites/Zombie/Attacking/right_1.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Attacking/right_2.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Attacking/right_3.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Attacking/right_4.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Attacking/right_5.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Attacking/right_6.png").convert_alpha(),
                pygame.image.load("Sprites/Zombie/Attacking/right_7.png").convert_alpha(),
            ],
        }
    
        skeleton_animations = {
            "idle_left": [
                pygame.image.load("Sprites/Skeleton/Idle/left_1.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Idle/left_2.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Idle/left_3.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Idle/left_4.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Idle/left_5.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Idle/left_6.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Idle/left_7.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Idle/left_8.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Idle/left_9.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Idle/left_10.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Idle/left_11.png").convert_alpha(),
            ],
            "idle_right": [
                pygame.image.load("Sprites/Skeleton/Idle/right_1.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Idle/right_2.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Idle/right_3.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Idle/right_4.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Idle/right_5.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Idle/right_6.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Idle/right_7.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Idle/right_8.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Idle/right_9.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Idle/right_10.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Idle/right_11.png").convert_alpha(),
            ],
            "walking_left": [
                pygame.image.load("Sprites/Skeleton/Walking/left_1.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Walking/left_2.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Walking/left_3.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Walking/left_4.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Walking/left_5.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Walking/left_6.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Walking/left_7.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Walking/left_8.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Walking/left_9.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Walking/left_10.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Walking/left_11.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Walking/left_12.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Walking/left_13.png").convert_alpha(),
            ],
            "walking_right": [
                pygame.image.load("Sprites/Skeleton/Walking/right_1.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Walking/right_2.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Walking/right_3.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Walking/right_4.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Walking/right_5.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Walking/right_6.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Walking/right_7.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Walking/right_8.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Walking/right_9.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Walking/right_10.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Walking/right_11.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Walking/right_12.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Walking/right_13.png").convert_alpha(),
            ],
            "attacking_left": [
                pygame.image.load("Sprites/Skeleton/Attacking/left_1.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/left_2.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/left_3.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/left_4.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/left_5.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/left_6.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/left_7.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/left_8.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/left_9.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/left_10.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/left_11.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/left_12.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/left_13.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/left_14.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/left_15.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/left_16.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/left_17.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/left_18.png").convert_alpha(),
            ],
            "attacking_right": [
                pygame.image.load("Sprites/Skeleton/Attacking/right_1.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/right_2.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/right_3.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/right_4.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/right_5.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/right_6.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/right_7.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/right_8.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/right_9.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/right_10.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/right_11.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/right_12.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/right_13.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/right_14.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/right_15.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/right_16.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/right_17.png").convert_alpha(),
                pygame.image.load("Sprites/Skeleton/Attacking/right_18.png").convert_alpha(),
            ],
        }
        
        # TODO DESIGN ANIMATIONS FOR THE BOSS
        
        # Load animations for zombie or skleleton.
        if self.enemy_type == 'zombie':
            self.animations = zombie_animations
        elif self.enemy_type == 'skeleton':
            self.animations = skeleton_animations
        
        # Start with the idle animation image.
        self.image = self.animations["idle_right"][0]
        # ENEMIES WILL BE POSITIONED BY CENTER
        self.rect = self.image.get_rect(center=self.position)
        
        # For the sake of avoiding lags, reduce boundaries slightly
        self.collision_rect = pygame.Rect(0, 0, self.rect.width - 2, self.rect.height - 2)
        self.collision_rect.center = self.position
        
        # Variables for animation control
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1  # seconds per frame
        self.pursue_timer = 0 
        
        self.lastAttackTime = 0  # for managing attack frequency


    def update(self, dt, player, health_system, collision_manager, bullet_manager, audio_manager):
        self.updateBehaviour(player, collision_manager, health_system, bullet_manager, audio_manager, dt)
        self.updateAnimation(dt)
        # Update the rect and hitbox to match the new position.
        self.rect.center = self.position
        self.collision_rect = pygame.Rect(0, 0, self.rect.width - 2, self.rect.height - 2)
        self.collision_rect.center = self.position


    def updateBehaviour(self, player, collision_manager, health_system, bullet_manager, audio_manager, dt):
        # Calculate distance to the player.
        player_center = pygame.math.Vector2(player.position.x + 16, player.position.y + 16)
        distance_to_player = self.position.distance_to(player_center)
        # Convert detection_radius from tiles to pixels
        effective_radius = self.detection_radius * 32
        
        if distance_to_player <= effective_radius:
            if player.inside_safe_spot:
                self.idle()
            else:
                self.pursuePlayer(player, collision_manager, health_system, bullet_manager, audio_manager, dt)
        else:
            self.idle()

    
    def pursuePlayer(self, player, collision_manager, health_system, bullet_manager, audio_manager, dt):
        start = self.get_grid_position()  # Convert enemy position to grid coordinates.
        goal = player.get_grid_position()   # Convert player position to grid coordinates.
        start_midpoint = pygame.math.Vector2((start[0] * 32 + 16, start[1] * 32 + 16 + 48))    
        path = Dijkstra_PathFinder.dijkstra(collision_manager.map_grid, start, goal)
        # IMPLEMENTAION IF I USE A STAR LATER INSTEAD: write  A_STAR_PathFinder.a_star()
        
        # Save the current position for collision resolution.
        prev_x = self.position.x
        prev_y = self.position.y
        
        if path:
            # Move toward the next waypoint in the path.
            next_waypoint = pygame.math.Vector2((path[0][0] * 32 + 16, path[0][1] * 32 + 16 + 48))

            wall_collisions = collision_manager.check_wall_collisions(self)
            if wall_collisions:
                # Because there is a collision, I need to direct the enemy to the centre --> will be no collision
                direction_vector = (start_midpoint - self.position).normalize()
            else:
                direction_vector = (next_waypoint - self.position).normalize()
                
            self.position += direction_vector * self.speed * dt

            # Introducing it because there was a bug of lagging animations (quickly changing left-right)
            self.pursue_timer += dt
            if self.pursue_timer >= 2 * self.animation_speed:
                self.pursue_timer = 0
                # Update direction for animation purposes:
                if abs(direction_vector.x) > abs(direction_vector.y):
                    self.direction = "left" if direction_vector.x < 0 else "right"
                else:
                    self.direction = "up" if direction_vector.y < 0 else "down"

            # If player collides with enemy, return enemy to previous position
            if collision_manager.check_sprite_collision(self, player):
                self.position.x = prev_x
                self.position.y = prev_y
                self.rect.center = self.position
                self.collision_rect = pygame.Rect(0, 0, self.rect.width - 2, self.rect.height - 2)
                self.collision_rect.center = self.position
            
            # Check if a bullet hits the enemy
            for bullet in bullet_manager.bullets.copy():
                if collision_manager.check_sprite_collision(self, bullet):
                    self.takeDamage(bullet.damage)
                    audio_manager.playSoundEffect("bullet_hit")
                
            # If close enough to the player, attempt to attack.
            player_center = pygame.math.Vector2(player.position.x + 16, player.position.y + 16)
            if self.position.distance_to(player_center) < 40:
                self.attackPlayer(health_system, audio_manager)
            else:
                self.animation_state = "walking"
        else:
            if start == goal:
                self.attackPlayer(health_system, audio_manager)
            # No valid path found; so idle.
            else:
                self.idle()
        
        
    def get_grid_position(self):
        tile_position_x = int((self.position.x) // 32)
        tile_position_y = int((self.position.y - 48) // 32)
        return (tile_position_x, tile_position_y)
    
    
    def attackPlayer(self, health_system, audio_manager):
        # Attack the player if enough time has passed since the last attack.
        current_time = time.time()
        if (current_time - self.lastAttackTime) >= self.damage_frequency:
            # Calling the health system’s take_damage() method.
            health_system.take_damage(self.damage_amount, audio_manager)
            self.lastAttackTime = current_time
        self.animation_state = "attacking"
    
    
    def idle(self):
        self.animation_state = "idle"
    
    
    def takeDamage(self, amount):
        # Reduce HP by the given amount. If HP is depleted, remove the enemy.
        self.HP -= amount
        if self.HP <= 0:
            self.kill()  # Remove the enemy from all groups. This is in-built python method
            
            
    def updateAnimation(self, dt):
        # Update the enemy's animation based on its state and direction.
        if self.animation_state == "attacking":
            if self.direction == "up":
                key = "attacking_right"
            elif self.direction == "down":
                key = "attacking_left"
            elif self.direction == "left":
                key = "attacking_left"
            elif self.direction == "right":
                key = "attacking_right"
        elif self.animation_state == "walking":
            if self.direction == "up":
                key = "walking_right"
            elif self.direction == "down":
                key = "walking_left"
            elif self.direction == "left":
                key = "walking_left"
            elif self.direction == "right":
                key = "walking_right"
        else:
            if self.direction == "up":
                key = "idle_right"
            elif self.direction == "down":
                key = "idle_left"
            elif self.direction == "left":
                key = "idle_left"
            elif self.direction == "right":
                key = "idle_right"
        
        # Retrieve the animation frames.
        frames = self.animations.get(key)
        self.animation_timer += dt
        # Validate that animation_frame is within range
        if self.animation_frame >= len(frames):
            self.animation_frame = len(frames) - 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % len(frames)
        self.image = frames[self.animation_frame]