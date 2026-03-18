"""
PokéTypes — Apprends les types Pokémon !
Pygame   |   pip install pygame
"""

import pygame
import sys
import math
import random

# ═══════════════════════════════════════════════════════════════════
#  INIT
# ═══════════════════════════════════════════════════════════════════
pygame.init()
WIDTH, HEIGHT = 960, 620
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PokéTypes — Apprends les types !")
clock = pygame.time.Clock()

# ── Fonts ──────────────────────────────────────────────────────────
def font(size, bold=False):
    for name in ["couriernew", "lucidaconsole", "consolas", "monospace"]:
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except Exception:
            pass
    return pygame.font.Font(None, size)

F_TITLE  = font(68, bold=True)
F_SUB    = font(17)
F_BTN    = font(24, bold=True)
F_LABEL  = font(15, bold=True)
F_TYPE   = font(22, bold=True)
F_SCORE  = font(20, bold=True)
F_FEED   = font(38, bold=True)
F_SMALL  = font(13)

# ── Palette ────────────────────────────────────────────────────────
BG_TOP   = (8,   8,  28)
BG_BOT   = (14, 14,  52)
WHITE    = (255, 255, 255)
GREY     = (140, 155, 175)
GOLD     = (255, 210,  55)
ACCENT   = ( 80, 200, 255)
ACCENT2  = (200,  80, 255)
RED_ERR  = (255,  70,  70)
GRN_OK   = ( 80, 220, 130)
DARK_PNL = ( 16,  18,  48)
BLACK    = (0 , 0, 0)

# ── Type colours & chart ────────────────────────────────────────────
TYPE_COL = {
    "Normal":   (168, 168, 120),
    "Feu":      (240, 100,  40),
    "Eau":      ( 80, 140, 240),
    "Plante":   ( 90, 190,  70),
    "Électrik": (248, 208,  40),
    "Glace":    (140, 210, 220),
    "Combat":   (200,  50,  40),
    "Poison":   (160,  64, 170),
    "Sol":      (220, 180,  60),
    "Vol":      (160, 140, 245),
    "Psy":      (248,  80, 140),
    "Insecte":  (160, 190,  30),
    "Roche":    (180, 155,  55),
    "Spectre":  (100,  80, 158),
    "Dragon":   (100,  50, 248),
    "Ténèbres": (100,  80,  72),
    "Acier":    (175, 180, 210),
    "Fée":      (235, 140, 175),
}
TYPES = list(TYPE_COL.keys())

