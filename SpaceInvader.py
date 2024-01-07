import pygame
import random
import math

S_WIDTH = 800 #screen width
S_HEIGHT = 800 #screen height

pygame.init()

# title and icon of the window
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(icon)

# create the screen and set the bckg
screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
background = pygame.image.load('img/background.jpg')

font = pygame.font.Font(None, 36)

# classes

class Player():
    # class to store the Player
    img = pygame.image.load('img/player.png')
    WIDTH = img.get_width()
    HEIGHT = img.get_height()

    def __init__(self): # constructor that spawns the object
        self.x = S_WIDTH / 2 - self.WIDTH / 2
        self.y = S_HEIGHT - self.HEIGHT * 1.5
        self.x_movement = 0

    def move_right(self):
        self.x_movement = 4

    def move_left(self):
        self.x_movement = -4

    def update(self):
        self.x += self.x_movement
        self.boundary_check()
        screen.blit(self.img, (self.x, self.y))

    def boundary_check(self):
        if self.x <= 0:
            self.x = 0
        elif self.x >= S_WIDTH - self.WIDTH:
            self.x = S_WIDTH - self.WIDTH

    def stop_moving(self):
        self.x_movement = 0

class Invader:
    img = pygame.image.load('img/invader.png')
    WIDTH = img.get_width()
    HEIGHT = img.get_height()
    y_shift = S_HEIGHT * 0.05

    def __init__(self): # constructor that spawns the object
        self.reset()
    
    def reset(self):
        self.x = random.randint(0, S_WIDTH - self.WIDTH)
        self.y = random.randint(int(S_HEIGHT * 0.0625), int(S_HEIGHT * 0.25))
        self.x_movement = 3

    def update(self):
        self.x += self.x_movement
        self.boundary_check()
        screen.blit(self.img, (self.x, self.y))

    def boundary_check(self):
        if self.x <= 0:
            self.x_movement = 3
            self.y += self.y_shift
        elif self.x >= S_WIDTH - self.WIDTH:
            self.x_movement = -3
            self.y = self.y_shift


class Bullet:

    img = pygame.image.load('img/bullet.png')
    WIDTH = img.get_width()
    HEIGHT = img.get_height()
    y_shift = S_HEIGHT * 0.03
    
    def __init__(self):
        self.x = 0
        self.reset()

    def reset(self):
        self.y = 0
        self.state = 'loaded'

    def fire(self, player):
        if self.state is 'loaded':
            self.x = player.x
            self.y = player.y
            self.state = 'fired'

    def did_hit(self, invader):
        distance = math.sqrt(((invader.x - self.x)**2) + ((invader.y - self.y)**2))
        if distance < invader.WIDTH * 0.4:
            return True
        else:
            return False

    def update(self):
        if self.state is 'fired':
            if self.y <= 0:
                self.reset()
            else:
                self.show()
                self.y -= self.y_shift
    
    def show(self):
        screen.blit(self.img, (self.x + self.WIDTH/2, self.y + self.HEIGHT/3))

class InvaderBullet:
    img = pygame.image.load('img/invader_bullet.png')
    WIDTH = img.get_width()
    HEIGHT = img.get_height()
    y_shift = S_HEIGHT * 0.02
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = 'fired'

    def did_hit(self, player):
        distance = math.sqrt(((player.x - self.x)**2) + ((player.y - self.y)**2))
        if distance < player.WIDTH * 0.4:
            return True
        else:
            return False

    def update(self):
        if self.state == 'fired':
            if self.y >= S_HEIGHT:
                self.reset()
            else:
                self.show()
                self.y += self.y_shift

    def reset(self):
        self.state = 'ready'

    def show(self):
        screen.blit(self.img, (self.x + self.WIDTH/2, self.y + self.HEIGHT/3))

# Initialize player, bullet, and invaders
player = Player()
bullet = Bullet()
num_invaders = 5  # Adjusted number of invaders
invaders = [Invader() for _ in range(num_invaders)]
invader_bullets = []

# Game variables
score = 0
lives = 3

# game loop
loop = True
clock = pygame.time.Clock()

while loop:
    screen.fill((0, 0, 0))  # reset screen to black
    screen.blit(background, (0, 0))  # places background image aligned to 0, 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # exit game on close
            loop = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move_left()
            if event.key == pygame.K_RIGHT:
                player.move_right()
            if event.key == pygame.K_SPACE:
                bullet.fire(player)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.stop_moving()

    player.update()
    bullet.update()

    for invader in invaders:
        was_hit = bullet.did_hit(invader)

        if was_hit:
            invader.reset()
            bullet.reset()
            score += 100

        invader.update()

        # Check if invader should shoot a bullet
        if random.random() < 0.02:  # Adjust this value for the frequency of shooting
            invader_bullet = InvaderBullet(invader.x, invader.y)
            invader_bullets.append(invader_bullet)

    for invader_bullet in invader_bullets:
        if invader_bullet.did_hit(player):
            invader_bullet.reset()
            lives -= 1

        invader_bullet.update()

    # Remove bullets that have moved off the screen
    invader_bullets = [bullet for bullet in invader_bullets if bullet.state == 'fired']

    # Draw score on the top left
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Draw lives on the top right
    lives_text = font.render(f'Lives: {lives}', True, (255, 255, 255))
    screen.blit(lives_text, (S_WIDTH - 100, 10))

    pygame.display.update()  # update / refresh the screen
    clock.tick(60)  # set the frame rate to 60 frames per second

    # Check if the player has run out of lives
    if lives == 0:
        loop = False

# Display game over message and final score
game_over_text = font.render('Game Over!', True, (255, 0, 0))
final_score_text = font.render(f'Final Score: {score}', True, (255, 255, 255))

screen.blit(game_over_text, (S_WIDTH // 2 - 100, S_HEIGHT // 2 - 50))
screen.blit(final_score_text, (S_WIDTH // 2 - 120, S_HEIGHT // 2))

pygame.display.update()

# Wait for a few seconds before quitting (you can adjust this duration)
pygame.time.delay(3000)

pygame.quit()