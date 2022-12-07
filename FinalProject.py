import pygame
import random
import sys
import time


win_posx = 700
win_posy = 300


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

score = 0
playtime = 1


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

def initialize_game(width, height):
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pygame Shooting")
    return surface

    
def game_loop(surface):
    
    background = pygame.image.load('spacefield.png').convert()
    bg_rect = background.get_rect()
    player_image = pygame.image.load('spaceship.png').convert()
    bullet_image = pygame.image.load('bullet.png').convert()
    asteroid_image = []
    asteroid_list = ['meteor1.png','meteor2.png', 'meteor3.png',
                     'meteor4.png', 'meteor5.png']
    for img in asteroid_list:
        asteroid_image.append(pygame.image.load(img).convert())

    shoot_sound = pygame.mixer.Sound('Shoot.wav')
    shoot_sound.set_volume(0.1)
    explosion_sound = pygame.mixer.Sound('Explosion.wav')
    explosion_sound.set_volume(0.1)
    
    pygame.mixer.music.load('space-wind.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(loops=-1)
    
    clock = pygame.time.Clock()
    sprite_group = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = PlayerShip(player_image)
    global player_health
    player_health= 100
    global score
    score = 0
    sprite_group.add(player)
    

    
    for i in range(10):
        enemy = Mob(asteroid_image)
        sprite_group.add(enemy)
        mobs.add(enemy)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_y:
                    restart()
                if event.key == pygame.K_n:
                    gameover(surface)
                    close_game()
                if event.key == pygame.K_SPACE:
                    player.shoot(sprite_group, bullets, bullet_image, shoot_sound)
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.shoot(sprite_group, bullets, bullet_image, shoot_sound)
                    
        

        sprite_group.update()
        
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            explosion_sound.play()
            mob = Mob(asteroid_image)
            sprite_group.add(mobs)
            mobs.add(mob)
            score += 10
            
        hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
        if hits:
            player_health -= 1
            if player_health < 0:
                continue_game(surface)
                
                
        surface.blit(background, bg_rect)
        sprite_group.draw(surface)
        score_update(surface)
        pygame.display.flip()
        clock.tick(FPS)
        
    pygame.quit()
    print("game played: ", playtime)
    print("Score : ", score)

def score_update(surface):
    font = pygame.font.SysFont('malgungothic',35)
    image = font.render(f'  점수 : {score}  HP: {player_health} ', True, WHITE)
    pos = image.get_rect()
    pos.move_ip(20,20)
    pygame.draw.rect(image, WHITE,(pos.x-20, pos.y-20, pos.width, pos.height), 2)
    surface.blit(image, pos)

def gameover(surface):
    font = pygame.font.SysFont('malgungothic',80)
    image = font.render('GAME OVER', True, WHITE)
    pos = image.get_rect()
    pos.move_ip(int(SCREEN_WIDTH/4)-30, int(SCREEN_HEIGHT/2)-70)
    surface.blit(image, pos)
    pygame.display.update()
    time.sleep(2)
    
def continue_game(surface):
    font = pygame.font.SysFont('malgungothic',80)
    image1 = font.render('CONTINUE?', True, WHITE)
    image2 = font.render('Y / N', True, WHITE)
    pos1 = image1.get_rect()
    pos2 = image2.get_rect()
    pos1.move_ip(int(SCREEN_WIDTH/4)-30, int(SCREEN_HEIGHT/2)-70)
    pos2.move_ip(int(SCREEN_WIDTH/4)+80, int(SCREEN_HEIGHT/2))
    surface.blit(image1, pos1)
    surface.blit(image2, pos2)
    pygame.display.update()
    time.sleep(2)
        
def close_game():
    pygame.quit()
    print('Game closed')

def restart():
    screen = initialize_game(SCREEN_WIDTH,SCREEN_HEIGHT)
    game_loop(screen)
    close_game()

class PlayerShip(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (130, 60))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9/2)
        self.rect.centerx = int(SCREEN_WIDTH / 2)
        self.rect.centery = SCREEN_HEIGHT - 20
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -10
        if keystate[pygame.K_RIGHT]:
            self.speedx = 10
        if keystate[pygame.K_UP]:
            self.speedy = -10
        if keystate[pygame.K_DOWN]:
            self.speedy = 10    
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
            
    def shoot(self, all_sprites,bullets, image, sound):
        bullet = Bullet(self.rect.centerx, self.rect.top, image)
        all_sprites.add(bullet)
        bullets.add(bullet)
        sound.play()
        
class Mob(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image_origin = random.choice(image)
        self.image_origin = pygame.transform.rotozoom(random.choice(image), 0, 0.7)


        self.image = self.image_origin
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9 / 2)
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange( 1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rotation = 0
        self.rotation_speed = random.randrange(-10, 10)  
        self.last_update = pygame.time.get_ticks()


    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rotation = (self.rotation + self.rotation_speed) % 360
            new_image = pygame.transform.rotate(self.image_origin, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT + 10 or self.rect.left < -25 or self.rect.right > SCREEN_WIDTH + 20:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 8)

        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (50, 80))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = player_y
        self.rect.centerx = player_x
        self.speedy = - 10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

if __name__ == '__main__':
    screen = initialize_game(SCREEN_WIDTH,SCREEN_HEIGHT)
    game_loop(screen)
    sys.exit()


