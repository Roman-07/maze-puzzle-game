import pygame

class AudioManager:
    def __init__(self):
        # Initializes default variables. Call initialise() after pygame.mixer is set up.
        self.backgroundMusic = None     # A string for the current background music file path
        self.musicTracks = None         # A set for future mapping of situation to music.
        self.soundEffects = None          # Dict mapping effect names to pygame.mixer.Sound objects
        self.volume = 1.0               # Float 0.0 - 1.0

    def initialise(self):
        # Loads audio resources and sets default values.
        self.loadAudioResources()
        self.volume = 0.8


    def loadAudioResources(self):
        # Loads sound effects into memory. It is a mapping for a dictionary.
        self.soundEffects = {
            "menu_selection": pygame.mixer.Sound("Sounds\\menu_selection.mp3"),
            "shoot": pygame.mixer.Sound("Sounds\\shoot.mp3"),
            "bullet_hit": pygame.mixer.Sound("Sounds\\bullet_hit.wav"),
            "player_damaged": pygame.mixer.Sound("Sounds\\player_damaged.mp3"),
            "try_again": pygame.mixer.Sound("Sounds\\try_again.mp3"),
            "level_completed": pygame.mixer.Sound("Sounds\\level_completed.wav"),
            "power_up_hp": pygame.mixer.Sound("Sounds\\power_up_hp.mp3"),
            "power_up_speed": pygame.mixer.Sound("Sounds\\power_up_speed.mp3"),
            "power_down": pygame.mixer.Sound("Sounds\\power_down.mp3"),
            "safe_spot": pygame.mixer.Sound("Sounds\\safe_spot.wav"),
            "puzzle_enter": pygame.mixer.Sound("Sounds\\puzzle_enter.mp3"),
            "puzzle_correct": pygame.mixer.Sound("Sounds\\puzzle_correct.wav"),
            "puzzle_incorrect": pygame.mixer.Sound("Sounds\\puzzle_incorrect.mp3"),  
        }
        
        # DO NOT FORGET TO ADD THE REST OF THE MUSIC FILES
        self.musicTracks = {
            'story_screen': "Sounds/story_screen.mp3",
            "menu": "Sounds/menu_theme.mp3",
            "instructions": "Sounds/instructions.mp3",
            "difficulty": "Sounds/difficulty.mp3",
            'level_1': "Sounds/level_1.mp3",
            'level_2': "Sounds/level_2.mp3",
            'level_3': "Sounds/level_3.mp3",
            'game_end': "Sounds/game_end.mp3",
        }


    def playBackgroundMusic(self, track_name):
        """
        Selects and plays background music for a given track name in a loop.
        """
        # Example placeholder logic for selecting a music file based on level
        # (In reality, you'd have some mapping from level -> music file path)
        music_file = None
        if track_name == 'story_screen':
            music_file = self.musicTracks['story_screen']
        elif track_name == "menu":
            music_file = self.musicTracks["menu"]
        elif track_name == 'instructions':
            music_file = self.musicTracks["instructions"]
        elif track_name == "difficulty":
            music_file = self.musicTracks["difficulty"]
        elif track_name == 'level_1':
            music_file = self.musicTracks["level_1"]
        elif track_name == 'level_2':
            music_file = self.musicTracks["level_2"]
        elif track_name == 'level_3':
            music_file = self.musicTracks["level_3"]
        elif track_name == 'game_end':
            music_file = self.musicTracks["game_end"]
        else:
            music_file = self.musicTracks["menu"]  # Default to menu music

        # If the file doesn't exist or isn't set, just return
        if not music_file:
            print("No background music file found for this level.")
            return

        # Load & play the background music
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)  # -1 for infinite looping
            self.backgroundMusic = music_file
        except pygame.error as e:
            print(f"Error loading music file '{music_file}': {e}")


    def playSoundEffect(self, effect):
        """
        Plays the given sound effect if it exists in the soundEffects dictionary.
        """

        # Get the Sound object from the dictionary
        sound_obj = self.soundEffects.get(effect)
        if sound_obj is None:
            print(f"Error: Sound effect not found: {effect}")
            return

        # Set volume and play the sound
        sound_obj.set_volume(self.volume)
        sound_obj.play()


    def stopAllSounds(self):
        """
        Stops all music.
        """
        # Stop background music
        pygame.mixer.music.stop()
        self.backgroundMusic = None