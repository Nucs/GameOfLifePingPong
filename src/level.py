class Level:
    def __init__(self, level_number, game_of_life):
        self.level_number = level_number
        self.game_of_life = game_of_life

    def generate(self):
        random.seed(self.level_number)
        self.game_of_life.grid = [[random.randint(0, 1) for _ in range(self.game_of_life.height)] for _ in range(self.game_of_life.width)]

class Score:
    def __init__(self):
        self.points = 0

    def increase(self, amount):
        self.points += amount

    def reset(self):
        self.points = 0

# Create a level and score instance
level = Level(1, game_of_life)
level.generate()
score = Score()

