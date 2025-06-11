

import pygame
import sys
import random

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
LIGHT_BLUE = (173, 216, 230)  # Sky color

# Player properties
PLAYER_ACC = 0.7
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.7
PLAYER_JUMP_STRENGTH = 18
PLAYER_MAX_FALL_SPEED = 15


# --- Sprite Classes ---

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            # Load player image with transparency handling
            loaded_image = pygame.image.load(
                "./assets/mario sprite.png").convert_alpha()
            self.image = pygame.transform.scale(loaded_image, (35, 35))
        except pygame.error as e:
            print(
                f"Warning: Could not load player image './assets/mario sprite.png': {e}")
            print("Falling back to default RED block for player.")
            # Fallback size from original code
            self.image = pygame.Surface((30, 40))
            self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.lives = 3
        self.score = 0
        self.invincible_timer = 0

    def jump(self):
        if self.on_ground:
            self.vel.y = -PLAYER_JUMP_STRENGTH
            self.on_ground = False

    def update(self, platforms):
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            if self.invincible_timer % 10 < 5:  # Flashing effect
                self.image.set_alpha(128)
            else:
                self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)

        self.acc = pygame.math.Vector2(0, PLAYER_GRAVITY)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x = PLAYER_ACC

        # Apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # Equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:  # Stop small movements
            self.vel.x = 0

        # Max fall speed
        if self.vel.y > PLAYER_MAX_FALL_SPEED:
            self.vel.y = PLAYER_MAX_FALL_SPEED

        self.pos += self.vel + 0.5 * self.acc

        # Collision handling
        self.rect.x = self.pos.x
        self.collide_with_platforms(platforms, 'horizontal')

        self.rect.y = self.pos.y
        self.on_ground = False  # Assume not on ground until vertical collision check
        self.collide_with_platforms(platforms, 'vertical')

        # Screen boundaries
        if self.pos.x > SCREEN_WIDTH - self.rect.width:
            self.pos.x = SCREEN_WIDTH - self.rect.width
            self.vel.x = 0
        if self.pos.x < 0:
            self.pos.x = 0
            self.vel.x = 0

        # Fell off screen
        if self.rect.top > SCREEN_HEIGHT:
            return self.lose_life()
        return None

    def collide_with_platforms(self, platforms, direction):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            if direction == 'horizontal':
                if self.vel.x > 0:  # Moving right
                    self.rect.right = hits[0].rect.left
                if self.vel.x < 0:  # Moving left
                    self.rect.left = hits[0].rect.right
                self.pos.x = self.rect.x
                self.vel.x = 0

            if direction == 'vertical':
                if self.vel.y > 0:  # Moving down
                    self.rect.bottom = hits[0].rect.top
                    self.on_ground = True
                if self.vel.y < 0:  # Moving up
                    self.rect.top = hits[0].rect.bottom
                self.pos.y = self.rect.y
                self.vel.y = 0

    def lose_life(self):
        if self.invincible_timer == 0:  # Only lose life if not invincible
            self.lives -= 1
            self.invincible_timer = FPS * 2  # 2 seconds of invincibility
            # Reset player position to current level's start
            # Access global current_level_index
            current_level_data = LEVELS[current_level_index]
            self.pos.x, self.pos.y = current_level_data["player_start"]
            self.rect.topleft = self.pos
            self.vel = pygame.math.Vector2(0, 0)  # Reset velocity
            if self.lives <= 0:
                return "game_over"
        return None

    def hit_enemy(self, enemy_rect):
        # Check if player is stomping on enemy (coming from above and landing on top)
        if self.vel.y > 0 and self.rect.bottom < enemy_rect.centery + 5:  # Small tolerance for stomp
            self.vel.y = -PLAYER_JUMP_STRENGTH / 2.5  # Small bounce after stomp
            return "stomp"
        else:  # Collided from side or bottom
            return self.lose_life()


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=BROWN):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, move_range_x=50):
        super().__init__()
        try:
            # Load enemy image with transparency handling
            original_turtle_image = pygame.image.load(
                "./assets/turtle for mario game.png").convert_alpha()
            # Scale the image
            self.image = pygame.transform.scale(
                original_turtle_image, (30, 30))
        except pygame.error as e:
            print(
                f"Warning: Could not load enemy image './assets/turtle for mario game.png': {e}")
            print("Falling back to default GREEN block for enemy.")
            # Fallback to a colored square if image loading fails
            self.image = pygame.Surface((25, 25))
            self.image.fill(GREEN)

        self.rect = self.image.get_rect()  # THIS IS KEY
        self.rect.topleft = (x, y)

        self.initial_x_pos = x  # The x-coordinate where the enemy initially spawns
        self.move_range_x = move_range_x  # How far to move left/right from initial_x_pos
        self.direction = 1  # 1 for right, -1 for left
        self.speed = 1

    def update(self, platforms):
        self.rect.x += self.speed * self.direction

        # Boundary check for patrol movement based on initial_x_pos and move_range_x
        if self.move_range_x > 0:  # Only patrol if a range is given
            if self.direction == 1:  # Moving right
                # Check if current topleft x exceeds the right patrol boundary
                if self.rect.x >= self.initial_x_pos + self.move_range_x:
                    self.rect.x = self.initial_x_pos + self.move_range_x  # Snap to boundary
                    self.direction = -1
            elif self.direction == -1:  # Moving left
                # Check if current topleft x is less than the left patrol boundary
                if self.rect.x <= self.initial_x_pos - self.move_range_x:
                    self.rect.x = self.initial_x_pos - self.move_range_x  # Snap to boundary
                    self.direction = 1

        # Collision with platforms (to turn around if it hits a wall)
        hit_platforms = pygame.sprite.spritecollide(self, platforms, False)
        for platform in hit_platforms:
            if self.direction > 0:  # Moving right when hit
                self.rect.right = platform.rect.left
            elif self.direction < 0:  # Moving left when hit
                self.rect.left = platform.rect.right
            self.direction *= -1  # Reverse direction upon hitting a platform
            break  # Handle only one platform collision per frame


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


