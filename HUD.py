import pygame
WHITE = (255, 255, 255)

class HUD:
    
    def __init__(self, initial_hp, start_time, font, initial_bullets=20):
        self.hp = initial_hp      # The starting health points
        self.timer = start_time   # The starting time in seconds
        self.bullets = initial_bullets # The starting bullet count
        self.font = font  # A Pygame font object for rendering text.
        # Loading all the 3 hud images and scaling them to the required size
        self.hp_image = pygame.image.load("Images\\HUD_heart.png").convert()
        self.hp_image = pygame.transform.scale(self.hp_image, (46, 46))
        self.timer_image = pygame.image.load("Images\\HUD_timer.png").convert()
        self.timer_image = pygame.transform.scale(self.timer_image, (46, 46))
        self.bullets_image = pygame.image.load("Images\\HUD_bullets.png").convert()
        self.bullets_image = pygame.transform.scale(self.bullets_image, (72, 36))


    def display_hud(self, screen):
        # Rendering the text
        hp_text = self.font.render(str(self.hp), True, WHITE)
        timer_text = self.font.render(self.format_time(self.timer), True, WHITE)
        bullets_text = self.font.render(str(self.bullets), True, WHITE)
        
        # Positioning with simple padding ((48-32)/2 = 8 pixels, and + 1 for adjustment)
        screen.blit(hp_text, (180, 9))   # HP at the top left
        screen.blit(timer_text, (640, 9))  # Timer at the top center
        screen.blit(bullets_text, (1100, 9))  # Bullets at the top right
        # Displaying the images
        screen.blit(self.hp_image, (100, 1))
        screen.blit(self.timer_image, (570, 1))
        screen.blit(self.bullets_image, (1000, 6))
    
    
    def update_hud(self, new_hp, new_bullets, current_time):
        self.update_hp(new_hp)
        self.update_bullets(new_bullets)
        self.update_timer(current_time) # New time (in seconds).
    
    
    def update_hp(self, new_hp):
        if new_hp < 0:
            self.hp = 0
        else:
            self.hp = new_hp
    
    
    def update_bullets(self, new_bullets):
        self.bullets = max(0, new_bullets)
    
    
    def update_timer(self, current_time):
        self.timer = current_time
        if self.timer < 0:
            self.timer = 0  # Timer stops at zero.
    
    
    def format_time(self, seconds):
        minutes = int(seconds) // 60
        secs = int(seconds) % 60
        return f"{minutes:02}:{secs:02}"