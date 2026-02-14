import pygame
import random

class PuzzlePortalManager:
    def __init__(self):
        
        # A dictionary to store all puzzles in the game along with their solutions
        self.puzzle_dataQA = {
            'level_1': {'must_solve_1': (pygame.image.load("Images/Puzzles/level1_mustsolve_1.png").convert_alpha(), 8),
                        'must_solve_2': (pygame.image.load("Images/Puzzles/level1_mustsolve_2.png").convert_alpha(), 10234),
                        'easy_1': (pygame.image.load("Images/Puzzles/level1_easy_1.png").convert_alpha(), 5),
                        'easy_2': (pygame.image.load("Images/Puzzles/level1_easy_2.png").convert_alpha(), 200),
                        'easy_3': (pygame.image.load("Images/Puzzles/level1_easy_3.png").convert_alpha(), 7),
                        'medium_1': (pygame.image.load("Images/Puzzles/level1_medium_1.png").convert_alpha(), 12),
                        'medium_2': (pygame.image.load("Images/Puzzles/level1_medium_2.png").convert_alpha(), 34),
                        'medium_3': (pygame.image.load("Images/Puzzles/level1_medium_3.png").convert_alpha(), 165),
                        'hard_1': (pygame.image.load("Images/Puzzles/level1_hard_1.png").convert_alpha(), 3),
                        'hard_2': (pygame.image.load("Images/Puzzles/level1_hard_2.png").convert_alpha(), 216),
                        'hard_3': (pygame.image.load("Images/Puzzles/level1_hard_3.png").convert_alpha(), 25),
            },
            'level_2': {'must_solve_1': (pygame.image.load("Images/Puzzles/level2_mustsolve_1.png").convert_alpha(), 13),
                        'must_solve_2': (pygame.image.load("Images/Puzzles/level2_mustsolve_2.png").convert_alpha(), 50),
                        'easy_1': (pygame.image.load("Images/Puzzles/level2_easy_1.png").convert_alpha(), 8),
                        'easy_2': (pygame.image.load("Images/Puzzles/level2_easy_2.png").convert_alpha(), 72),
                        'easy_3': (pygame.image.load("Images/Puzzles/level2_easy_3.png").convert_alpha(), 13000),
                        'medium_1': (pygame.image.load("Images/Puzzles/level2_medium_1.png").convert_alpha(), 360),
                        'medium_2': (pygame.image.load("Images/Puzzles/level2_medium_2.png").convert_alpha(), 4),
                        'medium_3': (pygame.image.load("Images/Puzzles/level2_medium_3.png").convert_alpha(), 17),
                        'hard_1': (pygame.image.load("Images/Puzzles/level2_hard_1.png").convert_alpha(), 36),
                        'hard_2': (pygame.image.load("Images/Puzzles/level2_hard_2.png").convert_alpha(), 15),
                        'hard_3': (pygame.image.load("Images/Puzzles/level2_hard_3.png").convert_alpha(), 1),
            },
            'level_3': {'must_solve_1': (pygame.image.load("Images/Puzzles/level3_mustsolve_1.png").convert_alpha(), 16),
                        'must_solve_2': (pygame.image.load("Images/Puzzles/level3_mustsolve_2.png").convert_alpha(), 1),
                        'easy_1': (pygame.image.load("Images/Puzzles/level3_easy_1.png").convert_alpha(), 10),
                        'easy_2': (pygame.image.load("Images/Puzzles/level3_easy_2.png").convert_alpha(), 1099),
                        'easy_3': (pygame.image.load("Images/Puzzles/level3_easy_3.png").convert_alpha(), 14),
                        'medium_1': (pygame.image.load("Images/Puzzles/level3_medium_1.png").convert_alpha(), 5),
                        'medium_2': (pygame.image.load("Images/Puzzles/level3_medium_2.png").convert_alpha(), 6),
                        'medium_3': (pygame.image.load("Images/Puzzles/level3_medium_3.png").convert_alpha(), 6),
                        'hard_1': (pygame.image.load("Images/Puzzles/level3_hard_1.png").convert_alpha(), 5),
                        'hard_2': (pygame.image.load("Images/Puzzles/level3_hard_2.png").convert_alpha(), 120),
                        'hard_3': (pygame.image.load("Images/Puzzles/level3_hard_3.png").convert_alpha(), 60),
            },
        }
        
        self.puzzle_details = {
            'level_1': {(1056, 208): {'type': 'easy', 'attempts_left': 3, 'teleport': (864, 368)},
                        (576, 368): {'type': 'medium', 'attempts_left': 3, 'teleport': (864, 656)},
                        (320, 528): {'type': 'hard', 'attempts_left': 3, 'teleport': (1024, 656)},
                        (768, 144): {'type': 'must_solve', 'attempts_left': 3, 'teleport': (768, 144)},
                        (832, 464): {'type': 'must_solve', 'attempts_left': 3, 'teleport': (832, 464)},
            },
            'level_2': {(1184, 592): {'type': 'easy', 'attempts_left': 3, 'teleport': (512, 304)},
                        (32, 176): {'type': 'medium', 'attempts_left': 3, 'teleport': (160, 176)},
                        (96, 560): {'type': 'hard', 'attempts_left': 3, 'teleport': (704, 528)},
                        (608, 112): {'type': 'must_solve', 'attempts_left': 3, 'teleport': (608, 112)},
                        (1024, 368): {'type': 'must_solve', 'attempts_left': 3, 'teleport': (1024, 368)},
            },
            'level_3': {(576, 656): {'type': 'easy', 'attempts_left': 3, 'teleport': (512, 656)},
                        (384, 144): {'type': 'medium', 'attempts_left': 3, 'teleport': (32, 656)},
                        (1024, 144): {'type': 'hard', 'attempts_left': 3, 'teleport': (480, 656)},
                        (480, 112): {'type': 'must_solve', 'attempts_left': 3, 'teleport': (480, 112)},
                        (544, 592): {'type': 'must_solve', 'attempts_left': 3, 'teleport': (544, 592)},
            }
        }
        
        self.current_puzzle_pos = None  # Will hold the puzzle coordinates when loaded
        self.current_puzzle_image = None  # Will hold the puzzle image when loaded
        self.current_puzzle_solution = None  # Will hold the puzzle solution when loaded
        self.current_puzzle_type = None # Will hold the puzzle type when loaded


    def load_puzzle(self, puzzle_pos, level):
        # Reset all the variables related to the current puzzle
        self.current_puzzle_pos = None
        self.current_puzzle_image = None
        self.current_puzzle_solution = None
        self.current_puzzle_type = None
        
        # Load the puzzle data
        self.current_puzzle_pos = puzzle_pos
        if puzzle_pos not in self.puzzle_details[f'level_{level}']:
            print(f"Puzzle not found at position {puzzle_pos}.")
            return
        self.current_puzzle_type = self.puzzle_details[f'level_{level}'][puzzle_pos]['type']

        if self.current_puzzle_type == 'must_solve':
            max_coord = 0
            for puzzle in list(self.puzzle_details[f'level_{level}'].keys()):
                if self.puzzle_details[f'level_{level}'][puzzle]['type'] == 'must_solve':
                    max_coord = max(max_coord, puzzle[0])
            if puzzle_pos[0] == max_coord:
                number = 2
            else:
                number = 1
            self.current_puzzle_image = self.puzzle_dataQA[f'level_{level}'][f'must_solve_{number}'][0]
            self.current_puzzle_solution = self.puzzle_dataQA[f'level_{level}'][f'must_solve_{number}'][1]
        else:
            number = random.randint(1, 3)
            self.current_puzzle_image = self.puzzle_dataQA[f'level_{level}'][f"{self.puzzle_details[f'level_{level}'][puzzle_pos]['type']}_{number}"][0]
            self.current_puzzle_solution = self.puzzle_dataQA[f'level_{level}'][f"{self.puzzle_details[f'level_{level}'][puzzle_pos]['type']}_{number}"][1]
    
    
    def check_puzzle_solution(self, player_input, level):

        if self.current_puzzle_solution is None:
            print("Puzzle solution is undefined.")
            return

        if player_input == str(self.current_puzzle_solution):
            self.puzzle_details[f'level_{level}'][self.current_puzzle_pos]['attempts_left'] = 0
            return True
        else:
            self.puzzle_details[f'level_{level}'][self.current_puzzle_pos]['attempts_left'] -= 1
            return False


    def teleport_player(self, level):
        return self.puzzle_details[f'level_{level}'][self.current_puzzle_pos]['teleport']
        

    def reset_puzzles(self):
        self.puzzle_details = {
            'level_1': {(1056, 208): {'type': 'easy', 'attempts_left': 3, 'teleport': (864, 368)},
                        (576, 368): {'type': 'medium', 'attempts_left': 3, 'teleport': (864, 656)},
                        (320, 528): {'type': 'hard', 'attempts_left': 3, 'teleport': (1024, 656)},
                        (768, 144): {'type': 'must_solve', 'attempts_left': 3, 'teleport': (768, 144)},
                        (832, 464): {'type': 'must_solve', 'attempts_left': 3, 'teleport': (832, 464)},
            },
            'level_2': {(1184, 592): {'type': 'easy', 'attempts_left': 3, 'teleport': (512, 304)},
                        (32, 176): {'type': 'medium', 'attempts_left': 3, 'teleport': (96, 176)},
                        (96, 560): {'type': 'hard', 'attempts_left': 3, 'teleport': (704, 528)},
                        (608, 112): {'type': 'must_solve', 'attempts_left': 3, 'teleport': (608, 112)},
                        (1024, 368): {'type': 'must_solve', 'attempts_left': 3, 'teleport': (1024, 368)},
            },
            'level_3': {(576, 656): {'type': 'easy', 'attempts_left': 3, 'teleport': (512, 656)},
                        (384, 144): {'type': 'medium', 'attempts_left': 3, 'teleport': (32, 656)},
                        (1024, 144): {'type': 'hard', 'attempts_left': 3, 'teleport': (480, 656)},
                        (480, 112): {'type': 'must_solve', 'attempts_left': 3, 'teleport': (480, 112)},
                        (544, 592): {'type': 'must_solve', 'attempts_left': 3, 'teleport': (544, 592)},
            }
        }
        self.current_puzzle_pos = None
        self.current_puzzle_image = None
        self.current_puzzle_solution = None
        self.current_puzzle_type = None