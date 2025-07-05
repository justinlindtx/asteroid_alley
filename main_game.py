# Author: Justin Lindberg
# Project name: Asteroid Alley
# Version: 1.0
# Date updated: 7/04/25

import pygame
import random
import sys
import json
import math

pygame.init()
pygame.mixer.init()

width, height = 400, 600
scorebox_width, scorebox_height = 150, 50
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Asteroid Alley")
big_font = pygame.font.SysFont("Impact", 35)
menu_font = pygame.font.SysFont("Impact", 30)
clock = pygame.time.Clock()

# Start music
pygame.mixer.music.load("audio/8bit-music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Load SFX
death_sound = pygame.mixer.Sound("audio/death-sound.mp3")
level_up = pygame.mixer.Sound("audio/8-bit-powerup.mp3")
level_up.set_volume(0.4)

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIME = (100, 240, 40)
LIME_2 = (145, 245, 101)

def main_menu():
    start_width, start_height = 140, 55
    button_rect = pygame.Rect(width // 2 - 70, 400, start_width, start_height)
    button_rect2 = pygame.Rect(width // 2 - 68, 402, start_width - 4, start_height - 4)
    galaxy = pygame.image.load('images/galaxy.png').convert()
    galaxy = pygame.transform.scale(galaxy, (galaxy.get_width() * 1.5, galaxy.get_height() * 1.5))
    
    # menu text
    menu1 = menu_font.render("Welcome to Asteroid Alley!", True, LIME)
    with open("save-data.json", "r") as file:
        data = json.load(file)
    score_font = pygame.font.SysFont("Consolas", 25)
    highscore_text = score_font.render(f"High score: {data["highscore"]}", True, LIME)
    highscore_pos = highscore_text.get_rect(bottomright=(width - 30, height - 30))
    base_size = highscore_text.get_size()
    font_amplitude = 0.07
    font_speed = 0.05
    frame = 0

    while True:
        clock.tick(60)
        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
        
        # Pulse font size
        scale_factor = 1 + font_amplitude * math.sin(frame * font_speed)
        new_size = (int(base_size[0] * scale_factor), int(base_size[1] * scale_factor))
        scaled_highscore = pygame.transform.smoothscale(highscore_text, new_size)
        scaled_pos = scaled_highscore.get_rect(center=highscore_pos.center)
        frame += 1

        screen.blit(galaxy, (width // 2 - galaxy.get_width() // 2, height // 2 - galaxy.get_height() // 2))
        screen.blit(menu1, (width // 2 - menu1.get_width() // 2, 120))
        screen.blit(scaled_highscore, scaled_pos)
        
        # start button
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, WHITE, button_rect)
            pygame.draw.rect(screen, BLACK, button_rect2)
            button_text = menu_font.render("Start", True, WHITE)
            if click:
                return # Start game when button is clicked
        else:
            pygame.draw.rect(screen, LIME, button_rect)
            pygame.draw.rect(screen, BLACK, button_rect2)
            button_text = menu_font.render("Start", True, LIME)
        screen.blit(button_text, button_text.get_rect(center=button_rect.center))
        
        pygame.display.flip()

def game_loop():
    # Background
    bg = pygame.image.load('images/background.png').convert()
    
    # Player
    player = pygame.image.load('images/spaceship.png').convert()
    player.set_colorkey(BLACK)
    player = pygame.transform.scale(player, 
                                    (player.get_width() * 1.6, 
                                    player.get_height() * 1.6))
    player_x = width // 2 - player.get_width() // 2
    player_y = 500
    player_speed = 6
    player_mask = pygame.mask.from_surface(player)

    # Asteroids
    asteroid_frames = [pygame.image.load("images/asteroid/asteroid1.png").convert(),
                       pygame.image.load("images/asteroid/asteroid2.png").convert(),
                       pygame.image.load("images/asteroid/asteroid3.png").convert(),
                       pygame.image.load("images/asteroid/asteroid4.png").convert(),
                       pygame.image.load("images/asteroid/asteroid5.png").convert(),
                       pygame.image.load("images/asteroid/asteroid6.png").convert(),
                       pygame.image.load("images/asteroid/asteroid7.png").convert(),
                       pygame.image.load("images/asteroid/asteroid8.png").convert(),]
    asteroid_masks = []
    for i in range(len(asteroid_frames)): # Rescale asteroid images
        image = asteroid_frames[i]
        image.set_colorkey(BLACK)
        scaled_image = pygame.transform.scale(image, (image.get_width() * 0.6, image.get_height() * 0.6))
        asteroid_frames[i] = scaled_image
        asteroid_masks.append(pygame.mask.from_surface(asteroid_frames[i]))

    asteroid_width = asteroid_frames[0].get_width()
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
        for coord, mask in zip(asteroids, asteroid_masks):
            coord['y'] += asteroid_speed
            if coord['y'] > height:
                score += 1
                coord['x'] = random.randint(0, width - asteroid_width)
                coord['y'] = random.randint(-(height), -50)
            screen.blit(asteroid_frames[frame_index], (coord['x'], coord['y']))
            # Collision detection
            offset = (coord['x'] - player_x, coord['y'] - player_y)
            if player_mask.overlap(mask, offset):
                pygame.display.flip()
                death_sound.play()
                running = False
        
        if score >= milestone:
            level_up.play()
            pygame.mixer.music.set_volume(0.5)
            milestone += 100

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

    # Save high score
    with open("save-data.json", "r") as file:
            data = json.load(file)
    if score > data["highscore"]:
        data["highscore"] = score
    with open("save-data.json", "w") as file:
        json.dump(data, file, indent=4)
    
    # Game over screen
    waiting = True
    subtitle_font = pygame.font.SysFont("Consolas", 18)
    gameover_bg = pygame.image.load("images/planet_stars.png").convert()
    
    while waiting:
        gameover_bg = pygame.transform.scale(gameover_bg, (width, height))
        screen.blit(gameover_bg, (0,0))
        game_over = big_font.render("Game over!", True, LIME)
        score_result = big_font.render("Score: " + str(score), True, LIME)
        game_over2 = subtitle_font.render("Press 'Enter' to return to menu", True, LIME)
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

# Run the game
while True:
    main_menu()
    game_loop()