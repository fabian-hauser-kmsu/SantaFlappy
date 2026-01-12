# Example file showing a circle moving on screen
import pygame
from random import randint

# pygame setup
pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_vel = 0.0
screen_vel = 200
screen_pos = 500

hindernisse = []
santa = pygame.image.load("SantaFlappy/Santa.png").convert_alpha()
tree = pygame.image.load("SantaFlappy/Tree.png").convert_alpha()
cloud = pygame.image.load("SantaFlappy/Cloud.png").convert_alpha()
tundra = pygame.image.load("SantaFlappy/tundra.png").convert()

santa = pygame.transform.scale(santa, (100, 33))
tree = pygame.transform.scale(tree, (50, 200))
cloud = pygame.transform.scale(cloud, (50, 200))
tundra = pygame.transform.scale(tundra, (500, 500))

background_width = tundra.get_width()
scroll_speed = 2 # Wie schnell der Hintergrund scrollt
background_x1 = 0 # Erste Position des Hintergrundbildes
background_x2 = background_width # Zweite Position des Hintergrundbildes (direkt dahinter)



offset = 0
for i in range(4):
    hindernisse.append((randint(100, 400),offset))
    offset += 200

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    background_x1 -= scroll_speed
    background_x2 -= scroll_speed

    # Wenn das erste Bild komplett aus dem Bildschirm gescrollt ist,
    # setze es hinter das zweite Bild.
    if background_x1 <= -background_width:
        background_x1 = background_width

    # Wenn das zweite Bild komplett aus dem Bildschirm gescrollt ist,
    # setze es hinter das erste Bild.
    if background_x2 <= -background_width:
        background_x2 = background_width

    # --- Zeichnen ---
    # Zeichne den ersten Teil des Hintergrunds
    screen.blit(tundra, (background_x1, 0))
    # Zeichne den zweiten Teil des Hintergrunds (direkt dahinter)
    screen.blit(tundra, (background_x2, 0))

    angle = -player_vel / 6
    angle = max(-45, min(45, angle))

    rotated_santa = pygame.transform.rotate(santa, angle)

    screen.blit(rotated_santa, player_pos)

    # Hier zeichnen wir Hindernisse

    for h in hindernisse:
        gap = h[0]
        pos = h[1] + screen_pos

        screen.blit(tree, (pos, gap +  50))
        screen.blit(tree, (pos + 20, gap + 150))
        screen.blit(tree, (pos - 20, gap + 150))

        screen.blit(cloud, (pos, gap - 250))    
        screen.blit(cloud, (pos + 10, gap - 300))    
        screen.blit(cloud, (pos - 10, gap - 300))  
        screen.blit(cloud, (pos + 20, gap - 400))    
        screen.blit(cloud, (pos - 20, gap - 400))    
        
        if pos < -50:
            hindernisse.remove(h)
            new_gap = randint(100, 400)
            new_pos = hindernisse[-1][1] + 200
            hindernisse.append((new_gap, new_pos))


    screen_pos -= screen_vel * dt

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        player_pos.y -= 300 * dt
        player_vel = -300
    else:
        player_pos.y += player_vel * dt

    player_vel += 500 * dt


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()