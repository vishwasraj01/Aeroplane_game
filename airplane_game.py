import pygame
import random
import sys
import os
import json
import math

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# High score file
HIGH_SCORE_FILE = "high_score.json"

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.life = 255

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 5
        self.size = max(0, self.size - 0.1)

    def draw(self, screen):
        if self.life > 0:
            alpha = min(255, self.life)
            color = (*self.color[:3], alpha)
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.size))

class Airplane(pygame.sprite.Sprite):
    def __init__(self, type="default"):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((50, 30), pygame.SRCALPHA)
        
        if type == "default":
            pygame.draw.polygon(self.image, BLUE, [(0, 15), (40, 0), (50, 15), (40, 30)])
            self.speed = 5
            self.health = 100
        elif type == "fast":
            pygame.draw.polygon(self.image, GREEN, [(0, 15), (40, 0), (50, 15), (40, 30)])
            self.speed = 7
            self.health = 80
        elif type == "tank":
            pygame.draw.polygon(self.image, RED, [(0, 15), (40, 0), (50, 15), (40, 30)])
            self.speed = 3
            self.health = 150
        
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 4
        self.rect.centery = SCREEN_HEIGHT // 2
        self.score = 0
        self.invincible = False
        self.invincible_timer = 0
        self.particles = []
        self.bullets = []
        self.shoot_timer = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

        # Update invincibility
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

        # Update particles
        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update()

        # Update bullets
        self.bullets = [b for b in self.bullets if b.life > 0]
        for bullet in self.bullets:
            bullet.update()

        # Shooting
        self.shoot_timer += 1
        if keys[pygame.K_SPACE] and self.shoot_timer >= 15:  # Shoot every 15 frames
            self.shoot()
            self.shoot_timer = 0

    def shoot(self):
        bullet = Bullet(self.rect.right, self.rect.centery)
        self.bullets.append(bullet)

    def draw_particles(self, screen):
        for particle in self.particles:
            particle.draw(screen)

    def draw_bullets(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)

    def add_particles(self, color):
        for _ in range(10):
            self.particles.append(Particle(self.rect.centerx, self.rect.centery, color))

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        self.life = 100  # Bullet lifetime in frames

    def update(self):
        self.x += self.speed
        self.life -= 1

    def draw(self, screen):
        if self.life > 0:
            pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), 3)

