# Made By Sokasuki

import pygame
import os
import random
import pickle

RESOLUTION = (880, 640)

class Object(object):
    def __init__(self, width, height, x_cord, y_cord, colour):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.rect = pygame.Rect(x_cord, y_cord, width, height)
        self.colour = colour

    def move(self, direction):
        global dif_state
        if self.rect.y <= 2:
            self.rect.y += RESOLUTION[1]-player.rect.height-10
        elif self.rect.y >= RESOLUTION[1]-player.rect.height:
            self.rect.y -= RESOLUTION[1]-player.rect.height-10
        elif direction == "up":
            self.rect.y += -8
        elif direction == "down":
            self.rect.y += 8
        elif direction == "left":
            if dif_state == "easy":
                self.rect.x += -5
            elif dif_state == "medium":
                self.rect.x += -8
            elif dif_state == "hard":
                self.rect.x += -11

class Player(Object):
    def __init__(self, width, height, x_cord, y_cord, colour, health, score):
        Object.__init__(self, width, height, x_cord, y_cord, colour)
        self.health = health
        self.score = score

class Health(object):
    def __init__(self):
        self.rect_1 = pygame.Rect(30, 30, 30, 30)
        self.rect_2 = pygame.Rect(70, 30, 30, 30)
        self.rect_3 = pygame.Rect(110, 30, 30, 30)
        self.colour_1 = HEARTS_C
        self.colour_2 = HEARTS_C
        self.colour_3 = HEARTS_C

class Barrier(Object):
    def __init__(self, width, height, x_cord, y_cord, colour):
        Object.__init__(self, width, height, x_cord, y_cord, colour)
        barriers.append(self)

class Candy(Object):
    def __init__(self, width, height, x_cord, y_cord, colour, score):
        Object.__init__(self, width, height, x_cord, y_cord, colour)
        candies.append(self)
        self.score = score

def high_score_func():
    try:
        high_score = pickle.load( open('highscore.p', 'rb'))
        if player.score > high_score:
            high_score = player.score
            pickle.dump(high_score, open('highscore.p', 'wb'))
    except EOFError:
        high_score = player.score
        pickle.dump(high_score, open('highscore.p', 'wb'))
    if high_score > player.score:
            return high_score
    else:
        high_score = player.score
        return high_score

def spawn_barrier():
    if random.randint(0, 1) == 1:
        while True:
            x = RESOLUTION[0] + 1
            y = random.randrange(0, int(RESOLUTION[1]) - int(RESOLUTION[1]/3), int(RESOLUTION[1]/30))
            for barrier in barriers:
                if barrier.rect.x == x or barrier.rect.y == y:
                    continue
            break

        Barrier(RESOLUTION[0]/15, RESOLUTION[1]/3, x, y, BARRIER_C)
    else:
        while True:
            x = RESOLUTION[0] + 1
            y = random.randrange(0, int(RESOLUTION[1]) - int(RESOLUTION[1]/3), int(RESOLUTION[1]/30))
            for barrier in barriers:
                if barrier.rect.x == x or barrier.rect.y == y:
                    continue
            break

        Barrier(RESOLUTION[0]/3, RESOLUTION[1]/15, x, y, BARRIER_C)

def spawn_candy():
    while True:
        x = RESOLUTION[0] + 1
        y = random.randrange(0, RESOLUTION[1])
        for candy in candies:
            if candy.rect.x == x or candy.rect.y == y:
                continue
        for barrier in barriers:
            if barrier.rect.x == x or barrier.rect.y == y:
                continue
        break
    rarity(Candy(RESOLUTION[0]/30, RESOLUTION[1]/30, x, y, CANDY_C_1, 1))
  
def destroy():
    global candies, barriers
    for barrier in barriers:
        if barrier.rect.x < -360:
            barriers.remove(barrier)
            del barrier
    for candy in candies:
        for barrier in barriers:
            if not collision(barrier, candy):
                candies.remove(candy)
                del candy
                return 
        if candy.rect.x < -360:
            candies.remove(candy)
            del candy

