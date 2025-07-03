import pygame
import random
import time
 
pygame.init()

width, height = 400, 600
scorebox_width, scorebox_height = 150, 50
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Game")
font = pygame.font.Font(None, size=35)
clock = pygame.time.Clock()

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (200, 0, 0)

def main_menu():
    while True:
        screen.fill(BLACK)
        menu_font = pygame.font.SysFont("Comic Sans MS", 25)
        menu1 = menu_font.render("Welcome to Block Dodger!", True, RED)
        menu2 = menu_font.render("Press any key to start", True, RED)
        screen.blit(menu1, (width // 2 - menu1.get_width() // 2, height // 3))
        screen.blit(menu2, (width // 2 - menu2.get_width() // 2, height // 2))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                return

def game_loop():
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

    score = 0
    running = True

    while True:
        clock.tick(60)
        screen.fill(BLACK)
        screen.blit(player, (player_x, player_y))
        hitbox = pygame.Rect(player_x, player_y, player.get_width(), player.get_height())

        # Score box
        pygame.draw.rect(screen, RED, (width - scorebox_width - 10, 10, scorebox_width, scorebox_height)) #border
        pygame.draw.rect(screen, BLACK, (width - scorebox_width - 8, 12, scorebox_width - 4, scorebox_height - 4))
        score_text = font.render(f"Score: {score}", True, RED)
        screen.blit(score_text, (width - scorebox_width, 20))

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
                score += 1
                enemy['x'] = random.randint(0, width - enemy_size)
                enemy['y'] = random.randint(-(height), -50)
            enemy_box = pygame.Rect(enemy['x'], enemy['y'], enemy_size, enemy_size)
            pygame.draw.rect(screen, RED, enemy_box)
            # Collision detection
            if hitbox.colliderect(enemy_box):
                screen.fill(RED)
                game_over = font.render("Game over!", True, BLACK)
                score_result = font.render("Score: " + str(score), True, BLACK)
                screen.blit(game_over, (width // 2 - game_over.get_width() // 2, 100))
                screen.blit(score_result, (width // 2 - score_result.get_width() // 2, 150))
                running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        pygame.display.flip()

        if(running == False): # check exit condition
            time.sleep(3)
            break
#end game_loop

# Run the game
while True:
    main_menu()
    game_loop()