class Boss(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.circle(self.image, ORANGE, (50, 50), 50)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = SCREEN_HEIGHT // 2 - 50
        self.health = 200 + level * 50
        self.speed = 2
        self.move_direction = 1
        self.shoot_timer = 0
        self.bullets = []

    def update(self):
        # Move up and down
        self.rect.y += self.speed * self.move_direction
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.move_direction *= -1

        # Move left slowly
        self.rect.x -= 1

        # Shooting
        self.shoot_timer += 1
        if self.shoot_timer >= 60:  # Shoot every second
            self.shoot()
            self.shoot_timer = 0

        # Update bullets
        self.bullets = [b for b in self.bullets if b.life > 0]
        for bullet in self.bullets:
            bullet.update()

    def shoot(self):
        # Shoot in multiple directions
        for angle in range(0, 360, 45):
            bullet = BossBullet(self.rect.centerx, self.rect.centery, angle)
            self.bullets.append(bullet)

    def draw_bullets(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)

class BossBullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = math.radians(angle)
        self.speed = 5
        self.life = 100

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.life -= 1

    def draw(self, screen):
        if self.life > 0:
            pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 5)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (200, 200, 200), (20, 20), 20)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 40)
        self.speed = random.randint(3, 7) + level
        self.health = 20 + level * 5

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, type="health"):
        super().__init__()
        self.type = type
        if type == "health":
            color = GREEN
        elif type == "invincible":
            color = YELLOW
        elif type == "speed":
            color = PURPLE
        
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (10, 10), 10)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 20)
        self.speed = 4

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Airplane Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.airplane = Airplane("default")
        self.all_sprites.add(self.airplane)
        self.obstacle_timer = 0
        self.powerup_timer = 0
        self.font = pygame.font.Font(None, 36)
        self.high_score = self.load_high_score()
        self.level = 1
        self.level_up_score = 1000
        self.boss = None
        self.boss_active = False
        self.boss_spawn_score = 5000
        
        # Initialize sounds with error handling
        self.sounds_enabled = True
        try:
            # Create assets directory if it doesn't exist
            if not os.path.exists("assets"):
                os.makedirs("assets")
                print("Please run generate_sounds.py to create sound effects")
                self.sounds_enabled = False
            else:
                self.crash_sound = pygame.mixer.Sound(os.path.join("assets", "crash.wav"))
                self.powerup_sound = pygame.mixer.Sound(os.path.join("assets", "powerup.wav"))
                self.background_music = pygame.mixer.Sound(os.path.join("assets", "background.wav"))
                self.background_music.play(-1)
        except (FileNotFoundError, pygame.error) as e:
            print(f"Sound error: {e}")
            print("Game will run without sound effects")
            self.sounds_enabled = False

    def load_high_score(self):
        try:
            with open(HIGH_SCORE_FILE, 'r') as f:
                return json.load(f).get('high_score', 0)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0

    def save_high_score(self):
        with open(HIGH_SCORE_FILE, 'w') as f:
            json.dump({'high_score': self.high_score}, f)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                elif event.key == pygame.K_1 and not self.game_over:
                    self.change_airplane("default")
                elif event.key == pygame.K_2 and not self.game_over:
                    self.change_airplane("fast")
                elif event.key == pygame.K_3 and not self.game_over:
                    self.change_airplane("tank")

    def change_airplane(self, type):
        old_score = self.airplane.score
        old_health = self.airplane.health
        self.airplane.kill()
        self.airplane = Airplane(type)
        self.airplane.score = old_score
        self.airplane.health = old_health
        self.all_sprites.add(self.airplane)

    def spawn_obstacles(self):
        if not self.boss_active:
            self.obstacle_timer += 1
            if self.obstacle_timer >= max(30, 60 - self.level * 5):
                obstacle = Obstacle(self.level)
                self.all_sprites.add(obstacle)
                self.obstacles.add(obstacle)
                self.obstacle_timer = 0

    def spawn_powerups(self):
        self.powerup_timer += 1
        if self.powerup_timer >= 300:
            powerup_type = random.choice(["health", "invincible", "speed"])
            powerup = PowerUp(powerup_type)
            self.all_sprites.add(powerup)
            self.powerups.add(powerup)
            self.powerup_timer = 0

    def check_boss_spawn(self):
        if not self.boss_active and self.airplane.score >= self.boss_spawn_score:
            self.boss = Boss(self.level)
            self.all_sprites.add(self.boss)
            self.boss_active = True
            self.boss_spawn_score += 5000

    def play_sound(self, sound):
        if self.sounds_enabled:
            try:
                sound.play()
            except:
                pass

    def check_collisions(self):
        if not self.airplane.invincible:
            # Check obstacle collisions
            if pygame.sprite.spritecollide(self.airplane, self.obstacles, True):
                self.airplane.health -= 20
                self.play_sound(self.crash_sound)
                self.airplane.add_particles(RED)
                if self.airplane.health <= 0:
                    self.game_over = True
                    if self.airplane.score > self.high_score:
                        self.high_score = self.airplane.score
                        self.save_high_score()

            # Check boss collisions
            if self.boss_active and pygame.sprite.collide_rect(self.airplane, self.boss):
                self.airplane.health -= 40
                self.play_sound(self.crash_sound)
                self.airplane.add_particles(RED)
                if self.airplane.health <= 0:
                    self.game_over = True
                    if self.airplane.score > self.high_score:
                        self.high_score = self.airplane.score
                        self.save_high_score()

            # Check boss bullet collisions
            if self.boss_active:
                for bullet in self.boss.bullets:
                    if (self.airplane.rect.collidepoint(bullet.x, bullet.y) and 
                        bullet.life > 0):
                        self.airplane.health -= 10
                        self.play_sound(self.crash_sound)
                        self.airplane.add_particles(RED)
                        bullet.life = 0
                        if self.airplane.health <= 0:
                            self.game_over = True
                            if self.airplane.score > self.high_score:
                                self.high_score = self.airplane.score
                                self.save_high_score()

        # Check powerup collisions
        powerup_collisions = pygame.sprite.spritecollide(self.airplane, self.powerups, True)
        for powerup in powerup_collisions:
            if powerup.type == "health":
                self.airplane.health = min(100, self.airplane.health + 20)
                self.airplane.add_particles(GREEN)
            elif powerup.type == "invincible":
                self.airplane.invincible = True
                self.airplane.invincible_timer = 180
                self.airplane.add_particles(YELLOW)
            elif powerup.type == "speed":
                self.airplane.speed = 8
                pygame.time.set_timer(pygame.USEREVENT, 5000)
                self.airplane.add_particles(PURPLE)
            self.play_sound(self.powerup_sound)

        # Check bullet collisions with boss
        if self.boss_active:
            for bullet in self.airplane.bullets:
                if (self.boss.rect.collidepoint(bullet.x, bullet.y) and 
                    bullet.life > 0):
                    self.boss.health -= 10
                    bullet.life = 0
                    if self.boss.health <= 0:
                        self.boss.kill()
                        self.boss_active = False
                        self.airplane.score += 1000
                        self.airplane.add_particles(WHITE)

    def check_level_up(self):
        if self.airplane.score >= self.level_up_score:
            self.level += 1
            self.level_up_score += 1000
            self.airplane.add_particles(WHITE)

    def reset_game(self):
        self.game_over = False
        self.airplane.health = 100
        self.airplane.score = 0
        self.airplane.rect.centerx = SCREEN_WIDTH // 4
        self.airplane.rect.centery = SCREEN_HEIGHT // 2
        self.airplane.speed = 5
        self.level = 1
        self.level_up_score = 1000
        self.boss_active = False
        self.boss_spawn_score = 5000
        if self.boss:
            self.boss.kill()
        for obstacle in self.obstacles:
            obstacle.kill()
        for powerup in self.powerups:
            powerup.kill()

    def update(self):
        if not self.game_over:
            self.all_sprites.update()
            self.spawn_obstacles()
            self.spawn_powerups()
            self.check_boss_spawn()
            self.check_collisions()
            self.check_level_up()
            self.airplane.score += 1

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw background with parallax effect
        for y in range(SCREEN_HEIGHT):
            color = (0, 0, max(0, min(255, y // 2)))
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
        
        # Draw stars
        for _ in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            brightness = random.randint(100, 255)
            pygame.draw.circle(self.screen, (brightness, brightness, brightness), (x, y), 1)
        
        self.all_sprites.draw(self.screen)
        self.airplane.draw_particles(self.screen)
        self.airplane.draw_bullets(self.screen)
        if self.boss_active:
            self.boss.draw_bullets(self.screen)
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.airplane.score}", True, WHITE)
        health_text = self.font.render(f"Health: {self.airplane.health}", True, WHITE)
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        airplane_type_text = self.font.render(f"Airplane: {self.airplane.type}", True, WHITE)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(health_text, (10, 50))
        self.screen.blit(high_score_text, (10, 90))
        self.screen.blit(level_text, (10, 130))
        self.screen.blit(airplane_type_text, (10, 170))

        if self.boss_active:
            boss_health_text = self.font.render(f"Boss Health: {self.boss.health}", True, ORANGE)
            self.screen.blit(boss_health_text, (SCREEN_WIDTH - 200, 10))

        if self.airplane.invincible:
            invincible_text = self.font.render("INVINCIBLE!", True, YELLOW)
            self.screen.blit(invincible_text, (SCREEN_WIDTH - 150, 50))

        if self.game_over:
            game_over_text = self.font.render("GAME OVER - Press R to Restart", True, WHITE)
            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2))

        # Draw controls help
        controls_text = self.font.render("Controls: 1-Default 2-Fast 3-Tank SPACE-Shoot", True, WHITE)
        self.screen.blit(controls_text, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT - 30))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit() 