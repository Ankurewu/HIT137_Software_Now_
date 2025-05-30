import pygame
import sys

# Theme: Animal vs Humans – Hero is a rabbit, enemies are wolves
# Game Title: Forest Guardian

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

# Level width for wrap-around
LEVEL_WIDTH = 2000

# Camera smoothing factor
CAMERA_SMOOTHING = 0.1

# Notification duration before boss appears (seconds)
BOSS_ALERT_DURATION = 2

# Draw health bars
def draw_health_bar(surface, x, y, current, maximum, bar_width=50, bar_height=5):
    ratio = current / maximum if maximum > 0 else 0
    pygame.draw.rect(surface, (255, 0, 0), (x, y, bar_width, bar_height))
    pygame.draw.rect(surface, (0, 255, 0), (x, y, int(bar_width * ratio), bar_height))

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.Vector2(0, 0)
        self.smoothing = CAMERA_SMOOTHING

    def custom_draw(self, player):
        target_x = player.rect.centerx - SCREEN_WIDTH // 2
        target_y = player.rect.centery - SCREEN_HEIGHT // 2
        self.offset.x += (target_x - self.offset.x) * self.smoothing
        self.offset.y += (target_y - self.offset.y) * self.smoothing
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset_rect = sprite.rect.copy()
            offset_rect.topleft -= self.offset
            screen.blit(sprite.image, offset_rect)
            if hasattr(sprite, 'health') and hasattr(sprite, 'max_health'):
                draw_health_bar(screen,
                                offset_rect.x,
                                offset_rect.y - 10,
                                sprite.health,
                                sprite.max_health)

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 60, (200, 200, 255))
        self.vel = pygame.Vector2(0, 0)
        self.speed = 5
        self.jump_power = -20
        self.gravity = 0.7
        self.max_health = 100
        self.health = 100
        self.lives = 3
        self.on_ground = False
        self.facing = 1

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        # Compute horizontal velocity
        self.vel.x = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        # Update facing based on movement direction
        if self.vel.x > 0:
            self.facing = 1
        elif self.vel.x < 0:
            self.facing = -1
        # Jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel.y = self.jump_power
        # Apply gravity
        self.vel.y += self.gravity
        # Move and collide
        self.rect.x += self.vel.x
        self._collide(platforms, 'horizontal')
        self.rect.y += self.vel.y
        self._collide(platforms, 'vertical')

    def _collide(self, platforms, direction):
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if direction == 'horizontal':
                    if self.vel.x > 0:
                        self.rect.right = p.rect.left
                    elif self.vel.x < 0:
                        self.rect.left = p.rect.right
                else:
                    if self.vel.y > 0:
                        self.rect.bottom = p.rect.top
                        self.vel.y = 0
                        self.on_ground = True
                    elif self.vel.y < 0:
                        self.rect.top = p.rect.bottom
                        self.vel.y = 0
        if direction == 'vertical' and self.vel.y != 0:
            self.on_ground = False

class Projectile(GameObject):
    def __init__(self, x, y, direction):
        super().__init__(x, y, 10, 5, (255, 165, 0))
        self.vel = 12 * direction
        self.damage = 25

    def update(self):
        self.rect.x += self.vel
        if self.rect.right < 0 or self.rect.left > LEVEL_WIDTH:
            self.kill()

class Enemy(GameObject):
    def __init__(self, x, y, is_boss=False, direction=-1):
        size = (60, 80) if is_boss else (30, 50)
        color = (50, 50, 50) if is_boss else (100, 100, 100)
        super().__init__(x, y, size[0], size[1], color)
        self.max_health = 150 if is_boss else 50
        self.health = self.max_health
        self.speed = 2
        self.direction = direction
        self.is_boss = is_boss
        self.active = True

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right < 0:
            self.rect.left = LEVEL_WIDTH
        elif self.rect.left > LEVEL_WIDTH:
            self.rect.right = 0

class Collectible(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20, (255, 255, 0))
        self.kind = 'health'

    def apply(self, player):
        player.health = min(player.max_health, player.health + 30)
        self.kill()

