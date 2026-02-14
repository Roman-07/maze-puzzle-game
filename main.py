import pygame
import sys
import time
import AudioManager
import MapRenderer
import CollisionManager
import HUD
import Timer
import Player
import Enemy
import BulletManager
import HealthSystem
import PuzzlePortalManager

pygame.init() # Initialise Pygame
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720   # Screen dimensions
FONT = pygame.font.Font('SpecialElite.ttf', 38)
# Setting a convenient reference to the colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SOFT_GOLD = (238, 192, 124)
DARK_BLUE = (30, 43, 79)  # Dark Blue (#1E2B4F)
HIGHLIGHT_COLOR = (245, 206, 66)


class States:
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None
  
class StartUp(States):
    
    def __init__(self):
        super().__init__()
        # After finishing this state, we'll move to 'storytelling'
        self.next = "storytelling"
        self.start_time = 0
        self.background = None


    def enter_state(self):
        print("StartUp: enter_state() -> Starting 5-second intro screen")
        self.start_time = time.time()
        
        # Load image once here instead of every frame
        self.background = pygame.image.load("Images\\1_Start-Up.png").convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))


    def get_event(self, event):
        # No checks here
        pass


    def update(self, screen, dt):
        """
        Runs each frame. After 5 seconds, we mark this state done.
        """
        if (time.time() - self.start_time) >= 5:
            self.done = True  # Will flip to 'storytelling' state next
        
        self.draw(screen)


    def draw(self, screen):
        # Clear screen (fill with black or any color)
        screen.fill((0, 0, 0))
        # Draw background image
        screen.blit(self.background, (0, 0)) 
   
     
    def cleanup(self):
        print("StartUp: cleanup() -> Finished intro screen")
        self.background = None  # Free reference if desired

class Storytelling(States):
    
    def __init__(self, audio_manager):
        super().__init__()
        self.next = "menu"
        self.start_time = 0
        self.background = None
        self.enter_pressed = False
        self.audio_manager = audio_manager


    def enter_state(self):
        print("Storytelling: enter_state() -> Starting backstory screen")
        self.start_time = time.time()

        # Load the background image once
        self.background = pygame.image.load("Images\\2_Story.png").convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Play the background music for the story screen
        self.audio_manager.playBackgroundMusic('story_screen')


    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            # User pressed Enter
            self.enter_pressed = True


    def update(self, screen, dt):
        """
        Runs each frame. If Enter is pressed or 60 seconds pass, we're done.
        """
        elapsed = time.time() - self.start_time

        if self.enter_pressed or elapsed >= 60:
            # Move on to the next state: "menu"
            print("Storytelling: Transitioning to Main Menu")
            self.done = True

        self.draw(screen)


    def draw(self, screen):
        # Clear the screen
        screen.fill((0, 0, 0))
        # Draw background image
        screen.blit(self.background, (0, 0))
  
    
    def cleanup(self):
        print("Storytelling: cleanup() -> Done with story screen")
        self.background = None
        self.audio_manager.stopAllSounds()

