import pygame
import random
import sys
import datetime
import json

pygame.init()

# Constants
WIDTH, HEIGHT = 500, 500
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
FONT = pygame.font.SysFont('consolas', 24)
LOG_FILE = "highscores.log"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Directions dictionary for keys
DIRECTIONS = {
    pygame.K_UP: (0, -1),
    pygame.K_w: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_s: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_a: (-1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_d: (1, 0),
}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Games")
clock = pygame.time.Clock()


def draw_text(text, pos, color=WHITE):
    img = FONT.render(text, True, color)
    screen.blit(img, pos)


def load_highscores():
    scores = []
    try:
        with open(LOG_FILE, 'r') as f:
            for line in f:
                scores.append(line.strip())
    except FileNotFoundError:
        pass
    return scores


def save_highscore(name, score):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a') as f:
        f.write(f"{name},{now},{score}\n")


def menu_screen():
    selected = 0
    options = ["Difficulty:", "Start Game", "High Scores", "Quit"]
    difficulties = ["Easy", "Medium", "Hard"]
    difficulty_speeds = {"Easy": 5, "Medium": 10, "Hard": 15}
    current_difficulty_index = 1  # default Medium
    highscores = load_highscores()

    while True:
        screen.fill(BLACK)
        draw_text("SNAKE GAME MENU", (150, 40), YELLOW)

        # Draw difficulty with left/right arrows hint if selected
        for i, option in enumerate(options):
            if option == "Difficulty:":
                color = GREEN if selected == i else WHITE
                diff_text = difficulties[current_difficulty_index]
                draw_text(f"{option} {diff_text}", (150, 120), color)
                if selected == i:
                    draw_text("< >", (320, 120), color)
            else:
                color = GREEN if selected == i else WHITE
                draw_text(option, (200, 160 + (i - 1) * 40), color)

        if selected == 2:  # High Scores option selected, show scores
            draw_text("HIGH SCORES:", (50, 280), YELLOW)
            if highscores:
                for idx, entry in enumerate(highscores[-5:]):
                    parts = entry.split(',')
                    if len(parts) >= 3:
                        name, datetime_str, score = parts[0], parts[1], parts[2]
                        draw_text(f"{name} - {score} - {datetime_str}", (50, 310 + idx * 30), WHITE)
            else:
                draw_text("No high scores yet.", (50, 310), WHITE)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)

                elif selected == 0 and event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    # Change difficulty left/right
                    if event.key == pygame.K_LEFT:
                        current_difficulty_index = (current_difficulty_index - 1) % len(difficulties)
                    else:
                        current_difficulty_index = (current_difficulty_index + 1) % len(difficulties)

                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if options[selected] == "Start Game":
                        # Return selected FPS speed to game loop
                        return difficulty_speeds[difficulties[current_difficulty_index]]
                    elif options[selected] == "Quit":
                        pygame.quit()
                        sys.exit()
                    elif options[selected] == "High Scores":
                        # Do nothing extra - highscores shown in menu

                        pass


def game_loop(fps):
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (0, -1)
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    score = 0
    paused = False

    while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key in DIRECTIONS and not paused:
                    new_dir = DIRECTIONS[event.key]
                    if (new_dir[0] != -direction[0]) or (new_dir[1] != -direction[1]):
                        direction = new_dir

        if paused:
            draw_pause()
            pygame.display.flip()
            continue

        new_head = (snake[-1][0] + direction[0], snake[-1][1] + direction[1])
        new_head = (new_head[0] % GRID_WIDTH, new_head[1] % GRID_HEIGHT)

        if new_head in snake:
            player_name = game_over_screen(score)
            save_highscore(player_name, score)
            return

        snake.append(new_head)

        if new_head == food:
            score += 1
            while True:
                food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                if food not in snake:
                    break
        else:
            snake.pop(0)

        screen.fill(BLACK)
        food_rect = pygame.Rect(food[0]*CELL_SIZE, food[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, food_rect)

        for segment in snake:
            rect = pygame.Rect(segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GREEN, rect)

        draw_text(f"Score: {score}", (10, 10), YELLOW)
        pygame.display.flip()


def draw_pause():
    pause_text = FONT.render("Paused. Press P to resume.", True, YELLOW)
    screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))


def game_over_screen(score):
    input_active = True
    player_name = ""
    while input_active:
        screen.fill(BLACK)
        draw_text("GAME OVER!", (180, 150), RED)
        draw_text(f"Score: {score}", (200, 190), WHITE)
        draw_text("Enter your name: " + player_name, (120, 230), YELLOW)
        draw_text("Press Enter to continue", (150, 270), WHITE)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and player_name.strip():
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    if len(player_name) < 10 and event.unicode.isprintable():
                        player_name += event.unicode

    return player_name.strip()


def main():
    while True:
        fps = menu_screen()
        game_loop(fps)


if __name__ == "__main__":
    main()