# chart[attaque][défense] = multiplicateur  (défaut = 1.0)
TYPE_CHART = {
    "Normal":   {"Roche": 0.5, "Spectre": 0,   "Acier": 0.5},
    "Feu":      {"Feu": 0.5,   "Eau": 0.5,    "Plante": 2,   "Glace": 2,
                 "Insecte": 2, "Roche": 0.5,  "Dragon": 0.5, "Acier": 2},
    "Eau":      {"Feu": 2,     "Eau": 0.5,    "Plante": 0.5, "Sol": 2,
                 "Roche": 2,   "Dragon": 0.5},
    "Plante":   {"Feu": 0.5,   "Eau": 2,      "Plante": 0.5, "Poison": 0.5,
                 "Sol": 2,     "Vol": 0.5,    "Insecte": 0.5,"Roche": 2,
                 "Dragon": 0.5,"Acier": 0.5},
    "Électrik": {"Eau": 2,     "Plante": 0.5, "Électrik": 0.5,"Sol": 0,
                 "Vol": 2,     "Dragon": 0.5},
    "Glace":    {"Feu": 0.5,   "Eau": 0.5,    "Plante": 2,   "Glace": 0.5,
                 "Sol": 2,     "Vol": 2,      "Dragon": 2,   "Acier": 0.5},
    "Combat":   {"Normal": 2,  "Glace": 2,    "Poison": 0.5, "Vol": 0.5,
                 "Psy": 0.5,   "Insecte": 0.5,"Roche": 2,   "Spectre": 0,
                 "Ténèbres": 2,"Acier": 2,    "Fée": 0.5},
    "Poison":   {"Plante": 2,  "Poison": 0.5, "Sol": 0.5,    "Roche": 0.5,
                 "Spectre": 0.5,"Acier": 0,   "Fée": 2},
    "Sol":      {"Feu": 2,     "Électrik": 2, "Plante": 0.5, "Poison": 2,
                 "Vol": 0,     "Insecte": 0.5,"Roche": 2,   "Acier": 2},
    "Vol":      {"Électrik": 0.5,"Plante": 2, "Combat": 2,   "Insecte": 2,
                 "Roche": 0.5, "Acier": 0.5},
    "Psy":      {"Combat": 2,  "Poison": 2,   "Psy": 0.5,    "Ténèbres": 0,
                 "Acier": 0.5},
    "Insecte":  {"Feu": 0.5,   "Plante": 2,   "Combat": 0.5, "Poison": 0.5,
                 "Vol": 0.5,   "Psy": 2,      "Spectre": 0.5,"Ténèbres": 2,
                 "Acier": 0.5, "Fée": 0.5},
    "Roche":    {"Feu": 2,     "Glace": 2,    "Combat": 0.5, "Sol": 0.5,
                 "Vol": 2,     "Insecte": 2,  "Acier": 0.5},
    "Spectre":  {"Normal": 0,  "Psy": 2,      "Spectre": 2,  "Ténèbres": 0.5},
    "Dragon":   {"Dragon": 2,  "Acier": 0.5,  "Fée": 0},
    "Ténèbres": {"Combat": 0.5,"Psy": 2,      "Spectre": 2,  "Ténèbres": 0.5,
                 "Fée": 0.5},
    "Acier":    {"Feu": 0.5,   "Eau": 0.5,    "Électrik": 0.5,"Glace": 2,
                 "Roche": 2,   "Acier": 0.5,  "Fée": 2},
    "Fée":      {"Feu": 0.5,   "Combat": 2,   "Poison": 0.5, "Dragon": 2,
                 "Ténèbres": 2,"Acier": 0.5},
}

def get_effectiveness(atk, def_types):
    m = 1.0
    for d in def_types:
        m *= TYPE_CHART.get(atk, {}).get(d, 1.0)
    return m

MULTS      = [0, 0.25, 0.5, 1.0, 2.0, 4.0]
MULT_LABEL = {0: "×0", 0.25: "×0.25", 0.5: "×0.5", 1.0: "×1", 2.0: "×2", 4.0: "×4"}
MULT_COL   = {0: (90,90,110), 0.25:(200,70,70), 0.5:(210,120,50),
              1.0:(140,140,140), 2.0:(70,200,120), 4.0:(70,210,255)}

DIFF_CFG = {
    "FACILE":    {"dual": 0.0},   # toujours 1 type défense
    "NORMAL":    {"dual": 0.5},   # 50 % deux types
    "DIFFICILE": {"dual": 0.8},   # 80 % deux types
    "EXTREME":   {"dual": 1.0},   # toujours 2 types
}
DIFFICULTIES = ["FACILE", "NORMAL", "DIFFICILE", "EXTREME"]
DIFF_COLS    = [(80,220,120),(80,200,255),(255,160,60),(255,70,70)]

HIGH_SCORE = 48320

# ═══════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════
class Stars:
    def __init__(self, n=160):
        self.stars = []
        for _ in range(n):
            self.stars.append(self._make(random.randint(0, HEIGHT)))

    def _make(self, y=None):
        return [random.randint(0, WIDTH),
                y if y is not None else 0,
                random.uniform(0.4, 2.2),
                random.uniform(0.15, 0.9),
                random.randint(100, 255)]

    def update(self):
        for s in self.stars:
            s[1] += s[3]
            if s[1] > HEIGHT:
                s[:] = self._make()

    def draw(self, surf):
        for x, y, r, _, b in self.stars:
            pygame.draw.circle(surf, (b, b, b), (int(x), int(y)), int(r))

