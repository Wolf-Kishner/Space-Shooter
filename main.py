import pygame
import time
import random


# To be able to display texts for scores we need to initialise the font module and declare the FONT Obj to render the text
pygame.mixer.init()
pygame.font.init()
# Window , BG , Now moving the Character
WIDTH,HEIGHT = 1000,800
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
FONT = pygame.font.SysFont('comicsans',30)
# Load the Background Image and resize it to the window size
BG = pygame.transform.scale(pygame.image.load('assets/bg.jpg'),(WIDTH,HEIGHT))
GAME_OVER = pygame.transform.scale(pygame.image.load('assets/game_over.png'),(WIDTH,HEIGHT))
# Name at the top of the Window
pygame.display.set_caption("Star wars")

class sprite:
    def __init__(self,height,width,velocity_x,velocity_y):
        self.height = height
        self.width = width
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
# ----------------------------------------------------------------------------------------------------------------
PLAYER = sprite(80,60,5,5)
STAR = sprite(25,35,5,5)
BULLET = sprite(15,15,5,5)
# ----------------------------------------------------------------------------------------------------------------
BULLET_COOLDOWN = 500
HEART_HEIGHT = 40
HEART_WIDTH = 40
# ----------------------------------------------------------------------------------------------------------------
HIGHEST_SCORE = 0
SPACESHIP_IMAGE = pygame.image.load('assets/level1.png')
SPACESHIP = pygame.transform.scale(SPACESHIP_IMAGE,(PLAYER.width,PLAYER.height))
ASTEROID_IMAGE = pygame.image.load("assets/asteroid.png")
ASTEROID = pygame.transform.scale(ASTEROID_IMAGE,(STAR.width,STAR.height))
BULLET_IMAGE = pygame.image.load("assets/bullet.png")
BULLET = pygame.transform.scale(BULLET_IMAGE,(BULLET.width,BULLET.height))
HEART = pygame.transform.scale(pygame.image.load("assets/health.png"),(HEART_WIDTH,HEART_HEIGHT))
# ----------------------------------------------------------------------------------------------------------------
playlist = ["assets/bg_music.mp3","assets/you_lose.mp3","assets/blaster.mp3","assets/darth.mp3"]

# ----------------------------------------------------------------------------------------------------------------

def restart_game():
    main()
    
