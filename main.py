"""
SPACE INVADER GAME
A classic arcade-style game where the player shoots descending aliens.
Includes menu system, high score tracking, and game over screens.
"""

import math
import random
import pygame
from pygame import mixer

# ==================== INITIALIZATION ====================
# Initialize pygame and create game window
pygame.init()
screen = pygame.display.set_mode((800, 600))  # Set screen dimensions

# ==================== COLOR DEFINITIONS ====================
# Define color constants for easy reference
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)      
RED = (255, 0, 0)        
BLUE = (0, 0, 128)       
GOLD = (255, 215, 0)     

# ==================== GAME ASSETS ====================

background = pygame.image.load('background.png')
mixer.music.load("background.wav")  
mixer.music.play(-1)  

# Set window title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# ==================== PLAYER SETUP ====================
playerImg = pygame.image.load('player.png')
playerX = 370  
playerY = 480  
playerX_change = 0  

# ==================== ENEMY SETUP ====================
enemyImg = []  
enemyX = []    
enemyY = []    
enemyX_change = []  
enemyY_change = []  
num_of_enemies = 6  

# Initialize enemies with random positions
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))  
    enemyY.append(random.randint(50, 150))  
    enemyX_change.append(4)  
    enemyY_change.append(40)  
    
# ==================== BULLET SETUP ====================
bulletImg = pygame.image.load('bullet.png')
bulletX = 0  
bulletY = 480  
bulletX_change = 0  
bulletY_change = 10  
bullet_state = "ready"  

# ==================== SCORE SYSTEM ====================
score_value = 0  
high_score = 0   
new_high_score = False  

# Try to load previous high score from file
try:
    with open('highscore.txt', 'r') as f:
        high_score = int(f.read())
except:
    high_score = 0  # Default if file doesn't exist

# Font setup for score display
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10  # Score position
testY = 10

# ==================== GAME STATE MANAGEMENT ====================
game_state = "menu"  # "menu", "play", or potentially others
game_over = False    # Flag for game over condition

# Fonts for different text elements
over_font = pygame.font.Font('freesansbold.ttf', 72)  # Game over text
button_font = pygame.font.Font('freesansbold.ttf', 36)  # Button text
title_font = pygame.font.Font('freesansbold.ttf', 64)# Menu title
menu_font = pygame.font.Font('freesansbold.ttf', 48)  # Menu items

# ==================== GAME FUNCTIONS ====================

def reset_game():
    """Reset all game variables to their initial state"""
    global playerX, playerY, playerX_change
    global enemyX, enemyY, enemyX_change, enemyY_change
    global bulletX, bulletY, bullet_state
    global score_value, new_high_score
    
    # Reset player position
    playerX = 370
    playerY = 480
    playerX_change = 0
    
    # Reset enemies with new random positions
    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, 736)
        enemyY[i] = random.randint(50, 150)
        enemyX_change[i] = 4
        enemyY_change[i] = 40
    
    # Reset bullet
    bulletX = 0
    bulletY = 480
    bullet_state = "ready"
    
    # Reset score (but keep high score)
    score_value = 0
    new_high_score = False

def save_high_score(score):
    """Save the high score to a file for persistence"""
    with open('highscore.txt', 'w') as f:
        f.write(str(score))

def show_score(x, y):
    """Display current score and high score on screen"""
    score = font.render(f"Score: {score_value}", True, WHITE)
    screen.blit(score, (x, y))
    
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    scree.blit(high_score_text, (x, y + 40))

def game_over_screen():
    """
    Display game over screen with:
    - Game over text
    - Final score
    - High score celebration (if applicable)
    - Restart and quit buttons
    """
    # Semi-transparent overlay for better readability
    overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    # Game Over text (centered)
    over_text = over_font.render("GAME OVER", True, WHITE)
    over_rect = over_text.get_rect(center=(400, 150))
    screen.blit(over_text, over_rect)
    
    # Final score display
    final_score = button_font.render(f"Final Score: {score_value}", True, WHITE)
    score_rect = final_score.get_rect(center=(400, 230))
    screen.blit(final_score, score_rect)
    
    # Special message if player achieved new high score
    if new_high_score:
        congrats_text = button_font.render("NEW HIGH SCORE!", True, GOLD)
        congrats_rect = congrats_text.get_rect(center=(400, 280))
        screen.blit(congrats_text, congrats_rect)
    
    # Restart button (green)
    restart_rect = pygame.Rect(200, 350, 200, 60)
    pygame.draw.rect(screen, GREEN, restart_rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, restart_rect, 2, border_radius=10)
    restart_text = button_font.render("Restart", True, BLACK)
    restart_text_rect = restart_text.get_rect(center=restart_rect.center)
    screen.blit(restart_text, restart_text_rect)
    
    # Quit button (red)
    quit_rect = pygame.Rect(400, 350, 200, 60)
    pygame.draw.rect(screen, RED, quit_rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, quit_rect, 2, border_radius=10)
    quit_text = button_font.render("Quit", True, WHITE)
    quit_text_rect = quit_text.get_rect(center=quit_rect.center)
    screen.blit(quit_text, quit_text_rect)
    
    return restart_rect, quit_rect  # Return button areas for click detection

