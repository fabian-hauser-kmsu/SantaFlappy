import pygame
from random import randint

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Santa Flappy")
clock = pygame.time.Clock()

try:
    santa_img = pygame.image.load("SantaFlappy/Santa.png").convert_alpha()
    tree_img = pygame.image.load("SantaFlappy/Tree.png").convert_alpha()
    cloud_img = pygame.image.load("SantaFlappy/Cloud.png").convert_alpha()
    tundra_img = pygame.image.load("SantaFlappy/tundra.png").convert()
except:
    santa_img = pygame.Surface((100, 33)); santa_img.fill((220, 50, 50))
    tree_img = pygame.Surface((50, 200)); tree_img.fill((34, 139, 34))
    cloud_img = pygame.Surface((50, 200)); cloud_img.fill((200, 230, 255))
    tundra_img = pygame.Surface((WIDTH, HEIGHT))
    tundra_img.fill((135, 206, 250))
    
santa_img = pygame.transform.scale(santa_img, (120, 70))
tree_img = pygame.transform.scale(tree_img, (150, int(HEIGHT * 0.6)))
cloud_img = pygame.transform.scale(cloud_img, (100, int(HEIGHT * 0.6)))
tundra_img = pygame.transform.scale(tundra_img, (WIDTH, HEIGHT))

tree_mask = pygame.mask.from_surface(tree_img)
cloud_mask = pygame.mask.from_surface(cloud_img)

player_pos = pygame.Vector2(WIDTH * 0.15, HEIGHT / 2)
player_vel = 0
gravity = 1400
jump_strength = -580
scroll_speed = 3

bg_x1 = 0
bg_x2 = WIDTH

hindernisse = []
spawn_dist = WIDTH * 0.5
for i in range(3):
    hindernisse.append([WIDTH + i * spawn_dist, randint(int(HEIGHT * 0.3), int(HEIGHT * 0.7)), False])

score = 0
high_score = 0

def reset_game():
    return (pygame.Vector2(WIDTH * 0.15, HEIGHT / 2), 
            0, 
            [[WIDTH + i * spawn_dist, randint(int(HEIGHT * 0.3), int(HEIGHT * 0.7)), False] for i in range(3)],
            0)

running = True
game_active = False
dt = 0

font_large = pygame.font.SysFont("Helvetica", int(HEIGHT * 0.08), bold=True)
font_medium = pygame.font.SysFont("Helvetica", int(HEIGHT * 0.05), bold=True)
font_small = pygame.font.SysFont("Helvetica", int(HEIGHT * 0.03))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                if game_active:
                    player_vel = jump_strength
                else:
                    player_pos, player_vel, hindernisse, score = reset_game()
                    game_active = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_active:
                player_vel = jump_strength
            else:
                player_pos, player_vel, hindernisse, score = reset_game()
                game_active = True
    
    if game_active:
        bg_x1 -= scroll_speed
        bg_x2 -= scroll_speed
        if bg_x1 <= -WIDTH: bg_x1 = WIDTH
        if bg_x2 <= -WIDTH: bg_x2 = WIDTH
        
        player_vel += gravity * dt
        player_vel = min(player_vel, 900)
        player_pos.y += player_vel * dt
        
        if player_pos.y < 0 or player_pos.y > HEIGHT - 50:
            game_active = False
            high_score = max(high_score, score)
        
        screen.blit(tundra_img, (bg_x1, 0))
        screen.blit(tundra_img, (bg_x2, 0))
        
        angle = -player_vel * 0.08
        angle = max(-45, min(45, angle))
        rotated_santa = pygame.transform.rotate(santa_img, angle)
        santa_rect = rotated_santa.get_rect(center=player_pos)
        screen.blit(rotated_santa, santa_rect)
        
        santa_mask = pygame.mask.from_surface(rotated_santa)
        
        for h in hindernisse:
            h[0] -= 500 * dt
            
            gap = 180
            top_rect = cloud_img.get_rect(midbottom=(h[0], h[1] - gap))
            bottom_rect = tree_img.get_rect(midtop=(h[0], h[1] + gap))
            
            screen.blit(cloud_img, top_rect)
            screen.blit(tree_img, bottom_rect)
            
            offset_top = (top_rect.x - santa_rect.x, top_rect.y - santa_rect.y)
            offset_bottom = (bottom_rect.x - santa_rect.x, bottom_rect.y - santa_rect.y)
            
            collision_top = santa_mask.overlap(cloud_mask, offset_top)
            collision_bottom = santa_mask.overlap(tree_mask, offset_bottom)
            
            if collision_top or collision_bottom:
                game_active = False
                high_score = max(high_score, score)
            
            if not h[2] and h[0] < player_pos.x:
                h[2] = True
                score += 1
            
            if h[0] < -100:
                h[0] = WIDTH + WIDTH//2
                h[1] = randint(int(HEIGHT * 0.3), int(HEIGHT * 0.7))
                h[2] = False
        
        score_text = font_medium.render(str(score), True, (255, 255, 255))
        score_shadow = font_medium.render(str(score), True, (50, 50, 50))
        screen.blit(score_shadow, (WIDTH // 2 - score_text.get_width() // 2 + 3, 53))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 50))
        
    else:
        screen.blit(tundra_img, (0, 0))
        
        if score > 0 or high_score > 0:
            game_over_text = font_large.render("GAME OVER", True, (255, 70, 70))
            game_over_shadow = font_large.render("GAME OVER", True, (100, 20, 20))
            screen.blit(game_over_shadow, (WIDTH // 2 - game_over_text.get_width() // 2 + 4, HEIGHT // 2 - 154))
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 150))
            
            score_display = font_medium.render(f"Score: {score}", True, (255, 255, 255))
            high_display = font_medium.render(f"Best: {high_score}", True, (255, 215, 0))
            screen.blit(score_display, (WIDTH // 2 - score_display.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(high_display, (WIDTH // 2 - high_display.get_width() // 2, HEIGHT // 2 + 20))
        else:
            title_text = font_large.render("SANTA FLAPPY", True, (255, 255, 255))
            title_shadow = font_large.render("SANTA FLAPPY", True, (50, 50, 50))
            screen.blit(title_shadow, (WIDTH // 2 - title_text.get_width() // 2 + 4, HEIGHT // 2 - 104))
            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))
        
        start_text = font_small.render("Press SPACE to start", True, (255, 255, 255))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 100))
        
        esc_text = font_small.render("ESC to quit", True, (200, 200, 200))
        screen.blit(esc_text, (WIDTH // 2 - esc_text.get_width() // 2, HEIGHT - 80))
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()