class Menu(States):
    
    def __init__(self, game_info, audio_manager):
        States.__init__(self)   # Using a super method
        self.next = 'game'
        self.normal_background = None
        self.paused_background = None
        self.game_info = game_info
        # Highlighted rectangles for menu options
        self.menu_options_rects = [
            pygame.Rect(420, 152, 446, 104),  # "Start Game / Resume"
            pygame.Rect(371, 284, 539, 104),  # "Instructions"
            pygame.Rect(413, 419, 453, 104),  # "Difficulty"
            pygame.Rect(525, 554, 230, 103),  # "Exit"
        ]
        self.audio_manager = audio_manager
        

    def enter_state(self):
        """
        Called once when we first enter the 'Menu' state.
        Load the images, set up default options, etc.
        """
        print("Menu state: enter_state() -> Entering Menu/Pause")
        self.normal_background = pygame.image.load("Images\\3_Menu_Normal.png").convert()
        self.normal_background = pygame.transform.scale(self.normal_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.paused_background = pygame.image.load("Images\\3_Menu_Paused.png").convert()
        self.paused_background = pygame.transform.scale(self.paused_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Create a surface for drawing semi-transparent shapes if you want alpha
        self.highlight_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        # Current selection starts at the top-most item
        self.selected_index = 0
        
        # Play the background music for the story screen
        self.audio_manager.playBackgroundMusic('menu')
        
        
    def get_event(self, event):
        """
        Called for each event. Decide how to transition to other states
        or set `self.done = True` with a chosen `self.next` state.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # Move highlight up
                self.selected_index = (self.selected_index - 1) % len(self.menu_options_rects)
                self.audio_manager.playSoundEffect('menu_selection')
            elif event.key == pygame.K_DOWN:
                # Move highlight down
                self.selected_index = (self.selected_index + 1) % len(self.menu_options_rects)
                self.audio_manager.playSoundEffect('menu_selection')
            elif event.key == pygame.K_RETURN:
                if self.selected_index == 0:
                    print("Selected: Start Game / Resume")
                    self.next = "game"
                    self.done = True
                elif self.selected_index == 1:
                    print("Selected: Instructions")
                    self.next = "instructions"
                    self.done = True
                elif self.selected_index == 2:
                    print("Selected: Difficulty")
                    self.next = "difficulty"
                    self.done = True
                elif self.selected_index == 3:
                    print("Selected: Exit")
                    self.quit = True
       
            
    def update(self, screen, dt):
        """
        Handle logic updates: user input, changing selected index, etc.
        No direct drawing here.
        """
        self.draw(screen)
    
        
    def draw(self, screen):
        """
        Handles all rendering (drawing) to the screen.
        """
        # A helper function to draw the highlight rect with rounded corners
        def draw_highlight(dest_surface, rect, color, border_radius=15):
            # If you're using a surface with an alpha channel, fill it each frame
            self.highlight_surface.fill((0, 0, 0, 0))  # Clear old drawing, fully transparent
            
            # Draw the rounded rectangle onto the highlight surface
            pygame.draw.rect(self.highlight_surface, color, rect, width=4, border_radius=border_radius)
            # Then blit the highlight_surface onto the destination (the screen)
            dest_surface.blit(self.highlight_surface, (0, 0))
            
        # Clear the screen
        screen.fill((0, 0, 0))    
        # Draw the correct background, using checking game_active
        if self.game_info['game_active'] == True:
            screen.blit(self.paused_background, (0, 0))
        else:
            screen.blit(self.normal_background, (0, 0))

        # Draw highlight around currently selected menu item
        self.current_rect = self.menu_options_rects[self.selected_index]
        draw_highlight(screen, self.current_rect, HIGHLIGHT_COLOR, border_radius=20)
      
      
    def cleanup(self):
        print("Menu: cleanup() -> Finished menu/pause")
        self.normal_background = None
        self.paused_background = None
        self.audio_manager.stopAllSounds()  

class Instructions(States):
    
    def __init__(self, audio_manager):
        super().__init__()
        self.next = "menu"
        self.start_time = 0
        self.background = None
        self.enter_pressed = False
        self.audio_manager = audio_manager

        
    def enter_state(self):
        print("Instructions: enter_state() -> Starting instructions screen")
        self.start_time = time.time()
        
        # Load the background image once
        self.background = pygame.image.load("Images\\4_Instructions.png").convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Play the background music for the instruction screen
        self.audio_manager.playBackgroundMusic('instructions')
        
        
    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            # User pressed Enter
            self.enter_pressed = True
            
            
    def update(self, screen, dt):
        elapsed = time.time() - self.start_time

        if self.enter_pressed or elapsed >= 60:
            # Move on to the next state: "menu"
            print("Instructions: Transitioning to Main Menu")
            self.done = True

        self.draw(screen)
        
        
    def draw(self, screen):
        # Clear the screen
        screen.fill((0, 0, 0))
        # Draw background image
        screen.blit(self.background, (0, 0))


    def cleanup(self):
        print("Instructions: cleanup() -> Finished instructions screen")
        self.enter_pressed = False   # Reset the enter_pressed flag for next time
        self.audio_manager.stopAllSounds()

class Difficulty(States):
    
    def __init__(self, game_info, audio_manager):
        States.__init__(self)
        self.next = 'menu'
        self.game_info = game_info
        self.normal_background = None
        self.paused_background = None
        self.enter_pressed = False
        # Highlighted rectangles for difficulty options
        self.difficulty_options_rects = [
            pygame.Rect(42, 290, 394, 104),  # "Beginner"
            pygame.Rect(492, 290, 342, 104),  # "Average"
            pygame.Rect(890, 290, 310, 104),  # "Expert"
        ]
        self.audio_manager = audio_manager
        self.difficulty_selected = 1 # Default to Average difficulty
    

    def enter_state(self):
        print("Difficulty: enter_state() -> Starting difficulty selection screen")
        self.start_background = pygame.image.load("Images\\5_Difficulty_Start.png").convert()
        self.start_background = pygame.transform.scale(self.start_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        if self.game_info['game_active'] == True:
            # If we came from the game, load the chosen difficulty background
            if self.difficulty_selected == 0:
                self.paused_background = pygame.image.load("Images\\5_Difficulty_beginner.png").convert()
                self.paused_background = pygame.transform.scale(self.paused_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            elif self.difficulty_selected == 1:
                self.paused_background = pygame.image.load("Images\\5_Difficulty_average.png").convert()
                self.paused_background = pygame.transform.scale(self.paused_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            elif self.difficulty_selected == 2:
                self.paused_background = pygame.image.load("Images\\5_Difficulty_expert.png").convert()
                self.paused_background = pygame.transform.scale(self.paused_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            # Current selection starts at the left-most item. This condition is in place
            # so that difficulty_selected will store the last chosen difficulty, and will
            # not be reset to 0 when difficulty menu is opened from the game (pause)
            self.difficulty_selected = 0
        
        # Create a surface for drawing semi-transparent shapes if you want alpha
        self.highlight_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        # Play the background music for the story screen
        self.audio_manager.playBackgroundMusic('difficulty')
    
    
    def get_event(self, event):
        if self.game_info['game_active'] == True:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # User pressed Enter
                self.enter_pressed = True
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # Move highlight left
                    self.difficulty_selected = (self.difficulty_selected - 1) % len(self.difficulty_options_rects)
                    self.audio_manager.playSoundEffect('menu_selection')
                elif event.key == pygame.K_RIGHT:
                    # Move highlight right
                    self.difficulty_selected = (self.difficulty_selected + 1) % len(self.difficulty_options_rects)
                    self.audio_manager.playSoundEffect('menu_selection')
                elif event.key == pygame.K_RETURN:
                    # Play click sound
                    if self.difficulty_selected == 0:
                        print("Selected: Beginner")
                    elif self.difficulty_selected == 1:
                        print("Selected: Average")
                    elif self.difficulty_selected == 2:
                        print("Selected: Expert")
                    
                    self.next = "menu"
                    self.done = True


    def update(self, screen, dt):
        if self.game_info['game_active'] == True:
            if self.enter_pressed:
                # Move on to the next state: "menu"
                print("Difficulty: Transitioning to Main Menu")
                self.done = True
                
        self.draw(screen)


    def draw(self, screen):
        # A helper function to draw the highlight rect with rounded corners
        def draw_highlight(dest_surface, rect, color, border_radius=15):
            # If you're using a surface with an alpha channel, fill it each frame
            self.highlight_surface.fill((0, 0, 0, 0))  # Clear old drawing, fully transparent
            
            # Draw the rounded rectangle onto the highlight surface
            pygame.draw.rect(self.highlight_surface, color, rect, width=4, border_radius=border_radius)
            # Then blit the highlight_surface onto the destination (the screen)
            dest_surface.blit(self.highlight_surface, (0, 0))
            
        # Clear the screen
        screen.fill((0, 0, 0))    
        # Draw the correct background, Using `game_active` to determine the options
        if self.game_info['game_active'] == True:
            screen.blit(self.paused_background, (0, 0))
        else:
            screen.blit(self.start_background, (0, 0))
            # Draw highlight around currently selected menu item
            self.current_rect = self.difficulty_options_rects[self.difficulty_selected]
            draw_highlight(screen, self.current_rect, HIGHLIGHT_COLOR, border_radius=20)


    def cleanup(self):
        print("Difficulty: cleanup() -> Finished difficulty selection screen")
        self.start_background = None
        self.paused_background = None
        self.enter_pressed = False
        self.audio_manager.stopAllSounds()
        # Update the game_info values with the chosen difficulty
        if self.difficulty_selected == 0:
                self.game_info['HP_scale'] = 2
                self.game_info['Time_scale'] = 2
        elif self.difficulty_selected == 1:
                self.game_info['HP_scale'] = 1
                self.game_info['Time_scale'] = 1
        elif self.difficulty_selected == 2:
                self.game_info['HP_scale'] = 0.5
                self.game_info['Time_scale'] = 0.5

class Game(States):
        
    def __init__(self, game_info, audio_manager):
        super().__init__()
        self.next = 'menu'
        self.game_info = game_info
        self.audio_manager = audio_manager

        # Create instances of your components
        self.map_renderer = MapRenderer.MapRenderer()
        self.collision_manager = CollisionManager.CollisionManager(32, 32)
        self.bullet_manager = BulletManager.BulletManager()
        
        # Create groups for sprites
        self.all_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        # Store all the starting positions for the player. First element is empty to match the level number
        self.starting_positions = [(0, 0), (40, 88), (32, 656), (1216, 80)]
        # Variables used for switching between levels
        self.current_level = 0
        self.level_switch = False
        self.level_reset = False
        
        
    def load_level_enemies(self, level_number):
        """
        Loads enemy data for the specified level, creates Enemy instances,
        and adds them to the enemy_sprites and all_sprites groups.
        """
        # Clear any existing enemies.
        self.enemy_sprites.empty()
        
        # Level data: spawn positions of all enemies for that level
        level_enemy_data = {
            1: [
                {"position": (32 + 16, 240 + 16), "enemy_type": "zombie"},
                {"position": (1152 + 16, 560 + 16), "enemy_type": "zombie"},
                {"position": (448 + 16, 144 + 16), "enemy_type": "skeleton"},
                {"position": (736 + 16, 272 + 16), "enemy_type": "skeleton"}
            ],
            2: [
                {"position": (160 + 16, 656 + 16), "enemy_type": "skeleton"},
                {"position": (352 + 16, 496 + 16), "enemy_type": "zombie"},
                {"position": (96 + 16, 144 + 16), "enemy_type": "zombie"},
                {"position": (768 + 16, 208 + 16), "enemy_type": "skeleton"},
                {"position": (896 + 16, 240 + 16), "enemy_type": "zombie"},
                {"position": (1088 + 16, 656 + 16), "enemy_type": "skeleton"}
            ],
            3: [
                {"position": (1088 + 16, 304 + 16), "enemy_type": "zombie"},
                {"position": (448 + 16, 336 + 16), "enemy_type": "skeleton"},
                {"position": (544 + 16, 336 + 16), "enemy_type": "zombie"},
                {"position": (640 + 16, 336 + 16), "enemy_type": "skeleton"},
                {"position": (736 + 16, 336 + 16), "enemy_type": "zombie"},
                {"position": (832 + 16, 336 + 16), "enemy_type": "skeleton"},
                {"position": (32 + 16, 208 + 16), "enemy_type": "zombie"},
                {"position": (256 + 16, 560 + 16), "enemy_type": "skeleton"}
            ]
        }

        # Get enemy configurations for this level.
        enemies_info = level_enemy_data.get(level_number, [])
        
        for info in enemies_info:
            enemy = Enemy.Enemy(info["position"], info["enemy_type"])
            self.enemy_sprites.add(enemy)
    
    
    def initialise(self):
        hp = int(self.game_info['HP_default'] * self.game_info['HP_scale'])
        time_value = int(self.game_info['Time_default'] * self.game_info['Time_scale'])

        self.hud = HUD.HUD(hp, time_value, FONT)
        self.timer = Timer.Timer(time_value)
        self.health_system = HealthSystem.HealthSystem(hp)
        self.puzzle_manager = PuzzlePortalManager.PuzzlePortalManager()
        # Variables for the puzzle system
        self.input_str = ""
        self.input_box = pygame.Rect(200, 500, 400, 50)
        self.puzzle_dimentions = (190, 140, 900, 450) # left, top, width, height
        self.puzzle_tried = False
        self.puzzle_result = None
        self.puzzle_result_timer = 0
        self.puzzle_result_duration = 2  # seconds
        self.puzzle_damage = 50

        # Create player or other game sprites and add them to the group
        self.player = Player.Player(self.starting_positions[self.current_level], 112, self.bullet_manager, self.audio_manager)
        self.all_sprites.add(self.player)
    
        self.load_level_enemies(self.current_level)
    
    
    def reset_level(self):
        if self.level_switch == True:
            # Update the current level number.
            self.current_level += 1
            # Update the level switch variable
            self.level_switch = False
            
        # Reset the player, health, and timer, and puzzle manager
        self.player.reset(self.starting_positions[self.current_level])
        self.health_system.reset()
        self.timer.reset_timer()
        self.timer.level_end = False
        self.puzzle_manager.reset_puzzles()
        self.input_str = ""
        self.puzzle_tried = False
        self.puzzle_result = None
        self.puzzle_result_timer = 0
        # Reset the bullet sprite group
        self.bullet_manager.bullets.empty()
        # Reset the level reset flag
        self.level_reset = False
        
        # Load new enemy objects for the level.
        self.load_level_enemies(self.current_level)
    
    
    def enter_state(self):
        print("Game: enter_state() -> Starting game state")
        if self.game_info['game_active'] == False:
            self.game_info['game_active'] = True
            self.current_level = 1
            self.initialise()
            
        # Reset / switch level if needed: update enemy sprites
        if self.level_reset == True:
            self.reset_level()
            
        # Resume timer if the game was paused
        if self.timer.is_paused == True:
                self.timer.resume_timer()
        
        self.map_renderer.load_map_data(str(self.current_level))
        self.map_renderer.scale_all_tiles()
        self.collision_manager.initialise(self.map_renderer)
        
        # Play the background music for the story screen
        self.audio_manager.playBackgroundMusic(f'level_{self.current_level}')

    
    def get_event(self, event):
        # Check escape was pressed to go to pause menu, and stop the timer
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print('Pause pressed')
            self.timer.pause_timer()
            self.next = 'menu'
            self.done = True
        elif self.player.solving_puzzle is not None:
            if self.puzzle_manager.puzzle_details[f'level_{self.current_level}'][self.player.solving_puzzle]['attempts_left'] != 0:
                # Does not allow to enter new input
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # User pressed Enter: process the submitted answer.
                        self.puzzle_tried = True
                        self.puzzle_result = self.puzzle_manager.check_puzzle_solution(self.input_str, self.current_level)
                    elif event.key == pygame.K_BACKSPACE:
                        # Remove the last character.
                        self.input_str = self.input_str[:-1]
                    else:
                        # Only accept digits.
                        if event.unicode.isdigit():
                            if len(self.input_str) < 17:
                                self.input_str += event.unicode
    
    
    def update(self, screen, dt):
        # Update the timer
        self.timer.update_timer(dt)
        
        # Check if the timer has reached zero --> try again screen
        if self.timer.level_end == True:
            self.next = 'try_again'
            self.done = True
            self.level_reset = True
        
        # Update sprites and any dynamic game logic
        self.all_sprites.update(dt, self.collision_manager, self.enemy_sprites, self.health_system, self.audio_manager, self.puzzle_manager, self.current_level)
        self.bullet_manager.update(dt, self.collision_manager, self.audio_manager, self.enemy_sprites)
        self.enemy_sprites.update(dt, self.player, self.health_system, self.collision_manager, self.bullet_manager, self.audio_manager)
        
        # Check if the player has run out of health --> try again screen
        if self.health_system.current_health == 0:
            self.next = 'try_again'
            self.done = True
            self.level_reset = True
        
        # Check if the player has reached the end of the level
        if self.player.door_reached == True and self.timer.level_end == False:
            if self.current_level == 3:
                self.next = 'end_game'
                self.done = True
            else:
                self.next = 'inter_level'
                self.done = True
                self.level_switch = True
                self.level_reset = True

        # Update HUD elements
        self.hud.update_hud(self.health_system.current_health, self.player.bulletCount, self.timer.get_remaining_time())

        # Finally, draw everything on screen
        self.draw(screen, dt)
        
        
    def draw(self, screen, dt):
        screen.fill(BLACK)
        # Draw the background map first
        self.map_renderer.draw(screen)
        
        # Draw all the sprites
        self.all_sprites.draw(screen)
        self.enemy_sprites.draw(screen)
        self.bullet_manager.draw(screen)
        
        # Draw the HUD overlay on top
        self.hud.display_hud(screen)
        
        # Draw the puzzle if the player is solving one
        if self.player.solving_puzzle is not None:
            puzzle_image = self.puzzle_manager.current_puzzle_image
            puzzle_image = pygame.transform.scale(puzzle_image, (self.puzzle_dimentions[2], self.puzzle_dimentions[3]))
            screen.blit(puzzle_image, (self.puzzle_dimentions[0], self.puzzle_dimentions[1]))
            # Draw the input box
            pygame.draw.rect(screen, BLACK, self.input_box, 2)
            # Render the text.
            input_text_surface = FONT.render(self.input_str, True, BLACK)
            screen.blit(input_text_surface, (self.input_box.x + 5, self.input_box.y + 10))
            
            if self.puzzle_tried:
                if self.puzzle_result == True:
                    self.audio_manager.playSoundEffect("puzzle_correct")
                else:
                    self.audio_manager.playSoundEffect("puzzle_incorrect")
                self.puzzle_tried = False
                self.input_str = ""
                    
            if self.puzzle_result is not None:
                if self.puzzle_result:
                    result_text_surface = FONT.render("Correct!", True, GREEN)
                else:
                    result_text_surface = FONT.render("Incorrect!", True, RED)
                
                screen.blit(result_text_surface, (self.input_box.x, self.input_box.y - 40))
                
                if self.puzzle_manager.puzzle_details[f'level_{self.current_level}'][self.player.solving_puzzle]['attempts_left'] == 0:
                    self.puzzle_result_timer += dt
                    if self.puzzle_result_timer >= self.puzzle_result_duration:
                        self.puzzle_result_timer = 0
                        if self.puzzle_result == True:
                            self.player.teleport(self.puzzle_manager.teleport_player(self.current_level))
                        if self.puzzle_manager.current_puzzle_type == 'must_solve':
                            if self.puzzle_result == False:
                                self.health_system.take_damage(self.puzzle_damage, self.audio_manager)
                        self.puzzle_tried = False
                        self.puzzle_result = None
                        self.player.solving_puzzle = None
    
    
    def cleanup(self):
        print("Game: cleanup() -> Finished / paused the game")
        self.audio_manager.stopAllSounds()
     
class Try_again(States):   
    def __init__(self, audio_manager):
        super().__init__()
        self.next = "game"
        self.background = None
        self.enter_pressed = False
        self.audio_manager = audio_manager
    
    def enter_state(self):
        print("Try again: enter_state() -> Starting try again screen")
        # Load the background image once
        self.background = pygame.image.load("Images\\6_Try_again.png").convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Play the background music for the try again screen
        self.audio_manager.playSoundEffect('try_again')
    
    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            # User pressed Enter
            self.enter_pressed = True
    
    def update(self, screen, dt):
        if self.enter_pressed:
            # Move on to the next state: "game"
            print("Try again: Transitioning to Game state")
            self.done = True

        self.draw(screen)
    
    def draw(self, screen):
        # Clear the screen
        screen.fill((0, 0, 0))
        # Draw background image
        screen.blit(self.background, (0, 0))

    def cleanup(self):
        print("Try again: cleanup() -> Closing try again screen")
        self.enter_pressed = False   # Reset the enter_pressed flag for next time
        self.audio_manager.stopAllSounds()
               
class Inter_level(States):
    def __init__(self, audio_manager):
        super().__init__()
        self.next = "game"
        self.background = None
        self.enter_pressed = False
        self.audio_manager = audio_manager
     
    def enter_state(self):
        print("Inter-level: enter_state() -> Starting inter-level screen")
        # Load the background image once
        self.background = pygame.image.load("Images\\7_Inter_level.png").convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Play the background music for the level completed screen
        self.audio_manager.playSoundEffect('level_completed')
    
    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            # User pressed Enter
            self.enter_pressed = True
    
    def update(self, screen, dt):
        if self.enter_pressed:
            # Move on to the next state: "game"
            print("Inter-level: Transitioning to Game state")
            self.done = True

        self.draw(screen)
      
    def draw(self, screen):
        # Clear the screen
        screen.fill((0, 0, 0))
        # Draw background image
        screen.blit(self.background, (0, 0))

    def cleanup(self):
        print("Inter-level: cleanup() -> Closing inter-level screen")
        self.enter_pressed = False   # Reset the enter_pressed flag for next time
        self.audio_manager.stopAllSounds()

class End_game(States):
    def __init__(self, audio_manager):
        super().__init__()
        self.next = "game"
        self.background = None
        self.enter_pressed = False
        self.audio_manager = audio_manager

        # Define the multi-line text for the end game message.
        self.text_lines = [
            "Congratulations!",
            "You have successfully defeated all the",
            "enemies, and you saved the world!",
            "Thank you for playing my game!",
            "By Roman, the developer :)"
        ]
        # Start with the text at the top (y=0) and set a scrolling speed (pixels per second).
        self.text_y = 0
        self.scroll_speed = 12


    def enter_state(self):
        print("End game: enter_state() -> Starting end game screen")
        # Load and scale the background image.
        self.background = pygame.image.load("Images\\8_End_game.jpg").convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # Play the background music for the story screen
        self.audio_manager.playBackgroundMusic('game_end')


    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.enter_pressed = True


    def update(self, screen, dt):
        # Update the vertical position of the text.
        self.text_y += self.scroll_speed * dt

        # If the top line of the text (at self.text_y) has moved below the bottom of the screen,
        # automatically end the state.
        if self.text_y >= SCREEN_HEIGHT:
            self.done = True
            self.quit = True

        # Also allow exit via Enter key.
        if self.enter_pressed:
            self.done = True
            self.quit = True

        self.draw(screen)


    def draw(self, screen):
        # Clear the screen and draw the background.
        screen.fill((0, 0, 0))
        screen.blit(self.background, (0, 0))
        
        # Draw each line of text.
        # Here, each line's y-coordinate is offset by self.text_y plus an increment for each line.
        line_height = FONT.get_height()
        for i, line in enumerate(self.text_lines):
            text_surface = FONT.render(line, True, SOFT_GOLD, DARK_BLUE)
            # Center the text horizontally.
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, self.text_y + i * line_height))
            screen.blit(text_surface, text_rect)


    def cleanup(self):
        print("End game: cleanup() -> Closing end game screen")
        self.audio_manager.stopAllSounds()


class Control:
    
    def __init__(self, **settings):
        # updates the instance's __dict__ (a dictionary that stores the
        # instance's attributes) with the provided settings, effectively
        # setting the attributes dynamically based on the keyword arguments
        # Now I can access these settings as attributes of the instance.
        self.__dict__.update(settings)
        self.done = False
        self.screen = pygame.display.set_mode(self.size, pygame.NOFRAME)
        pygame.display.set_caption(self.title)
        pygame.mixer.init()  # Initialise the mixer module for sound
        self.audio_manager = AudioManager.AudioManager()  # Create an instance of the AudioManager class
        self.audio_manager.initialise()
        self.clock = pygame.time.Clock()
        self.game_info= {'game_active': False,
                         'HP_default': 100,
                         'Time_default': 180,
                         'HP_scale': 1,
                         'Time_scale': 1,
        }
        
    # Set up all the states
    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        # Need to call enter_state() to start the first state
        self.state.enter_state()
        
    # Change between states
    def flip_state(self):
        self.state.done = False
        previous, self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.enter_state()
        self.state.previous = previous
        
    # Update the current state
    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, dt)
        
    # Get events from the current state
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            self.state.get_event(event)
            
    # Main game loop       
    def main_game_loop(self):
        while not self.done:
            # Setting the FPS restrictions
            delta_time = self.clock.tick(self.fps)/1000.0 
            self.event_loop()
            self.update(delta_time)
            pygame.display.update()


def main():
    settings = {
        'size': (SCREEN_WIDTH, SCREEN_HEIGHT),
        'fps': 60,
        'title': "MazeGame",
    }
    
    app = Control(**settings)
    state_dict = {
        "startup": StartUp(),
        "storytelling": Storytelling(app.audio_manager),
        "menu": Menu(app.game_info, app.audio_manager),                  # Menu class
        "difficulty": Difficulty(app.game_info, app.audio_manager),      # Difficulty class
        "instructions": Instructions(app.audio_manager),                 # Instructions class
        "game": Game(app.game_info, app.audio_manager),                  # Game class
        "try_again": Try_again(app.audio_manager),
        "inter_level": Inter_level(app.audio_manager),
        "end_game": End_game(app.audio_manager)
    }
    
    app.setup_states(state_dict, 'startup')
    app.main_game_loop()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()