def player(x, y):
    """Draw player ship at specified coordinates"""
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    """Draw enemy at specified coordinates"""
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    """Fire bullet from specified position"""
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # Offset for center alignment

def isCollision(enemyX, enemyY, bulletX, bulletY):
    """Check if bullet collides with enemy using distance formula"""
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    return distance < 27  # Collision if distance < threshold

def draw_start_menu():
    """
    Draw the start menu with:
    - Game title
    - High score display
    - Start game button
    - Quit button
    """
    screen.fill(BLACK)  # Black background
    
    # Title with shadow effect
    title_text = title_font.render("SPACE INVADER", True, BLUE)
    title_shadow = title_font.render("SPACE INVADER", True, WHITE)
    title_rect = title_text.get_rect(center=(403, 153))
    screen.blit(title_shadow, title_rect)
    title_rect = title_text.get_rect(center=(400, 150))
    screen.blit(title_text, title_rect)
    
    # High score display
    hs_text = button_font.render(f"High Score: {high_score}", True, WHITE)
    hs_rect = hs_text.get_rect(center=(400, 230))
    screen.blit(hs_text, hs_rect)
    
    # Start button (green)
    start_rect = pygame.Rect(200, 300, 200, 60)
    pygame.draw.rect(screen, GREEN, start_rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, start_rect, 2, border_radius=10)
    start_text = button_font.render("Start Game", True, BLACK)
    start_text_rect = start_text.get_rect(center=start_rect.center)
    screen.blit(start_text, start_text_rect)
    
    # Quit button (red)
    quit_rect = pygame.Rect(400, 300, 200, 60)
    pygame.draw.rect(screen, RED, quit_rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, quit_rect, 2, border_radius=10)
    quit_text = button_font.render("Quit", True, WHITE)
    quit_text_rect = quit_text.get_rect(center=quit_rect.center)
    screen.blit(quit_text, quit_text_rect)
    
    return start_rect, quit_rect  # Return button areas for click detection

# ==================== MAIN GAME LOOP ====================
running = True  
restart_button = None  
quit_button = None     
menu_quit_button = None  

while running:
    # ========== EVENT HANDLING ==========
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Window close button
            running = False

        # Menu screen event handling
        if game_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):  
                    game_state = "play"
                    game_over = False
                elif menu_quit_button.collidepoint(event.pos):  # Quit clicked
                    running = False

        # Gameplay event handling
        elif game_state == "play":
            if not game_over:
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        playerX_change = -5  # Move left
                    if event.key == pygame.K_RIGHT:
                        playerX_change = 5   # Move right
                    if event.key == pygame.K_SPACE:
                        if bullet_state == "ready":  
                            bulletSound = mixer.Sound("laser.wav")
                            bulletSound.play()
                            bulletX = playerX
                            fire_bullet(bulletX, bulletY)

                # Stop movement when key released
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        playerX_change = 0
            else:
                # Game over screen buttons
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button and restart_button.collidepoint(event.pos):
                        reset_game()  # Reset game state
                        game_over = False
                    elif quit_button and quit_button.collidepoint(event.pos):
                        running = False  # Quit game

    # ========== MENU SCREEN ==========
    if game_state == "menu":
        start_button, menu_quit_button = draw_start_menu()
        pygame.display.update()
        continue  

    # ========== GAME PLAY ==========
    screen.fill(BLACK)  
    screen.blit(background, (0, 0))  

    if not game_over:
        
        playerX += playerX_change
        playerX = max(0, min(playerX, 736))  

        
        for i in range(num_of_enemies):
            
            if enemyY[i] > 440:
                game_over = True
                
                if score_value > high_score:
                    new_high_score = True
                    high_score = score_value
                    save_high_score(high_score)  
                break

            
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:  
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]  
            elif enemyX[i] >= 736:  
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]  

            
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()
                bulletY = 480  
                bullet_state = "ready"
                score_value += 1  
                
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)  
            
        # Bullet handling
        if bulletY <= 0:  
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change  

        player(playerX, playerY)  
        show_score(textX, testY)  
    else:
        
        restart_button, quit_button = game_over_screen()
        show_score(textX, testY)  

    pygame.display.update()  


pygame.quit()
