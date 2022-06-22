
# Import libraries
import pygame
import random
import sqlite3

# Initialise window, FPS and colours
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
LEFT_WALL = 119
RIGHT_WALL = 682
TOP_WALL = 18
BOTTOM_WALL = 581

FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
CYAN = (0x00,0xCC,0xFF)

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./assets/player.png')

        self.rect = self.image.get_rect()
        self.rect.center = ((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 2))
        self.__playerX = 0
        self.__playerY = 0
        self.__vel = 4

    # This function will be called every frame in the game loop
    def update(self):
        # I need to reset them to 0 or else the character 
        # will move even if the player releases the button 
        self.__playerX = 0
        self.__playerY = 0

        # Mag is the speed of the player when moving diagonally
        # There is a constant so the player moves in all directions at the same speed
        mag = self.__vel * 0.707106781187
        mag = round(mag)
        # Player movement
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT] and keystate[pygame.K_UP]:
            self.__playerX = -mag
            self.__playerY = -mag

        elif keystate[pygame.K_LEFT] and keystate[pygame.K_DOWN]:
            self.__playerX = -mag
            self.__playerY = mag

        elif keystate[pygame.K_RIGHT] and keystate[pygame.K_UP]:
            self.__playerX = mag
            self.__playerY = -mag

        elif keystate[pygame.K_RIGHT] and keystate[pygame.K_DOWN]:
            self.__playerX = mag
            self.__playerY = mag

        elif keystate[pygame.K_LEFT]:
            self.__playerX = -self.__vel

        elif keystate[pygame.K_RIGHT]:
            self.__playerX = self.__vel

        elif keystate[pygame.K_UP]:
            self.__playerY = -self.__vel

        elif keystate[pygame.K_DOWN]:
            self.__playerY = self.__vel

        self.rect.x += self.__playerX
        self.rect.y += self.__playerY

        # Player boundaries
        if self.rect.left <= 124:
            self.rect.left = 124

        elif self.rect.right >= 678:
            self.rect.right = 678

        if self.rect.top <= 23:
            self.rect.top = 23

        elif self.rect.bottom >=577:
            self.rect.bottom = 577

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('./assets/bullet.png')
        self.rect = self.image.get_rect()
        rand_x_array = [random.randrange(0, LEFT_WALL), random.randrange(RIGHT_WALL, WINDOW_WIDTH)]
        rand_y_array = [random.randrange(0, TOP_WALL), random.randrange(BOTTOM_WALL, WINDOW_HEIGHT)]
        rand_velx_array = [random.randrange(-6, -1), random.randrange(1, 6)]
        rand_vely_array = [random.randrange(-6, -1), random.randrange(1, 6)]

        self.rect.x = rand_x_array[random.randint(0, 1)]
        self.rect.y = rand_y_array[random.randint(0, 1)]
        self.velx = rand_velx_array[random.randint(0, 1)]
        self.vely = rand_vely_array[random.randint(0, 1)]

        if self.rect.x < LEFT_WALL and self.velx < 0:
            self.velx = -(self.velx)
        elif self.rect.x > RIGHT_WALL and self.velx > 0:
            self.velx = -(self.velx)
        if self.rect.y < TOP_WALL and self.vely < 0:
            self.vely = -(self.vely)
        elif self.rect.y > BOTTOM_WALL and self.vely > 0:
            self.vely = -(self.vely)
        
    def update(self):
        self.rect.x += self.velx
        self.rect.y += self.vely

