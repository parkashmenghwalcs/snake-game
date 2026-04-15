import pygame
import random
import os

pygame.init()
pygame.mixer.init()

# Screen
WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Pro Ultimate")

# Colors
BG = (15, 18, 30)
GRID = (30, 35, 50)
SNAKE = (0, 200, 100)
HEAD = (0, 255, 150)
FOOD = (255, 80, 80)
WHITE = (255, 255, 255)

# Settings
BLOCK = 10
speed = 12

clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 22)
big_font = pygame.font.SysFont("arial", 40)

# Sounds
eat_sound = pygame.mixer.Sound("sounds/eat.wav")
gameover_sound = pygame.mixer.Sound("sounds/gameover.wav")

# High score
if not os.path.exists("highscore.txt"):
    with open("highscore.txt", "w") as f:
        f.write("0")

def get_high():
    with open("highscore.txt", "r") as f:
        data = f.read().strip()
        return int(data) if data else 0

def save_high(s):
    with open("highscore.txt", "w") as f:
        f.write(str(s))

def draw_grid():
    for x in range(0, WIDTH, BLOCK):
        pygame.draw.line(screen, GRID, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK):
        pygame.draw.line(screen, GRID, (0, y), (WIDTH, y))

def draw_snake(snake):
    for i, pos in enumerate(snake):
        color = HEAD if i == len(snake) - 1 else SNAKE
        pygame.draw.circle(screen, color, (pos[0] + 5, pos[1] + 5), 5)

def game():
    global speed

    x, y = WIDTH//2, HEIGHT//2
    dx, dy = 0, 0

    snake = []
    length = 1

    foodx = random.randrange(0, WIDTH, BLOCK)
    foody = random.randrange(0, HEIGHT, BLOCK)

    score = 0
    high = get_high()

    paused = False
    running = True
    game_over = False

    while running:

        # GAME OVER SCREEN
        while game_over:
            screen.fill(BG)

            t = big_font.render("GAME OVER", True, FOOD)
            screen.blit(t, (WIDTH//3, HEIGHT//3))

            t2 = font.render("R = Restart | Q = Quit", True, WHITE)
            screen.blit(t2, (WIDTH//3, HEIGHT//2))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                        game_over = False
                    if event.key == pygame.K_r:
                        game()

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                # Pause
                if event.key == pygame.K_p:
                    paused = not paused

                if not paused:
                    if event.key == pygame.K_LEFT and dx == 0:
                        dx, dy = -BLOCK, 0
                    elif event.key == pygame.K_RIGHT and dx == 0:
                        dx, dy = BLOCK, 0
                    elif event.key == pygame.K_UP and dy == 0:
                        dx, dy = 0, -BLOCK
                    elif event.key == pygame.K_DOWN and dy == 0:
                        dx, dy = 0, BLOCK

        if paused:
            pause_text = big_font.render("PAUSED", True, WHITE)
            screen.blit(pause_text, (WIDTH//3, HEIGHT//2))
            pygame.display.update()
            continue

        # MOVE
        x += dx
        y += dy

        # WALL COLLISION
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            gameover_sound.play()
            game_over = True

        screen.fill(BG)
        draw_grid()

        # FOOD
        pygame.draw.rect(screen, FOOD, [foodx, foody, BLOCK, BLOCK])

        # SNAKE
        head = [x, y]
        snake.append(head)

        if len(snake) > length:
            del snake[0]

        # SELF COLLISION
        for part in snake[:-1]:
            if part == head:
                gameover_sound.play()
                game_over = True

        draw_snake(snake)

        # EAT FOOD
        if x == foodx and y == foody:
            foodx = random.randrange(0, WIDTH, BLOCK)
            foody = random.randrange(0, HEIGHT, BLOCK)
            length += 1
            score += 10
            speed += 0.3
            eat_sound.play()

        # HIGH SCORE
        if score > high:
            high = score
            save_high(high)

        # UI
        score_text = font.render(f"Score: {score}  High: {high}", True, WHITE)
        screen.blit(score_text, (10, 10))

        level = "Easy" if score < 50 else "Medium" if score < 150 else "Hard"
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(level_text, (10, 35))

        pygame.display.update()
        clock.tick(speed)

    pygame.quit()
    quit()

game()