stars = Stars()

def draw_bg(surf):
    for y in range(HEIGHT):
        t = y / HEIGHT
        c = tuple(int(BG_TOP[i] + (BG_BOT[i]-BG_TOP[i])*t) for i in range(3))
        pygame.draw.line(surf, c, (0, y), (WIDTH, y))

def rounded_rect(surf, col, rect, r=10, border=0, border_col=None):
    pygame.draw.rect(surf, col, rect, border_radius=r)
    if border and border_col:
        pygame.draw.rect(surf, border_col, rect, width=border, border_radius=r)

def glow_rect(surf, col, rect, radius=10, glow=8, alpha_max=80):
    for g in range(glow, 0, -2):
        s = pygame.Surface((rect.w + g*4, rect.h + g*4), pygame.SRCALPHA)
        a = int(alpha_max * (g / glow))
        pygame.draw.rect(s, (*col, a), s.get_rect(), border_radius=radius+g)
        surf.blit(s, (rect.x - g*2, rect.y - g*2))

def type_badge(surf, type_name, cx, cy, w=160, h=50):
    col  = TYPE_COL.get(type_name, (128,128,128))
    dark = tuple(max(0, c - 60) for c in col)
    rect = pygame.Rect(cx - w//2, cy - h//2, w, h)
    glow_rect(surf, col, rect, radius=14, glow=10, alpha_max=100)
    rounded_rect(surf, dark, rect, r=14)
    rounded_rect(surf, col,  pygame.Rect(rect.x+2, rect.y+2, rect.w-4, rect.h-4), r=12)
    txt = F_TYPE.render(type_name.upper(), True, WHITE)
    surf.blit(txt, txt.get_rect(center=rect.center))


# ═══════════════════════════════════════════════════════════════════
#  BUTTON CLASS
# ═══════════════════════════════════════════════════════════════════
class Button:
    def __init__(self, cx, cy, w, h, label, accent=ACCENT, font=F_BTN):
        self.rect   = pygame.Rect(cx - w//2, cy - h//2, w, h)
        self.label  = label
        self.accent = accent
        self.font   = font
        self.hov    = False
        self.pulse  = random.uniform(0, 6.28)
        self.flash  = 0.0          # >0 = feedback flash
        self.flash_col = WHITE

    def update(self, mx, my, dt):
        self.hov    = self.rect.collidepoint(mx, my)
        self.pulse  = (self.pulse + dt * 3) % (2*math.pi)
        if self.flash > 0:
            self.flash = max(0, self.flash - dt * 3)

    def draw(self, surf, disabled=False):
        col = self.flash_col if self.flash > 0 else self.accent
        alpha = int(255 * self.flash)
        bg = (30, 40, 90) if self.hov and not disabled else (18, 22, 55)

        if self.hov and not disabled:
            glow_rect(surf, col, self.rect, glow=8, alpha_max=70)

        rounded_rect(surf, bg, self.rect, r=10)
        rounded_rect(surf, col, self.rect, r=10, border=2, border_col=col)

        if self.flash > 0:
            overlay = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            overlay.fill((*self.flash_col, int(120 * self.flash)))
            surf.blit(overlay, self.rect.topleft)

        txt_col = WHITE if (self.hov and not disabled) else GREY
        if disabled:
            txt_col = (60, 70, 90)
        txt = self.font.render(self.label, True, txt_col)
        surf.blit(txt, txt.get_rect(center=self.rect.center))

    def clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and self.rect.collidepoint(event.pos))

    def trigger_flash(self, col):
        self.flash     = 1.0
        self.flash_col = col


# ═══════════════════════════════════════════════════════════════════
#  MENU STATE
# ═══════════════════════════════════════════════════════════════════
diff_idx   = 1
high_score = HIGH_SCORE

btn_play = Button(WIDTH//2, 310, 290, 62, "▶  JOUER",    ACCENT)
btn_diff = Button(WIDTH//2, 392, 290, 52, "",            ACCENT2)
btn_quit = Button(WIDTH//2, 464, 290, 52, "✕  QUITTER",  (220,70,70))

def draw_menu_title(surf, t):
    text  = "PokéTypes"
    total = F_TITLE.size(text)[0]
    x     = WIDTH//2 - total//2
    for i, ch in enumerate(text):
        a  = t*2 + i*0.45
        c  = (int(128+127*math.sin(a)), int(128+127*math.sin(a+2.1)), int(128+127*math.sin(a+4.2)))
        cs = F_TITLE.render(ch, True, c)
        yo = int(6 * math.sin(t*2.5 + i*0.55))
        surf.blit(cs, (x, 80 + yo))
        x += cs.get_width()
    sub = F_SUB.render("Maîtrise des types — Attaque & Défense", True, GREY)
    surf.blit(sub, sub.get_rect(centerx=WIDTH//2, y=168))

def draw_highscore_panel(surf, t):
    pw, ph = 330, 74
    px = WIDTH//2 - pw//2
    py = 208
    p  = pygame.Surface((pw, ph), pygame.SRCALPHA)
    pygame.draw.rect(p, (20,20,60,185), (0,0,pw,ph), border_radius=12)
    ga = int(70+40*math.sin(t*2))
    pygame.draw.rect(p, (*GOLD, ga), (0,0,pw,ph), width=2, border_radius=12)
    surf.blit(p, (px, py))
    lbl = F_SMALL.render("🏆  MEILLEUR SCORE", True, GOLD)
    surf.blit(lbl, lbl.get_rect(centerx=WIDTH//2, y=py+9))
    val = F_SCORE.render(f"{high_score:,}".replace(",", " "), True, WHITE)
    surf.blit(val, val.get_rect(centerx=WIDTH//2, y=py+38))

def draw_menu(surf, t):
    draw_bg(surf)
    stars.draw(surf)
    draw_menu_title(surf, t)
    draw_highscore_panel(surf, t)
    btn_play.draw(surf)
    btn_diff.draw(surf)
    btn_quit.draw(surf)
    footer = F_SMALL.render("© 2026 PokéTypes Studio  |  v1.0", True, (55,65,95))
    surf.blit(footer, footer.get_rect(centerx=WIDTH//2, y=HEIGHT-20))


# ═══════════════════════════════════════════════════════════════════
#  GAME STATE
# ═══════════════════════════════════════════════════════════════════
MULT_BTN_W  = 118
MULT_BTN_H  = 56
MULT_BTN_Y  = 530
MULT_BTN_XS = [WIDTH//2 - (MULT_BTN_W + 12)*2.5 + (MULT_BTN_W + 12)*i
               for i in range(6)]

mult_buttons = [
    Button(int(MULT_BTN_XS[i]), MULT_BTN_Y, MULT_BTN_W, MULT_BTN_H,
           MULT_LABEL[m], MULT_COL[m])
    for i, m in enumerate(MULTS)
]

btn_menu = Button(60, 30, 110, 36, "← MENU", BLACK, F_SMALL)

# game vars
g_def_types   = []
g_atk_type    = ""
g_answer      = 1.0
g_score       = 0
g_streak      = 0
g_best_streak = 0
g_total       = 0
g_correct     = 0
g_feedback    = None   # None | "correct" | "wrong"
g_fb_timer    = 0.0
g_fb_msg      = ""
g_fb_col      = WHITE
g_anim_in     = 0.0   # 0→1 question enter animation
ANIM_SPEED    = 3.0

def new_question(difficulty):
    global g_def_types, g_atk_type, g_answer, g_feedback, g_anim_in
    dual_prob = DIFF_CFG[difficulty]["dual"]
    n_def = 2 if random.random() < dual_prob else 1
    # pick defense types (no duplicates)
    g_def_types = random.sample(TYPES, n_def)
    # pick attack type (any)
    g_atk_type  = random.choice(TYPES)
    g_answer    = get_effectiveness(g_atk_type, g_def_types)
    g_feedback  = None
    g_anim_in   = 0.0

def start_game(difficulty):
    global g_score, g_streak, g_best_streak, g_total, g_correct
    g_score = g_streak = g_best_streak = g_total = g_correct = 0
    new_question(difficulty)

def draw_panel(surf, label, cx, cy, types, t):
    """Draw a card panel for defense or attack side."""
    pw, ph = 340, 210
    px = cx - pw//2
    py = cy - ph//2

    # card bg with subtle glow
    card = pygame.Surface((pw, ph), pygame.SRCALPHA)
    pygame.draw.rect(card, (20, 22, 60, 210), (0, 0, pw, ph), border_radius=18)
    surf.blit(card, (px, py))

    # glowing border
    border_col = TYPE_COL.get(types[0], ACCENT) if types else ACCENT
    ga = int(100 + 40*math.sin(t*2))
    pygame.draw.rect(surf, (*border_col, ga),
                     pygame.Rect(px, py, pw, ph), width=2, border_radius=18)

    # label
    lbl = F_LABEL.render(label, True, GREY)
    surf.blit(lbl, lbl.get_rect(centerx=cx, y=py+14))

    # type badges
    if len(types) == 1:
        type_badge(surf, types[0], cx, cy + 10)
    elif len(types) == 2:
        type_badge(surf, types[0], cx, cy - 15)
        type_badge(surf, types[1], cx, cy + 52)

def draw_vs(surf, cx, cy, t):
    a = int(180 + 75*math.sin(t*3))
    col = (a, a//2, 255)
    vs = F_FEED.render("VS", True, col)
    surf.blit(vs, vs.get_rect(center=(cx, cy)))
    # lightning lines
    for dy in [-40, 40]:
        pygame.draw.line(surf, (*col, 120), (cx-6, cy+dy), (cx+6, cy+dy-20), 2)

def draw_score_bar(surf):
    acc = int(100 * g_correct / g_total) if g_total else 0
    txt = F_SCORE.render(
        f"Score : {g_score}  {g_streak}   Précision : {acc}%   Q.{g_total}",
        True, WHITE)
    surf.blit(txt, txt.get_rect(centerx=WIDTH//2, y=12))

def draw_feedback(surf):
    if not g_feedback:
        return
    alpha = int(255 * min(1, g_fb_timer * 2))
    s = pygame.Surface((WIDTH, 50), pygame.SRCALPHA)
    s.fill((*g_fb_col, min(60, alpha//2)))
    surf.blit(s, (0, HEIGHT//2 - 25))
    txt = F_FEED.render(g_fb_msg, True, (*g_fb_col, alpha))
    surf.blit(txt, txt.get_rect(center=(WIDTH//2, HEIGHT//2)))

def draw_game(surf, t, difficulty):
    draw_bg(surf)
    stars.draw(surf)

    # Entrance animation
    ease = min(1.0, g_anim_in)
    slide_y = int((1 - ease) * 60)

    # Score bar
    draw_score_bar(surf)

    # Panels
    def_cx = WIDTH//4
    atk_cx = 3*WIDTH//4
    panel_cy = 270 + slide_y

    draw_panel(surf, "ATTAQUE", atk_cx, panel_cy, [g_atk_type], t)
    draw_panel(surf, "DÉFENSE", def_cx, panel_cy, g_def_types,  t)
    draw_vs(surf, WIDTH//2, panel_cy, t)

    # Question prompt
    if g_def_types:
        q = F_LABEL.render("Quelle est l'efficacité de l'attaque sur la défense ?", True, GREY)
        surf.blit(q, q.get_rect(centerx=WIDTH//2, y=400))

    # Multiplier buttons
    waiting = (g_feedback is None)
    for i, btn in enumerate(mult_buttons):
        btn.draw(surf, disabled=not waiting)

    # Feedback overlay
    draw_feedback(surf)

    # Back button
    btn_menu.draw(surf)

    # Difficulty label top right
    diff_col = DIFF_COLS[DIFFICULTIES.index(difficulty)]
    d_txt = F_SMALL.render(f"Mode : {difficulty}", True, diff_col)
    surf.blit(d_txt, d_txt.get_rect(right=WIDTH-12, y=14))


# ═══════════════════════════════════════════════════════════════════
#  MAIN LOOP
# ═══════════════════════════════════════════════════════════════════
STATE       = "menu"
t           = 0.0
difficulty  = "NORMAL"

start_game(difficulty)  # pre-generate first question

while True:
    dt = clock.tick(60) / 1000.0
    t += dt
    mx, my = pygame.mouse.get_pos()

    # ── update diff button label
    btn_diff.label  = f"⚙  DIFF : {DIFFICULTIES[diff_idx]}"
    btn_diff.accent = DIFF_COLS[diff_idx]
    difficulty = DIFFICULTIES[diff_idx]

    # ─────────────────────────────────────────────────────────────
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if STATE == "game":
                STATE = "menu"
            else:
                pygame.quit(); sys.exit()

        # ── MENU events
        if STATE == "menu":
            if btn_play.clicked(event):
                start_game(difficulty)
                STATE = "game"
            if btn_diff.clicked(event):
                diff_idx = (diff_idx + 1) % len(DIFFICULTIES)
            if btn_quit.clicked(event):
                pygame.quit(); sys.exit()

        # ── GAME events
        elif STATE == "game":
            if btn_menu.clicked(event):
                STATE = "menu"

            # answer buttons – only if not in feedback pause
            if g_feedback is None:
                for i, btn in enumerate(mult_buttons):
                    if btn.clicked(event):
                        chosen = MULTS[i]
                        g_total += 1
                        if chosen == g_answer:
                            g_correct += 1
                            g_streak  += 1
                            g_best_streak = max(g_best_streak, g_streak)
                            pts = int(100 * (1 + 0.5*g_streak))
                            g_score += pts
                            g_feedback = "correct"
                            g_fb_msg   = f"✓  CORRECT !  +{pts} pts"
                            g_fb_col   = GRN_OK
                            btn.trigger_flash(GRN_OK)
                        else:
                            g_streak  = 0
                            g_feedback = "wrong"
                            # show correct answer label
                            correct_lbl = MULT_LABEL[g_answer]
                            g_fb_msg = f"✗  C'était {correct_lbl}"
                            g_fb_col = RED_ERR
                            btn.trigger_flash(RED_ERR)
                            # green flash on correct button
                            mult_buttons[MULTS.index(g_answer)].trigger_flash(GRN_OK)
                        g_fb_timer = 1.0

    # ─────────────────────────────────────────────────────────────
    # update
    stars.update()

    if STATE == "menu":
        btn_play.update(mx, my, dt)
        btn_diff.update(mx, my, dt)
        btn_quit.update(mx, my, dt)

    elif STATE == "game":
        g_anim_in += dt * ANIM_SPEED
        btn_menu.update(mx, my, dt)
        for b in mult_buttons:
            b.update(mx, my, dt)

        # feedback countdown
        if g_feedback is not None:
            g_fb_timer -= dt
            if g_fb_timer <= 0:
                g_feedback = None
                new_question(difficulty)

    # ─────────────────────────────────────────────────────────────
    # draw
    if STATE == "menu":
        draw_menu(screen, t)
    else:
        draw_game(screen, t, difficulty)

    pygame.display.flip()