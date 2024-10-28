import pygame
import random
import json
import os
import librosa

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("音樂節奏遊戲")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

CHINESE_FONT_PATH = "font.ttf"
FONT = pygame.font.Font(CHINESE_FONT_PATH, 36)

TRACKS = {'D': 0, 'F': 1, 'J': 2, 'K': 3}
KEYS = list(TRACKS.keys())
TRACK_WIDTH = SCREEN_WIDTH // len(TRACKS)

hit_sound = pygame.mixer.Sound("hit_sound.mp3")

def play_music(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(-1)

def load_high_score():
    if os.path.exists("high_score.json"):
        with open("high_score.json", "r") as file:
            data = json.load(file)
            return data.get("high_score", 0)
    else:
        return 0

def save_high_score(score):
    with open("high_score.json", "w") as file:
        json.dump({"high_score": score}, file)

def draw_text(text, size, color, x, y):
    font = pygame.font.Font(CHINESE_FONT_PATH, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def start_screen():
    screen.fill(WHITE)
    draw_text("按 Enter 開始遊戲", 48, BLACK, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

def game_over_screen(score, high_score):
    screen.fill(WHITE)
    draw_text(f"遊戲結束！您的分數: {score}", 36, BLACK, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
    draw_text(f"最高分數: {high_score}", 36, BLACK, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
    draw_text("按 R 重來遊戲", 36, BLACK, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False

class Block:
    def __init__(self, track, speed):
        self.track = track
        self.y = -50
        self.speed = speed
        self.active = True

    def move(self):
        self.y += self.speed

def main():
    clock = pygame.time.Clock()
    running = True
    blocks = []
    score = 0
    speed = 5
    miss_count = 0
    max_misses = 10
    high_score = load_high_score()

    play_music("music.mp3")

    hit_line_y = SCREEN_HEIGHT - 100

    start_screen()

    while running:
        screen.fill(WHITE)
        pressed_keys = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                key = event.unicode.upper()
                if key in TRACKS and len(pressed_keys) < 2:
                    pressed_keys.append(key)
                    track_index = TRACKS[key]
                    hit = False
                    for block in blocks:
                        if block.track == track_index and abs(block.y - hit_line_y) < 50:
                            block.active = False
                            score += 10
                            hit_sound.play()
                            hit = True
                            break
                    if not hit:
                        miss_count += 1

        blocks = [block for block in blocks if block.active and block.y < SCREEN_HEIGHT]
        for block in blocks:
            block.move()
            pygame.draw.rect(screen, BLACK, (block.track * TRACK_WIDTH, block.y, TRACK_WIDTH, 50))

        if random.random() < 0.03:
            track = random.choice(range(len(TRACKS)))
            blocks.append(Block(track, speed))

        pygame.draw.line(screen, BLACK, (0, hit_line_y), (SCREEN_WIDTH, hit_line_y), 2)

        score_text = FONT.render(f"Score: {score}", True, BLACK)
        miss_text = FONT.render(f"Misses: {miss_count}/{max_misses}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(miss_text, (10, 40))

        if miss_count >= max_misses:
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            game_over_screen(score, high_score)
            main()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
if __name__ == "__main__":
    main()
