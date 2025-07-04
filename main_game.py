# Author: Justin Lindberg
# Project name: Asteroid Alley
# Version: 1.0
# Date updated: 7/04/25

import pygame
import random
import sys
 
pygame.init()
pygame.mixer.init()

width, height = 400, 600
scorebox_width, scorebox_height = 150, 50
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Game")
font = pygame.font.SysFont("Impact", 35)
menu_font = pygame.font.SysFont("Impact", 30)
subtitle_font = pygame.font.SysFont("Arial", 20)
clock = pygame.time.Clock()

# Start music
pygame.mixer.music.load("audio/8bit-music.mp3")
pygame.mixer.music.set_volume(0.07)
pygame.mixer.music.play(-1)

# Load SFX
death_sound = pygame.mixer.Sound("audio/death-sound.mp3")
level_up = pygame.mixer.Sound("audio/8-bit-powerup.mp3")
level_up.set_volume(0.4)

# COLORS
BLACK = (0, 0, 0)
LIME = (100, 240, 40)

def main_menu():
    while True:
        screen.fill(BLACK)
        galaxy = pygame.image.load('images/galaxy.png').convert()
        galaxy = pygame.transform.scale(galaxy, (galaxy.get_width() * 1.5, galaxy.get_height() * 1.5))
        menu1 = menu_font.render("Welcome to Asteroid Alley!", True, LIME)
        menu2 = menu_font.render("Press any key to start", True, LIME)
        screen.blit(galaxy, (width // 2 - galaxy.get_width() // 2, height // 2 - galaxy.get_height() // 2))
        screen.blit(menu1, (width // 2 - menu1.get_width() // 2, 120))
        screen.blit(menu2, (width // 2 - menu2.get_width() // 2, 400))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

def game_loop():
    # Background
    bg = pygame.image.load('images/background.png').convert()
    
    # Player
    player = pygame.image.load('images/spaceship.png').convert_alpha()
    player = pygame.transform.scale(player, 
                                    (player.get_width() * 1.6, 
                                    player.get_height() * 1.6))
    player_x = width // 2 - player.get_width() // 2
    player_y = 500
    player_speed = 6

    # Asteroids
    asteroid_frames = [pygame.image.load("images/asteroid/asteroid1.png").convert(),
                       pygame.image.load("images/asteroid/asteroid2.png").convert(),
                       pygame.image.load("images/asteroid/asteroid3.png").convert(),
                       pygame.image.load("images/asteroid/asteroid4.png").convert(),
                       pygame.image.load("images/asteroid/asteroid5.png").convert(),
                       pygame.image.load("images/asteroid/asteroid6.png").convert(),
                       pygame.image.load("images/asteroid/asteroid7.png").convert(),
                       pygame.image.load("images/asteroid/asteroid8.png").convert(),]
    for i in range(len(asteroid_frames)): # Rescale asteroid images
        image = asteroid_frames[i]
        image.set_colorkey(BLACK)
        scaled_image = pygame.transform.scale(image, (image.get_width() * 0.6, image.get_height() * 0.6))
        asteroid_frames[i] = scaled_image

    asteroid_width = asteroid_frames[0].get_width()
    asteroid_height = asteroid_frames[0].get_height()
    asteroid_speed = 6
    num_asteroids = 4
    asteroids = [] # list of asteroid coords

    # Initialize asteroid locations
    for i in range(num_asteroids):
        x = random.randint(0, width - asteroid_width)
        y = random.randint(-(height), -50)
        asteroids.append({'x': x, 'y': y})

    # Initialize other variables
    frame_index = 0
    frame_delay = 10
    frame_counter = 0
    score = 0
    milestone = 0
    running = True

    # Main game loop
    while running: 
        clock.tick(60)
        screen.fill(BLACK)
        screen.blit(bg, (0,0))
        screen.blit(player, (player_x, player_y))

        # Score box
        pygame.draw.rect(screen, LIME, (width - scorebox_width - 10, 10, scorebox_width, scorebox_height)) #border
        pygame.draw.rect(screen, BLACK, (width - scorebox_width - 8, 12, scorebox_width - 4, scorebox_height - 4))
        score_text = menu_font.render(f"Score: {score}", True, LIME)
        screen.blit(score_text, (width - scorebox_width, 18))

        # Player movement
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and player_x > 0:
            player_x  -= player_speed
        if key[pygame.K_RIGHT] and player_x + player.get_width() < width:
            player_x += player_speed

        # Asteroid animation
        frame_counter += 1
        if frame_counter >= frame_delay:
            frame_counter = 0
            frame_index = (frame_index + 1) % len(asteroid_frames)
        
        # Asteroid movement
        hitbox = pygame.Rect(player_x, player_y, player.get_width(), player.get_height()) # update hitbox
        for coord in asteroids:
            coord['y'] += asteroid_speed
            if coord['y'] > height:
                score += 1
                coord['x'] = random.randint(0, width - asteroid_width)
                coord['y'] = random.randint(-(height), -50)
            asteroid_box = pygame.Rect(coord['x'], coord['y'], asteroid_width, asteroid_height)
            screen.blit(asteroid_frames[frame_index], (coord['x'], coord['y']))
            # Collision detection
            if hitbox.colliderect(asteroid_box):
                death_sound.play()
                running = False
        
        if score >= milestone:
            level_up.play()
            milestone += 100

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()

    # Game over screen
    waiting = True
    while waiting:
        screen.fill(LIME)
        game_over = font.render("Game over!", True, BLACK)
        score_result = font.render("Score: " + str(score), True, BLACK)
        game_over2 = subtitle_font.render("(Press 'Enter' to return to menu)", True, BLACK)
        screen.blit(game_over, (width // 2 - game_over.get_width() // 2, 100))
        screen.blit(score_result, (width // 2 - score_result.get_width() // 2, 180))
        screen.blit(game_over2, (width // 2 - game_over2.get_width() // 2, 250))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
#end game_loop

# Run the game
while True:
    main_menu()
    game_loop()