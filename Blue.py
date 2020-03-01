import pygame, random
pygame.init()

window = pygame.display.set_mode((500, 600))
pygame.display.set_caption("generic_topdown_shooter.exe")
# загрузка изображений
heartSprite = pygame.image.load('heart.png')
playerSprite = pygame.image.load('shuttle2.png')
enemyShipSprite1 = pygame.image.load('enemyship.png')
enemyBossSprite1 = pygame.image.load('bossenemy.png')
enemyShipSprite2 = pygame.image.load('enemyship_2.png')

score = 0


# класс игрока
class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.yike = False
        self.yeey = 0

    def draw(self, window):
        # отображение игрока
        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(window, (50, 41, 51), self.hitbox)
        window.blit(playerSprite, (self.x, self.y))
        if (self.yike == True) and (self.yeey != 25):
            pygame.draw.rect(window, (50, 41, 51), self.hitbox)
            self.yeey += 1
        elif self.yeey == 25:
            self.yike = False
            self.yeey = 0

    def hit(self):
        # получение урона
        print('ouch')
        self.yike = True


# класс снарядов
class Projectile(object):
    def __init__(self, x, y, rad, color, dir):
        self.x = x
        self.y = y
        self.rad = rad
        self.color = color
        # направление (дружелюбный/вражеский снаряд)
        self.dir = dir
        self.vel = 8 * dir

    def draw(self, window):
        # отображение снаряда
        pygame.draw.circle(window, self.color, (self.x, self.y), self.rad)


class Enemy(object):
    def __init__(self, x, y, width, height, vel, sprite, dird, dd, canShoot, shd, heal):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.sprite = sprite
        # время за которое враг заново выбирает направление
        self.dird = dird
        # время за которое враг движется вниз
        self.dd = dd
        # может ли враг стрелять
        self.canShoot = canShoot
        # время между выстрелами врага
        self.shd = shd
        # здоровье врага
        self.heal = heal
        # выбор направления
        self.dir = random.randint(0, 1)
        # таймер для выбора направления
        self.qv = 0
        # таймер для движения вниз
        self.ba = 0
        # таймер для стрельбы
        self.kd = 0
        self.yike = False
        self.yeey = 0
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self, window):
        self.move()
        # отображение врага
        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(window, (80, 40, 50), self.hitbox)
        window.blit(self.sprite, (self.x, self.y))
        if (self.yike == True) and (self.yeey != 3):
            pygame.draw.rect(window, (80, 40, 50), self.hitbox)
            self.yeey += 1
        elif self.yeey == 3:
            self.yike = False
            self.yeey = 0
        # таймеры
        self.qv += 1
        self.ba += 1
        self.kd += 1

    def move(self):
        # движение врага
        if self.qv == self.dird:
            self.dir = random.randint(0, 1)
            self.qv = 0
        if self.ba == self.dd:
            self.y += self.vel
            self.ba = 0
        if self.dir == 1:
            if self.x < 500 - self.width:
                self.x += self.vel
            elif self.x >= 500 - self.width:
                self.dir = 0
        else:
            if self.x > 0:
                self.x -= self.vel
            elif self.x <= 0:
                self.dir = 1

    def hit(self):
        # получение урона
        print('hit')
        self.heal -= 1
        self.yike = True


def redrawWindow():
    # рисование окна
    window.fill((35, 26, 36))
    gameOverText = gameOverFont.render('Game Over', 1, (255, 255, 255))
    scoreText = font.render(str(score), 1, (255, 255, 255))
    healthText = font.render(str(health) + '/' + str(healthMax), 1, (255, 255, 255))
    for ene in enemies:
        ene.draw(window)
    window.blit(scoreText, (0, 0))
    window.blit(healthText, (430, 0))
    window.blit(heartSprite, (415, 3))
    if health > 0:
        player.draw(window)
    if health <= 0:
        window.blit(gameOverText, (160, 240))
    for bul in bullets:
        bul.draw(window)
    pygame.display.update()


