import pygame

class CollisionManager:
    
    def __init__(self, tile_width, tile_height):
        self.tile_width = tile_width   # The width of each tile in pixels.
        self.tile_height = tile_height # The height of each tile in pixels.
        

    def initialise(self, map_renderer):
        self.tmx_data = map_renderer.get_tmx_data()   # Loaded Tiled map data (using pytmx).
        self.scaled_tiles = map_renderer.get_scaled_tiles()   # A dictionary mapping gid to tile Surface.
        self.map_grid = map_renderer.get_map_grid()
      
    
    def check_sprite_collision(self, sprite1, sprite2):
        # Checks collision between two sprites and output Boolean value
        collided = pygame.Rect.colliderect(sprite1.collision_rect, sprite2.collision_rect)
        return collided


    def get_tile_rects(self, layer_name):
        # Returns a list of pygame.Rect objects for all tiles in a specific layer.
        rects = []
        for layer in self.tmx_data.visible_layers:
            # Check if this is a tile layer and if its name matches the one we need.
            if hasattr(layer, 'data') and layer.name == layer_name:
                for x, y, gid in layer:
                    # Get the tile image (if available). We only need the rect.
                    tile = self.scaled_tiles.get(gid)
                    if tile:
                        rect = pygame.Rect(
                            x * self.tile_width, 
                            y * self.tile_height + 48, 
                            self.tile_width, 
                            self.tile_height
                        )
                        rects.append(rect)
        return rects


    def check_tile_collision(self, sprite, layer_name):
        # List of tile rects that collide with the sprite.
        collisions = []
        tile_rects = self.get_tile_rects(layer_name) # layer_name: Name of the layer to check (e.g., "Walls").
        for rect in tile_rects:
            if pygame.Rect.colliderect(sprite.collision_rect, rect):   # Checks collision between two rectangles
                collisions.append(rect)
                
        return collisions


    def check_wall_collisions(self, sprite):
        # Check collisions between the sprite and wall tiles.
        return self.check_tile_collision(sprite, "Walls")

    def check_door_collision(self, sprite):
        # Check collisions between the sprite and door tiles.
        return self.check_tile_collision(sprite, "ExitDoor")
    
    def check_speed_powerup_collisions(self, sprite):
        # Check collisions between the sprite and speed power-up tiles.
        return self.check_tile_collision(sprite, "PowerUpSpeed")
    
    def check_hp_powerup_collisions(self, sprite):
        # Check collisions between the sprite and hp power-up tiles.
        return self.check_tile_collision(sprite, "PowerUpHP")

    def check_safe_spot_collisions(self, sprite):
        # Check collisions between the sprite and portal tiles.
        return self.check_tile_collision(sprite, "SafeSpot")
    
    def check_portal_collisions(self, sprite):
        # Check collisions between the sprite and portal tiles.
        return self.check_tile_collision(sprite, "Portals")