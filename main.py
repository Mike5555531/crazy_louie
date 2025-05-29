# import pygame
# import sys
# import random
#
# # --- Constants ---
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 600
# FPS = 60
#
# # Colors
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# RED = (255, 0, 0)
# GREEN = (0, 255, 0)
# BLUE = (0, 0, 255)
# YELLOW = (255, 255, 0)
# BROWN = (139, 69, 19)
# LIGHT_BLUE = (173, 216, 230)  # Sky color
#
# # Player properties
# PLAYER_ACC = 0.7
# PLAYER_FRICTION = -0.12
# PLAYER_GRAVITY = 0.7
# PLAYER_JUMP_STRENGTH = 18
# PLAYER_MAX_FALL_SPEED = 15
#
#
# # --- Sprite Classes ---
#
# class Player(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         self.image = pygame.Surface((30, 40))
#         self.image.fill(RED)
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#
#         self.pos = pygame.math.Vector2(x, y)
#         self.vel = pygame.math.Vector2(0, 0)
#         self.acc = pygame.math.Vector2(0, 0)
#         self.on_ground = False
#         self.lives = 3
#         self.score = 0
#         self.invincible_timer = 0  # Timer for invincibility after getting hit
#
#     def jump(self):
#         if self.on_ground:
#             self.vel.y = -PLAYER_JUMP_STRENGTH
#             self.on_ground = False
#
#     def update(self, platforms):
#         if self.invincible_timer > 0:
#             self.invincible_timer -= 1
#             # Flicker effect for invincibility
#             if self.invincible_timer % 10 < 5:
#                 self.image.set_alpha(128)
#             else:
#                 self.image.set_alpha(255)
#         else:
#             self.image.set_alpha(255)
#
#         # Movement
#         self.acc = pygame.math.Vector2(0, PLAYER_GRAVITY)
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_LEFT] or keys[pygame.K_a]:
#             self.acc.x = -PLAYER_ACC
#         if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
#             self.acc.x = PLAYER_ACC
#
#         # Apply friction
#         self.acc.x += self.vel.x * PLAYER_FRICTION
#         # Equations of motion
#         self.vel += self.acc
#         if abs(self.vel.x) < 0.1:  # Stop if velocity is too small
#             self.vel.x = 0
#
#         # Cap fall speed
#         if self.vel.y > PLAYER_MAX_FALL_SPEED:
#             self.vel.y = PLAYER_MAX_FALL_SPEED
#
#         self.pos += self.vel + 0.5 * self.acc
#
#         # Collision detection (horizontal)
#         self.rect.x = self.pos.x
#         self.collide_with_platforms(platforms, 'horizontal')
#
#         # Collision detection (vertical)
#         self.rect.y = self.pos.y
#         self.on_ground = False  # Assume not on ground until proven
#         self.collide_with_platforms(platforms, 'vertical')
#
#         # Screen bounds (simple)
#         if self.pos.x > SCREEN_WIDTH - self.rect.width:
#             self.pos.x = SCREEN_WIDTH - self.rect.width
#             self.vel.x = 0
#         if self.pos.x < 0:
#             self.pos.x = 0
#             self.vel.x = 0
#
#         # Fall off screen
#         if self.rect.top > SCREEN_HEIGHT:
#             self.lose_life()
#
#     def collide_with_platforms(self, platforms, direction):
#         hits = pygame.sprite.spritecollide(self, platforms, False)
#         if hits:
#             if direction == 'horizontal':
#                 if self.vel.x > 0:  # Moving right
#                     self.rect.right = hits[0].rect.left
#                 if self.vel.x < 0:  # Moving left
#                     self.rect.left = hits[0].rect.right
#                 self.pos.x = self.rect.x
#                 self.vel.x = 0
#
#             if direction == 'vertical':
#                 if self.vel.y > 0:  # Moving down
#                     self.rect.bottom = hits[0].rect.top
#                     self.on_ground = True
#                 if self.vel.y < 0:  # Moving up
#                     self.rect.top = hits[0].rect.bottom
#                 self.pos.y = self.rect.y
#                 self.vel.y = 0
#
#     def lose_life(self):
#         if self.invincible_timer == 0:  # Only lose life if not invincible
#             self.lives -= 1
#             self.invincible_timer = FPS * 2  # 2 seconds of invincibility
#             # Reset position (or to a checkpoint if you implement that)
#             self.pos.x, self.pos.y = 100, SCREEN_HEIGHT - 100  # Example reset
#             self.vel = pygame.math.Vector2(0, 0)
#             if self.lives <= 0:
#                 return "game_over"
#         return None  # No state change if invincible or still has lives
#
#     def hit_enemy(self, enemy_rect):
#         # Basic "stomp" check (player must be above and falling)
#         if self.vel.y > 0 and self.rect.bottom < enemy_rect.centery:
#             self.vel.y = -PLAYER_JUMP_STRENGTH / 2  # Small bounce
#             return "stomp"
#         else:
#             return self.lose_life()  # Player gets hit
#
#
# class Platform(pygame.sprite.Sprite):
#     def __init__(self, x, y, width, height, color=BROWN):
#         super().__init__()
#         self.image = pygame.Surface((width, height))
#         self.image.fill(color)
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#
#
# class Enemy(pygame.sprite.Sprite):
#     def __init__(self, x, y, move_range_x=50):
#         super().__init__()
#         self.image = pygame.Surface((25, 25))
#         self.image.fill(GREEN)  # Simple enemy color
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#         self.start_x = x
#         self.move_range_x = move_range_x
#         self.direction = 1  # 1 for right, -1 for left
#         self.speed = 1
#
#     def update(self, platforms):
#         self.rect.x += self.speed * self.direction
#         if self.rect.x > self.start_x + self.move_range_x or self.rect.x < self.start_x - self.move_range_x:
#             self.direction *= -1
#
#         # Basic collision with platforms to prevent falling through (very simple)
#         # For more robust enemy platform interaction, you'd need similar gravity/collision as player
#         hit_platforms = pygame.sprite.spritecollide(self, platforms, False)
#         for platform in hit_platforms:
#             if self.direction > 0:  # Moving right
#                 self.rect.right = platform.rect.left
#             elif self.direction < 0:  # Moving left
#                 self.rect.left = platform.rect.right
#             self.direction *= -1  # Turn around
#             break
#
#
# class Coin(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         self.image = pygame.Surface((15, 15))
#         self.image.fill(YELLOW)
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#
#
# class Goal(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         self.image = pygame.Surface((30, 50))
#         self.image.fill(BLUE)  # Goal flag pole
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#
#
# # --- Level Data ---
# # Each level is a dictionary containing lists of tuples for object creation
# # Format: (x, y, width, height) for platforms, (x, y) for others
# # Player start: (x,y)
# # Goal: (x,y)
#
# LEVELS = [
#     {  # Level 1
#         "player_start": (50, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),  # Ground
#             (200, SCREEN_HEIGHT - 150, 100, 20),
#             (400, SCREEN_HEIGHT - 250, 100, 20),
#             (150, SCREEN_HEIGHT - 350, 150, 20),
#         ],
#         "enemies": [(300, SCREEN_HEIGHT - 65, 50)],
#         "coins": [(220, SCREEN_HEIGHT - 180), (420, SCREEN_HEIGHT - 280), (170, SCREEN_HEIGHT - 380)],
#         "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
#     },
#     {  # Level 2
#         "player_start": (50, 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),  # Ground
#             (0, 150, 100, 20),
#             (150, 250, 100, 20),
#             (300, 350, 100, 20),
#             (500, 250, 80, 20),
#             (650, 150, 80, 20),
#         ],
#         "enemies": [(400, SCREEN_HEIGHT - 65, 80), (200, 225, 30)],
#         "coins": [(170, 220), (320, 320), (520, 220), (670, 120)],
#         "goal": (SCREEN_WIDTH - 80, 100)
#     },
#     {  # Level 3 - More verticality
#         "player_start": (50, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, 200, 40),  # Start ground
#             (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 40, 200, 40),  # End ground
#             (250, SCREEN_HEIGHT - 120, 50, 20),
#             (350, SCREEN_HEIGHT - 200, 50, 20),
#             (450, SCREEN_HEIGHT - 280, 50, 20),  # Highest
#             (550, SCREEN_HEIGHT - 200, 50, 20),
#             (650, SCREEN_HEIGHT - 120, 50, 20),
#         ],
#         "enemies": [(450, SCREEN_HEIGHT - 305, 0)],  # Stationary enemy
#         "coins": [(260, SCREEN_HEIGHT - 150), (360, SCREEN_HEIGHT - 230), (560, SCREEN_HEIGHT - 230)],
#         "goal": (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 90)
#     },
#     {  # Level 4 - Gaps
#         "player_start": (50, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, 150, 40),
#             (250, SCREEN_HEIGHT - 60, 100, 20),
#             (450, SCREEN_HEIGHT - 80, 100, 20),
#             (650, SCREEN_HEIGHT - 40, 150, 40),
#         ],
#         "enemies": [(280, SCREEN_HEIGHT - 85, 30), (480, SCREEN_HEIGHT - 105, 30)],
#         "coins": [(100, SCREEN_HEIGHT - 70), (270, SCREEN_HEIGHT - 90), (470, SCREEN_HEIGHT - 110)],
#         "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
#     },
#     {  # Level 5 - More enemies
#         "player_start": (50, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
#             (100, SCREEN_HEIGHT - 140, 80, 20),
#             (300, SCREEN_HEIGHT - 180, 150, 20),
#             (550, SCREEN_HEIGHT - 140, 80, 20),
#         ],
#         "enemies": [
#             (200, SCREEN_HEIGHT - 65, 50),
#             (350, SCREEN_HEIGHT - 205, 60),
#             (500, SCREEN_HEIGHT - 65, 50),
#         ],
#         "coins": [(120, SCREEN_HEIGHT - 170), (370, SCREEN_HEIGHT - 210), (570, SCREEN_HEIGHT - 170)],
#         "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
#     },
#     {  # Level 6 - Tricky jumps
#         "player_start": (30, 100),
#         "platforms": [
#             (0, 150, 80, 20),  # Start
#             (200, 200, 50, 20),
#             (350, 150, 50, 20),  # Up
#             (200, 350, 50, 20),  # Down
#             (50, 450, SCREEN_WIDTH - 100, 20),  # Long bottom platform
#             (SCREEN_WIDTH - 100, 100, 50, 20)  # Goal platform
#         ],
#         "enemies": [(280, 425, 100), (450, 425, 100)],
#         "coins": [(210, 170), (360, 120), (210, 320), (SCREEN_WIDTH - 80, 70)],
#         "goal": (SCREEN_WIDTH - 80, 50)
#     },
#     {  # Level 7 - Final Challenge
#         "player_start": (50, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, 100, 40),
#             (150, SCREEN_HEIGHT - 80, 50, 20),
#             (250, SCREEN_HEIGHT - 120, 50, 20),
#             (350, SCREEN_HEIGHT - 160, 50, 20),  # Peak
#             (450, SCREEN_HEIGHT - 120, 50, 20),
#             (550, SCREEN_HEIGHT - 80, 50, 20),
#             (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 40, 100, 40),  # End platform
#         ],
#         "enemies": [
#             (80, SCREEN_HEIGHT - 65, 0),  # Guard start
#             (170, SCREEN_HEIGHT - 105, 0),
#             (270, SCREEN_HEIGHT - 145, 0),
#             (470, SCREEN_HEIGHT - 145, 0),
#             (570, SCREEN_HEIGHT - 105, 0),
#             (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 65, 0),  # Guard end
#         ],
#         "coins": [
#             (160, SCREEN_HEIGHT - 110), (360, SCREEN_HEIGHT - 190), (560, SCREEN_HEIGHT - 110)
#         ],
#         "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
#     }
# ]
#
#
# # --- Game Functions ---
# def load_level(level_data):
#     player = Player(*level_data["player_start"])
#     platforms = pygame.sprite.Group()
#     enemies = pygame.sprite.Group()
#     coins = pygame.sprite.Group()
#
#     for p_data in level_data["platforms"]:
#         platforms.add(Platform(*p_data))
#     for e_data in level_data["enemies"]:
#         enemies.add(Enemy(*e_data))
#     for c_data in level_data["coins"]:
#         coins.add(Coin(*c_data))
#
#     goal = Goal(*level_data["goal"])
#
#     all_sprites = pygame.sprite.Group()
#     all_sprites.add(player, platforms, enemies, coins, goal)
#
#     return player, platforms, enemies, coins, goal, all_sprites
#
#
# def draw_text(surface, text, size, x, y, color=WHITE):
#     font = pygame.font.Font(None, size)  # Use default font
#     text_surface = font.render(text, True, color)
#     text_rect = text_surface.get_rect()
#     text_rect.midtop = (x, y)
#     surface.blit(text_surface, text_rect)
#
#
# def show_message_screen(screen, clock, message, sub_message="Press SPACE to continue"):
#     screen.fill(LIGHT_BLUE)
#     draw_text(screen, message, 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, BLACK)
#     draw_text(screen, sub_message, 32, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, BLACK)
#     pygame.display.flip()
#     waiting = True
#     while waiting:
#         clock.tick(FPS)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.KEYUP:
#                 if event.key == pygame.K_SPACE:
#                     waiting = False
#                 if event.key == pygame.K_ESCAPE and (
#                         "Game Over" in message or "You Win" in message):  # Allow ESC to quit on end screens
#                     pygame.quit()
#                     sys.exit()
#
#
# # --- Game Initialization ---
# pygame.init()
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Simple Mario-like Game")
# clock = pygame.time.Clock()
#
# # --- Game Loop ---
# current_level_index = 0
# game_state = "start_screen"  # "playing", "level_complete", "game_over", "game_won", "start_screen"
#
# # Persist player stats between levels (if lives > 0)
# # This is done by not re-creating the player object fully from scratch unless game over
# player = None
# player_lives = 3
# player_score = 0
#
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if game_state == "playing":
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w:
#                     player.jump()
#         elif game_state in ["level_complete", "game_over", "game_won", "start_screen"]:
#             if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
#                 if game_state == "level_complete":
#                     current_level_index += 1
#                     if current_level_index < len(LEVELS):
#                         game_state = "playing"
#                         # Load next level, keeping score and lives
#                         # Re-create other sprites, reset player position based on new level data
#                         px, py = LEVELS[current_level_index]["player_start"]
#                         player.pos = pygame.math.Vector2(px, py)
#                         player.vel = pygame.math.Vector2(0, 0)  # Reset velocity
#                         # player object already exists, just need to re-init sprites
#                         _, platforms, enemies, coins, goal, all_sprites = load_level(LEVELS[current_level_index])
#                         all_sprites.add(player)  # Ensure player is in new all_sprites
#                     else:
#                         game_state = "game_won"
#                 elif game_state == "game_over" or game_state == "start_screen":
#                     current_level_index = 0
#                     player_lives = 3  # Reset for new game
#                     player_score = 0  # Reset for new game
#                     game_state = "playing"
#                     # Load first level
#                     player, platforms, enemies, coins, goal, all_sprites = load_level(LEVELS[current_level_index])
#                     player.lives = player_lives
#                     player.score = player_score
#                 elif game_state == "game_won":  # After winning, space restarts the game
#                     current_level_index = 0
#                     player_lives = 3
#                     player_score = 0
#                     game_state = "playing"
#                     player, platforms, enemies, coins, goal, all_sprites = load_level(LEVELS[current_level_index])
#                     player.lives = player_lives
#                     player.score = player_score
#
#     if game_state == "start_screen":
#         show_message_screen(screen, clock, "Simple Platformer", "Press SPACE to Start")
#         # After this, the event loop above will catch SPACE and change game_state to "playing"
#         # and load the first level.
#         # Initialize player here for the first time
#         player, platforms, enemies, coins, goal, all_sprites = load_level(LEVELS[current_level_index])
#         player.lives = player_lives
#         player.score = player_score
#
#
#     elif game_state == "playing":
#         # Update
#         player.update(platforms)
#         enemies.update(platforms)  # Pass platforms for basic enemy AI if needed
#
#         # Player fell off screen (handled in player.update(), returns "game_over")
#         if player.rect.top > SCREEN_HEIGHT + 50:  # extra buffer
#             game_over_reason = player.lose_life()
#             if game_over_reason == "game_over":
#                 game_state = "game_over"
#                 player_lives = player.lives  # Update global lives for display
#                 player_score = player.score  # Update global score for display
#                 continue
#
#         # Collisions
#         # Coins
#         coin_hits = pygame.sprite.spritecollide(player, coins, True)  # True to remove coin on hit
#         for coin in coin_hits:
#             player.score += 10
#             player_score = player.score  # Update global score
#
#         # Enemies
#         enemy_hits = pygame.sprite.spritecollide(player, enemies, False)  # False, handle kill/damage logic
#         for enemy in enemy_hits:
#             if player.invincible_timer == 0:  # Only interact if not invincible
#                 result = player.hit_enemy(enemy.rect)
#                 if result == "stomp":
#                     enemy.kill()  # Enemy is defeated
#                     player.score += 50
#                     player_score = player.score
#                 elif result == "game_over":
#                     game_state = "game_over"
#                     player_lives = player.lives
#                     player_score = player.score
#                     break  # Exit loop early if game over
#             if game_state == "game_over": break
#         if game_state == "game_over": continue
#
#         # Goal
#         if pygame.sprite.collide_rect(player, goal):
#             game_state = "level_complete"
#             player_lives = player.lives  # Persist for next level message
#             player_score = player.score  # Persist for next level message
#
#         # Draw
#         screen.fill(LIGHT_BLUE)  # Sky
#         all_sprites.draw(screen)
#
#         # UI Text (Score, Lives, Level)
#         draw_text(screen, f"Score: {player.score}", 30, SCREEN_WIDTH / 2, 10, BLACK)
#         draw_text(screen, f"Lives: {player.lives}", 30, 70, 10, BLACK)
#         draw_text(screen, f"Level: {current_level_index + 1}", 30, SCREEN_WIDTH - 70, 10, BLACK)
#
#
#     elif game_state == "level_complete":
#         if current_level_index + 1 < len(LEVELS):
#             show_message_screen(screen, clock, f"Level {current_level_index + 1} Complete!",
#                                 f"Score: {player_score} Lives: {player_lives}")
#         else:  # This means last level was completed
#             game_state = "game_won"  # Transition to game_won state
#             # No continue here, let the game_won state handle its screen
#
#     elif game_state == "game_over":
#         show_message_screen(screen, clock, "Game Over!", f"Final Score: {player_score}")
#         # Event loop handles restart
#
#     elif game_state == "game_won":
#         show_message_screen(screen, clock, "You Win!", f"Final Score: {player_score}")
#         # Event loop handles restart
#
#     pygame.display.flip()
#     clock.tick(FPS)
#
# pygame.quit()
# sys.exit()

