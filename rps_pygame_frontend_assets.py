# rps_pygame_frontend_assets.py
import pygame
import time
import threading
import os
import math
import random

from RPS_game import (
    easy1, easy2, medium, medium2, markov_chain, random_bot
)
from graph import plot_graph

# ---------- Config ----------
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

# asset filenames (change if you use different names)
ASSET_BG = "background.png"
ASSET_ROCK = "rock.png"
ASSET_PAPER = "paper.png"
ASSET_SCISSORS = "scissors.png"
ASSET_CLICK = "click.wav"
ASSET_WIN = "win.wav"
ASSET_LOSE = "lose.wav"
ASSET_BGM = "bgm.mp3"
ASSET_FONT = "font.ttf"

# window
WIDTH, HEIGHT = 980, 680
FPS = 60

# UI sizes (auto scale with window later)
ICON_SIZE = (140, 140)
BUTTON_SIZE = (160, 60)

# ---------- Init ----------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors — Polished Frontend")

clock = pygame.time.Clock()

# fonts (try custom font)
def load_font(size):
    try:
        return pygame.font.Font(os.path.join(ASSETS_DIR, ASSET_FONT), size)
    except Exception:
        return pygame.font.SysFont(None, size)

FONT = load_font(22)
BIG = load_font(42)
SM = load_font(18)

# ---------- Asset loaders with fallbacks ----------
def load_image(name, fallback_surface=None):
    path = os.path.join(ASSETS_DIR, name)
    try:
        img = pygame.image.load(path).convert_alpha()
        return img
    except Exception as e:
        # fallback to provided surface or a placeholder rect
        if fallback_surface:
            return fallback_surface
        placeholder = pygame.Surface((100,100), pygame.SRCALPHA)
        placeholder.fill((160,160,160,220))
        pygame.draw.rect(placeholder, (80,80,80), placeholder.get_rect(), 4)
        return placeholder

def load_sound(name):
    path = os.path.join(ASSETS_DIR, name)
    try:
        snd = pygame.mixer.Sound(path)
        return snd
    except Exception:
        return None

def play_sound_if_loaded(snd):
    if snd:
        try:
            snd.play()
        except Exception:
            pass

# images
bg_img = load_image(ASSET_BG, fallback_surface=None)  # may be None/placeholder
rock_img = load_image(ASSET_ROCK)
paper_img = load_image(ASSET_PAPER)
scissors_img = load_image(ASSET_SCISSORS)

# sounds
click_snd = load_sound(ASSET_CLICK)
win_snd = load_sound(ASSET_WIN)
lose_snd = load_sound(ASSET_LOSE)

# background music (looped)
bgm_path = os.path.join(ASSETS_DIR, ASSET_BGM)
if os.path.exists(bgm_path):
    try:
        pygame.mixer.music.load(bgm_path)
        pygame.mixer.music.set_volume(0.45)
        pygame.mixer.music.play(-1)  # loop forever
    except Exception:
        pass

# ---------- Bot list ----------
BOT_LIST = [
    ("Easy 1", easy1),
    ("Easy 2", easy2),
    ("Medium 1", medium),
    ("Medium 2", medium2),
    ("Hard ", markov_chain),
    ("Random Bot", random_bot),
]

CHOICE_NAMES = {"R": "Rock", "P": "Paper", "S": "Scissors"}
CHOICE_TO_IMG = {"R": rock_img, "P": paper_img, "S": scissors_img}

# ---------- Helpers ----------
def scaled(img, w, h):
    try:
        return pygame.transform.smoothscale(img, (w, h))
    except Exception:
        return pygame.transform.scale(img, (w, h))

def center_rect_for(img, center):
    rect = img.get_rect()
    rect.center = center
    return rect