class Level:
    def __init__(self, num, all_sprites, platforms, enemies, collectibles):
        for i in range(0, LEVEL_WIDTH, 200):
            p = GameObject(i, SCREEN_HEIGHT - 40, 200, 40, (34, 139, 34))
            platforms.add(p);
            all_sprites.add(p)
        if num < 3:
            for i in range(3 * num):
                e = Enemy(400 + i * 200, SCREEN_HEIGHT - 100)
                enemies.add(e);
                all_sprites.add(e)
        else:
            boss = Enemy(LEVEL_WIDTH + 100, SCREEN_HEIGHT - 140, is_boss=True, direction=-1)
            enemies.add(boss);
            all_sprites.add(boss)
        for i in range(2):
            c = Collectible(300 + i * 600, SCREEN_HEIGHT - 120)
            collectibles.add(c);
            all_sprites.add(c)

class Game:
    def __init__(self):
        pygame.init()
        global screen
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Forest Guardian')
        self.clock = pygame.time.Clock()
        self.score = 0
        self.state = 'PLAY'
        self.camera_group = CameraGroup()
        self.reset()

    def reset(self):
        self.score = 0
        self.state = 'PLAY'
        self.camera_group.empty()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.player = Player(100, SCREEN_HEIGHT - 100)
        self.camera_group.add(self.player)
        self.projectiles = pygame.sprite.Group()
        self.level_no = 1
        self.boss_timer = BOSS_ALERT_DURATION * FPS
        self.load_level()

    def load_level(self):
        Level(self.level_no, self.camera_group, self.platforms, self.enemies, self.collectibles)

    def run(self):
        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f and self.state == 'PLAY':
                        offset = (self.player.rect.width // 2 + 5) * self.player.facing
                        proj = Projectile(self.player.rect.centerx + offset,
                                           self.player.rect.centery,
                                           self.player.facing)
                        self.camera_group.add(proj)
                        self.projectiles.add(proj)
                    if event.key == pygame.K_r and self.state == 'GAMEOVER':
                        self.reset()
            if self.state == 'PLAY':
                self.update()
            self.draw()

    def update(self):
        self.player.update(self.platforms)
        self.projectiles.update()
        self.enemies.update()
        for p in self.projectiles:
            hit = pygame.sprite.spritecollideany(p, self.enemies)
            if hit:
                hit.health -= p.damage
                p.kill()
                if hit.health <= 0:
                    hit.kill()
                    self.score += 200 if hit.is_boss else 50
        if pygame.sprite.spritecollideany(self.player, self.enemies):
            self.player.health -= 1
            if self.player.health <= 0:
                self.player.lives -= 1
                self.player.health = self.player.max_health
                if self.player.lives <= 0:
                    self.state = 'GAMEOVER'
        for c in pygame.sprite.spritecollide(self.player, self.collectibles, False):
            c.apply(self.player)
            self.score += 25
        if not any(not en.is_boss for en in self.enemies) and self.level_no < 3:
            self.level_no += 1
            self.load_level()
            self.player.rect.topleft = (100, SCREEN_HEIGHT - 100)
        if self.level_no == 3 and self.boss_timer > 0:
            self.boss_timer -= 1
        if self.level_no == 3 and not any(en.is_boss for en in self.enemies):
            self.state = 'GAMEOVER'

    def draw(self):
        screen.fill((135, 206, 235))
        if self.state == 'PLAY':
            if self.level_no == 3 and self.boss_timer > 0:
                f = pygame.font.SysFont(None, 50)
                txt = f.render('Boss incoming!', True, (255, 0, 0))
                rct = txt.get_rect(midtop=(SCREEN_WIDTH // 2, 10))
                screen.blit(txt, rct)
            self.camera_group.custom_draw(self.player)
            hud = pygame.font.SysFont(None, 30)
            screen.blit(hud.render(f'Score: {self.score}', True, (0, 0, 0)), (10, 10))
            screen.blit(hud.render(f'Lives: {self.player.lives}', True, (0, 0, 0)), (10, 40))
        else:
            f = pygame.font.SysFont(None, 60)
            txt = f.render('Game Over! Press R to Restart', True, (255, 0, 0))
            rct = txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(txt, rct)
        pygame.display.flip()

if __name__ == '__main__':
    Game().run()