font = pygame.font.SysFont('lucidaconsole', 20, True)
gameOverFont = pygame.font.SysFont('lucidaconsole', 30)
# таймеры для появления врагов
timer = 0
goonspawntimer = 200
thugspawntimer = 100
bossspawntimer = 0
# характеристики игрока
player = Player(218, 525, 52, 52)
isShoot = 0
health = 3
healthMax = 3 + (score // 10000)
# характеристики врагов
enemySpawnPos = random.randint(0, 390)
goon = Enemy(enemySpawnPos, 10, 31, 45, 6, enemyShipSprite1, 6, 4, False, 0, 3)
thug = Enemy(enemySpawnPos, 10, 40, 40, 3, enemyShipSprite2, 20, 8, True, 25, 5)
boss = Enemy(enemySpawnPos, 10, 110, 41, 2, enemyBossSprite1, 10, 6, True, 40, 20)
# списки снарядов и врагов
bullets = []
enemies = []
run = True


while run:
    pygame.time.delay(50)

    # проверка может ли игрок стрелять на данный момент
    if isShoot > 0:
        isShoot += 1
    if score < 35000:
        if isShoot > 10 - score // 5000:
            isShoot = 0
    else:
        if isShoot > 3:
            isShoot = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # проверка врагов
    for ene in enemies:
        # стрельба врагов
        if ene.canShoot == True:
            if ene.kd == ene.shd:
                if ene.vel > 2:
                    bullets.append(Projectile(ene.x + ene.width // 2, ene.y + ene.height, 5, (102, 102, 255), 1))
                elif ene.vel <= 2:
                    bullets.append(Projectile(ene.x + ene.width // 2, ene.y + ene.height, 7, (204, 61, 0), 1))
                ene.kd = 0
        # смерть врага
        if ene.heal == 0:
            score += ene.vel * 40
            if ene.vel == 2:
                health = healthMax
            print(score // 5000)
            enemies.pop(enemies.index(ene))
        if ene.y > 600:
            enemies.pop(enemies.index(ene))
        # враг попадает в игрока
        if ene.y < player.hitbox[1] + player.hitbox[3] and ene.y + ene.height > player.hitbox[1]:
            if ene.x < player.hitbox[0] + player.hitbox[2] and ene.x + ene.width > player.hitbox[0]:
                if health > 0:
                    if player.yike == False:
                        player.hit()
                        health -= 1
                        if ene in enemies:
                            enemies.pop(enemies.index(ene))


    # проверка пуль
    for bl in bullets:
        # попадание пуль во врагов
        for ene in enemies:
            if bl.y - bl.rad < ene.hitbox[1] + ene.hitbox[3] and bl.y + bl.rad > ene.hitbox[1]:
                if bl.x - bl.rad < ene.hitbox[0] + ene.hitbox[2] and bl.x + bl.rad > ene.hitbox[0]:
                    if bl.dir == -1:
                        ene.hit()
                        score += ene.vel * 10
                        if bl in bullets:
                            bullets.pop(bullets.index(bl))
        # попадание пуль в игрока
        if bl.y - bl.rad < player.hitbox[1] + player.hitbox[3] and bl.y + bl.rad > player.hitbox[1]:
            if bl.x - bl.rad < player.hitbox[0] + player.hitbox[2] and bl.x + bl.rad > player.hitbox[0]:
                if bl.dir == 1:
                    if health > 0:
                        if player.yike == False:
                            player.hit()
                            health -= 1
                            bullets.pop(bullets.index(bl))

        if bl.y < 600 and bl.y > 0:
            bl.y += bl.vel
        else:
            bullets.pop(bullets.index(bl))

    keys = pygame.key.get_pressed()
    # управление персонажем
    if keys[pygame.K_SPACE]:
        if health > 0:
            if isShoot == 0:
                bullets.append(Projectile(player.x + player.width // 2, player.y, 6, (205, 165, 0), -1))
                isShoot = 1
    if keys[pygame.K_LEFT]:
        if health > 0:
            if player.x >= 0:
                if keys[pygame.K_LSHIFT]:
                    player.x -= 20
                else:
                    player.x -= player.vel
    if keys[pygame.K_RIGHT]:
        if health > 0:
            if player.x < 500 - player.width:
                if keys[pygame.K_LSHIFT]:
                    player.x += 20
                else:
                    player.x += player.vel
    if keys[pygame.K_ESCAPE]:
        pygame.quit()

    # появление врагов
    if goonspawntimer == 200:
        for i in range(timer // 3000 + 1):
            enemies.append(Enemy(enemySpawnPos, 10, 31, 45, 6, enemyShipSprite1, 6, 4, False, 0, 3))
            enemySpawnPos = random.randint(0, 390)
        goonspawntimer = 0
    if thugspawntimer == 326:
        for i in range(timer // 5000 + 1):
            enemies.append(Enemy(enemySpawnPos, 10, 40, 40, 3, enemyShipSprite2, 20, 8, True, 25, 5))
            enemySpawnPos = random.randint(0, 390)
        thugspawntimer = 0
    if bossspawntimer == 1001:
        for i in range(timer // 7000 + 1):
            enemies.append(Enemy(enemySpawnPos, 10, 110, 41, 2, enemyBossSprite1, 10, 6, True, 40, 20))
            enemySpawnPos = random.randint(0, 390)
        bossspawntimer = 0

    # улучшение здоровья
    if score >= 10000:
        healthMax = 3 + score // 10000

    # таймеры
    timer += 1
    goonspawntimer += 1
    thugspawntimer += 1
    bossspawntimer += 1
    enemySpawnPos = random.randint(0, 390)
    redrawWindow()

pygame.quit()
