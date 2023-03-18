import pygame
import numpy as np
import random

class Paddle:
    def __init__(self, x, y, speed=10):
        self.x = x
        self.y = y
        self.speed = speed
        self.height = 100
        self.width = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, keys):
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < 600 - self.height:
            self.y += self.speed
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

class Ball:
    def __init__(self, x, y, speed=10):
        self.x = x
        self.y = y
        self.speed = speed
        self.vx = -speed
        self.vy = 0
        self.radius = 5
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def update(self, paddle, game_of_life):
        self.x += self.vx
        self.y += self.vy
        success = 0

        # Check for collision with top or bottom walls
        if self.y <= self.radius:
            self.y = self.radius
            self.vy = -self.vy
        elif self.y >= 600 - self.radius:
            self.y = 600 - self.radius
            self.vy = -self.vy

        # Check for collision with left or right walls
        if self.x <= 0:
            self.vx = -self.vx
        elif self.x >= 1280 - self.radius:
            self.reset()
            return 0, 1

        # Check for collision with paddle
        if paddle.rect.collidepoint(self.x-self.radius*2, self.y) and self.vx > 0:
            self.vx = -abs(self.vx)  # Ensures that the ball always bounces to the left
            self.vy += (self.y - paddle.y - paddle.height // 2) // 10
            angle_variation = random.uniform(-1, 1) * 0.03 * np.pi
            self.vx, self.vy = self.rotate_vector(self.vx, self.vy, angle_variation)
            self.x = paddle.rect.right + self.radius  # Ensures the ball doesn't get stuck inside the paddle
            game_of_life.spawn_cells(3)
            game_of_life.update() # update without rendering
            
            return 0, 0

        cell_x, cell_y = (self.x - game_of_life.cell_size) // game_of_life.cell_size, self.y // game_of_life.cell_size

        if 0 <= cell_x < game_of_life.grid.shape[1] and 0 <= cell_y < game_of_life.grid.shape[0]:
            points_to_check = [
                (self.x, self.y),
                (self.x + self.radius, self.y),
                (self.x - self.radius, self.y),
                (self.x, self.y + self.radius),
                (self.x, self.y - self.radius),
            ]

            for point_x, point_y in points_to_check:
                cell_x, cell_y = int(point_x // game_of_life.cell_size), int(point_y // game_of_life.cell_size)

                if 0 <= cell_x < game_of_life.grid.shape[1] and 0 <= cell_y < game_of_life.grid.shape[0]:
                    if game_of_life.grid[cell_y, cell_x] == 1:
                        # Calculate the surface normal
                        left = game_of_life.grid[cell_y, (cell_x - 1) % game_of_life.cols]
                        right = game_of_life.grid[cell_y, (cell_x + 1) % game_of_life.cols]
                        top = game_of_life.grid[(cell_y - 1) % game_of_life.rows, cell_x]
                        bottom = game_of_life.grid[(cell_y + 1) % game_of_life.rows, cell_x]
                        surface_normal = np.array([right - left, bottom - top])

                        norm = np.linalg.norm(surface_normal)
                        if norm != 0:
                            # Normalize the surface normal
                            surface_normal = surface_normal / norm

                            # Calculate the incoming vector
                            incoming_vector = np.array([self.vx, self.vy])

                            # Calculate the reflection vector
                            reflection_vector = incoming_vector - 2 * np.dot(incoming_vector, surface_normal) * surface_normal

                            # Update the ball's velocity
                            self.vx, self.vy = reflection_vector
                        else:
                            # Reverse both x and y velocities if surface normal is a zero vector
                            self.vx, self.vy = -self.vx, -self.vy

                        angle_variation = random.uniform(-1, 1) * 0.03 * np.pi
                        self.vx, self.vy = self.rotate_vector(self.vx, self.vy, angle_variation)

                        game_of_life.grid[cell_y, cell_x] = 0
                        success = 1
                        break


        velocity_magnitude = np.sqrt(self.vx**2 + self.vy**2)
        self.vx, self.vy = (self.vx / velocity_magnitude) * self.speed, (self.vy / velocity_magnitude) * self.speed

        # Adjust horizontal velocity if vertical velocity is only 5% of the total velocity
        if abs(self.vy) <= 0.10 * self.speed and self.x > game_of_life.cell_size * game_of_life.cols:
            self.vx += np.sign(self.vx) * self.speed * 0.10
            self.vy -= np.sign(self.vy) * self.speed * 0.10

            # Clamp the velocity to maintain a constant speed
            velocity_magnitude = np.sqrt(self.vx**2 + self.vy**2)
            self.vx, self.vy = (self.vx / velocity_magnitude) * self.speed, (self.vy / velocity_magnitude) * self.speed

        self.rect.x = self.x
        self.rect.y = self.y

        return success, 0

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius)

    def reset(self):
        self.x = 960
        self.y = 300
        self.vx = -5
        self.vy = 0
        angle_variation = random.uniform(-1, 1) * 0.3 * np.pi
        self.vx, self.vy = self.rotate_vector(self.vx, self.vy, angle_variation)

    def rotate_vector(self, vx, vy, angle):
        c, s = np.cos(angle), np.sin(angle)
        new_vx = vx * c - vy * s
        new_vy = vx * s + vy * c
        return new_vx, new_vy