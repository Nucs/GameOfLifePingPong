import pygame
import sys
from game_of_life import GameOfLife
from ping_pong import Paddle, Ball

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ping Pong & Game of Life")
clock = pygame.time.Clock()

# Game objects
game_of_life = GameOfLife(SCREEN_WIDTH // 2, SCREEN_HEIGHT)
paddle = Paddle(SCREEN_WIDTH - 30, SCREEN_HEIGHT // 2 - 50)
ball = Ball(SCREEN_WIDTH - 60, SCREEN_HEIGHT // 2)

# Score
score = 0
font = pygame.font.Font(None, 36)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Update game objects
    if ball.x > SCREEN_WIDTH // 2:
        game_of_life.update()
    paddle.update(keys)
    bounced, missed = ball.update(paddle, game_of_life)
    if bounced:
        score += 1
    if missed:
        score = int(score / 2)

    # Draw game objects
    screen.fill(BLACK)
    game_of_life.draw(screen)
    paddle.draw(screen)
    ball.draw(screen)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH - 300, 10))

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)
