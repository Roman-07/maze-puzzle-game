class HealthSystem:
    
    def __init__(self, max_health):
        self.max_health = max_health
        self.current_health = max_health

    def take_damage(self, amount, audio_manager):
        # Subtract the damage amount
        self.current_health -= amount
        if self.current_health < 0:
            self.current_health = 0
        # Play sound
        audio_manager.playSoundEffect("player_damaged")

    def heal(self, amount):
        if amount < 0:
            print("Error: Healing amount must be positive.")
            return
        
        # Heal the player by the amount given
        self.current_health += amount
        # Validate that it does not exceed the maximum amount
        if self.current_health > self.max_health:
            self.current_health = self.max_health

    def is_alive(self):
        # Check if the player is still alive (i.e., current health > 0).
        # return: True if current_health > 0, else False.
        return self.current_health > 0
    
    def reset(self):
        self.current_health = self.max_health
