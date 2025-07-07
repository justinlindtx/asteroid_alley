"""
Project Name: Asteroid Alley
Author: Justin Lindberg
Version: 1.0
Date updated: July 7, 2025
Description: A 2D arcade-style space game built with Pygame. Players dodge asteroids, collect gems,
and unlock ships from a shop menu using in-game currency.

Dependencies:
- pygame (see requirements.txt)

Usage:
- Run with: python main_game.py
- Press enter to start (or click the start button)
- Use arrow keys to move left and right
- Navigate menus with mouse clicks
"""

import pygame
import random
import sys
import json
import math

pygame.init()
pygame.mixer.init()

width, height = 400, 600
scorebox_width, scorebox_height = 155, 50
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Asteroid Alley")
title_font = pygame.font.SysFont("Impact", 50)
menu_font = pygame.font.SysFont("Impact", 30)
clock = pygame.time.Clock()

# Start music
pygame.mixer.music.load("audio/8bit-music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Load SFX
death_sound = pygame.mixer.Sound("audio/death-sound.mp3")
level_up = pygame.mixer.Sound("audio/level-up.mp3")
shield_sound = pygame.mixer.Sound("audio/shield-powerup.mp3")
lose_shield = pygame.mixer.Sound("audio/8-bit-explosion.mp3")
gem_sound = pygame.mixer.Sound("audio/coin.mp3")
select_sound = pygame.mixer.Sound('audio/collect-item.mp3')
fail_sound = pygame.mixer.Sound("audio/retro-hurt.mp3")
gem_sound.set_volume(0.3)

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LIME = (100, 240, 40)
SKY = (50, 170, 255)

def main_menu():
    start_width, start_height = 140, 55
    start_button_rect = pygame.Rect(width // 2 - 70, 360, start_width, start_height)
    start_button_rect2 = pygame.Rect(width // 2 - 68, 362, start_width - 4, start_height - 4)
    shop_button_rect = pygame.Rect(width // 2 - 70, 430, start_width, start_height)
    shop_button_rect2 = pygame.Rect(width // 2 - 68, 432, start_width - 4, start_height - 4)
    menu_font_selected = pygame.font.SysFont("Impact", 26)
    galaxy = pygame.image.load('images/galaxy.png').convert()
    galaxy = pygame.transform.scale(galaxy, (galaxy.get_width() * 1.5, galaxy.get_height() * 1.5))
    gem_icon = pygame.image.load('images/gem.png').convert()
    gem_icon.set_colorkey(BLACK)
    gem_icon = pygame.transform.scale(gem_icon, (35, 35))
    
    # menu text
    game_title = title_font.render("Asteroid Alley", True, LIME)
    with open("save-data.json", "r") as file:
        data = json.load(file)
    gem_text = pygame.font.SysFont("Consolas", 25).render(str(data["gems"]), True, RED)
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
        screen.blit(game_title, (width // 2 - game_title.get_width() // 2, 110))
        screen.blit(scaled_highscore, scaled_pos)
        screen.blit(gem_icon, (10, 10))
        screen.blit(gem_text, (50, 18))

        # start button
        if start_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, WHITE, start_button_rect)
            pygame.draw.rect(screen, BLACK, start_button_rect2)
            button_text = menu_font_selected.render("Start", True, WHITE)
            if click:
                return # Start game when button is clicked
        else:
            pygame.draw.rect(screen, LIME, start_button_rect)
            pygame.draw.rect(screen, BLACK, start_button_rect2)
            button_text = menu_font.render("Start", True, LIME)
        screen.blit(button_text, button_text.get_rect(center=start_button_rect.center))

        # Shop button
        if shop_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, WHITE, shop_button_rect)
            pygame.draw.rect(screen, BLACK, shop_button_rect2)
            button_text = menu_font_selected.render("Shop", True, WHITE)
            if click:
                select_sound.play()
                pygame.mixer.music.set_volume(0.5)
                shop_screen() # Go to shop when button is clicked
                # Update gem count when returning from shop
                with open("save-data.json", "r") as file:
                    data = json.load(file)
                gem_text = pygame.font.SysFont("Consolas", 25).render(str(data["gems"]), True, RED)
        else:
            pygame.draw.rect(screen, LIME, shop_button_rect)
            pygame.draw.rect(screen, BLACK, shop_button_rect2)
            button_text = menu_font.render("Shop", True, LIME)
        screen.blit(button_text, button_text.get_rect(center=shop_button_rect.center))
        
        pygame.display.flip()

def play_game():
    level_up.play()
    pygame.mixer.music.set_volume(0.5)
    
    # Load save data
    with open("save-data.json", "r") as file:
        data = json.load(file)
    
    # Background
    bg = pygame.image.load('images/background.png').convert()
    
    # Player
    for ship in data["spaceships"]:
        if ship["selected"] == True:
            player_image = ship["filename"]
    player = pygame.image.load(player_image).convert()
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
                       pygame.image.load("images/asteroid/asteroid8.png").convert()]
    asteroid_masks = []
    for i in range(len(asteroid_frames)): # Rescale asteroid images
        image = asteroid_frames[i]
        image.set_colorkey(BLACK)
        scaled_image = pygame.transform.scale(image, (image.get_width() * 0.6, image.get_height() * 0.6))
        asteroid_frames[i] = scaled_image
        asteroid_masks.append(pygame.mask.from_surface(asteroid_frames[i]))

    asteroid_width = asteroid_frames[0].get_width()
    asteroid_speed = 6
    num_asteroids = 5
    asteroids = [] # list of asteroid coords

    # Initialize asteroid locations
    for i in range(num_asteroids):
        x = random.randint(0, width - asteroid_width)
        snapped_x = (x // asteroid_width) * asteroid_width
        y = random.randint(-(height), -50)
        for other_coord in asteroids:
            if snapped_x == other_coord['x'] and abs(y - other_coord['y']) < 100:
                y -= 200
        asteroids.append({'x': snapped_x, 'y': y})

    # Gems and gem counter
    gem = pygame.image.load('images/gem.png').convert()
    gem.set_colorkey(BLACK)
    gem = pygame.transform.scale(gem, (35, 35))
    gem_mask = pygame.mask.from_surface(gem)
    gem_text = pygame.font.SysFont("Consolas", 25).render(str(data["gems"]), True, RED)
    gem_x = (random.randint(0, width - asteroid_width) // asteroid_width) * asteroid_width + 40
    gem_y = -30
    gem_speed = 4

    # Shield powerups
    shield_frames = [pygame.image.load('images/shield/shield1.png').convert(),
                     pygame.image.load('images/shield/shield2.png').convert(),
                     pygame.image.load('images/shield/shield3.png').convert(),
                     pygame.image.load('images/shield/shield4.png').convert()]
    shield_masks = []
    for i in range(len(shield_frames)): # Rescale shield images
        image = shield_frames[i]
        image.set_colorkey(BLACK)
        shield_width = 40
        scaled_image = pygame.transform.scale(image, (shield_width, shield_width))
        shield_frames[i] = scaled_image
        shield_masks.append(pygame.mask.from_surface(shield_frames[i]))
    shield_speed = 4
    shield_x = (random.randint(0, width - asteroid_width) // asteroid_width) * asteroid_width + 30
    shield_y = -70

    # Background scrolling
    scroll_speed = 1
    bg_y1 = 0
    bg_y2 = -height

    # Initialize other variables
    asteroid_frame_index = 0
    shield_frame_index = 0
    frame_delay1 = 10
    frame_counter = 0
    score = 0
    score_box_color = LIME
    flashing = False
    channel = None
    milestone = 100
    num_shields = 0
    gem_time = pygame.time.get_ticks() + random.randint(10000, 15000) # 10-15 seconds
    shield_time = pygame.time.get_ticks() + random.randint(40000, 70000) # 40-70 seconds
    is_gem = False
    is_shield = False
    running = True

    # Main game loop
    while running: 
        clock.tick(60)
        screen.fill(BLACK)

        # Move background
        bg_y1 += scroll_speed
        bg_y2 += scroll_speed
        if bg_y1 > height:
            bg_y1 = -height
        if bg_y2 > height:
            bg_y2 = -height
        screen.blit(bg, (0, bg_y1))
        screen.blit(bg, (0, bg_y2))

        # Animations
        frame_counter += 1
        if frame_counter >= frame_delay1:
            frame_counter = 0
            asteroid_frame_index = (asteroid_frame_index + 1) % len(asteroid_frames)
            shield_frame_index = (shield_frame_index + 1) % len(shield_frames)
            if flashing:
                score_box_color = WHITE if score_box_color == LIME else LIME

        # Gems
        now = pygame.time.get_ticks()
        if now >= gem_time:
            is_gem = True
            gem_time = now + random.randint(10000, 20000)
        if is_gem:
            gem_y += gem_speed
            screen.blit(gem, (gem_x, gem_y))
            if gem_y > height:
                gem_x = (random.randint(0, width - asteroid_width) // asteroid_width) * asteroid_width + 40
                gem_y = -30
                is_gem = False
                gem_time = now + random.randint(10000, 20000)

        # Shields
        now = pygame.time.get_ticks()
        if now >= shield_time:
            is_shield = True
            shield_time = now + random.randint(40000, 70000)
        if is_shield:
            shield_y += shield_speed
            screen.blit(shield_frames[shield_frame_index], (shield_x, shield_y))
            if shield_y > height:
                shield_x = (random.randint(0, width - asteroid_width) // asteroid_width) * asteroid_width + 30
                shield_y = -70
                is_shield = False
                shield_time = now + random.randint(40000, 70000)

        # Player movement
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and player_x > 0:
            player_x  -= player_speed
        if key[pygame.K_RIGHT] and player_x + player.get_width() < width:
            player_x += player_speed
        screen.blit(player, (player_x, player_y))
        
        # Draw shield around player
        if num_shields > 0:
            circle_radius = 30
            circle_color = (50, 170, 255, 64) # 64 means 25% transparency
            circle_surface = pygame.Surface((circle_radius * 2, circle_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, circle_color, (circle_radius, circle_radius), circle_radius)
            player_pos = player.get_rect(topleft=(player_x, player_y))
            circle_pos = (player_pos.centerx - circle_radius, player_pos.centery - circle_radius)
            screen.blit(circle_surface, circle_pos)

        # Check gem collision
        gem_offset = (gem_x - player_x, gem_y - player_y)
        if player_mask.overlap(gem_mask, gem_offset):
            gem_sound.play()
            pygame.mixer.music.set_volume(0.5)
            data["gems"] += 1
            gem_text = pygame.font.SysFont("Consolas", 25).render(str(data["gems"]), True, RED)
            gem_x = (random.randint(0, width - asteroid_width) // asteroid_width) * asteroid_width + 40
            gem_y = -30
            is_gem = False

        # Check shield collision
        shield_offset = (shield_x - player_x, shield_y - player_y)
        if player_mask.overlap(shield_masks[shield_frame_index], shield_offset):
            shield_sound.play()
            pygame.mixer.music.set_volume(0.5)
            shield_x = (random.randint(0, width - asteroid_width) // asteroid_width) * asteroid_width + 30
            shield_y = -70
            is_shield = False
            num_shields += 1
        
        # Asteroid movement
        for coord, mask in zip(asteroids, asteroid_masks):
            coord['y'] += asteroid_speed
            if coord['y'] > height: # reset asteroid position
                score += 1
                coord['x'] = (random.randint(0, width - asteroid_width) // asteroid_width) * asteroid_width
                coord['y'] = random.randint(-(height), -50)
                # Adjust position if overlap occurs
                for other_coord in asteroids:
                    if coord is other_coord:
                        continue
                    if coord['x'] == other_coord['x'] and abs(coord['y'] - other_coord['y']) < 100:
                        coord['y'] -= 200
            screen.blit(asteroid_frames[asteroid_frame_index], (coord['x'], coord['y']))
            # Check asteroid collision with player
            asteroid_offset = (coord['x'] - player_x, coord['y'] - player_y)
            if player_mask.overlap(mask, asteroid_offset):
                if num_shields > 0:
                    num_shields -= 1
                    lose_shield.play()
                    pygame.mixer.music.set_volume(0.5)
                    coord['x'] = (random.randint(0, width - asteroid_width) // asteroid_width) * asteroid_width
                    coord['y'] = random.randint(-(height), -50)
                else:
                    pygame.display.flip()
                    death_sound.play()
                    pygame.mixer.music.set_volume(0.5)
                    running = False
        
        # Milestone reached
        if score == milestone:
            channel = level_up.play()
            pygame.mixer.music.set_volume(0.5)
            milestone += 100
        if channel is not None and channel.get_busy():
            flashing = True
        else:
            flashing = False
            score_box_color = LIME
        
        # Score box
        pygame.draw.rect(screen, score_box_color, (width - scorebox_width - 14, 10, scorebox_width, scorebox_height)) #border
        pygame.draw.rect(screen, BLACK, (width - scorebox_width - 12, 12, scorebox_width - 4, scorebox_height - 4))
        score_text = menu_font.render(f"Score: {score}", True, score_box_color)
        screen.blit(score_text, (width - scorebox_width - 8, 18))

        # Gem display
        screen.blit(gem, (10, 10))
        screen.blit(gem_text, (50, 18))

        # Shield display
        for i in range(num_shields):
            pygame.draw.rect(screen, SKY, (15 + 30*i, height - 40, 15, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        
        pygame.display.flip()

    # Save game data
    if score > data["highscore"]:
        data["highscore"] = score
    with open("save-data.json", "w") as file:
        json.dump(data, file, indent=4)
    
    # Game over screen
    waiting = True
    subtitle_font = pygame.font.SysFont("Consolas", 18)
    gameover_bg = pygame.image.load("images/planet_stars.png").convert()
    big_font = pygame.font.SysFont("Impact", 35)
    
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

def shop_screen():
    bg = pygame.image.load('images/background.png').convert()
    gem_icon = pygame.image.load('images/gem.png').convert()
    gem_icon.set_colorkey(BLACK)
    gem_icon = pygame.transform.scale(gem_icon, (35, 35))
    shop_font = pygame.font.SysFont("Impact", 25)
    shop_font_selected = pygame.font.SysFont("Impact", 22)
    back_width, back_height = 85, 50
    back_button_rect = pygame.Rect(10, 10, back_width, back_height)
    back_button_rect2 = pygame.Rect(12, 12, back_width - 4, back_height - 4)
    buy_sound = pygame.mixer.Sound('audio/buy-item.mp3')
    with open("save-data.json", "r") as file:
        data = json.load(file)
    
    # Load ship images
    ship_images = []
    for ship in data["spaceships"]:
        tmp_image = pygame.image.load(ship["filename"]).convert()
        tmp_image.set_colorkey(BLACK)
        tmp_image = pygame.transform.scale(tmp_image,
                                    (tmp_image.get_width() * 1.4, 
                                    tmp_image.get_height() * 1.4))
        ship_images.append(tmp_image)
    # Load images for locked ships
    lock_image = pygame.image.load("images/locked.png").convert()
    lock_image.set_colorkey(BLACK)
    lock_image = pygame.transform.scale(lock_image, (lock_image.get_width() * 1.3, lock_image.get_height() * 1.3))
    buy_button_image = pygame.image.load('images/buy-ship-button.png').convert_alpha()
    buy_button_image = pygame.transform.scale(buy_button_image, (buy_button_image.get_width() * 3.2, buy_button_image.get_height() * 3.2))
    buy_button_rect = buy_button_image.get_rect(topleft=(width // 2 - buy_button_image.get_width() // 2, 500))

    # Find selected ship
    for i, ship in enumerate(data["spaceships"]):
        if ship["selected"] == True:
            ship_selected_index = i
    ship_looking_index = ship_selected_index

    # Background scrolling
    scroll_speed = 1
    bg_x1 = 0
    bg_x2 = -width
    
    while True:
        clock.tick(60)
        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()
        click = False
        gem_text = pygame.font.SysFont("Consolas", 25).render(str(data["gems"]), True, RED)
        
        # Move background
        bg_x1 += scroll_speed
        bg_x2 += scroll_speed
        if bg_x1 > width:
            bg_x1 = -width
        if bg_x2 > width:
            bg_x2 = -width
        screen.blit(bg, (bg_x1, 0))
        screen.blit(bg, (bg_x2, 0))

        screen.blit(gem_icon, (110, 18))
        screen.blit(gem_text, (150, 26))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
        
        # Draw ships on grid
        start_x, start_y = 65, 220
        gap = 100
        buy_button_y = 500
        for i, ship in enumerate(data["spaceships"][:6]):
            box_size = 70
            col = i % 3
            row = i // 3
            x = start_x + gap * col
            y = start_y + gap * row
            if i == ship_selected_index:
                x -= 3
                y -= 3
                box_size += 6
            if i == ship_looking_index:
                ship_text = pygame.font.SysFont("Consolas", 22).render(str(ship["name"]), True, LIME)
            rect = pygame.Rect(x, y, box_size, box_size)
            # Detect mouse selections
            if rect.collidepoint(mouse_pos) or i == ship_looking_index:
                pygame.draw.rect(screen, WHITE, rect)
                if click and ship["unlocked"] == True: # change selected ship
                    data["spaceships"][ship_selected_index]["selected"] = False
                    data["spaceships"][i]["selected"] = True
                    ship_selected_index = i
                    ship_looking_index = i
                elif click:
                    ship_looking_index = i
            else:
                pygame.draw.rect(screen, LIME, rect)
            if i == ship_selected_index:
                pygame.draw.rect(screen, BLACK, (x + 6, y + 6, box_size - 12, box_size - 12))
            else:
                pygame.draw.rect(screen, BLACK, (x + 3, y + 3, box_size - 6, box_size - 6))
            image_rect = ship_images[i].get_rect(center=rect.center)
            screen.blit(ship_images[i], image_rect)

            # Display images for locked ships
            if ship["unlocked"] == False:
                screen.blit(lock_image, image_rect)
            if i == ship_looking_index and ship["unlocked"] == False:
                if buy_button_rect.collidepoint(mouse_pos):
                    buy_button_y += 2
                    screen.blit(buy_button_image, (width // 2 - buy_button_image.get_width() // 2, buy_button_y))
                    buy_text = pygame.font.SysFont("Consolas", 24).render("Buy", True, RED)
                    # Buying the ship
                    if click and data["gems"] >= ship["cost"]:
                        buy_sound.play()
                        pygame.mixer.music.set_volume(0.5)
                        data["gems"] -= ship["cost"]
                        data["spaceships"][i]["unlocked"] = True
                        data["spaceships"][i]["selected"] = True
                        ship_selected_index = i
                    elif click:
                        fail_sound.play()
                        pygame.mixer.music.set_volume(0.5)
                else:
                    screen.blit(buy_button_image, buy_button_rect)
                    buy_text = pygame.font.SysFont("Consolas", 24).render("Buy", True, BLACK)
                screen.blit(buy_text, (140, buy_button_y + 8))
                screen.blit(gem_icon, (180, buy_button_y))
                cost_text = pygame.font.SysFont("Consolas", 24).render(str(ship["cost"]), True, RED)
                screen.blit(cost_text, (215, buy_button_y + 8))

            # Play sounds
            if rect.collidepoint(mouse_pos) and click:
                select_sound.play()
                pygame.mixer.music.set_volume(0.5)


        screen.blit(ship_text, (width // 2 - ship_text.get_width() // 2, 455))

        # Back button
        if back_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, WHITE, back_button_rect)
            pygame.draw.rect(screen, BLACK, back_button_rect2)
            button_text = shop_font_selected.render("Back", True, WHITE)
            if click:
                select_sound.play()
                pygame.mixer.music.set_volume(0.5)
                # Write save data back to file
                with open("save-data.json", "w") as file:
                    json.dump(data, file, indent=4)
                return # Return to main menu
        else:
            pygame.draw.rect(screen, LIME, back_button_rect)
            pygame.draw.rect(screen, BLACK, back_button_rect2)
            button_text = shop_font.render("Back", True, LIME)
        screen.blit(button_text, button_text.get_rect(center=back_button_rect.center))

        pygame.display.flip()

# Run the game
while True:
    main_menu()
    play_game()