class Database():

    def __init__(self):
        self.connection = sqlite3.connect('leaderboard.db')
        self.cursor = self.connection.cursor()
        print('Connected to SQLite')

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS leaderboard (
                id INT PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                score INT NOT NULL
            );
        ''')

    def save_score_to_table(self, name, score):
        # id exists to act as a primary key so there 
        # is no clashing between primary keys 
        id = random.randrange(0, 1000)
        self.cursor.execute(f'''
        INSERT INTO leaderboard (id, name, score)
        VALUES ("{id}", "{name}", "{score}")
        ''')
        self.connection.commit()

    def read_scores(self):
        db_names = []
        db_scores = []
        self.cursor.execute('''
        SELECT name, score from leaderboard;
        ''')

        rows = self.cursor.fetchall()

        for row in rows:
            db_names.append(row[0])
            db_scores.append(row[1])

        return db_names, db_scores

# Functions
def terminate():
    pygame.quit()

def wait_player():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                return

def bubble():
    db_names, db_scores= database.read_scores()
    swapped = True
    n = len(db_names)
    while swapped == True and n >= 0:
        swapped = False
        for i in range(0, n-1):
            if db_scores[i] < db_scores[i+1]:
                db_names[i], db_names[i+1], = db_names[i+1], db_names[i]
                db_scores[i], db_scores[i+1], = db_scores[i+1], db_scores[i]
                swapped= True

        n -= 1

    return db_names, db_scores

def menu(POINTER, MENU_SCREEN, BLACK):
    pointer_x = 175
    pointer_y = 130
    run = True
    while run:
        screen.fill(BLACK)
        screen.blit(MENU_SCREEN, (0,0))
        screen.blit(POINTER,(pointer_x, pointer_y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and pointer_y > 130:
                    pointer_y -= 160
                if event.key == pygame.K_DOWN and pointer_y < 450:
                    pointer_y += 160

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    if pointer_y == 130 and pointer_x != 175:
                        pointer_x += 155
                    if pointer_y == 290:
                        pointer_x -= 155
                    if pointer_y == 450 and pointer_x != 175:
                        pointer_x += 155

                if event.key == pygame.K_RETURN:
                    if pointer_y == 130:
                        return
                    if pointer_y == 290:
                        leaderboard()
                    if pointer_y == 450:
                        terminate()

        pygame.display.update()

def leaderboard():
    db_names, db_scores = bubble()
    run = True
    y = 150
    amount = 5

    screen.fill(BLACK)

    print_text('Name', font, CYAN, 250, 50)
    print_text('Score', font, CYAN, 430, 50)

    if len(db_names) < 5:
        amount = len(db_names)

    for i in range(0, amount):
            print_text(str(db_names[i]), font, CYAN, 280, y)
            print_text(str(db_scores[i]), font, CYAN, 430, y)
            y = y + 80

    pygame.display.update()

    while run:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

def game_over_screen(POINTER, SAVE_SCREEN, BLACK):
    pointer_x = 280
    pointer_y = 250
    run = True
    while run:
        screen.fill(BLACK)
        screen.blit(SAVE_SCREEN, (0,0))
        screen.blit(POINTER,(pointer_x, pointer_y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and pointer_y > 250:
                    pointer_y -= 130
                if event.key == pygame.K_DOWN and pointer_y < 380:
                    pointer_y += 130

                if event.key == pygame.K_RETURN or event.key == pygame.K_z:
                    if pointer_y == 250:
                        run = False
                        break
                    if pointer_y == 380:
                        terminate()

        pygame.display.update()
    
    save_score(score, BLACK)

def save_score(score, BLACK):
    database.create_table()
    name = ""
    letter = ""
    run = True
    while run:
        screen.fill(BLACK)
        screen.blit(SAVE_SCORE_SCREEN, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                letter = str((pygame.key.name(event.key)))
                name = name + letter
                print(name)

                if len(name) == 3:
                    print(name, score)
                    database.save_score_to_table(name, score)

                    return name

        pygame.display.update()
    
def print_text(text, font, colour, x, y):
    label = font.render(text, 1, colour)
    screen.blit(label, (x, y))

# This will keep track of how many frames have passed and
# allow us to figure out how much real time has passed
frame_count = 0
time_passed = 0
score = 0
level = 1
level_score = 0
mobs = []
player_alive = True
spawn_rate = 30
level_change = True

# Initialize the game and clock
pygame.init()
main_clock = pygame.time.Clock()

# Initialise screen, caption and icon
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Super Calum Game")
icon = pygame.image.load('./assets/icon.png')
pygame.display.set_icon(icon)

# Put all of the sprites into a group so they can be called
# to update at the same time
player_group = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = Player()
player_group.add(player)
database = Database()

# Set up font and background variables
font = pygame.font.Font('./assets/SuperMario256.ttf', 40)
TITLE_SCREEN = pygame.image.load('./assets/title.png')
MENU_SCREEN = pygame.image.load('./assets/menu.png')
SAVE_SCREEN = pygame.image.load('./assets/savescreen.png')
SAVE_SCORE_SCREEN = pygame.image.load('./assets/savescorescreen.png')
BACKGROUND = pygame.image.load('./assets/background.png')
POINTER = pygame.image.load('./assets/pointer.png')

screen.blit(TITLE_SCREEN, (0,0))
pygame.display.update()

# This function will finish when the player inputs a command and the 
# program won't continue until this condition is fulfilled
wait_player()        
        
screen.blit(MENU_SCREEN, (0,0))
pygame.display.update()

menu(POINTER, MENU_SCREEN, BLACK)

# Game loop
run = True
while run:

    # Every frame

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            terminate()

    # Score 

    time_passed += 1
    frame_count += 1
    if frame_count == 60: 
        # Every second

        score += 1
        frame_count = 0
        level_score += 1

    if time_passed == spawn_rate:
        mobs.add(Mob())
        time_passed = 0

    if level_change == True:
        if level_score == 15:
            level += 1
            spawn_rate -= 5
            level_score = 0

            if level == 5:
                level_change = False

    player_group.update()
    mobs.update()

    for _ in pygame.sprite.spritecollide(player, mobs, False):
        player_alive = False

    screen.fill(BLACK)
    screen.blit(BACKGROUND,(0,0))

    print_text(f'Score: {score}', font, CYAN, 125, 30)
    if level == 5:
        print_text(f'Final Level', font, CYAN, 400, 30)
    else:
        print_text(f'Level {level}', font, CYAN, 495, 30)

    player_group.draw(screen)
    mobs.draw(screen)
    pygame.display.flip()
    main_clock.tick(FPS)

    if player_alive == False:
        break

game_over_screen(POINTER, SAVE_SCREEN, BLACK)
leaderboard()