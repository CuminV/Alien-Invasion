import json


class Config:
    """User-configurable settings changed through the menu."""

    def __init__(self):
        # Config file
        self.config_file = 'config.json'
        
        # Video
        self.width = 1920
        self.height = 1080
        self.display_mode = "fullscreen"

        # Audio
        self.music_volume = 50
        self.sfx_volume = 50

        # Gameplay
        self.difficulty = "medium"
        
        self.load()

    @property
    def resolution(self):
        return (self.width, self.height)


    def to_dict(self):
        return {'width': self.width, 
                'height': self.height, 
                'display_mode': self.display_mode,
                'music_volume': self.music_volume, 
                'sfx_volume': self.sfx_volume, 
                'difficulty': self.difficulty,
            }
    
     
    def load(self):
        try:
            with open(self.config_file, 'r') as f:
                user_config = json.load(f)
        except FileNotFoundError: 
            return
        
        self.width = user_config['width']
        self.height = user_config['height']
        self.display_mode = user_config['display_mode']
        self.music_volume = user_config['music_volume']            
        self.sfx_volume = user_config['sfx_volume']
        self.difficulty = user_config['difficulty']
     
            
    def save(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.to_dict(), f)