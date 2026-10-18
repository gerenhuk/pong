from pygame import *

WIDTH, HEIGHT = 800, 600
init()
mixer.init()  
screen = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
display.set_caption("Пінг-Понг")

font_win = font.Font(None, 72)
font_main = font.Font(None, 36)

try:
    img_player = image.load("Player.png").convert_alpha()
    img_computer = image.load("Computer.png").convert_alpha()
    img_ball = image.load("Ball.png").convert_alpha()  
    img_ball_motion = image.load("BallMotion.png").convert_alpha()
    img_score_bar = image.load("ScoreBar.png").convert_alpha()
    img_board = image.load("Board.png").convert_alpha()
    
    img_player = transform.scale(img_player, (20, 100))
    img_computer = transform.scale(img_computer, (20, 100))
    img_ball = transform.scale(img_ball, (20, 20))
    img_ball_motion = transform.scale(img_ball_motion, (20, 20))
    img_score_bar = transform.scale(img_score_bar, (WIDTH, 50))
    img_board = transform.scale(img_board, (WIDTH, HEIGHT))
except Exception as e:
    img_player = img_computer = img_ball = img_ball_motion = img_score_bar = img_board = None

try:
    sound_hit = mixer.Sound("sound.mp3")
except Exception as e:
    sound_hit = None

paddle_0_y = HEIGHT // 2 - 50
paddle_1_y = HEIGHT // 2 - 50
paddle_speed = 7

ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = 5
ball_speed_y = 5

score_0 = 0
score_1 = 0

winner = None
game_over = False

while True:
    for e in event.get():
        if e.type == QUIT:
            exit()
        if e.type == KEYDOWN:
            if winner is not None and e.key == K_k:
                score_0 = 0
                score_1 = 0
                ball_x = WIDTH // 2
                ball_y = HEIGHT // 2
                winner = None

    if winner is None:
        keys = key.get_pressed()
        if keys[K_w] and paddle_0_y > 50:
            paddle_0_y -= paddle_speed
        if keys[K_s] and paddle_0_y < HEIGHT - 100:
            paddle_0_y += paddle_speed

        if keys[K_UP] and paddle_1_y > 50:
            paddle_1_y -= paddle_speed
        if keys[K_DOWN] and paddle_1_y < HEIGHT - 100:
            paddle_1_y += paddle_speed

        ball_x += ball_speed_x
        ball_y += ball_speed_y

        if ball_y <= 60 or ball_y >= HEIGHT - 10:
            ball_speed_y *= -1
            if sound_hit:
                sound_hit.play()

        ball_rect = Rect(ball_x - 10, ball_y - 10, 20, 20)
        p0_rect = Rect(20, paddle_0_y, 20, 100)
        p1_rect = Rect(WIDTH - 40, paddle_1_y, 20, 100)

        if ball_rect.colliderect(p0_rect) or ball_rect.colliderect(p1_rect):
            ball_speed_x *= -1
            if sound_hit:
                sound_hit.play()

        if ball_x < 0:
            score_1 += 1
            ball_x = WIDTH // 2
            ball_y = HEIGHT // 2
            ball_speed_x *= -1
        elif ball_x > WIDTH:
            score_0 += 1
            ball_x = WIDTH // 2
            ball_y = HEIGHT // 2
            ball_speed_x *= -1

        if score_0 >= 5:
            winner = 0
        elif score_1 >= 5:
            winner = 1

    if img_board:
        screen.blit(img_board, (0, 0))
    else:
        screen.fill((30, 30, 30))

    if img_player:
        screen.blit(img_player, (20, paddle_0_y))
    else:
        draw.rect(screen, (0, 255, 0), (20, paddle_0_y, 20, 100))

    if img_computer:
        screen.blit(img_computer, (WIDTH - 40, paddle_1_y))
    else:
        draw.rect(screen, (255, 0, 255), (WIDTH - 40, paddle_1_y, 20, 100))

    if img_ball:
        screen.blit(img_ball, (ball_x - 10, ball_y - 10))
    else:
        draw.circle(screen, (255, 255, 255), (ball_x, ball_y), 10)

    if img_score_bar:
        screen.blit(img_score_bar, (0, 0))

    score_text = font_main.render(f"{score_0} : {score_1}", True, (255, 255, 255))
    screen.blit(score_text, (WIDTH // 2 - 25, 10))

    if winner is not None:
        screen.fill((20, 20, 20))
        text = f"Гравець {winner + 1} переміг!"
        win_text = font_win.render(text, True, (255, 215, 0))
        text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(win_text, text_rect)

        restart_text = font_win.render('К - рестарт', True, (255, 215, 0))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
        screen.blit(restart_text, restart_rect)

    display.update()
    clock.tick(60)
