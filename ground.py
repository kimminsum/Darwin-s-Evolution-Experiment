import pygame, os, random
pygame.init()
 
FPS=60

SCREEN = pygame.display.set_mode((400,500))
pygame.display.set_caption('caption')

x=50
y=450
vel = 3
width = 20
height = 20

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        super().__init__() 
        self.vel = 3
        self.image = pygame.Surface((width, height))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect(topleft = (x, y))
   
class B(pygame.sprite.Sprite):
    def __init__(self,x,y,radius, color):
        super().__init__() 
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.vel = vel
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (self.x, self.y))
       
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.Surface((20,20))
        self.image.fill((255, 0, 0))
        y = random.randrange (0, 480)
        x = 400
        self.rect = self.image.get_rect(topleft = (x, y))
        self.speed = random.randrange(1,3)

player = Player(x, y, width, height)

enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and len(bullets) < 5:
                bullet = B(player.rect.centerx, player.rect.centery, 3, (0,0,0))
                bullets.add(bullet)
                all_sprites.add(bullet)

    if len(enemies) < 8:
        e = Enemy()
        enemies.add(e)
        all_sprites.add(e)

    for bullet in bullets:
        if bullet.rect.right < 500:
            bullet.rect.x += bullet.vel
        else:
            bullet.kill()
    for enemy in enemies:
        if enemy.rect.right > 0:
            enemy.rect.x -= enemy.speed
        else:
            enemy.kill()

    pygame.sprite.groupcollide(bullets, enemies, True, True)
            
    keys = pygame.key.get_pressed()            
    if keys[pygame.K_w] and player.rect.top > player.vel:
        player.rect.y -= player.vel
    if keys[pygame.K_s] and player.rect.bottom < 500 - player.vel:
        player.rect.y += player.vel
    
    SCREEN.fill((190, 232, 220))
    all_sprites.draw(SCREEN)
    pygame.display.update()

pygame.quit()