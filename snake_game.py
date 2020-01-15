import pygame
import random
import time
import json

RED = (225, 0, 0)
WHITE = (225, 225, 225)
BLACK = (0, 0, 0)
GREEN = (0, 155, 0)
BLUE = (0, 0, 225)
choice_set = True
start_menu = True
BLOCK_SIZE = 20
GAME_RULES = """Don't run the snake into the wall, or his own tail ==> you die.
Use your cursor keys: up, left, right, and down.
Keyboard "P" may be used for "Pause"
Eat the colored apples to gain points."""


def read_configuration():
    with open('conf/config.json') as json_file:
        return json.load(json_file)


def write_score(score):
    with open('db/score.txt', 'w') as f:
        f.write(str(score))


def read_score():
    with open('db/score.txt', 'r') as f:
        return int(f.read())


conf = read_configuration()
game_conf = conf["game"]
set_1_conf = conf["set_1"]
set_2_conf = conf["set_2"]

WINDOW_WIDTH = int(game_conf['WINDOW_WIDTH'])
WINDOW_HEIGHT = int(game_conf['WINDOW_HEIGHT'])
FPS = int(game_conf['FPS'])

pygame.init()
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption(game_conf['caption'])
font_name = pygame.font.match_font('couriernew')

head_img = pygame.image.load(set_1_conf["head_img"])
body_image = pygame.image.load(set_1_conf["body_img"])
apple_img = pygame.image.load(set_1_conf["apple_img"])
tail_img = pygame.image.load(set_1_conf["tail_img"])
game_background = pygame.image.load(set_1_conf["game_background"])
menu_background = pygame.image.load(game_conf["menu_background"])
start_background = pygame.image.load(game_conf["start_background"])
clock = pygame.time.Clock()
direction = "right"