#
# import pygame
# import sys
# import random
#
# # --- Constants ---
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 600
# FPS = 60
#
# # Colors
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# RED = (255, 0, 0)
# GREEN = (0, 255, 0)
# BLUE = (0, 0, 255)
# YELLOW = (255, 255, 0)
# BROWN = (139, 69, 19)
# LIGHT_BLUE = (173, 216, 230)  # Sky color
#
# # Player properties
# PLAYER_ACC = 0.7
# PLAYER_FRICTION = -0.12
# PLAYER_GRAVITY = 0.7
# PLAYER_JUMP_STRENGTH = 18
# PLAYER_MAX_FALL_SPEED = 15
#
#
# # --- Sprite Classes ---
#
# class Player(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         self.image = pygame.Surface((30, 40))
#         self.image.fill(RED)
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#
#         self.pos = pygame.math.Vector2(x, y)
#         self.vel = pygame.math.Vector2(0, 0)
#         self.acc = pygame.math.Vector2(0, 0)
#         self.on_ground = False
#         self.lives = 3  # Default lives
#         self.score = 0  # Default score
#         self.invincible_timer = 0
#
#     def jump(self):
#         if self.on_ground:
#             self.vel.y = -PLAYER_JUMP_STRENGTH
#             self.on_ground = False
#
#     def update(self, platforms):
#         if self.invincible_timer > 0:
#             self.invincible_timer -= 1
#             if self.invincible_timer % 10 < 5:
#                 self.image.set_alpha(128)
#             else:
#                 self.image.set_alpha(255)
#         else:
#             self.image.set_alpha(255)
#
#         self.acc = pygame.math.Vector2(0, PLAYER_GRAVITY)
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_LEFT] or keys[pygame.K_a]:
#             self.acc.x = -PLAYER_ACC
#         if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
#             self.acc.x = PLAYER_ACC
#
#         self.acc.x += self.vel.x * PLAYER_FRICTION
#         self.vel += self.acc
#         if abs(self.vel.x) < 0.1:
#             self.vel.x = 0
#
#         if self.vel.y > PLAYER_MAX_FALL_SPEED:
#             self.vel.y = PLAYER_MAX_FALL_SPEED
#
#         self.pos += self.vel + 0.5 * self.acc
#
#         self.rect.x = self.pos.x
#         self.collide_with_platforms(platforms, 'horizontal')
#
#         self.rect.y = self.pos.y
#         self.on_ground = False
#         self.collide_with_platforms(platforms, 'vertical')
#
#         if self.pos.x > SCREEN_WIDTH - self.rect.width:
#             self.pos.x = SCREEN_WIDTH - self.rect.width
#             self.vel.x = 0
#         if self.pos.x < 0:
#             self.pos.x = 0
#             self.vel.x = 0
#
#         if self.rect.top > SCREEN_HEIGHT:  # Fall off screen check
#             return self.lose_life()  # Return state change if game over
#         return None
#
#     def collide_with_platforms(self, platforms, direction):
#         hits = pygame.sprite.spritecollide(self, platforms, False)
#         if hits:
#             if direction == 'horizontal':
#                 if self.vel.x > 0:
#                     self.rect.right = hits[0].rect.left
#                 if self.vel.x < 0:
#                     self.rect.left = hits[0].rect.right
#                 self.pos.x = self.rect.x
#                 self.vel.x = 0
#
#             if direction == 'vertical':
#                 if self.vel.y > 0:
#                     self.rect.bottom = hits[0].rect.top
#                     self.on_ground = True
#                 if self.vel.y < 0:
#                     self.rect.top = hits[0].rect.bottom
#                 self.pos.y = self.rect.y
#                 self.vel.y = 0
#
#     def lose_life(self):
#         if self.invincible_timer == 0:
#             self.lives -= 1
#             self.invincible_timer = FPS * 2
#             self.pos.x, self.pos.y = 100, SCREEN_HEIGHT - 100  # Reset position
#             self.vel = pygame.math.Vector2(0, 0)
#             if self.lives <= 0:
#                 return "game_over"
#         return None
#
#     def hit_enemy(self, enemy_rect):
#         if self.vel.y > 0 and self.rect.bottom < enemy_rect.centery + 5:  # Added a small tolerance
#             self.vel.y = -PLAYER_JUMP_STRENGTH / 2.5  # Slightly better bounce
#             return "stomp"
#         else:
#             return self.lose_life()
#
#
# class Platform(pygame.sprite.Sprite):
#     def __init__(self, x, y, width, height, color=BROWN):
#         super().__init__()
#         self.image = pygame.Surface((width, height))
#         self.image.fill(color)
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#
#
# class Enemy(pygame.sprite.Sprite):
#     def __init__(self, x, y, move_range_x=50):
#         super().__init__()
#         self.image = pygame.Surface((25, 25))
#         self.image.fill(GREEN)
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#         self.start_x = x
#         self.move_range_x = move_range_x
#         self.direction = 1
#         self.speed = 1
#
#     def update(self, platforms):
#         self.rect.x += self.speed * self.direction
#         if self.move_range_x > 0:  # Only reverse if move_range_x is not 0
#             if self.rect.x > self.start_x + self.move_range_x or \
#                     self.rect.x < self.start_x - self.move_range_x:
#                 self.direction *= -1
#
#         hit_platforms = pygame.sprite.spritecollide(self, platforms, False)
#         for platform in hit_platforms:
#             if self.speed * self.direction > 0:
#                 self.rect.right = platform.rect.left
#             elif self.speed * self.direction < 0:
#                 self.rect.left = platform.rect.right
#             if self.move_range_x > 0:  # Only reverse if it's supposed to move
#                 self.direction *= -1
#             break
#
#
# class Coin(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         self.image = pygame.Surface((15, 15))
#         self.image.fill(YELLOW)
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#
#
# class Goal(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         self.image = pygame.Surface((30, 50))
#         self.image.fill(BLUE)
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#
#
# # --- Level Data (same as before) ---
# LEVELS = [
#     {  # Level 1
#         "player_start": (50, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),  # Ground
#             (200, SCREEN_HEIGHT - 150, 100, 20),
#             (400, SCREEN_HEIGHT - 250, 100, 20),
#             (150, SCREEN_HEIGHT - 350, 150, 20),
#         ],
#         "enemies": [(300, SCREEN_HEIGHT - 65, 50)],
#         "coins": [(220, SCREEN_HEIGHT - 180), (420, SCREEN_HEIGHT - 280), (170, SCREEN_HEIGHT - 380)],
#         "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
#     },
#     {  # Level 2
#         "player_start": (50, 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),  # Ground
#             (0, 150, 100, 20),
#             (150, 250, 100, 20),
#             (300, 350, 100, 20),
#             (500, 250, 80, 20),
#             (650, 150, 80, 20),
#         ],
#         "enemies": [(400, SCREEN_HEIGHT - 65, 80), (200, 225, 30)],
#         "coins": [(170, 220), (320, 320), (520, 220), (670, 120)],
#         "goal": (SCREEN_WIDTH - 80, 100)
#     },
#     {  # Level 3 - More verticality
#         "player_start": (50, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, 200, 40),
#             (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 40, 200, 40),
#             (250, SCREEN_HEIGHT - 120, 50, 20),
#             (350, SCREEN_HEIGHT - 200, 50, 20),
#             (450, SCREEN_HEIGHT - 280, 50, 20),
#             (550, SCREEN_HEIGHT - 200, 50, 20),
#             (650, SCREEN_HEIGHT - 120, 50, 20),
#         ],
#         "enemies": [(450, SCREEN_HEIGHT - 305, 0)],
#         "coins": [(260, SCREEN_HEIGHT - 150), (360, SCREEN_HEIGHT - 230), (560, SCREEN_HEIGHT - 230)],
#         "goal": (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 90)
#     },
#     {  # Level 4 - Gaps
#         "player_start": (50, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, 150, 40),
#             (250, SCREEN_HEIGHT - 60, 100, 20),
#             (450, SCREEN_HEIGHT - 80, 100, 20),
#             (650, SCREEN_HEIGHT - 40, 150, 40),
#         ],
#         "enemies": [(280, SCREEN_HEIGHT - 85, 30), (480, SCREEN_HEIGHT - 105, 30)],
#         "coins": [(100, SCREEN_HEIGHT - 70), (270, SCREEN_HEIGHT - 90), (470, SCREEN_HEIGHT - 110)],
#         "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
#     },
#     {  # Level 5 - More enemies
#         "player_start": (50, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
#             (100, SCREEN_HEIGHT - 140, 80, 20),
#             (300, SCREEN_HEIGHT - 180, 150, 20),
#             (550, SCREEN_HEIGHT - 140, 80, 20),
#         ],
#         "enemies": [
#             (200, SCREEN_HEIGHT - 65, 50),
#             (350, SCREEN_HEIGHT - 205, 60),
#             (500, SCREEN_HEIGHT - 65, 50),
#         ],
#         "coins": [(120, SCREEN_HEIGHT - 170), (370, SCREEN_HEIGHT - 210), (570, SCREEN_HEIGHT - 170)],
#         "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
#     },
#     {  # Level 6 - Tricky jumps
#         "player_start": (30, 100),
#         "platforms": [
#             (0, 150, 80, 20),
#             (200, 200, 50, 20),
#             (350, 150, 50, 20),
#             (200, 350, 50, 20),
#             (50, 450, SCREEN_WIDTH - 100, 20),
#             (SCREEN_WIDTH - 100, 100, 50, 20)
#         ],
#         "enemies": [(280, 425, 100), (450, 425, 100)],
#         "coins": [(210, 170), (360, 120), (210, 320), (SCREEN_WIDTH - 80, 70)],
#         "goal": (SCREEN_WIDTH - 80, 50)
#     },
#     {  # Level 7 - Final Challenge
#         "player_start": (50, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, 100, 40),
#             (150, SCREEN_HEIGHT - 80, 50, 20),
#             (250, SCREEN_HEIGHT - 120, 50, 20),
#             (350, SCREEN_HEIGHT - 160, 50, 20),
#             (450, SCREEN_HEIGHT - 120, 50, 20),
#             (550, SCREEN_HEIGHT - 80, 50, 20),
#             (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 40, 100, 40),
#         ],
#         "enemies": [
#             (80, SCREEN_HEIGHT - 65, 0),
#             (170, SCREEN_HEIGHT - 105, 0),
#             (270, SCREEN_HEIGHT - 145, 0),
#             (470, SCREEN_HEIGHT - 145, 0),
#             (570, SCREEN_HEIGHT - 105, 0),
#             (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 65, 0),
#         ],
#         "coins": [
#             (160, SCREEN_HEIGHT - 110), (360, SCREEN_HEIGHT - 190), (560, SCREEN_HEIGHT - 110)
#         ],
#         "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
#     }
# ]
#
#
# # --- Game Functions ---
# def load_level_sprites(level_data):  # Renamed to avoid confusion with creating player
#     platforms = pygame.sprite.Group()
#     enemies = pygame.sprite.Group()
#     coins = pygame.sprite.Group()
#
#     for p_data in level_data["platforms"]:
#         platforms.add(Platform(*p_data))
#     for e_data in level_data["enemies"]:
#         enemies.add(Enemy(*e_data))
#     for c_data in level_data["coins"]:
#         coins.add(Coin(*c_data))
#
#     goal = Goal(*level_data["goal"])
#
#     # Note: Player is NOT created here. It's managed separately.
#     return platforms, enemies, coins, goal
#
#
# def draw_text(surface, text, size, x, y, color=WHITE):
#     font = pygame.font.Font(None, size)
#     text_surface = font.render(text, True, color)
#     text_rect = text_surface.get_rect()
#     text_rect.midtop = (x, y)
#     surface.blit(text_surface, text_rect)
#
#
# def show_message_screen(screen, clock, message, sub_message="Press SPACE to continue"):
#     # This function still blocks and waits for SPACE, used for game over/level complete
#     screen.fill(LIGHT_BLUE)
#     draw_text(screen, message, 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, BLACK)
#     draw_text(screen, sub_message, 32, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, BLACK)
#     pygame.display.flip()
#     waiting = True
#     while waiting:
#         clock.tick(FPS)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.KEYUP:
#                 if event.key == pygame.K_SPACE:
#                     waiting = False
#                 if event.key == pygame.K_ESCAPE and ("Game Over" in message or "You Win" in message):
#                     pygame.quit()
#                     sys.exit()
#
#
# # --- Game Initialization ---
# pygame.init()
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Simple Mario-like Game")
# clock = pygame.time.Clock()
#
# # --- Game Variables ---
# current_level_index = 0
# game_state = "start_screen"
# player = None  # Player object
# all_sprites = pygame.sprite.Group()
# platforms = pygame.sprite.Group()
# enemies = pygame.sprite.Group()
# coins = pygame.sprite.Group()
# goal = None
#
# # Persistent stats (these will be copied to/from player object)
# game_player_lives = 3
# game_player_score = 0
#
# # --- Game Loop ---
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#         # Handle JUMP input only when playing and player exists
#         if game_state == "playing" and player:
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w:
#                     player.jump()
#
#         # Handle SPACE for state transitions (start, level complete, game over, game won)
#         if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
#             if game_state == "start_screen":
#                 game_state = "playing"
#                 current_level_index = 0
#                 game_player_lives = 3  # Reset for new game
#                 game_player_score = 0
#
#                 player = Player(*LEVELS[current_level_index]["player_start"])
#                 player.lives = game_player_lives
#                 player.score = game_player_score
#
#                 platforms, enemies, coins, goal = load_level_sprites(LEVELS[current_level_index])
#                 all_sprites.empty()
#                 all_sprites.add(player, platforms, enemies, coins, goal)
#
#             elif game_state == "level_complete":
#                 current_level_index += 1
#                 if current_level_index < len(LEVELS):
#                     game_state = "playing"
#                     # Player object persists, reset its position and load new level elements
#                     player.pos = pygame.math.Vector2(*LEVELS[current_level_index]["player_start"])
#                     player.rect.topleft = player.pos
#                     player.vel = pygame.math.Vector2(0, 0)
#                     player.on_ground = False  # Good to reset this
#                     player.invincible_timer = 0  # Reset invincibility
#
#                     platforms, enemies, coins, goal = load_level_sprites(LEVELS[current_level_index])
#                     all_sprites.empty()
#                     all_sprites.add(player, platforms, enemies, coins, goal)
#                     # game_player_score and game_player_lives are already up-to-date from player object
#                 else:
#                     game_state = "game_won"  # All levels completed
#
#             elif game_state == "game_over" or game_state == "game_won":  # Restart game
#                 game_state = "playing"
#                 current_level_index = 0
#                 game_player_lives = 3
#                 game_player_score = 0
#
#                 player = Player(*LEVELS[current_level_index]["player_start"])
#                 player.lives = game_player_lives
#                 player.score = game_player_score
#
#                 platforms, enemies, coins, goal = load_level_sprites(LEVELS[current_level_index])
#                 all_sprites.empty()
#                 all_sprites.add(player, platforms, enemies, coins, goal)
#
#     # --- Game State Logic & Drawing ---
#     if game_state == "start_screen":
#         screen.fill(LIGHT_BLUE)
#         draw_text(screen, "Simple Platformer", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, BLACK)
#         draw_text(screen, "Press SPACE to Start", 32, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, BLACK)
#
#     elif game_state == "playing":
#         if not player:  # Should not happen if logic is correct, defensive
#             game_state = "start_screen"  # Fallback
#             continue
#
#         # Update player and check for falling off screen
#         player_state_change = player.update(platforms)
#         if player_state_change == "game_over":
#             game_player_lives = player.lives
#             game_player_score = player.score
#             game_state = "game_over"
#             continue  # Skip rest of playing logic for this frame
#
#         enemies.update(platforms)
#
#         # Collisions
#         coin_hits = pygame.sprite.spritecollide(player, coins, True)
#         for coin in coin_hits:
#             player.score += 10
#         game_player_score = player.score  # Update global score display
#
#         enemy_hits = pygame.sprite.spritecollide(player, enemies, False)
#         for enemy in enemy_hits:
#             if player.invincible_timer == 0:
#                 result = player.hit_enemy(enemy.rect)
#                 if result == "stomp":
#                     enemy.kill()
#                     player.score += 50
#                     game_player_score = player.score  # Update global score display
#                 elif result == "game_over":
#                     game_player_lives = player.lives
#                     game_player_score = player.score
#                     game_state = "game_over"
#                     break
#             if game_state == "game_over": break
#         if game_state == "game_over": continue
#
#         if goal and pygame.sprite.collide_rect(player, goal):
#             game_player_lives = player.lives  # Persist for message
#             game_player_score = player.score  # Persist for message
#             game_state = "level_complete"
#             # current_level_index is NOT incremented here yet.
#             # It will be incremented when SPACE is pressed to proceed from level_complete screen.
#
#         # Draw everything
#         screen.fill(LIGHT_BLUE)
#         all_sprites.draw(screen)
#
#         draw_text(screen, f"Score: {game_player_score}", 30, SCREEN_WIDTH / 2, 10, BLACK)
#         draw_text(screen, f"Lives: {game_player_lives}", 30, 70, 10, BLACK)
#         draw_text(screen, f"Level: {current_level_index + 1}", 30, SCREEN_WIDTH - 70, 10, BLACK)
#
#     elif game_state == "level_complete":
#         # Message uses current_level_index + 1 for display (level just finished)
#         # game_player_score and game_player_lives are already updated from player object
#         show_message_screen(screen, clock, f"Level {current_level_index + 1} Complete!",
#                             f"Score: {game_player_score} Lives: {game_player_lives}")
#         # The main event loop will handle SPACE press to change state to 'playing' (for next level)
#         # or 'game_won' if it was the last level. The state change to 'game_won' if applicable
#         # is handled in the event loop part for "level_complete".
#
#     elif game_state == "game_over":
#         show_message_screen(screen, clock, "Game Over!", f"Final Score: {game_player_score}")
#         # Main event loop handles SPACE press to restart.
#
#     elif game_state == "game_won":
#         show_message_screen(screen, clock, "You Win!", f"Final Score: {game_player_score}")
#         # Main event loop handles SPACE press to restart.
#
#     pygame.display.flip()
#     clock.tick(FPS)
#
# pygame.quit()
# sys.exit()