def collision(obj, obj2):
    global candies, barriers
    if obj.rect.x <= obj2.rect.x <= obj.rect.x+obj.rect.width or obj.rect.x <= obj2.rect.x+obj2.rect.width <= obj.rect.x+obj.rect.width:
        if obj.rect.y <= obj2.rect.y <= obj.rect.y+obj.rect.height or obj.rect.y <= obj2.rect.y+obj2.rect.height <= obj.rect.y+obj.rect.height:
            if type(obj2).__name__ == "Player":
                if type(obj).__name__ == 'Barrier':
                    barriers.remove(obj)
                    del obj
                elif type(obj).__name__ == 'Candy':
                    candies.remove(obj)
                    del obj
                return False
            elif type(obj2).__name__ == "Candy":
                return False
            else:
                del obj2
    return True

def rarity(candy):
    num = random.randint(1, 100)
    if 30 <= num <= 100:
        candy.score = 1
        candy.colour = CANDY_C_1
    elif 5 <= num <= 30:
        candy.score = 2
        candy.colour = CANDY_C_2
    elif 2 <= num <= 5:
        candy.score = 5
        candy.colour = CANDY_C_3
    else:
        candy.score = 20
        candy.colour = CHEESE

# Define Function For Each Screen
def intro():
    global RUNNING, MENU, END, INTRO, MUTE, INSTRUCTIONS, barrier_spawn_rate, high_score, barriers, candies, health, dif_state

    # Sets Framerate
    CLOCK.tick(60)

    # Leave Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            INTRO = False
        elif event.type == pygame.KEYDOWN:
            INTRO = False
            INSTRUCTIONS = True
    # Draw Screen
    SCREEN.fill(BACKGROUND_C)
    end_text = font.render("Get Candy!", True, TITLE_C)
    end_text_2 = font.render("Hit Any Key To Start", True, TITLE_C)
    inst_text = font.render("You are an animal from the local zoo.", True, TITLE_C)
    inst_text_2 = font.render("Try and get as much as candy as you can,", True, TITLE_C)
    inst_text_3 = font.render("while avoiding the barriers!", True, TITLE_C)

    
    SCREEN.blit(end_text, (RESOLUTION[0]/2 - RESOLUTION[0]/4, RESOLUTION[1]/2 - RESOLUTION[1]/6))
    SCREEN.blit(end_text_2, (RESOLUTION[0]/2 - RESOLUTION[0]/4, RESOLUTION[1]/4 - RESOLUTION[1]/6))
    SCREEN.blit(inst_text, (50, 400))
    SCREEN.blit(inst_text_2, (50, 460))
    SCREEN.blit(inst_text_3, (50, 510))

    pygame.display.flip()

def instructions():
    global RUNNING, MENU, END, INTRO, MUTE, INSTRUCTIONS, barrier_spawn_rate, high_score, barriers, candies, health, dif_state

    # Sets Framerate
    CLOCK.tick(60)

    # Leave Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            INSTRUCTIONS = False
        elif event.type == pygame.KEYDOWN:
            RUNNING = True
            INSTRUCTIONS = False

    # Draw Screen
    SCREEN.fill(BACKGROUND_C)
    controls = font.render("W = UP and S = DOWN", True, TITLE_C)
    controls_2 = font.render("Hit escape to access settings", True, TITLE_C)
    controls_3 = font.render("Go off the screen to come out the other end", True, TITLE_C)
    controls_4 = font.render("Change the difficulty to get more candies", True, TITLE_C)
    start_text = font.render("Hit Any Key To Start", True, TITLE_C)
    inst_text = font.render("Blue = 1 Candy", True, TITLE_C)
    inst_text_2 = font.render("Red = 2 Candies", True, TITLE_C)
    inst_text_3 = font.render("Orange = 5 Candies", True, TITLE_C)

    
    SCREEN.blit(controls, (50, 50))
    SCREEN.blit(controls_2, (50, 110))
    SCREEN.blit(controls_3, (50, 170))
    SCREEN.blit(controls_4, (50, 230))
    SCREEN.blit(inst_text, (50, 290))
    SCREEN.blit(inst_text_2, (50, 350))
    SCREEN.blit(inst_text_3, (50, 410))
    SCREEN.blit(start_text, (300, 490))

    pygame.display.flip()

