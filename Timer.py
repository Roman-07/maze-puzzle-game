class Timer:
    
    def __init__(self, level_time):
        if level_time <= 0:
            raise ValueError("Level time must be greater than 0")
        self.level_time = level_time
        self.current_time = level_time
        self.is_paused = False
        self.level_end = False
    
    
    def update_timer(self, dt):
        """ Decrements the timer by dt if not paused. """
        if not self.is_paused and self.current_time > 0:
            self.current_time -= dt
            if self.current_time <= 0:
                self.current_time = 0
                # Trigger level-end event.
                self.level_end = True
    
    
    def pause_timer(self):
        self.is_paused = True
    
    
    def resume_timer(self):
        self.is_paused = False
    
    
    def reset_timer(self):
        self.current_time = self.level_time
    
    
    def get_remaining_time(self):
        """Returns the current remaining time in seconds."""
        return self.current_time