#
# import pygame
# import sys
# import random
#
# # --- Constants ---
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 600
# FPS = 60
#
# # Colors
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# RED = (255, 0, 0)
# GREEN = (0, 255, 0)
# BLUE = (0, 0, 255)
# YELLOW = (255, 255, 0)
# BROWN = (139, 69, 19)
# LIGHT_BLUE = (173, 216, 230)  # Sky color
#
# # Player properties
# PLAYER_ACC = 0.7
# PLAYER_FRICTION = -0.12
# PLAYER_GRAVITY = 0.7
# PLAYER_JUMP_STRENGTH = 18
# PLAYER_MAX_FALL_SPEED = 15
#
#
# # --- Sprite Classes ---
#
# class Player(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         self.image = pygame.Surface((30, 40))
#         self.image.fill(RED)
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#
#         self.pos = pygame.math.Vector2(x, y)
#         self.vel = pygame.math.Vector2(0, 0)
#         self.acc = pygame.math.Vector2(0, 0)
#         self.on_ground = False
#         self.lives = 3
#         self.score = 0
#         self.invincible_timer = 0
#
#     def jump(self):
#         if self.on_ground:
#             self.vel.y = -PLAYER_JUMP_STRENGTH
#             self.on_ground = False
#
#     def update(self, platforms):
#         if self.invincible_timer > 0:
#             self.invincible_timer -= 1
#             if self.invincible_timer % 10 < 5:
#                 self.image.set_alpha(128)
#             else:
#                 self.image.set_alpha(255)
#         else:
#             self.image.set_alpha(255)
#
#         self.acc = pygame.math.Vector2(0, PLAYER_GRAVITY)
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_LEFT] or keys[pygame.K_a]:
#             self.acc.x = -PLAYER_ACC
#         if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
#             self.acc.x = PLAYER_ACC
#
#         self.acc.x += self.vel.x * PLAYER_FRICTION
#         self.vel += self.acc
#         if abs(self.vel.x) < 0.1:
#             self.vel.x = 0
#
#         if self.vel.y > PLAYER_MAX_FALL_SPEED:
#             self.vel.y = PLAYER_MAX_FALL_SPEED
#
#         self.pos += self.vel + 0.5 * self.acc
#
#         self.rect.x = self.pos.x
#         self.collide_with_platforms(platforms, 'horizontal')
#
#         self.rect.y = self.pos.y
#         self.on_ground = False
#         self.collide_with_platforms(platforms, 'vertical')
#
#         if self.pos.x > SCREEN_WIDTH - self.rect.width:
#             self.pos.x = SCREEN_WIDTH - self.rect.width
#             self.vel.x = 0
#         if self.pos.x < 0:
#             self.pos.x = 0
#             self.vel.x = 0
#
#         if self.rect.top > SCREEN_HEIGHT:
#             return self.lose_life()
#         return None
#
#     def collide_with_platforms(self, platforms, direction):
#         hits = pygame.sprite.spritecollide(self, platforms, False)
#         if hits:
#             if direction == 'horizontal':
#                 if self.vel.x > 0:
#                     self.rect.right = hits[0].rect.left
#                 if self.vel.x < 0:
#                     self.rect.left = hits[0].rect.right
#                 self.pos.x = self.rect.x
#                 self.vel.x = 0
#
#             if direction == 'vertical':
#                 if self.vel.y > 0:
#                     self.rect.bottom = hits[0].rect.top
#                     self.on_ground = True
#                 if self.vel.y < 0:
#                     self.rect.top = hits[0].rect.bottom
#                 self.pos.y = self.rect.y
#                 self.vel.y = 0
#
#     def lose_life(self):
#         if self.invincible_timer == 0:
#             self.lives -= 1
#             self.invincible_timer = FPS * 2
#             # Reset to a default safe spot or current level's start
#             # For simplicity, using a generic reset. A better approach would be current level start.
#             current_level_data = LEVELS[current_level_index]  # Access global current_level_index
#             self.pos.x, self.pos.y = current_level_data["player_start"]
#             self.rect.topleft = self.pos
#             self.vel = pygame.math.Vector2(0, 0)
#             if self.lives <= 0:
#                 return "game_over"
#         return None
#
#     def hit_enemy(self, enemy_rect):
#         if self.vel.y > 0 and self.rect.bottom < enemy_rect.centery + 5:
#             self.vel.y = -PLAYER_JUMP_STRENGTH / 2.5
#             return "stomp"
#         else:
#             return self.lose_life()
#
#
# class Platform(pygame.sprite.Sprite):
#     def __init__(self, x, y, width, height, color=BROWN):
#         super().__init__()
#         self.image = pygame.Surface((width, height))
#         self.image.fill(color)
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#
#
# class Enemy(pygame.sprite.Sprite):
#     def __init__(self, x, y, move_range_x=50):
#         super().__init__()
#         self.image = pygame.Surface((25, 25))
#         self.image.fill(GREEN)
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#         self.start_x = x
#         self.move_range_x = move_range_x
#         self.direction = 1
#         self.speed = 1
#
#     def update(self, platforms):
#         self.rect.x += self.speed * self.direction
#         if self.move_range_x > 0:
#             if self.rect.x > self.start_x + self.move_range_x or \
#                     self.rect.x < self.start_x - self.move_range_x:
#                 self.direction *= -1
#
#         hit_platforms = pygame.sprite.spritecollide(self, platforms, False)
#         for platform in hit_platforms:
#             if self.speed * self.direction > 0:
#                 self.rect.right = platform.rect.left
#             elif self.speed * self.direction < 0:
#                 self.rect.left = platform.rect.right
#             if self.move_range_x > 0:
#                 self.direction *= -1
#             break
#
#
# class Coin(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         self.image = pygame.Surface((15, 15))
#         self.image.fill(YELLOW)
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#
#
# class Goal(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         self.image = pygame.Surface((30, 50))
#         self.image.fill(BLUE)
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#
#
# # --- Level Data ---
# LEVELS = [
#     {  # Level 1
#         "player_start": (50, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40), (200, SCREEN_HEIGHT - 150, 100, 20),
#             (400, SCREEN_HEIGHT - 250, 100, 20), (150, SCREEN_HEIGHT - 350, 150, 20),
#         ],
#         "enemies": [(300, SCREEN_HEIGHT - 65, 50)],
#         "coins": [(220, SCREEN_HEIGHT - 180), (420, SCREEN_HEIGHT - 280), (170, SCREEN_HEIGHT - 380)],
#         "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
#     },
#     {  # Level 2
#         "player_start": (50, 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40), (0, 150, 100, 20),
#             (150, 250, 100, 20), (300, 350, 100, 20),
#             (500, 250, 80, 20), (650, 150, 80, 20),
#         ],
#         "enemies": [(400, SCREEN_HEIGHT - 65, 80), (200, 225, 30)],
#         "coins": [(170, 220), (320, 320), (520, 220), (670, 120)],
#         "goal": (SCREEN_WIDTH - 80, 100)
#     },
#     {  # Level 3 - More verticality
#         "player_start": (50, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, 200, 40), (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 40, 200, 40),
#             (250, SCREEN_HEIGHT - 120, 50, 20), (350, SCREEN_HEIGHT - 200, 50, 20),
#             (450, SCREEN_HEIGHT - 280, 50, 20), (550, SCREEN_HEIGHT - 200, 50, 20),
#             (650, SCREEN_HEIGHT - 120, 50, 20),
#         ],
#         "enemies": [(450, SCREEN_HEIGHT - 305, 0)],
#         "coins": [(260, SCREEN_HEIGHT - 150), (360, SCREEN_HEIGHT - 230), (560, SCREEN_HEIGHT - 230)],
#         "goal": (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 90)
#     },
#     {  # Level 4 - Gaps
#         "player_start": (50, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, 150, 40), (250, SCREEN_HEIGHT - 60, 100, 20),
#             (450, SCREEN_HEIGHT - 80, 100, 20), (650, SCREEN_HEIGHT - 40, 150, 40),
#         ],
#         "enemies": [(280, SCREEN_HEIGHT - 85, 30), (480, SCREEN_HEIGHT - 105, 30)],
#         "coins": [(100, SCREEN_HEIGHT - 70), (270, SCREEN_HEIGHT - 90), (470, SCREEN_HEIGHT - 110)],
#         "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
#     },
#     {  # Level 5 - More enemies
#         "player_start": (50, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40), (100, SCREEN_HEIGHT - 140, 80, 20),
#             (300, SCREEN_HEIGHT - 180, 150, 20), (550, SCREEN_HEIGHT - 140, 80, 20),
#         ],
#         "enemies": [
#             (200, SCREEN_HEIGHT - 65, 50), (350, SCREEN_HEIGHT - 205, 60), (500, SCREEN_HEIGHT - 65, 50),
#         ],
#         "coins": [(120, SCREEN_HEIGHT - 170), (370, SCREEN_HEIGHT - 210), (570, SCREEN_HEIGHT - 170)],
#         "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
#     },
#     {  # Level 6 - Tricky jumps
#         "player_start": (30, 100),
#         "platforms": [
#             (0, 150, 80, 20), (200, 200, 50, 20), (350, 150, 50, 20),
#             (200, 350, 50, 20), (50, 450, SCREEN_WIDTH - 100, 20),
#             (SCREEN_WIDTH - 100, 100, 50, 20)
#         ],
#         "enemies": [(280, 425, 100), (450, 425, 100)],
#         "coins": [(210, 170), (360, 120), (210, 320), (SCREEN_WIDTH - 80, 70)],
#         "goal": (SCREEN_WIDTH - 80, 50)
#     },
#     {  # Level 7 - Final Challenge (Original)
#         "player_start": (50, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, 100, 40), (150, SCREEN_HEIGHT - 80, 50, 20),
#             (250, SCREEN_HEIGHT - 120, 50, 20), (350, SCREEN_HEIGHT - 160, 50, 20),
#             (450, SCREEN_HEIGHT - 120, 50, 20), (550, SCREEN_HEIGHT - 80, 50, 20),
#             (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 40, 100, 40),
#         ],
#         "enemies": [
#             (80, SCREEN_HEIGHT - 65, 0), (170, SCREEN_HEIGHT - 105, 0),
#             (270, SCREEN_HEIGHT - 145, 0), (470, SCREEN_HEIGHT - 145, 0),
#             (570, SCREEN_HEIGHT - 105, 0), (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 65, 0),
#         ],
#         "coins": [(160, SCREEN_HEIGHT - 110), (360, SCREEN_HEIGHT - 190), (560, SCREEN_HEIGHT - 110)],
#         "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
#     },
#     {  # Level 8: "The Ascent"
#         "player_start": (50, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, 150, 40),  # Start ground
#             (100, SCREEN_HEIGHT - 140, 70, 20),
#             (50, SCREEN_HEIGHT - 240, 70, 20),
#             (150, SCREEN_HEIGHT - 340, 70, 20),
#             (250, SCREEN_HEIGHT - 440, SCREEN_WIDTH - 250, 20),  # Top long platform
#             (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, 100, 20),  # Lower platform to goal
#         ],
#         "enemies": [(300, SCREEN_HEIGHT - 465, 100), (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 125, 0)],
#         "coins": [(120, SCREEN_HEIGHT - 170), (70, SCREEN_HEIGHT - 270), (170, SCREEN_HEIGHT - 370),
#                   (400, SCREEN_HEIGHT - 470)],
#         "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 150)
#     },
#     {  # Level 9: "Corridor Run"
#         "player_start": (30, SCREEN_HEIGHT - 80),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),  # Main ground
#             (150, SCREEN_HEIGHT - 120, 80, 20),  # hop
#             (300, SCREEN_HEIGHT - 120, 80, 20),  # hop
#             (450, SCREEN_HEIGHT - 120, 80, 20),  # hop
#             (600, SCREEN_HEIGHT - 120, 80, 20),  # hop
#         ],
#         "enemies": [
#             (100, SCREEN_HEIGHT - 65, 30), (250, SCREEN_HEIGHT - 65, 30),
#             (400, SCREEN_HEIGHT - 65, 30), (550, SCREEN_HEIGHT - 65, 30),
#             (350, SCREEN_HEIGHT - 145, 30)
#         ],
#         "coins": [(170, SCREEN_HEIGHT - 150), (320, SCREEN_HEIGHT - 150), (470, SCREEN_HEIGHT - 150),
#                   (620, SCREEN_HEIGHT - 150)],
#         "goal": (SCREEN_WIDTH - 60, SCREEN_HEIGHT - 90)
#     },
#     {  # Level 10: "Maze of Platforms"
#         "player_start": (50, 50),
#         "platforms": [
#             (0, 100, 100, 20),  # Start
#             (150, 180, 100, 20),
#             (0, 260, 100, 20),
#             (150, 340, 100, 20),  # Lower path
#             (300, 100, 100, 20),  # Upper path
#             (450, 180, 100, 20),
#             (300, 260, 100, 20),  # Dead end with coin
#             (600, 100, SCREEN_WIDTH - 600, 20),  # Top right path to goal
#             (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)  # Bottom floor (pitfall)
#         ],
#         "enemies": [(180, 155, 30), (50, 235, 0), (480, 155, 30)],
#         "coins": [(320, 230), (70, 70), (320, 70), (620, 70)],
#         "goal": (SCREEN_WIDTH - 80, 50)
#     },
#     {  # Level 11: "Enemy Gauntlet"
#         "player_start": (50, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
#             (100, SCREEN_HEIGHT - 150, 80, 20),
#             (250, SCREEN_HEIGHT - 200, 300, 20),  # Central platform
#             (SCREEN_WIDTH - 180, SCREEN_HEIGHT - 150, 80, 20),
#         ],
#         "enemies": [
#             (150, SCREEN_HEIGHT - 65, 50), (250, SCREEN_HEIGHT - 65, 50),
#             (350, SCREEN_HEIGHT - 65, 50), (450, SCREEN_HEIGHT - 65, 50),
#             (300, SCREEN_HEIGHT - 225, 80), (450, SCREEN_HEIGHT - 225, 80),
#             (120, SCREEN_HEIGHT - 175, 0), (SCREEN_WIDTH - 160, SCREEN_HEIGHT - 175, 0)
#         ],
#         "coins": [(130, SCREEN_HEIGHT - 180), (390, SCREEN_HEIGHT - 230), (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 180)],
#         "goal": (SCREEN_WIDTH / 2 - 15, SCREEN_HEIGHT - 270)  # Goal on central platform
#     },
#     {  # Level 12: "Final Leap"
#         "player_start": (30, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, 100, 40),  # Start
#             (200, SCREEN_HEIGHT - 80, 50, 20),  # Step 1
#             (350, SCREEN_HEIGHT - 120, 50, 20),  # Step 2
#             (500, SCREEN_HEIGHT - 160, 50, 20),  # Step 3 - a bit tricky
#             (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 40, 100, 40),  # Goal platform
#             # Tiny platforms as traps or distractions
#             (150, SCREEN_HEIGHT - 200, 20, 20),
#             (600, SCREEN_HEIGHT - 250, 20, 20),
#         ],
#         "enemies": [
#             (215, SCREEN_HEIGHT - 105, 0),  # Guard step 1
#             (365, SCREEN_HEIGHT - 145, 0),  # Guard step 2
#             (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 65, 50)  # Patrol near goal
#         ],
#         "coins": [
#             (215, SCREEN_HEIGHT - 110), (365, SCREEN_HEIGHT - 150), (515, SCREEN_HEIGHT - 190),
#             (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 70)
#         ],
#         "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
#     }
# ]
#
#
# # --- Game Functions ---
# def load_level_sprites(level_data):
#     platforms = pygame.sprite.Group()
#     enemies = pygame.sprite.Group()
#     coins = pygame.sprite.Group()
#
#     for p_data in level_data["platforms"]:
#         platforms.add(Platform(*p_data))
#     for e_data in level_data["enemies"]:
#         enemies.add(Enemy(*e_data))
#     for c_data in level_data["coins"]:
#         coins.add(Coin(*c_data))
#
#     goal = Goal(*level_data["goal"])
#     return platforms, enemies, coins, goal
#
#
# def draw_text(surface, text, size, x, y, color=WHITE):
#     font = pygame.font.Font(None, size)
#     text_surface = font.render(text, True, color)
#     text_rect = text_surface.get_rect()
#     text_rect.midtop = (x, y)
#     surface.blit(text_surface, text_rect)
#
#
# def show_message_screen(screen, clock, message, sub_message="Press SPACE to continue"):
#     screen.fill(LIGHT_BLUE)
#     draw_text(screen, message, 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, BLACK)
#     draw_text(screen, sub_message, 32, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, BLACK)
#     pygame.display.flip()
#     waiting = True
#     while waiting:
#         clock.tick(FPS)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.KEYUP:
#                 if event.key == pygame.K_SPACE:
#                     waiting = False
#                 if event.key == pygame.K_ESCAPE and (
#                         "Game Over" in message or "You Win" in message or "Simple Platformer" in message):
#                     pygame.quit()
#                     sys.exit()
#
#
# # --- Game Initialization ---
# pygame.init()
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Simple Mario-like Game - 12 Levels")
# clock = pygame.time.Clock()
#
# # --- Game Variables ---
# current_level_index = 0
# game_state = "start_screen"
# player = None
# all_sprites = pygame.sprite.Group()
# platforms = pygame.sprite.Group()
# enemies = pygame.sprite.Group()
# coins = pygame.sprite.Group()
# goal = None
#
# game_player_lives = 3
# game_player_score = 0
#
# # --- Game Loop ---
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#         if game_state == "playing" and player:
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w:
#                     player.jump()
#
#         if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
#             if game_state == "start_screen":
#                 game_state = "playing"
#                 current_level_index = 0
#                 game_player_lives = 3
#                 game_player_score = 0
#
#                 player = Player(*LEVELS[current_level_index]["player_start"])
#                 player.lives = game_player_lives
#                 player.score = game_player_score
#
#                 platforms, enemies, coins, goal = load_level_sprites(LEVELS[current_level_index])
#                 all_sprites.empty()
#                 all_sprites.add(player, platforms, enemies, coins, goal)
#
#             elif game_state == "level_complete":
#                 current_level_index += 1
#                 if current_level_index < len(LEVELS):
#                     game_state = "playing"
#                     player.pos = pygame.math.Vector2(*LEVELS[current_level_index]["player_start"])
#                     player.rect.topleft = player.pos
#                     player.vel = pygame.math.Vector2(0, 0)
#                     player.on_ground = False
#                     player.invincible_timer = 0
#
#                     platforms, enemies, coins, goal = load_level_sprites(LEVELS[current_level_index])
#                     all_sprites.empty()
#                     all_sprites.add(player, platforms, enemies, coins, goal)
#                 else:
#                     game_state = "game_won"
#
#             elif game_state == "game_over" or game_state == "game_won":
#                 game_state = "playing"  # Or "start_screen" if you prefer going back to title
#                 current_level_index = 0
#                 game_player_lives = 3
#                 game_player_score = 0
#
#                 player = Player(*LEVELS[current_level_index]["player_start"])
#                 player.lives = game_player_lives
#                 player.score = game_player_score
#
#                 platforms, enemies, coins, goal = load_level_sprites(LEVELS[current_level_index])
#                 all_sprites.empty()
#                 all_sprites.add(player, platforms, enemies, coins, goal)
#
#         if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
#             if game_state == "start_screen" or game_state == "game_over" or game_state == "game_won":
#                 running = False  # Allow quitting from these screens with ESC
#
#     if game_state == "start_screen":
#         screen.fill(LIGHT_BLUE)
#         draw_text(screen, "Simple Platformer", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, BLACK)
#         draw_text(screen, "Press SPACE to Start", 32, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, BLACK)
#         draw_text(screen, "Press ESC to Quit", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.75, BLACK)
#
#
#     elif game_state == "playing":
#         if not player:
#             game_state = "start_screen"
#             continue
#
#         player_state_change = player.update(platforms)
#         if player_state_change == "game_over":
#             game_player_lives = player.lives  # Should be 0
#             game_player_score = player.score
#             game_state = "game_over"
#             continue
#
#         enemies.update(platforms)
#
#         coin_hits = pygame.sprite.spritecollide(player, coins, True)
#         for coin in coin_hits:
#             player.score += 10
#         game_player_score = player.score
#
#         enemy_hits = pygame.sprite.spritecollide(player, enemies, False)
#         for enemy in enemy_hits:
#             if player.invincible_timer == 0:
#                 result = player.hit_enemy(enemy.rect)
#                 if result == "stomp":
#                     enemy.kill()
#                     player.score += 50
#                     game_player_score = player.score
#                 elif result == "game_over":
#                     game_player_lives = player.lives  # Should be 0
#                     game_player_score = player.score
#                     game_state = "game_over"
#                     break
#             if game_state == "game_over": break
#         if game_state == "game_over": continue
#
#         if goal and pygame.sprite.collide_rect(player, goal):
#             game_player_lives = player.lives
#             game_player_score = player.score
#             game_state = "level_complete"
#
#         screen.fill(LIGHT_BLUE)
#         all_sprites.draw(screen)
#
#         draw_text(screen, f"Score: {game_player_score}", 30, SCREEN_WIDTH / 2, 10, BLACK)
#         draw_text(screen, f"Lives: {player.lives if player else game_player_lives}", 30, 70, 10,
#                   BLACK)  # Use player.lives directly if available
#         draw_text(screen, f"Level: {current_level_index + 1}", 30, SCREEN_WIDTH - 70, 10, BLACK)
#
#     elif game_state == "level_complete":
#         show_message_screen(screen, clock, f"Level {current_level_index + 1} Complete!",
#                             f"Score: {game_player_score} Lives: {game_player_lives}\nPress SPACE for Next Level")
#
#     elif game_state == "game_over":
#         show_message_screen(screen, clock, "Game Over!",
#                             f"Final Score: {game_player_score}\nPress SPACE to Restart or ESC to Quit")
#
#     elif game_state == "game_won":
#         show_message_screen(screen, clock, "You Win! All Levels Cleared!",
#                             f"Final Score: {game_player_score}\nPress SPACE to Restart or ESC to Quit")
#
#     pygame.display.flip()
#     clock.tick(FPS)
#
# pygame.quit()
# sys.exit()