def running():
    global RUNNING, MENU, END, INTRO, MUTE, INSTRUCTIONS, barrier_spawn_rate, high_score, barriers, candies, health, dif_state

    # Sets Framerate
    CLOCK.tick(60)

    # Leave Game & Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
            END = False
            MENU = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            RUNNING = False
            MENU = True
        elif event.type == SPAWN:
            if len(barriers) < 10:
                spawn_barrier()
            spawn_candy()
        elif event.type == MINUTE:
            if not barrier_spawn_rate == 200:
                barrier_spawn_rate -= 200
                pygame.time.set_timer(SPAWN, barrier_spawn_rate)
        elif event.type == SECONDS:
            player.colour = PLAYER_C

    #Garbage Collector 
    destroy()

    # Collision
    for barrier in barriers:
        if not collision(barrier, player):
            player.colour = PLAYER_HURT_C
            pygame.time.set_timer(SECONDS, 1000*2)
            if MUTE == False:
                pygame.mixer.music.load('barrier.aif')
                pygame.mixer.music.play()
            player.health -= 1
            player.rect.x += 30
            if health.colour_3 == (255,7,131):
                health.colour_3 = BLACK_C
            elif health.colour_2 == (255,7,131):
                health.colour_2 = BLACK_C
            elif health.colour_1 == (255,7,131):
                health.colour_1 = BLACK_C
    
    for candy in candies:
        if not collision(candy, player):
            if dif_state == "easy":
                player.score += candy.score
            elif dif_state == "medium":
                player.score += candy.score * 2
            elif dif_state == "hard":
                player.score += candy.score * 3

            if MUTE == False:
                pygame.mixer.music.load('candy.aif')
                pygame.mixer.music.play()
    # Move Player
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        player.move("up")
    if key[pygame.K_s]:
        player.move("down")

    # Move All Barriers
    for barrier in barriers:
        barrier.move("left")

    # Move All Candies
    for candy in candies:
        candy.move("left")

    # End game 
    if player.health < 1:
        RUNNING = False
        END = True
        if MUTE == False:
            pygame.mixer.music.load('death.aif')
            pygame.mixer.music.play()
        player.colour = PLAYER_C

    # Drawing The Screen
    SCREEN.fill(BACKGROUND_C)
    
    for candy in candies:
        if candy.colour != CHEESE:
            pygame.draw.circle(SCREEN, candy.colour, (candy.rect.x, candy.rect.y), int(candy.rect.width/2), int(candy.rect.width/2))
        else:
            pygame.draw.rect(SCREEN, candy.colour, candy.rect)
    for barrier in barriers:
        pygame.draw.rect(SCREEN, barrier.colour, barrier.rect)

    pygame.draw.rect(SCREEN, health.colour_1, health.rect_1)
    pygame.draw.rect(SCREEN, health.colour_2, health.rect_2)
    pygame.draw.rect(SCREEN, health.colour_3, health.rect_3)

    score = font.render("Candies: " + str(player.score), True, TITLE_C)
    SCREEN.blit(score, (RESOLUTION[0]-360 , 30))

    pygame.draw.rect(SCREEN, player.colour, player.rect)

    pygame.display.flip()

def end():
    global RUNNING, MENU, END, INTRO, MUTE, INSTRUCTIONS, barrier_spawn_rate, high_score, barriers, candies, health, dif_state

    # Sets Framerate
    CLOCK.tick(60)

    # Leave Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
            END = False
            MENU = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            RUNNING = False
            END = False
            MENU = False  
        elif event.type == pygame.KEYDOWN:
            END = False
            RUNNING = True
            player.health = 3
            barrier_spawn_rate = 1000
            health = Health()
            barriers = []
            candies = [] 
            player.rect.x -=90
            player.score = 0
            barrier_spawn_rate = 1000
            pygame.time.set_timer(SPAWN, barrier_spawn_rate)
            dif_state = "easy"

    # Draw Screen
    SCREEN.fill(BACKGROUND_C)
    end_text = font.render("High Score: " + str(high_score_func()) , True, TITLE_C)
    score = font.render("Candies: " + str(player.score), True, TITLE_C)
    instruction = font.render("Press any key to try again.", True, TITLE_C)
    instruction_2 = font.render("Press escape to quit.", True, TITLE_C)
    SCREEN.blit(end_text, (RESOLUTION[0]/2 - RESOLUTION[0]/4, RESOLUTION[1]/2 - RESOLUTION[1]/6))
    SCREEN.blit(score, (RESOLUTION[0]-360 , 30))
    SCREEN.blit(instruction, (RESOLUTION[0]-700 , 400))
    SCREEN.blit(instruction_2, (RESOLUTION[0]-700 , 500))
    pygame.display.flip()