# Button class (supports image or color)
class UIButton:
    def __init__(self, rect, text="", image=None, rounded=8, base_color=(20,20,30), hover_color=(80,80,120)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.image = image
        self.rounded = rounded
        self.base_color = base_color
        self.hover_color = hover_color

    def draw(self, surf, mouse_pos):
        is_hover = self.rect.collidepoint(mouse_pos)
        color = self.hover_color if is_hover else self.base_color
        pygame.draw.rect(surf, color, self.rect, border_radius=self.rounded)
        if self.image:
            img = scaled(self.image, self.rect.width - 12, self.rect.height - 12)
            surf.blit(img, (self.rect.x + 6, self.rect.y + 6))
        if self.text:
            txt = FONT.render(self.text, True, (240,240,240))
            surf.blit(txt, (self.rect.x + (self.rect.width - txt.get_width())//2,
                            self.rect.y + (self.rect.height - txt.get_height())//2))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

# ---------- Simple confetti particle for win effect ----------
particles = []
def spawn_confetti(x, y, amount=40):
    for _ in range(amount):
        particles.append({
            "x": x,
            "y": y,
            "vx": random.uniform(-3,3),
            "vy": random.uniform(-6,-1),
            "life": random.uniform(0.6,1.6),
            "color": (random.randint(50,255), random.randint(50,255), random.randint(50,255))
        })

def update_particles(dt):
    alive = []
    for p in particles:
        p["vy"] += 9.8 * dt  # gravity
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["life"] -= dt
        if p["life"] > 0:
            alive.append(p)
    particles[:] = alive

def draw_particles(surf):
    for p in particles:
        r = max(1, int(4 * p["life"]))
        pygame.draw.circle(surf, p["color"], (int(p["x"]), int(p["y"])), r)

# ---------- Match runner (similar to previous) ----------
class MatchRunner:
    def __init__(self):
        self.reset_match()

    def reset_match(self):
        self.history = []
        self.results = {"p1":0, "p2":0, "tie":0}
        self.p1_prev = ""
        self.p2_prev = ""
        self.rounds_total = 5
        self.round_index = 0
        self.playing = False
        self.last_round = None  # (p1,p2,result)
        self.mode = "Human vs Bot"
        self.bot1_idx = 0
        self.bot2_idx = 1
        self.cpu_reveal_progress = 0.0  # for shake animation
        self.revealed_choice = None

    def reset_bot_states_if_needed(self):
        # reset markov_chain and other stateful bots by calling with empty prev
        for name, func in (BOT_LIST[self.bot1_idx], BOT_LIST[self.bot2_idx]):
            if func is markov_chain:
                try:
                    func('')
                except Exception:
                    pass

    def play_one_round(self, p1_func, p2_func, human_choice=None):
        # p1 is function that expects opponent previous; human_choice if present used as p1 play
        if human_choice is not None:
            p1_play = human_choice
        else:
            p1_play = p1_func(self.p2_prev)
        p2_play = p2_func(self.p1_prev)

        # decide winner
        if p1_play == p2_play:
            result = "tie"
            self.results["tie"] += 1
        else:
            wins = {("P","R"), ("R","S"), ("S","P")}
            if (p1_play, p2_play) in wins:
                result = "p1"
                self.results["p1"] += 1
            else:
                result = "p2"
                self.results["p2"] += 1

        self.history.append(result)
        self.last_round = (p1_play, p2_play, result)
        self.p1_prev, self.p2_prev = p2_play, p1_play
        self.round_index += 1

    def run_bot_vs_bot(self):
        self.playing = True
        self.reset_bot_states_if_needed()
        bot1_func = BOT_LIST[self.bot1_idx][1]
        bot2_func = BOT_LIST[self.bot2_idx][1]
        self.p1_prev = ""
        self.p2_prev = ""
        self.round_index = 0
        self.revealed_choice = None
        while self.playing and self.round_index < self.rounds_total:
            # "shake" for 0.6s visually, then reveal
            self.cpu_reveal_progress = 0.0
            # to visually show shaking we update progress in main thread; here we just sleep
            time.sleep(0.6)
            self.play_one_round(bot1_func, bot2_func)
            self.revealed_choice = self.last_round[1]
            time.sleep(0.4)
        self.playing = False

    def run_human_vs_bot_single(self, choice):
        # plays one human round instantly (called from UI)
        if not self.playing:
            return
        bot_func = BOT_LIST[self.bot2_idx][1]
        # simulate small delay for CPU reveal
        self.cpu_reveal_progress = 0.0
        time.sleep(0.25)
        self.play_one_round(lambda prev: choice, bot_func, human_choice=choice)

match = MatchRunner()

# ---------- UI elements creation ----------
# Positions
left_col_x = 40
right_col_x = 450

btn_play = UIButton((WIDTH - 350, HEIGHT - 120, 180, 56), text="Play Match")
btn_mode = UIButton((left_col_x, 50, 240, 44), text="Mode: Human vs Bot")

btn_bot1_left = UIButton((left_col_x, 120, 48, 44), text="<")
btn_bot1_right = UIButton((left_col_x + 160, 120, 48, 44), text=">")
btn_bot2_left = UIButton((left_col_x, 190, 48, 44), text="<")
btn_bot2_right = UIButton((left_col_x + 160, 190, 48, 44), text=">")

btn_rounds_minus = UIButton((left_col_x, 260, 48, 44), text="-")
btn_rounds_plus = UIButton((left_col_x + 160, 260, 48, 44), text="+")

btn_rock = UIButton((right_col_x + 20, 430, 150, 90), text="ROCK", image=rock_img)
btn_paper = UIButton((right_col_x + 190, 430, 150, 90), text="PAPER", image=paper_img)
btn_scissors = UIButton((right_col_x + 360, 430, 150, 90), text="SCISSORS", image=scissors_img)

# ---------- Utilities ----------
def start_bot_vs_bot_thread():
    if match.playing:
        return
    match.history = []
    match.results = {"p1":0, "p2":0, "tie":0}
    match.last_round = None
    match.p1_prev = ""
    match.p2_prev = ""
    match.round_index = 0
    t = threading.Thread(target=match.run_bot_vs_bot, daemon=True)
    t.start()

def end_match_and_plot_once():
    name1 = BOT_LIST[match.bot1_idx][0] if match.mode == "Bot vs Bot" else "You"
    name2 = BOT_LIST[match.bot2_idx][0]
    threading.Thread(target=plot_graph, args=(match.history, name1, name2), daemon=True).start()

# ---------- Main loop ----------
running = True
plot_triggered = False

while running:
    dt = clock.tick(FPS) / 1000.0
    mouse_pos = pygame.mouse.get_pos()

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if btn_play.clicked(event.pos):
                play_sound_if_loaded(click_snd)
                if match.mode == "Bot vs Bot":
                    start_bot_vs_bot_thread()
                else:
                    # start human match mode (just set playing True)
                    match.playing = True
                    match.history = []
                    match.results = {"p1":0, "p2":0, "tie":0}
                    match.p1_prev = ""
                    match.p2_prev = ""
                    match.round_index = 0
            elif btn_mode.clicked(event.pos):
                play_sound_if_loaded(click_snd)
                match.mode = "Bot vs Bot" if match.mode == "Human vs Bot" else "Human vs Bot"
                btn_mode.text = f"Mode: {match.mode}"
            elif btn_bot1_left.clicked(event.pos):
                play_sound_if_loaded(click_snd)
                match.bot1_idx = (match.bot1_idx - 1) % len(BOT_LIST)
            elif btn_bot1_right.clicked(event.pos):
                play_sound_if_loaded(click_snd)
                match.bot1_idx = (match.bot1_idx + 1) % len(BOT_LIST)
            elif btn_bot2_left.clicked(event.pos):
                play_sound_if_loaded(click_snd)
                match.bot2_idx = (match.bot2_idx - 1) % len(BOT_LIST)
            elif btn_bot2_right.clicked(event.pos):
                play_sound_if_loaded(click_snd)
                match.bot2_idx = (match.bot2_idx + 1) % len(BOT_LIST)
            elif btn_rounds_minus.clicked(event.pos):
                play_sound_if_loaded(click_snd)
                match.rounds_total = max(1, match.rounds_total - 1)
            elif btn_rounds_plus.clicked(event.pos):
                play_sound_if_loaded(click_snd)
                match.rounds_total = match.rounds_total + 1
            elif btn_rock.clicked(event.pos) and match.mode == "Human vs Bot":
                if match.playing and match.round_index < match.rounds_total:
                    play_sound_if_loaded(click_snd)
                    match.run_human_vs_bot_single("R")
                    # play reveal sound & confetti if win
                    if match.last_round:
                        if match.last_round[2] == "p1":
                            play_sound_if_loaded(win_snd)
                            spawn_confetti(WIDTH//2, HEIGHT//2)
                        elif match.last_round[2] == "p2":
                            play_sound_if_loaded(lose_snd)
                    if match.round_index >= match.rounds_total:
                        match.playing = False
                        plot_triggered = True
            elif btn_paper.clicked(event.pos) and match.mode == "Human vs Bot":
                if match.playing and match.round_index < match.rounds_total:
                    play_sound_if_loaded(click_snd)
                    match.run_human_vs_bot_single("P")
                    if match.last_round:
                        if match.last_round[2] == "p1":
                            play_sound_if_loaded(win_snd)
                            spawn_confetti(WIDTH//2, HEIGHT//2)
                        elif match.last_round[2] == "p2":
                            play_sound_if_loaded(lose_snd)
                    if match.round_index >= match.rounds_total:
                        match.playing = False
                        plot_triggered = True
            elif btn_scissors.clicked(event.pos) and match.mode == "Human vs Bot":
                if match.playing and match.round_index < match.rounds_total:
                    play_sound_if_loaded(click_snd)
                    match.run_human_vs_bot_single("S")
                    if match.last_round:
                        if match.last_round[2] == "p1":
                            play_sound_if_loaded(win_snd)
                            spawn_confetti(WIDTH//2, HEIGHT//2)
                        elif match.last_round[2] == "p2":
                            play_sound_if_loaded(lose_snd)
                    if match.round_index >= match.rounds_total:
                        match.playing = False
                        plot_triggered = True

    # Update animation state
    update_particles(dt)

    # Draw background
    screen.fill((18,20,28))
    if bg_img:
        try:
            b = scaled(bg_img, WIDTH, HEIGHT)
            screen.blit(b, (0,0))
        except Exception:
            pass

    # Left column (controls)
    screen_rect = screen.get_rect()
    draw_x = left_col_x = 40
    draw_y = 32

    title_surf = BIG.render("Rock • Paper • Scissors", True, (245,245,245))
    screen.blit(title_surf, (left_col_x, 6))

    btn_mode.draw(screen, mouse_pos)

    # Bot selectors
    draw_label = lambda txt, x, y: screen.blit(FONT.render(txt, True, (255,235,120)), (x,y))
    draw_label("Bot 1:", left_col_x, 120 - 24)
    btn_bot1_left.draw(screen, mouse_pos)
    btn_bot1_right.draw(screen, mouse_pos)
    draw_label(BOT_LIST[match.bot1_idx][0], left_col_x + 60, 126)

    draw_label("Bot 2:", left_col_x, 190 - 24)
    btn_bot2_left.draw(screen, mouse_pos)
    btn_bot2_right.draw(screen, mouse_pos)
    draw_label(BOT_LIST[match.bot2_idx][0], left_col_x + 60, 196)

    draw_label("Rounds:", left_col_x, 260 - 24)
    btn_rounds_minus.draw(screen, mouse_pos)
    btn_rounds_plus.draw(screen, mouse_pos)
    draw_label(str(match.rounds_total), left_col_x + 60, 266)

    PLAY_IDLE_COLOR = (40, 180, 40)      # green
    PLAY_ACTIVE_COLOR = (60, 60, 60) 
    if match.playing:
        btn_play.base_color = PLAY_ACTIVE_COLOR
        btn_play.hover_color = PLAY_ACTIVE_COLOR   # no hover during play
    else:
        btn_play.base_color = PLAY_IDLE_COLOR
        btn_play.hover_color = (70, 220, 70)       # lighter green on hover
    if match.playing:
        btn_play.text = "Playing..."
    else:
        btn_play.text = "Play Match"

    btn_play.draw(screen, mouse_pos)

    # Right column (game area)
    right_x = 480
    draw_label("Scores:", right_x, 80)
    draw_label(f"P1: {match.results['p1']}", right_x, 120)
    draw_label(f"P2: {match.results['p2']}", right_x, 150)
    draw_label(f"Ties: {match.results['tie']}", right_x, 180)

    # Last round display with icons and small shake for CPU reveal
    if match.last_round:
        p1_play, p2_play, result = match.last_round
        # left icon (P1)
        left_center = (right_x + 120, 270)
        right_center = (right_x + 340, 270)

        img1 = CHOICE_TO_IMG.get(p1_play)
        img2 = CHOICE_TO_IMG.get(p2_play)

        if img1:
            im1 = scaled(img1, 140, 140)
            screen.blit(im1, center_rect_for(im1, left_center))
        else:
            screen.blit(FONT.render(str(p1_play), True, (255,255,255)), left_center)

        # CPU "shake" effect before reveal: if playing and cpu_reveal_progress < 0.6
        if match.playing and match.mode == "Bot vs Bot":
            # show a blurred/rotated placeholder
            shake = math.sin(time.time()*30) * 6
            reveal_pos = (right_center[0] + shake, right_center[1])
            if img2:
                im2 = scaled(img2, 140, 140)
                screen.blit(im2, center_rect_for(im2, reveal_pos))
            else:
                screen.blit(FONT.render(str(p2_play), True, (255,255,255)), reveal_pos)
        else:
            if img2:
                im2 = scaled(img2, 140, 140)
                screen.blit(im2, center_rect_for(im2, right_center))
            else:
                screen.blit(FONT.render(str(p2_play), True, (255,255,255)), right_center)

        # result text
        res_txt = "Tie" if result == "tie" else ("P1 won" if result == "p1" else "P2 won")
        screen.blit(BIG.render(res_txt, True, (255,235,120)), (right_x + 160, 360))

    # Draw human control buttons if in Human mode
    if match.mode == "Human vs Bot":
        draw_label("Your Moves:", right_x, 400)
        btn_rock.draw(screen, mouse_pos)
        btn_paper.draw(screen, mouse_pos)
        btn_scissors.draw(screen, mouse_pos)

    # draw particles (confetti)
    draw_particles(screen)

    # If Bot vs Bot finished & not yet plotted, trigger plot
    if not match.playing and len(match.history) > 0 and plot_triggered is False:
        # trigger only once per finished match
        plot_triggered = True
        end_match_and_plot_once()
        # reset history so we don't re-plot unless new match
        match.history = []

    pygame.display.flip()

pygame.quit()