def game_over_screen():
    WIN.blit(GAME_OVER,(0,0))
    lost_text = FONT.render("The Empire won ,better luck next time ",1,"red")
    game_over = FONT.render(f"Press ENTER to start the REBELLION",1,"white")
    WIN.blit(lost_text,(WIDTH//2 - lost_text.get_width()//2,HEIGHT//2 - lost_text.get_height()//2))
    WIN.blit(game_over,(WIDTH//2 - game_over.get_width()//2,HEIGHT//2 + game_over.get_height()//2))
    pygame.display.update()
    pygame.mixer.music.stop()
    pygame.mixer.music.load(playlist[3])
    pygame.mixer.music.set_volume(0.9)
    pygame.mixer.music.play()
    isPressed = False
    while isPressed == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isPressed = True
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    isPressed = True
                    restart_game()
#--------------------------------------------------------------------------------------------------------------- 
def draw(player,elapsed_time,stars,bullets):
    # blit is a method to draw on the screen and we speicfy the Coodinates wher the Top left corner is 0,0
    WIN.blit(BG,(0,0))
    time_text = FONT.render(f"Time:{round(elapsed_time)}s",1,("white"))
    score = FONT.render(f"Score: {HIGHEST_SCORE}",1,"white")
    health = FONT.render(f"Health: {HEALTH}",1,"red")
    WIN.blit(time_text,(10,10))
    WIN.blit(score,(10,40))
    WIN.blit(HEART,(750,10))
    WIN.blit(health,(800,10))
    WIN.blit(SPACESHIP,(player.x,player.y))
    # Update the display
    for bullet in bullets:
        WIN.blit(BULLET, (bullet.x, bullet.y))
    for star in stars:
        WIN.blit(ASTEROID,(star.x,star.y))
    pygame.display.update()

def main():
    # The Close button functionanlity is not by default we need to program it manually
    run = True
    global last_bullet
    global HIGHEST_SCORE
    global HEALTH 
    HEALTH = 100 
    HIGHEST_SCORE = 0
    last_bullet = 0
    # Starting position of the Player 4th Quadrant Position
    # Starting coordinates of the Player and its dimensiiions
    player = pygame.Rect(200,HEIGHT-PLAYER.height,PLAYER.width,PLAYER.height)
    
    # Lets setup the clock obj
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    # ADDING THE PROJECTILES
    star_add_increment = 2000
    star_count = 0 
    stars = []
    bullets = []
    hit = False
    pygame.mixer.music.load(playlist[0])
    pygame.mixer.music.set_volume(0.9)
    pygame.mixer.music.play(-1, 0.0)

# Tells us when we should add a new star to the screen

    # Once we set this players pos we need to draw it onto the screen
    while run:
        # Returns the number of ms since the last clock tick
        star_count += clock.tick(60) # 60 frames per second
        elapsed_time = time.time() - start_time
        if star_count > star_add_increment :
            for _ in range(3):
                # This generates 3 stars everytime that cond is satisfied
                star_x = random.randint(0,WIDTH-STAR.width)
                # negative dilay so that it apperas from the top of the screen
                star = pygame.Rect(star_x,-STAR.width,STAR.width,STAR.height) 
                stars.append(star)
            # The time in which we are incrementing our star
            star_add_increment = max(200,star_add_increment - 50)
            star_count = 0
        
        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        # We will need to adjust the speed of the movement of the player atm it is really fast
        # The speed the while runs at determines the speed of the player 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER.velocity_x >=0 :
            player.x -= PLAYER.velocity_x
        if keys[pygame.K_RIGHT] and player.x + PLAYER.velocity_x + PLAYER.width <= WIDTH:
            player.x += PLAYER.velocity_x
        if keys[pygame.K_UP] and player.y - PLAYER.velocity_y >= 0:
            player.y -= PLAYER.velocity_y
        if keys[pygame.K_DOWN] and player.y + PLAYER.velocity_y + PLAYER.height <= HEIGHT:
            player.y += PLAYER.velocity_y
        if keys[pygame.K_SPACE] and  pygame.time.get_ticks() - last_bullet > BULLET_COOLDOWN:
            bullet = pygame.Rect(player.x + player.width//2 - BULLET.width//2,player.y, BULLET.width,BULLET.height)
            bullets.append(bullet)
            blaster_sound = pygame.mixer.Sound(playlist[2])
            blaster_sound.play()
            last_bullet = pygame.time.get_ticks()
        
        for bullet in bullets[:]:
                bullet.y -= BULLET.velocity_y
                if bullet.y <= 0:
                    bullets.remove(bullet)
                for star in stars[:]:
                    if bullet.colliderect(star):
                        HIGHEST_SCORE += 1 
                        stars.remove(star)
                        bullets.remove(bullet)
                        break
        # Looping through the copy
        for star in stars[:]:
            star.y += STAR.velocity_y
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y  + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break
        
        if(hit == True): 
            HEALTH -= 25
            hit = False
            # Play the game over music
            if (HEALTH <= 0):
                pygame.mixer.music.stop()
                pygame.mixer.music.load(playlist[1])
                pygame.mixer.music.set_volume(0.9)
                pygame.mixer.music.play()
                game_over_screen()
                break            
        draw(player,elapsed_time,stars,bullets)

    #    So far we can dodge bullets by going off the screen we need to avoid that 
    pygame.quit()
    

# Making sure that this file wasnt imported we are running the code as it is 
if __name__ == "__main__":
    main()