# --- Level Data (12 Levels) ---
LEVELS = [
    {  # Level 1
        "player_start": (50, SCREEN_HEIGHT - 100),
        "platforms": [
            (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH,
             40), (200, SCREEN_HEIGHT - 150, 100, 20),
            (400, SCREEN_HEIGHT - 250, 100, 20), (150, SCREEN_HEIGHT - 350, 150, 20),
        ],
        "enemies": [(300, SCREEN_HEIGHT - 70, 50)],  # x, y, move_range_x
        "coins": [(220, SCREEN_HEIGHT - 180), (420, SCREEN_HEIGHT - 280), (170, SCREEN_HEIGHT - 380)],
        "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
    },
    {  # Level 2
        "player_start": (50, 100),
        "platforms": [
            (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40), (0, 150, 100, 20),
            (150, 250, 100, 20), (300, 350, 100, 20),
            (500, 250, 80, 20), (650, 150, 80, 20),
        ],
        "enemies": [(400, SCREEN_HEIGHT - 70, 80), (200, 220, 30)],
        "coins": [(170, 220), (320, 320), (520, 220), (670, 120)],
        "goal": (SCREEN_WIDTH - 80, 100)
    },
    {  # Level 3 - More verticality
        "player_start": (50, SCREEN_HEIGHT - 100),
        "platforms": [
            (0, SCREEN_HEIGHT - 40, 200, 40), (SCREEN_WIDTH -
                                               200, SCREEN_HEIGHT - 40, 200, 40),
            (250, SCREEN_HEIGHT - 120, 50, 20), (350, SCREEN_HEIGHT - 200, 50, 20),
            (450, SCREEN_HEIGHT - 280, 50, 20), (550, SCREEN_HEIGHT - 200, 50, 20),
            (650, SCREEN_HEIGHT - 120, 50, 20),
        ],
        # move_range_x = 0 means it turns at walls
        "enemies": [(470, SCREEN_HEIGHT - 310, 20)],
        "coins": [(260, SCREEN_HEIGHT - 150), (360, SCREEN_HEIGHT - 230), (560, SCREEN_HEIGHT - 230)],
        "goal": (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 90)
    },
    {  # Level 4 - Gaps
        "player_start": (50, SCREEN_HEIGHT - 100),
        "platforms": [
            (0, SCREEN_HEIGHT - 40, 150, 40), (250, SCREEN_HEIGHT - 60, 100, 20),
            (450, SCREEN_HEIGHT - 80, 100, 20), (650, SCREEN_HEIGHT - 40, 150, 40),
        ],
        "enemies": [(280, SCREEN_HEIGHT - 90, 30), (480, SCREEN_HEIGHT - 110, 30)],
        "coins": [(100, SCREEN_HEIGHT - 70), (270, SCREEN_HEIGHT - 90), (470, SCREEN_HEIGHT - 110)],
        "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
    },
    {  # Level 5 - More enemies
        "player_start": (50, SCREEN_HEIGHT - 100),
        "platforms": [
            (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH,
             40), (100, SCREEN_HEIGHT - 140, 80, 20),
            (300, SCREEN_HEIGHT - 180, 150, 20), (550, SCREEN_HEIGHT - 140, 80, 20),
        ],
        "enemies": [
            (200, SCREEN_HEIGHT - 70, 50), (350, SCREEN_HEIGHT -
                                            210, 60), (500, SCREEN_HEIGHT - 70, 50),
        ],
        "coins": [(120, SCREEN_HEIGHT - 170), (370, SCREEN_HEIGHT - 210), (570, SCREEN_HEIGHT - 170)],
        "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
    },
    {  # Level 6 - Tricky jumps
        "player_start": (30, 100),
        "platforms": [
            (0, 150, 80, 20), (200, 200, 50, 20), (350, 150, 50, 20),(475,50, 50, 20),
            (220, 350, 50, 20), (50, 450, SCREEN_WIDTH - 100, 20),
            (SCREEN_WIDTH - 100, 100, 50, 20)
        ],
        "enemies": [(280, 420, 100), (450, 420, 100)],
        "coins": [(210, 170), (360, 120), (210, 320), (SCREEN_WIDTH - 80, 70)],
        "goal": (SCREEN_WIDTH - 80, 50)
    },
    {  # Level 7 - Final Challenge (Original)
        "player_start": (50, SCREEN_HEIGHT - 100),
        "platforms": [
            (0, SCREEN_HEIGHT - 40, 100, 40), (150, SCREEN_HEIGHT - 80, 50, 20),
            (250, SCREEN_HEIGHT - 120, 50, 20), (350, SCREEN_HEIGHT - 160, 50, 20),
            (450, SCREEN_HEIGHT - 120, 50, 20), (550, SCREEN_HEIGHT - 80, 50, 20),
            (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 40, 100, 40),
        ],
        "enemies": [
            (80, SCREEN_HEIGHT - 70, 20), (170, SCREEN_HEIGHT - 110, 20),
            (270, SCREEN_HEIGHT - 150, 20), (470, SCREEN_HEIGHT - 150, 20),
            (570, SCREEN_HEIGHT - 110, 20), (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 70, 20),
        ],
        "coins": [(160, SCREEN_HEIGHT - 110), (360, SCREEN_HEIGHT - 190), (560, SCREEN_HEIGHT - 110)],
        "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
    },
    {  # Level 8: "The Ascent"
        "player_start": (50, SCREEN_HEIGHT - 100),
        "platforms": [
            (0, SCREEN_HEIGHT - 40, 150, 40),
            (100, SCREEN_HEIGHT - 140, 70, 20), (50, SCREEN_HEIGHT - 240, 70, 20),
            (150, SCREEN_HEIGHT - 340, 70, 20), (250,
                                                 SCREEN_HEIGHT - 440, 250, 20),
            (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, 100, 20),
        ],
        "enemies": [(300, SCREEN_HEIGHT - 470, 100), (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 130, 20)],
        "coins": [(120, SCREEN_HEIGHT - 170), (70, SCREEN_HEIGHT - 270), (170, SCREEN_HEIGHT - 370),
                  (400, SCREEN_HEIGHT - 470)],
        "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 150)
    },
    {  # Level 9: "Corridor Run"
        "player_start": (30, SCREEN_HEIGHT - 80),
        "platforms": [
            (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
            (150, SCREEN_HEIGHT - 120, 80, 20), (300, SCREEN_HEIGHT - 120, 80, 20),
            (450, SCREEN_HEIGHT - 120, 80, 20), (600, SCREEN_HEIGHT - 120, 80, 20),
        ],
        "enemies": [
            (100, SCREEN_HEIGHT - 70, 30), (250, SCREEN_HEIGHT - 70, 30),
            (400, SCREEN_HEIGHT - 70, 30), (550, SCREEN_HEIGHT - 70, 30),
            (350, SCREEN_HEIGHT - 150, 30)
        ],
        "coins": [(170, SCREEN_HEIGHT - 150), (320, SCREEN_HEIGHT - 150), (470, SCREEN_HEIGHT - 150),
                  (620, SCREEN_HEIGHT - 150)],
        "goal": (SCREEN_WIDTH - 60, SCREEN_HEIGHT - 90)
    },
    {  # Level 10: "Maze of Platforms"
        "player_start": (50, 50),
        "platforms": [
            (0, 100, 100, 20), (150, 180, 100, 20), (0, 260, 100, 20),
            (150, 340, 100, 20), (300, 100, 100, 20), (450, 180, 100, 20),
            (300, 260, 100, 20), (600, 100, SCREEN_WIDTH - 600, 20),
            (0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 40)
        ],
        "enemies": [(180, 150, 30), (50, 240, 0), (480, 150, 30)],
        "coins": [(320, 230), (70, 70), (320, 70), (620, 70)],
        "goal": (SCREEN_WIDTH - 80, 50)
    },
    {  # Level 11: "Enemy Gauntlet"
        "player_start": (50, SCREEN_HEIGHT - 100),
        "platforms": [
            (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
            (100, SCREEN_HEIGHT - 150, 80, 20), (250, SCREEN_HEIGHT - 200, 300, 20),
            (SCREEN_WIDTH - 180, SCREEN_HEIGHT - 150, 80, 20),
        ],
        "enemies": [
            (150, SCREEN_HEIGHT - 70, 50), (250, SCREEN_HEIGHT - 70, 50),
            (350, SCREEN_HEIGHT - 70, 50), (450, SCREEN_HEIGHT - 70, 50),
            (300, SCREEN_HEIGHT - 230, 80), (450, SCREEN_HEIGHT - 230, 80),
            (120, SCREEN_HEIGHT - 180, 50), (SCREEN_WIDTH - 160, SCREEN_HEIGHT - 180, 50)
        ],
        "coins": [(130, SCREEN_HEIGHT - 180), (390, SCREEN_HEIGHT - 180), (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 180)],
        "goal": (SCREEN_WIDTH / 2 - 15, SCREEN_HEIGHT - 270)
    },
    {  # Level 12: "Final Leap"
        "player_start": (30, SCREEN_HEIGHT - 100),
        "platforms": [
            (0, SCREEN_HEIGHT - 40, 100, 40), (200, SCREEN_HEIGHT - 80, 50, 20),
            (350, SCREEN_HEIGHT - 120, 50, 20), (500, SCREEN_HEIGHT - 160, 50, 20),
            (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 40, 100, 40),
            (150, SCREEN_HEIGHT - 200, 20, 20), (600, SCREEN_HEIGHT - 250, 20, 20),
        ],
        "enemies": [
            (215, SCREEN_HEIGHT - 110, 20), (365, SCREEN_HEIGHT - 150, 20),
            # (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 70, 50)
        ],
        "coins": [
            (215, SCREEN_HEIGHT - 110), (365,
                                         SCREEN_HEIGHT - 150), (515, SCREEN_HEIGHT - 190),
            (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 70)
        ],
        "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
    }
]


# --- Game Functions ---
def load_level_sprites(level_data):
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()

    for p_data in level_data["platforms"]:
        platforms.add(Platform(*p_data))
    for e_data in level_data["enemies"]:
        enemies.add(Enemy(*e_data))
    for c_data in level_data["coins"]:
        coins.add(Coin(*c_data))

    goal = Goal(*level_data["goal"])
    return platforms, enemies, coins, goal


def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)  # Use default system font
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def show_message_screen(screen, clock, message, sub_message="Press SPACE to continue"):
    screen.fill(LIGHT_BLUE)
    draw_text(screen, message, 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, BLACK)
    draw_text(screen, sub_message, 32, SCREEN_WIDTH /
              2, SCREEN_HEIGHT / 2, BLACK)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False
                # Allow ESC to quit from game over/win screens
                if event.key == pygame.K_ESCAPE and (
                        "Game Over" in message or "You Win" in message or "Simple Platformer" in message):
                    pygame.quit()
                    sys.exit()


# --- Game Initialization ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Mario-like Game - 12 Levels")
clock = pygame.time.Clock()

# --- Game Variables ---
current_level_index = 0
game_state = "start_screen"
player = None  # Will be initialized when game starts
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()
goal = None

game_player_lives = 3  # To hold lives/score data between states
game_player_score = 0

# --- Game Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "playing" and player:  # Ensure player exists before processing jump
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    player.jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                if game_state == "start_screen":
                    game_state = "playing"
                    current_level_index = 0



                    game_player_lives = 3  # Reset for new game
                    game_player_score = 0

                    # Initialize player for the first level
                    player = Player(
                        *LEVELS[current_level_index]["player_start"])
                    player.lives = game_player_lives
                    player.score = game_player_score

                    platforms, enemies, coins, goal = load_level_sprites(
                        LEVELS[current_level_index])
                    all_sprites.empty()  # Clear previous sprites
                    all_sprites.add(player, platforms, enemies, coins, goal)

                elif game_state == "game_over" or game_state == "game_won":
                    # Restart game from level 1
                    game_state = "playing"
                    current_level_index = 0

                    game_player_lives = 3
                    game_player_score = 0

                    player = Player(
                        *LEVELS[current_level_index]["player_start"])
                    player.lives = game_player_lives
                    player.score = game_player_score

                    platforms, enemies, coins, goal = load_level_sprites(
                        LEVELS[current_level_index])
                    all_sprites.empty()
                    all_sprites.add(player, platforms, enemies, coins, goal)

            if event.key == pygame.K_ESCAPE:
                # Allow ESC to quit from start, game over, or game won screens
                if game_state == "start_screen" or game_state == "game_over" or game_state == "game_won":
                    running = False

    # --- Game State Logic & Drawing ---
    if game_state == "start_screen":
        screen.fill(LIGHT_BLUE)
        draw_text(screen, "Simple Platformer", 64,
                  SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, BLACK)
        draw_text(screen, "Press SPACE to Start", 32,
                  SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, BLACK)
        draw_text(screen, "Press ESC to Quit", 22,
                  SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.75, BLACK)

    elif game_state == "playing":
        if not player:  # Should not happen if logic is correct, but a safeguard
            game_state = "start_screen"
            continue

        # Update player and check for state changes (e.g., fell off screen)
        player_state_change = player.update(platforms)
        if player_state_change == "game_over":
            game_player_lives = player.lives  # Persist final stats
            game_player_score = player.score
            game_state = "game_over"
            continue  # Skip rest of playing logic for this frame

        # Update enemies
        enemies.update(platforms)

        # Check for coin collection
        coin_hits = pygame.sprite.spritecollide(
            player, coins, True)  # True to remove coin
        for coin in coin_hits:
            player.score += 10
        game_player_score = player.score  # Keep game_player_score updated

        # Check for enemy collisions
        if player.invincible_timer == 0:  # Only check if not invincible
            enemy_hits = pygame.sprite.spritecollide(
                player, enemies, False)  # False: don't kill enemy yet
            for enemy in enemy_hits:
                # Player handles hit logic
                result = player.hit_enemy(enemy.rect)
                if result == "stomp":
                    enemy.kill()  # Remove stomped enemy
                    player.score += 50
                    game_player_score = player.score
                elif result == "game_over":
                    game_player_lives = player.lives
                    game_player_score = player.score
                    game_state = "game_over"
                    break  # Exit enemy collision loop
            if game_state == "game_over":
                continue  # Skip to next frame if game over

        # Check for goal collision
        if goal and pygame.sprite.collide_rect(player, goal):
            game_player_lives = player.lives  # Persist current stats for message screen
            game_player_score = player.score
            game_state = "level_complete"
            # current_level_index still points to the level just finished
            # The 'level_complete' state block will handle the message and transition
            # continue # Let the next frame handle the level_complete state

        # --- Draw everything for "playing" state ---
        screen.fill(LIGHT_BLUE)  # Background
        # Draw all sprites (player, platforms, enemies, coins, goal)
        all_sprites.draw(screen)

        # Draw HUD
        draw_text(screen, f"Score: {game_player_score}",
                  30, SCREEN_WIDTH / 2, 10, BLACK)
        draw_text(
            screen, f"Lives: {player.lives if player else game_player_lives}", 30, 70, 10, BLACK)
        draw_text(
            screen, f"Level: {current_level_index + 1}", 30, SCREEN_WIDTH - 70, 10, BLACK)

    elif game_state == "level_complete":
        # Display message for the level just completed
        # Note: game_player_lives and game_player_score were updated before transitioning here
        show_message_screen(screen, clock, f"Level {current_level_index + 1} Complete!",
                            f"Score: {game_player_score} Lives: {player.lives}\nPress SPACE for Next Level")

        # After show_message_screen returns (SPACE was pressed):
        current_level_index += 1
        if current_level_index < len(LEVELS):
            game_state = "playing"
            # Reset player for the new level, keeping current lives and score
            player.pos = pygame.math.Vector2(
                *LEVELS[current_level_index]["player_start"])
            player.rect.topleft = player.pos
            player.vel = pygame.math.Vector2(0, 0)
            player.on_ground = False
            player.invincible_timer = 0  # Reset invincibility

            platforms, enemies, coins, goal = load_level_sprites(
                LEVELS[current_level_index])
            all_sprites.empty()
            all_sprites.add(player, platforms, enemies, coins, goal)
        else:
            game_state = "game_won"  # All levels completed

    elif game_state == "game_over":
        show_message_screen(screen, clock, "Game Over!",
                            f"Final Score: {game_player_score}\nPress SPACE to Restart or ESC to Quit")
        # SPACE key in event loop will reset to "start_screen" then "playing"

    elif game_state == "game_won":
        show_message_screen(screen, clock, "You Win! All Levels Cleared!",
                            f"Final Score: {game_player_score}\nPress SPACE to Restart or ESC to Quit")
        # SPACE key in event loop will reset to "start_screen" then "playing"

    pygame.display.flip()  # Update the full screen
    clock.tick(FPS)  # Control game speed

pygame.quit()
sys.exit()