def draw_text(surf, text, text_size, color, x, y):
    font = pygame.font.Font(font_name, text_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def snake(snake_list):
    head = head_img
    body = body_image
    tail = tail_img
    tail_pos = 0
    if direction == "right":
        head = pygame.transform.rotate(head_img, 270)
    if direction == "left":
        head = pygame.transform.rotate(head_img, 90)
    if direction == "up":
        head = head_img
    if direction == "down":
        head = pygame.transform.rotate(head_img, 180)
    screen.blit(head, (snake_list[-1][0], snake_list[-1][1]))

    if direction == "right":
        tail = pygame.transform.rotate(tail_img, 270)
        tail_pos = snake_list[0][0] - BLOCK_SIZE, snake_list[0][1]
    if direction == "left":
        tail = pygame.transform.rotate(tail_img, 90)
        tail_pos = snake_list[0][0] + BLOCK_SIZE, snake_list[0][1]
    if direction == "up":
        tail = tail_img
        tail_pos = snake_list[0][0], snake_list[0][1] + BLOCK_SIZE
    if direction == "down":
        tail = pygame.transform.rotate(tail_img, 180)
        tail_pos = snake_list[0][0], snake_list[0][1] - BLOCK_SIZE
    screen.blit(tail, tail_pos)
    for XnY in snake_list[:-1]:
        if direction == "right":
            body = pygame.transform.rotate(body_image, 270)
        if direction == "left":
            body = pygame.transform.rotate(body_image, 90)
        if direction == "up":
            body = body_image
        if direction == "down":
            body = pygame.transform.rotate(body_image, 180)
        screen.blit(body, (XnY[0], XnY[1]))


def quit_func():
    pygame.quit()
    quit()


def start_func(high_score):
    global choice_set, start_menu
    while start_menu:
        screen.blit(start_background, (0, 0))
        draw_text(screen, "START MENU", 50, GREEN, WINDOW_WIDTH / 2, WINDOW_HEIGHT - 550)
        draw_text(screen, game_conf["rule_1"], 20, RED, WINDOW_WIDTH / 2, WINDOW_HEIGHT - 450)
        draw_text(screen, game_conf["rule_2"], 20, RED, WINDOW_WIDTH / 2, WINDOW_HEIGHT - 400)
        draw_text(screen, game_conf["rule_3"], 20, RED, WINDOW_WIDTH / 2, WINDOW_HEIGHT - 350)
        draw_text(screen, game_conf["rule_4"], 20, RED, WINDOW_WIDTH / 2, WINDOW_HEIGHT - 300)
        draw_text(screen, game_conf["rule_5"], 20, RED, WINDOW_WIDTH / 2, WINDOW_HEIGHT - 250)
        draw_text(screen, "press n to continue or q to quit", 25, BLUE, WINDOW_WIDTH / 2, WINDOW_HEIGHT - 200)
        draw_text(screen, "GOOD LUCK", 50, GREEN, WINDOW_WIDTH / 2, WINDOW_HEIGHT - 70)
        draw_text(screen, "high_score: " + str(high_score), 40, GREEN, WINDOW_WIDTH / 2, 450)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_func()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quit_func()
                elif event.key == pygame.K_n:
                    snake_set()
                    start_menu = False


def snake_set():
    selected_conf = set_1_conf
    global head_img, apple_img, body_image, tail_img, game_background, choice_set, start_menu
    while choice_set:
        screen.blit(start_background, (0, 0))
        draw_text(screen, "set_1", 20, BLUE, WINDOW_WIDTH / 2 - 250, WINDOW_HEIGHT - 550)
        draw_text(screen, "set_2", 20, BLUE, WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT - 550)
        draw_text(screen, "set_3", 20, BLUE, WINDOW_WIDTH / 2 + 50, WINDOW_HEIGHT - 550)
        draw_text(screen, "set_4", 20, BLUE, WINDOW_WIDTH / 2 + 250, WINDOW_HEIGHT - 550)
        screen.blit(pygame.image.load(set_1_conf["full_set_1"]), (WINDOW_WIDTH / 2 - 300, WINDOW_HEIGHT - 500))
        screen.blit(pygame.image.load(set_2_conf["full_set_2"]), (WINDOW_WIDTH / 2 - 150, WINDOW_HEIGHT - 500))
        screen.blit(pygame.image.load(game_conf["credit_card"]), (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 500))
        screen.blit(pygame.image.load(game_conf["credit_card"]), (WINDOW_WIDTH / 2 + 200, WINDOW_HEIGHT - 500))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_func()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quit_func()
                elif event.key == pygame.K_1:
                    selected_conf = set_1_conf
                    choice_set = False
                elif event.key == pygame.K_2:
                    selected_conf = set_2_conf
                    choice_set = False
    head_img = pygame.image.load(selected_conf["head_img"])
    body_image = pygame.image.load(selected_conf["body_img"])
    apple_img = pygame.image.load(selected_conf["apple_img"])
    tail_img = pygame.image.load(selected_conf["tail_img"])
    game_background = pygame.image.load(selected_conf["game_background"])


def game_loop():
    global direction
    lead_x = WINDOW_WIDTH / 2
    lead_y = WINDOW_HEIGHT / 2
    lead_y_change = 0
    lead_x_change = 0
    apple_pos_x = random.randrange(0, WINDOW_WIDTH - BLOCK_SIZE, BLOCK_SIZE)
    apple_pos_y = random.randrange(0, WINDOW_HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
    sleep_time = 1
    score = 2
    snake_list = []
    snake_length = 1
    finish = False
    try_again = False
    pause = False
    direction = "right"
    high_score = read_score()
    start_func(high_score)
    while not finish:
        if pause:
            finish, pause, try_again = pause_func(finish, pause, try_again, score, high_score)
        if try_again:
            finish, try_again, high_score = try_again_func(finish, try_again, score, high_score)

        if not finish:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause = True
                    if event.key == pygame.K_LEFT:
                        direction = "left"
                        lead_x_change = -BLOCK_SIZE
                        lead_y_change = 0
                    elif event.key == pygame.K_RIGHT:
                        direction = "right"
                        lead_x_change = BLOCK_SIZE
                        lead_y_change = 0
                    elif event.key == pygame.K_UP:
                        direction = "up"
                        lead_y_change = -BLOCK_SIZE
                        lead_x_change = 0
                    elif event.key == pygame.K_DOWN:
                        direction = "down"
                        lead_y_change = BLOCK_SIZE
                        lead_x_change = 0
            if lead_x >= WINDOW_WIDTH or lead_x < 0 or lead_y >= WINDOW_HEIGHT or lead_y < 0:
                draw_text(screen, "you lose", 25, RED, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
                pygame.display.update()
                time.sleep(sleep_time)
                try_again = True

            lead_y += lead_y_change
            lead_x += lead_x_change
            screen.blit(game_background, (0, 0))

            snake_head = [lead_x, lead_y]
            snake_list.append(snake_head)

            if len(snake_list) > snake_length:
                del snake_list[0]
            for i in snake_list[:-1]:
                if i == snake_list[-1]:
                    draw_text(screen, "you lose", 25, RED, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
                    pygame.display.update()
                    time.sleep(sleep_time)
                    try_again = True

            snake(snake_list)
            screen.blit(apple_img, (apple_pos_x, apple_pos_y))
            pygame.display.update()

            if lead_x == apple_pos_x and lead_y == apple_pos_y:
                apple_pos_x = round(random.randrange(0, WINDOW_HEIGHT - BLOCK_SIZE) / 20.0) * 20.0
                apple_pos_y = round(random.randrange(0, WINDOW_HEIGHT - BLOCK_SIZE) / 20.0) * 20.0
                snake_length += 1
                score += 1

            clock.tick(FPS)


def try_again_func(finish, try_again, score, high_score):
    if score > high_score:
        high_score = score
        write_score(high_score)
    while try_again:
        screen.blit(menu_background, (0, 0))
        draw_text(screen, "GAME OVER", 50, RED, WINDOW_WIDTH / 2, WINDOW_HEIGHT - 500)
        draw_text(screen, "press r to try again or  press q to exit", 25, RED, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        draw_text(screen, "high_score: " + str(high_score), 25, BLUE, 200, 500)
        draw_text(screen, "your_score: " + str(score), 25, BLUE, 600, 500)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
                try_again = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    try_again = False
                    finish = True
                    game_loop()
                    break
                elif event.key == pygame.K_q:
                    try_again = False
                    finish = True
    return finish, try_again, high_score


def pause_func(finish, pause, try_again, score, high_score):
    while pause:
        screen.blit(menu_background, (0, 0))
        draw_text(screen, "MENU", 50, RED, WINDOW_WIDTH / 2, WINDOW_HEIGHT - 500)
        draw_text(screen, "press c to resume or  press q to exit", 25, RED, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        draw_text(screen, "high_score: " + str(high_score), 25, BLUE, 200, 500)
        draw_text(screen, "your_score: " + str(score), 25, BLUE, 600, 500)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
                try_again = False
                pause = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    finish = True
                    try_again = False
                    pause = False

                elif event.key == pygame.K_c:
                    pause = False
    return finish, pause, try_again


def main():
    game_loop()
    quit_func()


if __name__ == '__main__':
    main()
