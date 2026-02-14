import os
import pygame
import pytmx

class MapRenderer:
    
    def __init__(self, scale=2):
        """ Loads a TMX file using pytmx, and scales tiles by 2. """
        self.scale = scale    # How much to scale each tile image (2 = double size)
        self.filename = None
        self.tmx_data = None
        # Will store scaled versions of each tile image keyed by GID
        self.scaled_tiles = {}


    def load_map_data(self, level):
        """Loads the TMX data using pytmx."""
        # Validation for the existence of the TMX file.
        self.filename = None   # Reset the filename in case it was set previously.
        self.tmx_data = None   # Reset the TMX data in case it was set previously.
        self.scaled_tiles = {} # Reset the scaled tiles in case they were set previously.
        self.width = 0
        self.height = 0
        self.filename = self.filename = f"Maps/Level_{level}.tmx"   # Path to the TMX file.
        if not os.path.exists(self.filename):
            print(f"Error: TMX file '{self.filename}' not found.")
            pygame.quit()
            raise SystemExit
        try:
            self.tmx_data = pytmx.load_pygame(self.filename, pixelalpha=True)
            self.width = self.tmx_data.width * self.tmx_data.tilewidth * self.scale
            self.height = self.tmx_data.height * self.tmx_data.tileheight * self.scale
        except Exception as e:
            print(f"Error loading TMX file {self.filename}: {e}")
            pygame.quit()
            raise SystemExit
        
        
    def get_tmx_data(self):
        return self.tmx_data


    def scale_all_tiles(self):
        """
        Creates scaled versions of each tile image and stores them in self.scaled_tiles.
        Iterates through all possible GIDs in the TMX data.
        """
        max_gid = self.tmx_data.maxgid
        for gid in range(max_gid):
            tile_img = self.tmx_data.get_tile_image_by_gid(gid)
            if tile_img:
                # Scale the tile image
                w, h = tile_img.get_width(), tile_img.get_height()
                scaled_img = pygame.transform.scale(tile_img, (w * self.scale, h * self.scale))
                self.scaled_tiles[gid] = scaled_img
                
    def get_scaled_tiles(self):
        return self.scaled_tiles


    def get_map_grid(self):
        map = [[0 for i in range(40)] for j in range(21)]
        for layer in self.tmx_data.visible_layers:
            # Check if this is a tile layer and if its name matches the one we need.
            if hasattr(layer, 'data') and layer.name == "Walls":
                for x, y, gid in layer:
                    # Get the tile image (if available). We only need the rect.
                    tile = self.scaled_tiles.get(gid)
                    if tile:
                        map[y][x] = 1
        return map


    def draw(self, screen):
        """
        Draws the map by looking up each tile's scaled
        image and blitting it at scaled positions.
        """
        tilewidth = self.tmx_data.tilewidth * self.scale
        tileheight = self.tmx_data.tileheight * self.scale

        for layer in self.tmx_data.visible_layers:
            # Only tile layers have 'data'; object layers do not.
            if hasattr(layer, 'data'):
                for x, y, gid in layer:
                    tile = self.scaled_tiles.get(gid)
                    if tile:
                        # size of the maze map needed (as rectangle): [0, 48, 1280, 672]
                        # Multiply tile coordinates by the scale-adjusted width/height, and add 48 to y to account for space for HUD.
                        screen.blit(tile, (x * tilewidth, y * tileheight + 48))