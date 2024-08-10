import random
import sys

import pygame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)  # Color for special food

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

def load_music(file_path):
    try:
        pygame.mixer.music.load(file_path)
    except pygame.error as e:
        print(f"Error loading music file: {e}")

        # Informing the user incase they couldn't load the music
        print("Music file not found. Continuing without background music.")


# Load background music
music_file_path = 'D:/MASTERS/Snake game/arcade music.mp3'
load_music(music_file_path)
pygame.mixer.music.set_volume(0.1)  # Adjust volume if needed
pygame.mixer.music.play(loops=-1)  # Play music indefinitely

# Global variables
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
direction = (1, 0)  # Initial direction (right)
score = 0  # Initialize score
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
special_food = None
food_counter = 0

# Special food size, can adjust as needed
SPECIAL_FOOD_SIZE = 30

# Function to reset game state
def reset_game():
    global snake, direction, food, score, special_food, food_counter
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (1, 0)
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    special_food = None
    score = 0
    food_counter = 0

# Function to spawn special food
def spawn_special_food():
    global special_food
    special_food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

# Main game loop
def main():
    global direction, score, food_counter, food, special_food  # Declare global variables

    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    # Check if mouse click is within replay button area
                    if SCREEN_WIDTH // 2 - 50 <= event.pos[0] <= SCREEN_WIDTH // 2 + 50 and SCREEN_HEIGHT // 2 + 50 <= event.pos[1] <= SCREEN_HEIGHT // 2 + 100:
                        reset_game()
                        game_over = False
                    # Check if mouse click is within quit button area
                    elif SCREEN_WIDTH // 2 - 50 <= event.pos[0] <= SCREEN_WIDTH // 2 + 50 and SCREEN_HEIGHT // 2 + 150 <= event.pos[1] <= SCREEN_HEIGHT // 2 + 200:
                        pygame.quit()
                        sys.exit()

        if not game_over:
            # Move the snake
            head = snake[-1]
            new_head = (head[0] + direction[0], head[1] + direction[1])
            snake.append(new_head)

            # Check collision with food
            if new_head == food:
                score += 1
                food_counter += 1
                if food_counter % 10 == 0:  # Spawn special food every 10 regular foods
                    spawn_special_food()
                else:
                    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

            # Check collision with special food
            elif special_food and new_head == special_food:
                score += 5
                special_food = None  # Reset special food after eaten
                food_counter = 0  # Reset food counter after special food

            else:
                snake.pop(0)

            # Check collision with boundaries
            if new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT:
                game_over = True
                game_over_message = "Game Over! The snake touched the boundary"

            # Check collision with itself
            if new_head in snake[:-1]:
                game_over = True
                game_over_message = "Game Over! The snake tried to eat itself"

            # Clear the screen
            screen.fill(BLACK)

            # Draw the food
            pygame.draw.rect(screen, RED, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

            # Draw the special food if it exists
            if special_food:
                # Larger size for special food
                pygame.draw.rect(screen, YELLOW, (special_food[0] * GRID_SIZE, special_food[1] * GRID_SIZE, SPECIAL_FOOD_SIZE, SPECIAL_FOOD_SIZE))

            # Draw the snake
            for segment in snake:
                pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

            # Display the score
            font = pygame.font.Font(None, 24)
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

            # If game over, display appropriate message and buttons
            if game_over:
                font = pygame.font.Font(None, 36)
                lose_text = font.render(game_over_message, True, RED)
                text_rect = lose_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(lose_text, text_rect)
                # Replay button
                pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, 100, 50))
                font = pygame.font.Font(None, 24)
                replay_text = font.render("Replay", True, BLACK)
                replay_rect = replay_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 75))
                screen.blit(replay_text, replay_rect)
                # Quit button
                pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 150, 100, 50))
                quit_text = font.render("Quit", True, BLACK)
                quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 175))
                screen.blit(quit_text, quit_rect)

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(10)  # Adjust FPS as needed

if __name__ == "__main__":
    main()
