"""
Defines and is a placeholder for each game
"""

class Game:
    def __init__(self, title, platform, photo):
        self.title = title
        self.platform = platform
        self.photo = photo

    def __repr__(self):
        return f"Game(title='{self.title}', platform='{self.platform}', photo='{self.photo}')"

