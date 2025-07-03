import pygame
import random
import time

# def menu_screen():
#     screen.fill(BLACK)
    
#end menu_screen

pygame.init()

width, height = 400, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Game")
font = pygame.font.Font(None, size=30)
clock = pygame.time.Clock()

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (200, 0, 0)

# PLAYER
player = pygame.image.load('images/diamond.png').convert_alpha()
player = pygame.transform.scale(player, 
                                (player.get_width() * 0.8, 
                                 player.get_height() * 0.8))
player_x = width // 2 - player.get_width() // 2
player_y = 500
player_speed = 6

# Enemies
enemy_size = 30
enemy_speed = 6
num_enemies = 3
enemies = []

# Place enemies
for i in range(num_enemies):
    x = random.randint(0, width - enemy_size)
    y = random.randint(-(height), -50)
    enemies.append({'x': x, 'y': y})

running = True

while True:
    screen.fill(BLACK)
    screen.blit(player, (player_x, player_y))
    hitbox = pygame.Rect(player_x, player_y, player.get_width(), player.get_height())

    # Player movement
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and player_x > 0:
        player_x  -= player_speed
    if key[pygame.K_RIGHT] and player_x + player.get_width() < width:
        player_x += player_speed

    # Enemy movement
    for enemy in enemies:
        enemy['y'] += enemy_speed
        if enemy['y'] > height:
            enemy['x'] = random.randint(0, width - enemy_size)
            enemy['y'] = random.randint(-(height), -50)
        enemy_box = pygame.Rect(enemy['x'], enemy['y'], enemy_size, enemy_size)
        pygame.draw.rect(screen, RED, enemy_box)
        # Collision detection
        if hitbox.colliderect(enemy_box):
            screen.fill(RED)
            text = font.render("Game over!", True, BLACK)
            screen.blit(text, (width // 2 - text.get_width() // 2, 100))
            running = False 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()
    clock.tick(60)
    if(running == False): # check exit condition
        time.sleep(3)
        break

pygame.quit()