def menu():
    global RUNNING, MENU, END, INTRO, MUTE, INSTRUCTIONS, barrier_spawn_rate, high_score, barriers, candies, health, dif_state

    # Sets Framerate
    CLOCK.tick(60)

    # Leave Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
            END = False
            MENU = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            MENU = False
            RUNNING = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            MUTE = not MUTE
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            if dif_state == "easy":
                dif_state = "medium"
            elif dif_state == "medium":
                dif_state = "hard"
            elif dif_state == "hard":
                dif_state = "easy"

    # Sets Mute State
    if MUTE == True:
        mute_state = "unmute"
    else:
        mute_state = "mute"

    # Draw Screen
    SCREEN.fill(BACKGROUND_C)
    end_text = font.render("MENU ", True, TITLE_C)
    SCREEN.blit(end_text, (300, RESOLUTION[1]/2 - RESOLUTION[1]/6))

    mute_text = font.render("Press 'm' to {}".format(mute_state), True, TITLE_C)
    SCREEN.blit(mute_text, (50, RESOLUTION[1]/2 - RESOLUTION[1]/6 + 100))

    dif_text = font.render("Press 'd' to change mode. Current Mode: {}".format(dif_state), True, TITLE_C)
    SCREEN.blit(dif_text, (50, RESOLUTION[1]/2 - RESOLUTION[1]/6 + 200))

    back_text = font.render("Hit escape to get back to the game", True, TITLE_C)
    SCREEN.blit(back_text, (200, RESOLUTION[1]/2 - RESOLUTION[1]/6 + 300))

    pygame.display.flip()

def main():
    global RUNNING, MENU, END, INTRO, MUTE, INSTRUCTIONS, barrier_spawn_rate, high_score, barriers, candies, health, dif_state
    
    while INTRO:
        intro()
    while INSTRUCTIONS:
        instructions()
    while RUNNING:
        running()
    while END:
        end()
    while MENU:
        menu()

# Initialize Pygame
os.environ["SDL_VIDEO_CENTERED"] =  "1"
pygame.init()

# Set Up Display
pygame.display.set_caption("Sweet Tooth")
SCREEN = pygame.display.set_mode(RESOLUTION)
CLOCK = pygame.time.Clock()
font = pygame.font.SysFont("none", 50)

# Colours
CANDY_C_1 = (102,244,255)
CANDY_C_2 = (255,102,128)
CANDY_C_3 = (247,151,31)
CHEESE = (245, 236, 183)
BLACK_C = (0, 0, 0)
PLAYER_C = (94,149,152)
PLAYER_HURT_C = (255, 0, 0)
BARRIER_C = (141,122,126)
HEARTS_C = (255,7,131)
BACKGROUND_C = (255,248,245)
TITLE_C = (254,127,30)

# Initialize Player
high_score = 0
player = Player(RESOLUTION[0]/30, RESOLUTION[1]/30, 
    RESOLUTION[0]/2.5, RESOLUTION[1]/2, PLAYER_C, 3, 0)

# Initialize Lists 
barriers = []
candies = []

# Initialize Timers
SPAWN = pygame.USEREVENT
barrier_spawn_rate = 1000
pygame.time.set_timer(SPAWN, barrier_spawn_rate)

MINUTE = pygame.USEREVENT+1
pygame.time.set_timer(MINUTE, 1000*10)

SECONDS = pygame.USEREVENT+2
pygame.time.set_timer(SECONDS, 1000*2)

RUNNING = False
END = False
MENU = False
INTRO = True
MUTE = False
INSTRUCTIONS = False
dif_state = "easy"
high_score_func()
health = Health()

while True:
    main()
    if RUNNING or END or MENU or INTRO:
        continue
    else:
        break

if __name__ == '__main__':
    main()
