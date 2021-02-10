import pygame
import os
from pygame.constants import K_DOWN, K_RIGHT, K_d, K_s
pygame.font.init()
pygame.mixer.init()

# Global variables
WIDTH, HEIGHT = 900, 500
SWDTH, SHIGHT = (55, 40)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60
SPEED = 5
BULL_SPEED = 9
MAX_BULL = 5
SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Pygame_random", "space.png")), (WIDTH, HEIGHT))

# Hit 
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Set a border in the window
BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT)

# Set the health score font
HEALTH_FONT = pygame.font.SysFont("comicsams", 30)

# Set the winner message font:
WINNER_FONT = pygame.font.SysFont("comicsam", 100)

# Import the images
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Pygame_random", "spaceship_yellow.png"))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Pygame_random", "spaceship_red.png"))

# Resize and rotate the images
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SWDTH, SHIGHT)), 90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SWDTH, SHIGHT)), 270)

# Set the sound effects
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Pygame_random", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Pygame_random", "Gun+Silencer.mp3"))

# Window configurations
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #This set the windows size
pygame.display.set_caption("Spaceship game") # This changes the caption name

# Draw in the window
def draw_function(red, yellow, red_bull, yellow_bull, RED_HEALTH, YELLOW_HEALTH):

    # set the color
    WIN.blit(SPACE, (0, 0))

    # Update the border in the window
    pygame.draw.rect(WIN, RED, BORDER)

    # Draw the health score
    red_health_score = HEALTH_FONT.render("Health: " + str(RED_HEALTH), 1, WHITE)
    yellow_health_score = HEALTH_FONT.render("Halth: " + str (YELLOW_HEALTH), 1, WHITE)
    WIN.blit(red_health_score, (WIDTH - red_health_score.get_width() - 10, 10))
    WIN.blit(yellow_health_score, (10, 10))

    # Update the image spaceships
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    # Draw the bullets
    for bullet in red_bull:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bull:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()

# Handle the bullets
def bull_hand(yellow_bull, red_bull, yellow, red):
    for bullet in yellow_bull:
        bullet.x += BULL_SPEED
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bull.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bull.remove(bullet)
    for bullet in red_bull:
        bullet.x -= BULL_SPEED
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bull.remove(bullet)
        elif bullet.x < 0:
            red_bull.remove(bullet)

def winner(winner_text):
    # Draw the winner message
    draw_wtext = WINNER_FONT.render(winner_text, 1, WHITE)
    WIN.blit(draw_wtext, (WIDTH/2 - draw_wtext.get_width()/2, HEIGHT/2-draw_wtext.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1500)

# The main loop
def main():

    yellow = pygame.Rect(100, 250, SWDTH, SHIGHT)
    red = pygame.Rect(800, 250, SWDTH, SHIGHT)
    RED_HEALTH = 10
    YELLOW_HEALTH = 10

    # List of bullets
    yellow_bull = []
    red_bull = []

    # Set the clock for the update
    clock = pygame.time.Clock()

    run = True
    while run:
        
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bull) < MAX_BULL:
                    bullet = pygame.Rect(yellow.x+yellow.width, yellow.y+yellow.height//2-2, 10, 5)
                    yellow_bull.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bull) < MAX_BULL:
                    bullet = pygame.Rect(red.x+red.width, red.y+red.height//2-2, 10, 5)
                    red_bull.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                RED_HEALTH -= 1
                BULLET_HIT_SOUND.play()

            if event.type ==YELLOW_HIT:
                YELLOW_HEALTH -= 1
                BULLET_HIT_SOUND.play()
        
        winner_text = ""
        if RED_HEALTH <= 0:
            winner_text = "Yellow wins"
        if YELLOW_HEALTH <= 0:
            winner_text = "Red wins"
        
        if winner_text != "":
            winner(winner_text)
            break

        bull_hand(yellow_bull, red_bull, yellow, red)

        # Key function
        keys_pressed = pygame.key.get_pressed()
        
        # Yellow keys
        if keys_pressed[pygame.K_a] and yellow.x-SPEED > 0:
            yellow.x -= SPEED
        if keys_pressed[pygame.K_w] and yellow.y-SPEED > 0:
            yellow.y -= SPEED
        if keys_pressed[K_d] and yellow.x+SPEED+yellow.width < BORDER.x:
            yellow.x += SPEED
        if keys_pressed[K_s] and yellow.y+SPEED+yellow.height < HEIGHT:
            yellow.y += SPEED

        # Red keys
        if keys_pressed[pygame.K_LEFT] and red.x-SPEED-red.width > BORDER.x:
            red.x -= SPEED
        if keys_pressed[pygame.K_UP] and red.y-SPEED > 0:
            red.y -= SPEED
        if keys_pressed[K_RIGHT] and red.x+red.width < WIDTH:
            red.x += SPEED
        if keys_pressed[K_DOWN] and red.y+SPEED+red.height < HEIGHT:
            red.y += SPEED

        draw_function(red, yellow, red_bull, yellow_bull, RED_HEALTH, YELLOW_HEALTH)

    main()

if __name__ == "__main__":
    main()