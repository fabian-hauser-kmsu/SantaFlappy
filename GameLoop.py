import pygame
from random import randint

pygame.init()
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Santa Flappy")
clock = pygame.time.Clock()

try:
    santa_img = pygame.image.load("SantaFlappy/Santa.png").convert_alpha()
    tree_img = pygame.image.load("SantaFlappy/Tree.png").convert_alpha()
    cloud_img = pygame.image.load("SantaFlappy/Cloud.png").convert_alpha()
    tundra_img = pygame.image.load("SantaFlappy/tundra.png").convert()
except:
    santa_img = pygame.Surface((100, 33)); santa_img.fill("red")
    tree_img = pygame.Surface((50, 200)); tree_img.fill("green")
    cloud_img = pygame.Surface((50, 200)); cloud_img.fill("white")
    tundra_img = pygame.Surface((500, 500)); tundra_img.fill("blue")

santa_img = pygame.transform.scale(santa_img, (60, 25))
tree_img = pygame.transform.scale(tree_img, (50, 300))
cloud_img = pygame.transform.scale(cloud_img, (60, 300))
tundra_img = pygame.transform.scale(tundra_img, (WIDTH, HEIGHT))

player_pos = pygame.Vector2(100, HEIGHT / 2)
player_vel = 0
gravity = 800
jump_strength = -300

scroll_speed = 2
bg_x1 = 0
bg_x2 = WIDTH

hindernisse = []
spawn_dist = 250
for i in range(3):
    hindernisse.append([WIDTH + i * spawn_dist, randint(150, 350)])

def reset_game():
    return pygame.Vector2(100, HEIGHT / 2), 0, [[WIDTH + i * spawn_dist, randint(150, 350)] for i in range(3)]

running = True
game_active = True
dt = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    player_vel = jump_strength
                else:
                    player_pos, player_vel, hindernisse = reset_game()
                    game_active = True

    if game_active:
        bg_x1 -= scroll_speed
        bg_x2 -= scroll_speed
        if bg_x1 <= -WIDTH: bg_x1 = WIDTH
        if bg_x2 <= -WIDTH: bg_x2 = WIDTH

        player_vel += gravity * dt
        player_pos.y += player_vel * dt

        if player_pos.y < 0 or player_pos.y > HEIGHT:
            game_active = False

        screen.blit(tundra_img, (bg_x1, 0))
        screen.blit(tundra_img, (bg_x2, 0))

        angle = -player_vel * 0.1
        angle = max(-30, min(30, angle))
        rotated_santa = pygame.transform.rotate(santa_img, angle)
        santa_rect = rotated_santa.get_rect(center=player_pos)
        screen.blit(rotated_santa, santa_rect)

        for h in hindernisse:
            h[0] -= 200 * dt
            
            top_rect = cloud_img.get_rect(midbottom=(h[0], h[1] - 60))
            bottom_rect = tree_img.get_rect(midtop=(h[0], h[1] + 60))

            screen.blit(cloud_img, top_rect)
            screen.blit(tree_img, bottom_rect)

            if santa_rect.colliderect(top_rect) or santa_rect.colliderect(bottom_rect):
                game_active = False

            if h[0] < -50:
                h[0] = WIDTH + 100
                h[1] = randint(150, 350)

    else:
        font = pygame.font.SysFont("Arial", 40)
        text = font.render("GAME OVER", True, "red")
        screen.blit(text, (WIDTH//2 - 200, HEIGHT//2))

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()