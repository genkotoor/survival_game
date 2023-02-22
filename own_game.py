"""our first pygame game"""
import sys
import pygame
import random
import time

pygame.init()

# create clock
clock = pygame.time.Clock()

# create a game window
back_color = (255, 255, 255)  # background color
win_size = (2880, 1600)
mw = pygame.display.set_mode(win_size)  # main window
mw.fill(back_color)
start_time = time.time()

class Character():
    """player is circle which is capable of movement"""
    def __init__(self, x=0, y=0, radius=10, color=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = 5

    def move_up(self):
        # check if player isn't touching top of screen
        if self.y - self.radius > 0:
            self.y -= self.speed

    def move_down(self):
        # check if player isn't touching bottom of screen
        if self.y + self.radius < win_size[1]:
            self.y += self.speed

    def move_left(self):
        # check if player isn't touching left of screen
        if self.x - self.radius > 0:
            self.x -= self.speed

    def move_right(self):
        # check if player isn't touching right of screen
        if self.x + self.radius < win_size[0]:
            self.x += self.speed

    def draw(self):
        pygame.draw.circle(mw, self.color, (self.x, self.y), self.radius)

    def is_touching(self, other):
        """check if self is touching other"""
        # get distance between self and other
        distance = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        # check if distance is less than sum of radii
        if distance < self.radius + other.radius:
            return True
        return False

RED = (255, 0, 0)
# rgb = (red, green, blue)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


player = Character(500, 500, 50, BLUE)
player.draw()

enemies = list()
enemies_directions = list() # implement

i = 0
while i < 10:
    # make coordinates random in range of screen, but not too close to the player
    enemy_x = random.randint(0, win_size[0])
    enemy_y = random.randint(0, win_size[1])
    while (enemy_x >= 400 and enemy_x <= 600) or (enemy_y >= 400 and enemy_y <= 600):
        enemy_x = random.randint(0, win_size[0])
        enemy_y = random.randint(0, win_size[1])
    enemies.append(Character(enemy_x, enemy_y, 50, RED))
    enemies_directions.append(0)
    i += 1

for enemy in enemies:
    enemy.draw()

rand_x = random.randint(0, win_size[0])
rand_y = random.randint(0, win_size[1])
extra_file = Character(rand_x, rand_y, 50, YELLOW)
extra_file.draw()

lives = 1

# main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.move_up()
    if keys[pygame.K_DOWN]:
        player.move_down()
    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()

    if random.randint(0, 30) == 0:
        for i in range(len(enemies_directions)):
            random_number = random.randint(1, 4)
            enemies_directions[i] = random_number

    for enemy, random_number in zip(enemies, enemies_directions):
        if random_number == 1:
            enemy.move_up()
        if random_number == 2:
            enemy.move_right()
        if random_number == 3:
            enemy.move_down()
        if random_number == 4:
            enemy.move_left()

    # move extra life similar to enemies
    if random.randint(0, 30) == 0:
        random_number = random.randint(1, 4)
    if random_number == 1:
        extra_file.move_up()
    if random_number == 2:
        extra_file.move_right()
    if random_number == 3:
        extra_file.move_down()
    if random_number == 4:
        extra_file.move_left()

    # check if player is touching extra life
    if player.is_touching(extra_file):
        lives += 1
        extra_file.x = random.randint(0, win_size[0])
        extra_file.y = random.randint(0, win_size[1])

    # for each enemy, check if it collides with player and if so, stop the game and show the time
    for enemy in enemies:
        # use is touching function
        if player.is_touching(enemy):
            lives -= 1
            # remove enemy from the list
            enemies.remove(enemy)

    if lives == 0:
        print('game over')
        score = time.time() - start_time
        # display score on the screen
        font = pygame.font.SysFont('Arial', 60)
        text = font.render('Score: ' + str(score), True, (255, 0, 0))
        mw.blit(text, (500, 500))
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        sys.exit()

    if random.randint(0, 100) == 0:
        enemy = random.choice(enemies)
        enemies.append(Character(enemy.x, enemy.y, 50, RED))
        enemies_directions.append(0)

    # render text with extra lives in the top right corner
    font = pygame.font.SysFont('Arial', 60)
    text = font.render('Lives: ' + str(lives), True, (255, 0, 0))
    mw.blit(text, (0, 0))
    pygame.display.update()
    mw.fill(back_color)
    player.draw()
    for enemy in enemies:
        enemy.draw()
    extra_file.draw()
    clock.tick(40)