# import pygame
# import sys
# import random
#
# # --- Constants ---
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 600
# FPS = 60
#
# # Colors
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# RED = (255, 0, 0)
# GREEN = (0, 255, 0)
# BLUE = (0, 0, 255)
# YELLOW = (255, 255, 0)
# BROWN = (139, 69, 19)
# LIGHT_BLUE = (173, 216, 230)  # Sky color
#
# # Player properties
# PLAYER_ACC = 0.7
# PLAYER_FRICTION = -0.12
# PLAYER_GRAVITY = 0.7
# PLAYER_JUMP_STRENGTH = 18
# PLAYER_MAX_FALL_SPEED = 15
#
#
# # --- Sprite Classes ---
#
# class Player(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         # self.image = pygame.Surface((30, 40))
#         # self.image.fill(RED)
#         self.image = pygame.image.load("./assets/mario sprite.png").convert()
#         self.image = pygame.transform.scale(self.image,(35,35))
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#
#         self.pos = pygame.math.Vector2(x, y)
#         self.vel = pygame.math.Vector2(0, 0)
#         self.acc = pygame.math.Vector2(0, 0)
#         self.on_ground = False
#         self.lives = 3
#         self.score = 0
#         self.invincible_timer = 0
#
#     def jump(self):
#         if self.on_ground:
#             self.vel.y = -PLAYER_JUMP_STRENGTH
#             self.on_ground = False
#
#     def update(self, platforms):
#         if self.invincible_timer > 0:
#             self.invincible_timer -= 1
#             if self.invincible_timer % 10 < 5:
#                 self.image.set_alpha(128)
#             else:
#                 self.image.set_alpha(255)
#         else:
#             self.image.set_alpha(255)
#
#         self.acc = pygame.math.Vector2(0, PLAYER_GRAVITY)
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_LEFT] or keys[pygame.K_a]:
#             self.acc.x = -PLAYER_ACC
#         if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
#             self.acc.x = PLAYER_ACC
#
#         self.acc.x += self.vel.x * PLAYER_FRICTION
#         self.vel += self.acc
#         if abs(self.vel.x) < 0.1:
#             self.vel.x = 0
#
#         if self.vel.y > PLAYER_MAX_FALL_SPEED:
#             self.vel.y = PLAYER_MAX_FALL_SPEED
#
#         self.pos += self.vel + 0.5 * self.acc
#
#         self.rect.x = self.pos.x
#         self.collide_with_platforms(platforms, 'horizontal')
#
#         self.rect.y = self.pos.y
#         self.on_ground = False
#         self.collide_with_platforms(platforms, 'vertical')
#
#         if self.pos.x > SCREEN_WIDTH - self.rect.width:
#             self.pos.x = SCREEN_WIDTH - self.rect.width
#             self.vel.x = 0
#         if self.pos.x < 0:
#             self.pos.x = 0
#             self.vel.x = 0
#
#         if self.rect.top > SCREEN_HEIGHT:
#             return self.lose_life()
#         return None
#
#     def collide_with_platforms(self, platforms, direction):
#         hits = pygame.sprite.spritecollide(self, platforms, False)
#         if hits:
#             if direction == 'horizontal':
#                 if self.vel.x > 0:
#                     self.rect.right = hits[0].rect.left
#                 if self.vel.x < 0:
#                     self.rect.left = hits[0].rect.right
#                 self.pos.x = self.rect.x
#                 self.vel.x = 0
#
#             if direction == 'vertical':
#                 if self.vel.y > 0:
#                     self.rect.bottom = hits[0].rect.top
#                     self.on_ground = True
#                 if self.vel.y < 0:
#                     self.rect.top = hits[0].rect.bottom
#                 self.pos.y = self.rect.y
#                 self.vel.y = 0
#
#     def lose_life(self):
#         if self.invincible_timer == 0:
#             self.lives -= 1
#             self.invincible_timer = FPS * 2
#             current_level_data = LEVELS[current_level_index]
#             self.pos.x, self.pos.y = current_level_data["player_start"]
#             self.rect.topleft = self.pos  # Update rect position
#             self.vel = pygame.math.Vector2(0, 0)
#             if self.lives <= 0:
#                 return "game_over"
#         return None
#
#     def hit_enemy(self, enemy_rect):
#         if self.vel.y > 0 and self.rect.bottom < enemy_rect.centery + 5:
#             self.vel.y = -PLAYER_JUMP_STRENGTH / 2.5
#             return "stomp"
#         else:
#             return self.lose_life()
#
#
# class Platform(pygame.sprite.Sprite):
#     def __init__(self, x, y, width, height, color=BROWN):
#         super().__init__()
#         self.image = pygame.Surface((width, height))
#         self.image.fill(color)
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#
#
# class Enemy(pygame.sprite.Sprite):
#     def __init__(self, x, y, move_range_x=50):
#         super().__init__()
#         self.image = pygame.Surface((25, 25))
#         self.image.fill(RED)
#         # img = pygame.image.load("./assets/turtle for mario game.png")
#         # self.image.blit(img, (32,32))
#         # self.image = pygame.transform.scale(self.image, (35, 35))
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#         self.start_x = x
#         self.move_range_x = move_range_x
#         self.direction = 1
#         self.speed = 1
#
#     def update(self, platforms):
#         self.rect.x += self.speed * self.direction
#         if self.move_range_x > 0:
#             if self.rect.x > self.start_x + self.move_range_x or \
#                     self.rect.x < self.start_x - self.move_range_x:
#                 self.direction *= -1
#
#         hit_platforms = pygame.sprite.spritecollide(self, platforms, False)
#         for platform in hit_platforms:
#             if self.speed * self.direction > 0:
#                 self.rect.right = platform.rect.left
#             elif self.speed * self.direction < 0:
#                 self.rect.left = platform.rect.right
#             if self.move_range_x > 0:
#                 self.direction *= -1
#             break
#
#
# class Coin(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         self.image = pygame.Surface((15, 15))
#         self.image.fill(YELLOW)
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#
#
# class Goal(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         self.image = pygame.Surface((30, 50))
#         self.image.fill(BLUE)
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#
#
# # --- Level Data (12 Levels) ---
# LEVELS = [
#     {  # Level 1
#         "player_start": (50, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40), (200, SCREEN_HEIGHT - 150, 100, 20),
#             (400, SCREEN_HEIGHT - 250, 100, 20), (150, SCREEN_HEIGHT - 350, 150, 20),
#         ],
#         "enemies": [(300, SCREEN_HEIGHT - 65, 50)],
#         "coins": [(220, SCREEN_HEIGHT - 180), (420, SCREEN_HEIGHT - 280), (170, SCREEN_HEIGHT - 380)],
#         "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
#     },
#     {  # Level 2
#         "player_start": (50, 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40), (0, 150, 100, 20),
#             (150, 250, 100, 20), (300, 350, 100, 20),
#             (500, 250, 80, 20), (650, 150, 80, 20),
#         ],
#         "enemies": [(400, SCREEN_HEIGHT - 65, 80), (200, 225, 30)],
#         "coins": [(170, 220), (320, 320), (520, 220), (670, 120)],
#         "goal": (SCREEN_WIDTH - 80, 100)
#     },
#     {  # Level 3 - More verticality
#         "player_start": (50, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, 200, 40), (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 40, 200, 40),
#             (250, SCREEN_HEIGHT - 120, 50, 20), (350, SCREEN_HEIGHT - 200, 50, 20),
#             (450, SCREEN_HEIGHT - 280, 50, 20), (550, SCREEN_HEIGHT - 200, 50, 20),
#             (650, SCREEN_HEIGHT - 120, 50, 20),
#         ],
#         "enemies": [(450, SCREEN_HEIGHT - 305, 0)],
#         "coins": [(260, SCREEN_HEIGHT - 150), (360, SCREEN_HEIGHT - 230), (560, SCREEN_HEIGHT - 230)],
#         "goal": (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 90)
#     },
#     {  # Level 4 - Gaps
#         "player_start": (50, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, 150, 40), (250, SCREEN_HEIGHT - 60, 100, 20),
#             (450, SCREEN_HEIGHT - 80, 100, 20), (650, SCREEN_HEIGHT - 40, 150, 40),
#         ],
#         "enemies": [(280, SCREEN_HEIGHT - 85, 30), (480, SCREEN_HEIGHT - 105, 30)],
#         "coins": [(100, SCREEN_HEIGHT - 70), (270, SCREEN_HEIGHT - 90), (470, SCREEN_HEIGHT - 110)],
#         "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
#     },
#     {  # Level 5 - More enemies
#         "player_start": (50, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40), (100, SCREEN_HEIGHT - 140, 80, 20),
#             (300, SCREEN_HEIGHT - 180, 150, 20), (550, SCREEN_HEIGHT - 140, 80, 20),
#         ],
#         "enemies": [
#             (200, SCREEN_HEIGHT - 65, 50), (350, SCREEN_HEIGHT - 205, 60), (500, SCREEN_HEIGHT - 65, 50),
#         ],
#         "coins": [(120, SCREEN_HEIGHT - 170), (370, SCREEN_HEIGHT - 210), (570, SCREEN_HEIGHT - 170)],
#         "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
#     },
#     {  # Level 6 - Tricky jumps
#         "player_start": (30, 100),
#         "platforms": [
#             (0, 150, 80, 20), (200, 200, 50, 20), (350, 150, 50, 20),
#             (200, 350, 50, 20), (50, 450, SCREEN_WIDTH - 100, 20),
#             (SCREEN_WIDTH - 100, 100, 50, 20)
#         ],
#         "enemies": [(280, 425, 100), (450, 425, 100)],
#         "coins": [(210, 170), (360, 120), (210, 320), (SCREEN_WIDTH - 80, 70)],
#         "goal": (SCREEN_WIDTH - 80, 50)
#     },
#     {  # Level 7 - Final Challenge (Original)
#         "player_start": (50, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, 100, 40), (150, SCREEN_HEIGHT - 80, 50, 20),
#             (250, SCREEN_HEIGHT - 120, 50, 20), (350, SCREEN_HEIGHT - 160, 50, 20),
#             (450, SCREEN_HEIGHT - 120, 50, 20), (550, SCREEN_HEIGHT - 80, 50, 20),
#             (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 40, 100, 40),
#         ],
#         "enemies": [
#             (80, SCREEN_HEIGHT - 65, 0), (170, SCREEN_HEIGHT - 105, 0),
#             (270, SCREEN_HEIGHT - 145, 0), (470, SCREEN_HEIGHT - 145, 0),
#             (570, SCREEN_HEIGHT - 105, 0), (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 65, 0),
#         ],
#         "coins": [(160, SCREEN_HEIGHT - 110), (360, SCREEN_HEIGHT - 190), (560, SCREEN_HEIGHT - 110)],
#         "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
#     },
#     {  # Level 8: "The Ascent"
#         "player_start": (50, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, 150, 40),
#             (100, SCREEN_HEIGHT - 140, 70, 20), (50, SCREEN_HEIGHT - 240, 70, 20),
#             (150, SCREEN_HEIGHT - 340, 70, 20), (250, SCREEN_HEIGHT - 440, SCREEN_WIDTH - 250, 20),
#             (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, 100, 20),
#         ],
#         "enemies": [(300, SCREEN_HEIGHT - 465, 100), (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 125, 0)],
#         "coins": [(120, SCREEN_HEIGHT - 170), (70, SCREEN_HEIGHT - 270), (170, SCREEN_HEIGHT - 370),
#                   (400, SCREEN_HEIGHT - 470)],
#         "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 150)
#     },
#     {  # Level 9: "Corridor Run"
#         "player_start": (30, SCREEN_HEIGHT - 80),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
#             (150, SCREEN_HEIGHT - 120, 80, 20), (300, SCREEN_HEIGHT - 120, 80, 20),
#             (450, SCREEN_HEIGHT - 120, 80, 20), (600, SCREEN_HEIGHT - 120, 80, 20),
#         ],
#         "enemies": [
#             (100, SCREEN_HEIGHT - 65, 30), (250, SCREEN_HEIGHT - 65, 30),
#             (400, SCREEN_HEIGHT - 65, 30), (550, SCREEN_HEIGHT - 65, 30),
#             (350, SCREEN_HEIGHT - 145, 30)
#         ],
#         "coins": [(170, SCREEN_HEIGHT - 150), (320, SCREEN_HEIGHT - 150), (470, SCREEN_HEIGHT - 150),
#                   (620, SCREEN_HEIGHT - 150)],
#         "goal": (SCREEN_WIDTH - 60, SCREEN_HEIGHT - 90)
#     },
#     {  # Level 10: "Maze of Platforms"
#         "player_start": (50, 50),
#         "platforms": [
#             (0, 100, 100, 20), (150, 180, 100, 20), (0, 260, 100, 20),
#             (150, 340, 100, 20), (300, 100, 100, 20), (450, 180, 100, 20),
#             (300, 260, 100, 20), (600, 100, SCREEN_WIDTH - 600, 20),
#             (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
#         ],
#         "enemies": [(180, 155, 30), (50, 235, 0), (480, 155, 30)],
#         "coins": [(320, 230), (70, 70), (320, 70), (620, 70)],
#         "goal": (SCREEN_WIDTH - 80, 50)
#     },
#     {  # Level 11: "Enemy Gauntlet"
#         "player_start": (50, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
#             (100, SCREEN_HEIGHT - 150, 80, 20), (250, SCREEN_HEIGHT - 200, 300, 20),
#             (SCREEN_WIDTH - 180, SCREEN_HEIGHT - 150, 80, 20),
#         ],
#         "enemies": [
#             (150, SCREEN_HEIGHT - 65, 50), (250, SCREEN_HEIGHT - 65, 50),
#             (350, SCREEN_HEIGHT - 65, 50), (450, SCREEN_HEIGHT - 65, 50),
#             (300, SCREEN_HEIGHT - 225, 80), (450, SCREEN_HEIGHT - 225, 80),
#             (120, SCREEN_HEIGHT - 175, 0), (SCREEN_WIDTH - 160, SCREEN_HEIGHT - 175, 0)
#         ],
#         "coins": [(130, SCREEN_HEIGHT - 180), (390, SCREEN_HEIGHT - 230), (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 180)],
#         "goal": (SCREEN_WIDTH / 2 - 15, SCREEN_HEIGHT - 270)
#     },
#     {  # Level 12: "Final Leap"
#         "player_start": (30, SCREEN_HEIGHT - 100),
#         "platforms": [
#             (0, SCREEN_HEIGHT - 40, 100, 40), (200, SCREEN_HEIGHT - 80, 50, 20),
#             (350, SCREEN_HEIGHT - 120, 50, 20), (500, SCREEN_HEIGHT - 160, 50, 20),
#             (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 40, 100, 40),
#             (150, SCREEN_HEIGHT - 200, 20, 20), (600, SCREEN_HEIGHT - 250, 20, 20),
#         ],
#         "enemies": [
#             (215, SCREEN_HEIGHT - 105, 0), (365, SCREEN_HEIGHT - 145, 0),
#             (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 65, 50)
#         ],
#         "coins": [
#             (215, SCREEN_HEIGHT - 110), (365, SCREEN_HEIGHT - 150), (515, SCREEN_HEIGHT - 190),
#             (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 70)
#         ],
#         "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
#     }
# ]
#
#
# # --- Game Functions ---
# def load_level_sprites(level_data):
#     platforms = pygame.sprite.Group()
#     enemies = pygame.sprite.Group()
#     coins = pygame.sprite.Group()
#
#     for p_data in level_data["platforms"]:
#         platforms.add(Platform(*p_data))
#     for e_data in level_data["enemies"]:
#         enemies.add(Enemy(*e_data))
#     for c_data in level_data["coins"]:
#         coins.add(Coin(*c_data))
#
#     goal = Goal(*level_data["goal"])
#     return platforms, enemies, coins, goal
#
#
# def draw_text(surface, text, size, x, y, color=WHITE):
#     font = pygame.font.Font(None, size)
#     text_surface = font.render(text, True, color)
#     text_rect = text_surface.get_rect()
#     text_rect.midtop = (x, y)
#     surface.blit(text_surface, text_rect)
#
#
# def show_message_screen(screen, clock, message, sub_message="Press SPACE to continue"):
#     screen.fill(LIGHT_BLUE)
#     draw_text(screen, message, 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, BLACK)
#     draw_text(screen, sub_message, 32, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, BLACK)
#     pygame.display.flip()
#     waiting = True
#     while waiting:
#         clock.tick(FPS)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.KEYUP:
#                 if event.key == pygame.K_SPACE:
#                     waiting = False
#                 if event.key == pygame.K_ESCAPE and (
#                         "Game Over" in message or "You Win" in message or "Simple Platformer" in message):
#                     pygame.quit()
#                     sys.exit()
#
#
# # --- Game Initialization ---
# pygame.init()
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Simple Mario-like Game - 12 Levels")
# clock = pygame.time.Clock()
#
# # --- Game Variables ---
# current_level_index = 0
# game_state = "start_screen"
# player = None
# all_sprites = pygame.sprite.Group()
# platforms = pygame.sprite.Group()
# enemies = pygame.sprite.Group()
# coins = pygame.sprite.Group()
# goal = None
#
# game_player_lives = 3
# game_player_score = 0
#
# # --- Game Loop ---
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#         if game_state == "playing" and player:
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w:
#                     player.jump()
#
#         # Handle K_SPACE for specific state transitions (start, game over, game won)
#         # K_SPACE for level_complete is handled within its own state block now
#         if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
#             if game_state == "start_screen":
#                 game_state = "playing"
#                 current_level_index = 0
#                 game_player_lives = 3
#                 game_player_score = 0
#
#                 player = Player(*LEVELS[current_level_index]["player_start"])
#                 player.lives = game_player_lives
#                 player.score = game_player_score
#
#                 platforms, enemies, coins, goal = load_level_sprites(LEVELS[current_level_index])
#                 all_sprites.empty()
#                 all_sprites.add(player, platforms, enemies, coins, goal)
#
#             # REMOVED: K_SPACE handling for "level_complete" from here.
#
#             elif game_state == "game_over" or game_state == "game_won":
#                 game_state = "playing"
#                 current_level_index = 0
#                 game_player_lives = 3
#                 game_player_score = 0
#
#                 player = Player(*LEVELS[current_level_index]["player_start"])
#                 player.lives = game_player_lives
#                 player.score = game_player_score
#
#                 platforms, enemies, coins, goal = load_level_sprites(LEVELS[current_level_index])
#                 all_sprites.empty()
#                 all_sprites.add(player, platforms, enemies, coins, goal)
#
#         if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
#             if game_state == "start_screen" or game_state == "game_over" or game_state == "game_won":
#                 running = False
#
#                 # --- Game State Logic & Drawing ---
#
#     if game_state == "start_screen":
#         screen.fill(LIGHT_BLUE)
#         draw_text(screen, "Simple Platformer", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, BLACK)
#         draw_text(screen, "Press SPACE to Start", 32, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, BLACK)
#         draw_text(screen, "Press ESC to Quit", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.75, BLACK)
#
#     elif game_state == "playing":
#         if not player:
#             game_state = "start_screen"
#             continue
#
#         player_state_change = player.update(platforms)
#         if player_state_change == "game_over":
#             game_player_lives = player.lives
#             game_player_score = player.score
#             game_state = "game_over"
#             continue
#
#         enemies.update(platforms)
#
#         coin_hits = pygame.sprite.spritecollide(player, coins, True)
#         for coin in coin_hits:
#             player.score += 10
#         game_player_score = player.score
#
#         enemy_hits = pygame.sprite.spritecollide(player, enemies, False)
#         for enemy in enemy_hits:
#             if player.invincible_timer == 0:
#                 result = player.hit_enemy(enemy.rect)
#                 if result == "stomp":
#                     enemy.kill()
#                     player.score += 50
#                     game_player_score = player.score
#                 elif result == "game_over":
#                     game_player_lives = player.lives
#                     game_player_score = player.score
#                     game_state = "game_over"
#                     break
#             if game_state == "game_over": break
#         if game_state == "game_over": continue
#
#         if goal and pygame.sprite.collide_rect(player, goal):
#             game_player_lives = player.lives  # Persist for message screen
#             game_player_score = player.score  # Persist for message screen
#             game_state = "level_complete"
#             # current_level_index still points to the level just finished
#             # The next block 'elif game_state == "level_complete":' will handle showing the message
#             # and then transitioning.
#             # continue # Add continue to process the level_complete state in the same frame if desired
#             # or let it be handled in the next frame. For clarity, let next frame handle.
#
#         # Draw everything for playing state
#         screen.fill(LIGHT_BLUE)
#         all_sprites.draw(screen)
#
#         draw_text(screen, f"Score: {game_player_score}", 30, SCREEN_WIDTH / 2, 10, BLACK)
#         draw_text(screen, f"Lives: {player.lives if player else game_player_lives}", 30, 70, 10, BLACK)
#         draw_text(screen, f"Level: {current_level_index + 1}", 30, SCREEN_WIDTH - 70, 10, BLACK)
#
#     elif game_state == "level_complete":
#         # Display message for the level just completed (current_level_index refers to the finished level)
#         show_message_screen(screen, clock, f"Level {current_level_index + 1} Complete!",
#                             f"Score: {game_player_score} Lives: {game_player_lives}\nPress SPACE for Next Level")
#
#         # After show_message_screen returns (meaning SPACE was pressed):
#         current_level_index += 1  # Increment for the *next* level
#         if current_level_index < len(LEVELS):
#             game_state = "playing"
#             # Reset player and load sprites for the new current_level_index
#             player.pos = pygame.math.Vector2(*LEVELS[current_level_index]["player_start"])
#             player.rect.topleft = player.pos  # Update rect as well
#             player.vel = pygame.math.Vector2(0, 0)
#             player.on_ground = False
#             player.invincible_timer = 0
#
#             platforms, enemies, coins, goal = load_level_sprites(LEVELS[current_level_index])
#             all_sprites.empty()
#             all_sprites.add(player, platforms, enemies, coins, goal)
#         else:
#             game_state = "game_won"  # All levels done
#
#     elif game_state == "game_over":
#         show_message_screen(screen, clock, "Game Over!",
#                             f"Final Score: {game_player_score}\nPress SPACE to Restart or ESC to Quit")
#         # K_SPACE handling in the event loop will restart the game.
#
#     elif game_state == "game_won":
#         show_message_screen(screen, clock, "You Win! All Levels Cleared!",
#                             f"Final Score: {game_player_score}\nPress SPACE to Restart or ESC to Quit")
#         # K_SPACE handling in the event loop will restart the game.
#
#     pygame.display.flip()
#     clock.tick(FPS)
#
# pygame.quit()
# sys.exit()


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
            loaded_image = pygame.image.load("./assets/mario sprite.png").convert_alpha()
            self.image = pygame.transform.scale(loaded_image, (35, 35))
        except pygame.error as e:
            print(f"Warning: Could not load player image './assets/mario sprite.png': {e}")
            print("Falling back to default RED block for player.")
            self.image = pygame.Surface((30, 40))  # Fallback size from original code
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
            current_level_data = LEVELS[current_level_index]  # Access global current_level_index
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
            original_turtle_image = pygame.image.load("./assets/turtle for mario game.png").convert_alpha()
            # Scale the image
            self.image = pygame.transform.scale(original_turtle_image, (30, 30))
        except pygame.error as e:
            print(f"Warning: Could not load enemy image './assets/turtle for mario game.png': {e}")
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
            (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40), (200, SCREEN_HEIGHT - 150, 100, 20),
            (400, SCREEN_HEIGHT - 250, 100, 20), (150, SCREEN_HEIGHT - 350, 150, 20),
        ],
        "enemies": [(300, SCREEN_HEIGHT - 65, 50)],  # x, y, move_range_x
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
        "enemies": [(400, SCREEN_HEIGHT - 65, 80), (200, 225, 30)],
        "coins": [(170, 220), (320, 320), (520, 220), (670, 120)],
        "goal": (SCREEN_WIDTH - 80, 100)
    },
    {  # Level 3 - More verticality
        "player_start": (50, SCREEN_HEIGHT - 100),
        "platforms": [
            (0, SCREEN_HEIGHT - 40, 200, 40), (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 40, 200, 40),
            (250, SCREEN_HEIGHT - 120, 50, 20), (350, SCREEN_HEIGHT - 200, 50, 20),
            (450, SCREEN_HEIGHT - 280, 50, 20), (550, SCREEN_HEIGHT - 200, 50, 20),
            (650, SCREEN_HEIGHT - 120, 50, 20),
        ],
        "enemies": [(450, SCREEN_HEIGHT - 305, 0)],  # move_range_x = 0 means it turns at walls
        "coins": [(260, SCREEN_HEIGHT - 150), (360, SCREEN_HEIGHT - 230), (560, SCREEN_HEIGHT - 230)],
        "goal": (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 90)
    },
    {  # Level 4 - Gaps
        "player_start": (50, SCREEN_HEIGHT - 100),
        "platforms": [
            (0, SCREEN_HEIGHT - 40, 150, 40), (250, SCREEN_HEIGHT - 60, 100, 20),
            (450, SCREEN_HEIGHT - 80, 100, 20), (650, SCREEN_HEIGHT - 40, 150, 40),
        ],
        "enemies": [(280, SCREEN_HEIGHT - 85, 30), (480, SCREEN_HEIGHT - 105, 30)],
        "coins": [(100, SCREEN_HEIGHT - 70), (270, SCREEN_HEIGHT - 90), (470, SCREEN_HEIGHT - 110)],
        "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
    },
    {  # Level 5 - More enemies
        "player_start": (50, SCREEN_HEIGHT - 100),
        "platforms": [
            (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40), (100, SCREEN_HEIGHT - 140, 80, 20),
            (300, SCREEN_HEIGHT - 180, 150, 20), (550, SCREEN_HEIGHT - 140, 80, 20),
        ],
        "enemies": [
            (200, SCREEN_HEIGHT - 65, 50), (350, SCREEN_HEIGHT - 205, 60), (500, SCREEN_HEIGHT - 65, 50),
        ],
        "coins": [(120, SCREEN_HEIGHT - 170), (370, SCREEN_HEIGHT - 210), (570, SCREEN_HEIGHT - 170)],
        "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
    },
    {  # Level 6 - Tricky jumps
        "player_start": (30, 100),
        "platforms": [
            (0, 150, 80, 20), (200, 200, 50, 20), (350, 150, 50, 20),
            (200, 350, 50, 20), (50, 450, SCREEN_WIDTH - 100, 20),
            (SCREEN_WIDTH - 100, 100, 50, 20)
        ],
        "enemies": [(280, 425, 100), (450, 425, 100)],
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
            (80, SCREEN_HEIGHT - 65, 0), (170, SCREEN_HEIGHT - 105, 0),
            (270, SCREEN_HEIGHT - 145, 0), (470, SCREEN_HEIGHT - 145, 0),
            (570, SCREEN_HEIGHT - 105, 0), (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 65, 0),
        ],
        "coins": [(160, SCREEN_HEIGHT - 110), (360, SCREEN_HEIGHT - 190), (560, SCREEN_HEIGHT - 110)],
        "goal": (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 90)
    },
    {  # Level 8: "The Ascent"
        "player_start": (50, SCREEN_HEIGHT - 100),
        "platforms": [
            (0, SCREEN_HEIGHT - 40, 150, 40),
            (100, SCREEN_HEIGHT - 140, 70, 20), (50, SCREEN_HEIGHT - 240, 70, 20),
            (150, SCREEN_HEIGHT - 340, 70, 20), (250, SCREEN_HEIGHT - 440, SCREEN_WIDTH - 250, 20),
            (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, 100, 20),
        ],
        "enemies": [(300, SCREEN_HEIGHT - 465, 100), (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 125, 0)],
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
            (100, SCREEN_HEIGHT - 65, 30), (250, SCREEN_HEIGHT - 65, 30),
            (400, SCREEN_HEIGHT - 65, 30), (550, SCREEN_HEIGHT - 65, 30),
            (350, SCREEN_HEIGHT - 145, 30)
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
            (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
        ],
        "enemies": [(180, 155, 30), (50, 235, 0), (480, 155, 30)],
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
            (150, SCREEN_HEIGHT - 65, 50), (250, SCREEN_HEIGHT - 65, 50),
            (350, SCREEN_HEIGHT - 65, 50), (450, SCREEN_HEIGHT - 65, 50),
            (300, SCREEN_HEIGHT - 225, 80), (450, SCREEN_HEIGHT - 225, 80),
            (120, SCREEN_HEIGHT - 175, 0), (SCREEN_WIDTH - 160, SCREEN_HEIGHT - 175, 0)
        ],
        "coins": [(130, SCREEN_HEIGHT - 180), (390, SCREEN_HEIGHT - 230), (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 180)],
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
            (215, SCREEN_HEIGHT - 105, 0), (365, SCREEN_HEIGHT - 145, 0),
            (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 65, 50)
        ],
        "coins": [
            (215, SCREEN_HEIGHT - 110), (365, SCREEN_HEIGHT - 150), (515, SCREEN_HEIGHT - 190),
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
    draw_text(screen, sub_message, 32, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, BLACK)
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
                    player = Player(*LEVELS[current_level_index]["player_start"])
                    player.lives = game_player_lives
                    player.score = game_player_score

                    platforms, enemies, coins, goal = load_level_sprites(LEVELS[current_level_index])
                    all_sprites.empty()  # Clear previous sprites
                    all_sprites.add(player, platforms, enemies, coins, goal)

                elif game_state == "game_over" or game_state == "game_won":
                    # Restart game from level 1
                    game_state = "playing"
                    current_level_index = 0
                    game_player_lives = 3
                    game_player_score = 0

                    player = Player(*LEVELS[current_level_index]["player_start"])
                    player.lives = game_player_lives
                    player.score = game_player_score

                    platforms, enemies, coins, goal = load_level_sprites(LEVELS[current_level_index])
                    all_sprites.empty()
                    all_sprites.add(player, platforms, enemies, coins, goal)

            if event.key == pygame.K_ESCAPE:
                # Allow ESC to quit from start, game over, or game won screens
                if game_state == "start_screen" or game_state == "game_over" or game_state == "game_won":
                    running = False

    # --- Game State Logic & Drawing ---
    if game_state == "start_screen":
        screen.fill(LIGHT_BLUE)
        draw_text(screen, "Simple Platformer", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, BLACK)
        draw_text(screen, "Press SPACE to Start", 32, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, BLACK)
        draw_text(screen, "Press ESC to Quit", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.75, BLACK)

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
        coin_hits = pygame.sprite.spritecollide(player, coins, True)  # True to remove coin
        for coin in coin_hits:
            player.score += 10
        game_player_score = player.score  # Keep game_player_score updated

        # Check for enemy collisions
        if player.invincible_timer == 0:  # Only check if not invincible
            enemy_hits = pygame.sprite.spritecollide(player, enemies, False)  # False: don't kill enemy yet
            for enemy in enemy_hits:
                result = player.hit_enemy(enemy.rect)  # Player handles hit logic
                if result == "stomp":
                    enemy.kill()  # Remove stomped enemy
                    player.score += 50
                    game_player_score = player.score
                elif result == "game_over":
                    game_player_lives = player.lives
                    game_player_score = player.score
                    game_state = "game_over"
                    break  # Exit enemy collision loop
            if game_state == "game_over": continue  # Skip to next frame if game over

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
        all_sprites.draw(screen)  # Draw all sprites (player, platforms, enemies, coins, goal)

        # Draw HUD
        draw_text(screen, f"Score: {game_player_score}", 30, SCREEN_WIDTH / 2, 10, BLACK)
        draw_text(screen, f"Lives: {player.lives if player else game_player_lives}", 30, 70, 10, BLACK)
        draw_text(screen, f"Level: {current_level_index + 1}", 30, SCREEN_WIDTH - 70, 10, BLACK)

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
            player.pos = pygame.math.Vector2(*LEVELS[current_level_index]["player_start"])
            player.rect.topleft = player.pos
            player.vel = pygame.math.Vector2(0, 0)
            player.on_ground = False
            player.invincible_timer = 0  # Reset invincibility

            platforms, enemies, coins, goal = load_level_sprites(LEVELS[current_level_index])
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