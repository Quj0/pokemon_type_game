"""
PokéTypes — Apprends les types Pokémon !
pip install pygame
Mets type_chart.png dans le même dossier que ce fichier.
"""

import pygame
import sys
import math
import random
import array
import os

# ═══════════════════════════════════════════════════════════════════
#  INIT
# ═══════════════════════════════════════════════════════════════════
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

WIDTH, HEIGHT = 980, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PokéTypes — Apprends les types !")
clock = pygame.time.Clock()

# ── Fonts ──────────────────────────────────────────────────────────
def mkfont(size, bold=False):
    for name in ["couriernew", "lucidaconsole", "consolas", "monospace"]:
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except Exception:
            pass
    return pygame.font.Font(None, size)

F_TITLE = mkfont(68, bold=True)
F_SUB   = mkfont(17)
F_BTN   = mkfont(24, bold=True)
F_LABEL = mkfont(15, bold=True)
F_TYPE  = mkfont(22, bold=True)
F_SCORE = mkfont(20, bold=True)
F_FEED  = mkfont(38, bold=True)
F_SMALL = mkfont(13)
F_BIG   = mkfont(46, bold=True)
F_MED   = mkfont(28, bold=True)

# ── Palette ────────────────────────────────────────────────────────
BG_TOP   = (8,   8,  28)
BG_BOT   = (14, 14,  52)
WHITE    = (255, 255, 255)
BLACK    = (0, 0, 0)
GREY     = (140, 155, 175)
GOLD     = (255, 210,  55)
ACCENT   = ( 80, 200, 255)
ACCENT2  = (200,  80, 255)
RED_ERR  = (255,  70,  70)
GRN_OK   = ( 80, 220, 130)
HEART_R  = (255,  60,  90)
HEART_G  = ( 55,  55,  75)

# ── Type colours ───────────────────────────────────────────────────
TYPE_COL = {
    "Normal":   (168, 168, 120),
    "Feu":      (240, 100,  40),
    "Eau":      ( 80, 140, 240),
    "Plante":   ( 90, 190,  70),
    "Electrik": (248, 208,  40),
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
    "Tenebres": (100,  80,  72),
    "Acier":    (175, 180, 210),
    "Fee":      (235, 140, 175),
}
TYPES = list(TYPE_COL.keys())

# Full Type Chart Gen6+ — ATTACK -> {DEFENSE: multiplier}
TYPE_CHART = {
    "Normal":   {"Roche": 0.5,  "Spectre": 0,    "Acier": 0.5},
    "Feu":      {"Feu": 0.5,    "Eau": 0.5,      "Plante": 2,    "Glace": 2,
                 "Insecte": 2,  "Roche": 0.5,    "Dragon": 0.5,  "Acier": 2},
    "Eau":      {"Feu": 2,      "Eau": 0.5,      "Plante": 0.5,  "Sol": 2,
                 "Roche": 2,    "Dragon": 0.5},
    "Electrik": {"Eau": 2,      "Electrik": 0.5, "Plante": 0.5,  "Sol": 0,
                 "Vol": 2,      "Dragon": 0.5},
    "Plante":   {"Feu": 0.5,    "Eau": 2,        "Plante": 0.5,  "Poison": 0.5,
                 "Sol": 2,      "Vol": 0.5,      "Insecte": 0.5, "Roche": 2,
                 "Dragon": 0.5, "Acier": 0.5},
    "Glace":    {"Feu": 0.5,    "Eau": 0.5,      "Plante": 2,    "Glace": 0.5,
                 "Sol": 2,      "Vol": 2,        "Dragon": 2,    "Acier": 0.5},
    "Combat":   {"Normal": 2,   "Glace": 2,      "Poison": 0.5,  "Vol": 0.5,
                 "Psy": 0.5,    "Insecte": 0.5,  "Roche": 2,     "Spectre": 0,
                 "Tenebres": 2, "Acier": 2,      "Fee": 0.5},
    "Poison":   {"Plante": 2,   "Poison": 0.5,   "Sol": 0.5,     "Roche": 0.5,
                 "Spectre": 0.5,"Acier": 0,      "Fee": 2},
    "Sol":      {"Feu": 2,      "Electrik": 2,   "Plante": 0.5,  "Poison": 2,
                 "Vol": 0,      "Insecte": 0.5,  "Roche": 2,     "Acier": 2},
    "Vol":      {"Electrik": 0.5,"Plante": 2,    "Combat": 2,    "Insecte": 2,
                 "Roche": 0.5,  "Acier": 0.5},
    "Psy":      {"Combat": 2,   "Poison": 2,     "Psy": 0.5,     "Tenebres": 0,
                 "Acier": 0.5},
    "Insecte":  {"Feu": 0.5,    "Plante": 2,     "Combat": 0.5,  "Poison": 0.5,
                 "Vol": 0.5,    "Psy": 2,        "Spectre": 0.5, "Tenebres": 2,
                 "Acier": 0.5,  "Fee": 0.5},
    "Roche":    {"Feu": 2,      "Glace": 2,      "Combat": 0.5,  "Sol": 0.5,
                 "Vol": 2,      "Insecte": 2,    "Acier": 0.5},
    "Spectre":  {"Normal": 0,   "Psy": 2,        "Spectre": 2,   "Tenebres": 0.5},
    "Dragon":   {"Dragon": 2,   "Acier": 0.5,    "Fee": 0},
    "Tenebres": {"Combat": 0.5, "Psy": 2,        "Spectre": 2,   "Tenebres": 0.5,
                 "Fee": 0.5},
    "Acier":    {"Feu": 0.5,    "Eau": 0.5,      "Electrik": 0.5,"Glace": 2,
                 "Roche": 2,    "Acier": 0.5,    "Fee": 2},
    "Fee":      {"Feu": 0.5,    "Combat": 2,     "Poison": 0.5,  "Dragon": 2,
                 "Tenebres": 2, "Acier": 0.5},
}

# Display names (with accents, for rendering)
TYPE_DISPLAY = {
    "Normal":"Normal","Feu":"Feu","Eau":"Eau","Plante":"Plante",
    "Electrik":"Electrik","Glace":"Glace","Combat":"Combat","Poison":"Poison",
    "Sol":"Sol","Vol":"Vol","Psy":"Psy","Insecte":"Insecte","Roche":"Roche",
    "Spectre":"Spectre","Dragon":"Dragon","Tenebres":"Tenebres",
    "Acier":"Acier","Fee":"Fee",
}

def get_effectiveness(atk, def_types):
    m = 1.0
    for d in def_types:
        m *= TYPE_CHART.get(atk, {}).get(d, 1.0)
    return m

MULTS      = [0, 0.25, 0.5, 1.0, 2.0, 4.0]
MULT_LABEL = {0:"x0", 0.25:"x0.25", 0.5:"x0.5", 1.0:"x1", 2.0:"x2", 4.0:"x4"}
MULT_COL   = {
    0:    (90, 90,110),
    0.25: (200,70, 70),
    0.5:  (210,120,50),
    1.0:  (140,140,140),
    2.0:  (70, 200,120),
    4.0:  (70, 210,255),
}

DIFFICULTIES = ["FACILE", "NORMAL", "DIFFICILE", "EXTREME"]
DIFF_COLS    = [(80,220,120),(80,200,255),(255,160,60),(255,70,70)]
DIFF_CFG     = {
    "FACILE":    {"dual": 0.0},
    "NORMAL":    {"dual": 0.5},
    "DIFFICILE": {"dual": 0.8},
    "EXTREME":   {"dual": 1.0},
}
MAX_LIVES = 3

# ═══════════════════════════════════════════════════════════════════
#  SOUND SYNTHESIS  (no external files needed)
# ═══════════════════════════════════════════════════════════════════
SAMPLE_RATE = 44100

def make_sound(seq, vol=0.35, wave="sine"):
    """seq = list of (freq_hz, duration_ms)"""
    total_ms = sum(d for _, d in seq)
    n = int(SAMPLE_RATE * total_ms / 1000)
    buf = array.array("h", [0] * n)
    pos = 0
    for freq, dur_ms in seq:
        seg = int(SAMPLE_RATE * dur_ms / 1000)
        for i in range(min(seg, n - pos)):
            t = i / SAMPLE_RATE
            fade = 1.0
            if i < seg * 0.05:
                fade = i / max(1, seg * 0.05)
            elif i > seg * 0.75:
                fade = (seg - i) / max(1, seg * 0.25)
            if wave == "sine":
                v = math.sin(2 * math.pi * freq * t)
            else:  # square
                v = 1.0 if math.sin(2 * math.pi * freq * t) >= 0 else -1.0
            buf[pos + i] = int(v * fade * vol * 32767)
        pos += seg
    try:
        return pygame.sndarray.make_sound(buf)
    except Exception:
        return None

SFX_CLICK    = make_sound([(700, 35), (900, 35)],            vol=0.2)
SFX_CORRECT  = make_sound([(523,80),(659,80),(784,160)],      vol=0.3)
SFX_WRONG    = make_sound([(280,110),(200,230)],              vol=0.35, wave="square")
SFX_LOSE_HP  = make_sound([(180,130),(130,260)],              vol=0.38, wave="square")
SFX_GAMEOVER = make_sound([(392,120),(349,120),(330,130),(262,420)], vol=0.38)

def play(sfx):
    try:
        if sfx: sfx.play()
    except Exception:
        pass

# ═══════════════════════════════════════════════════════════════════
#  STARS
# ═══════════════════════════════════════════════════════════════════
class Stars:
    def __init__(self, n=170):
        self.data = [[random.randint(0,WIDTH), random.randint(0,HEIGHT),
                      random.uniform(0.4,2.2), random.uniform(0.15,0.9),
                      random.randint(100,255)] for _ in range(n)]
    def update(self):
        for s in self.data:
            s[1] += s[3]
            if s[1] > HEIGHT:
                s[0]=random.randint(0,WIDTH); s[1]=0
                s[2]=random.uniform(0.4,2.2); s[4]=random.randint(100,255)
    def draw(self, surf):
        for x,y,r,_,b in self.data:
            pygame.draw.circle(surf,(b,b,b),(int(x),int(y)),int(r))

stars = Stars()

# ═══════════════════════════════════════════════════════════════════
#  DRAW HELPERS
# ═══════════════════════════════════════════════════════════════════
def draw_bg(surf):
    for y in range(HEIGHT):
        t = y / HEIGHT
        c = tuple(int(BG_TOP[i] + (BG_BOT[i]-BG_TOP[i])*t) for i in range(3))
        pygame.draw.line(surf, c, (0,y), (WIDTH,y))

def rr(surf, col, rect, r=10, bw=0, bc=None):
    pygame.draw.rect(surf, col, rect, border_radius=r)
    if bw and bc:
        pygame.draw.rect(surf, bc, rect, width=bw, border_radius=r)

def glow_rect(surf, col, rect, radius=10, glow=8, alpha_max=80):
    for g in range(glow, 0, -2):
        s = pygame.Surface((rect.w+g*4, rect.h+g*4), pygame.SRCALPHA)
        a = int(alpha_max*(g/glow))
        pygame.draw.rect(s, (*col,a), s.get_rect(), border_radius=radius+g)
        surf.blit(s, (rect.x-g*2, rect.y-g*2))

def type_badge(surf, type_key, cx, cy, w=155, h=48):
    col  = TYPE_COL.get(type_key, (128,128,128))
    dark = tuple(max(0,c-60) for c in col)
    rect = pygame.Rect(cx-w//2, cy-h//2, w, h)
    glow_rect(surf, col, rect, radius=14, glow=10, alpha_max=90)
    rr(surf, dark, rect, r=14)
    rr(surf, col, pygame.Rect(rect.x+2,rect.y+2,rect.w-4,rect.h-4), r=12)
    txt = F_TYPE.render(type_key.upper(), True, WHITE)
    surf.blit(txt, txt.get_rect(center=rect.center))

def draw_heart(surf, cx, cy, filled, size=22):
    col = HEART_R if filled else HEART_G
    r = size // 2
    pygame.draw.circle(surf, col, (cx - r//2, cy - r//4), r//2 + 2)
    pygame.draw.circle(surf, col, (cx + r//2, cy - r//4), r//2 + 2)
    pts = [(cx-r, cy-r//5), (cx, cy+r), (cx+r, cy-r//5)]
    pygame.draw.polygon(surf, col, pts)

# ═══════════════════════════════════════════════════════════════════
#  BUTTON
# ═══════════════════════════════════════════════════════════════════
class Button:
    def __init__(self, cx, cy, w, h, label, accent=ACCENT, fnt=None):
        self.rect   = pygame.Rect(cx-w//2, cy-h//2, w, h)
        self.label  = label
        self.accent = accent
        self.fnt    = fnt or F_BTN
        self.hov    = False
        self.pulse  = random.uniform(0, 6.28)
        self.flash  = 0.0
        self.fcol   = WHITE

    def update(self, mx, my, dt):
        self.hov   = self.rect.collidepoint(mx,my)
        self.pulse = (self.pulse + dt*3) % (2*math.pi)
        if self.flash > 0:
            self.flash = max(0, self.flash - dt*3)

    def draw(self, surf, disabled=False):
        col = self.fcol if self.flash > 0 else self.accent
        bg  = (30,40,90) if (self.hov and not disabled) else (18,22,55)
        if self.hov and not disabled:
            glow_rect(surf, col, self.rect, glow=8, alpha_max=70)
        rr(surf, bg,  self.rect, r=10)
        rr(surf, col, self.rect, r=10, bw=2, bc=col)
        if self.flash > 0:
            ov = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            ov.fill((*self.fcol, int(110*self.flash)))
            surf.blit(ov, self.rect.topleft)
        tc = WHITE if (self.hov and not disabled) else BLACK
        if disabled: tc = (60,70,90)
        t = self.fnt.render(self.label, True, tc)
        surf.blit(t, t.get_rect(center=self.rect.center))

    def clicked(self, event):
        return (event.type==pygame.MOUSEBUTTONDOWN
                and event.button==1
                and self.rect.collidepoint(event.pos))

    def trigger_flash(self, col):
        self.flash = 1.0; self.fcol = col

# ═══════════════════════════════════════════════════════════════════
#  TYPE CHART IMAGE
# ═══════════════════════════════════════════════════════════════════
CHART_IMG = None
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
for candidate in [os.path.join(SCRIPT_DIR,"type_chart.png"), "type_chart.png"]:
    if os.path.exists(candidate):
        try:
            raw = pygame.image.load(candidate).convert_alpha()
            iw, ih = raw.get_size()
            margin = 50
            scale  = min((WIDTH-margin*2)/iw, (HEIGHT-margin*2)/ih)
            CHART_IMG = pygame.transform.smoothscale(
                raw, (int(iw*scale), int(ih*scale)))
        except Exception:
            pass
        break

# ═══════════════════════════════════════════════════════════════════
#  MENU BUTTONS
# ═══════════════════════════════════════════════════════════════════
diff_idx   = 1
high_score = 0

btn_play = Button(WIDTH//2, 315, 290, 62, "Jouer",    ACCENT)
btn_diff = Button(WIDTH//2, 397, 290, 52, "",          ACCENT2)
btn_quit = Button(WIDTH//2, 469, 290, 52, "Quitter",  (220,70,70))

# ── Game screen buttons ───────────────────────────────────────────
MULT_W, MULT_H = 118, 54
MULT_Y   = HEIGHT - 40
MULT_XS  = [WIDTH//2 - (MULT_W+10)*2.5 + (MULT_W+10)*i for i in range(6)]
mult_btns = [Button(int(MULT_XS[i]), MULT_Y, MULT_W, MULT_H,
                    MULT_LABEL[m], MULT_COL[m]) for i,m in enumerate(MULTS)]

btn_back = Button(55,  28, 100, 34, "<- Menu", GREY,       F_SMALL)
btn_help = Button(55, HEIGHT-40, 110, 38, "? AIDE",  (180,120,255), F_SMALL)

# ── Game over buttons ─────────────────────────────────────────────
btn_retry = Button(WIDTH//2, 435, 260, 58, "Rejouer",  GRN_OK)
btn_menu2 = Button(WIDTH//2, 510, 260, 50, "<- Menu",  GREY)

# ═══════════════════════════════════════════════════════════════════
#  GAME VARIABLES
# ═══════════════════════════════════════════════════════════════════
g_def_types=[]; g_atk_type=""; g_answer=1.0
g_score=0; g_streak=0; g_best_streak=0
g_total=0; g_correct=0; g_lives=MAX_LIVES
g_feedback=None; g_fb_timer=0.0; g_fb_msg=""; g_fb_col=WHITE
g_anim_in=0.0

def new_question(difficulty):
    global g_def_types, g_atk_type, g_answer, g_feedback, g_anim_in
    dual_prob = DIFF_CFG[difficulty]["dual"]
    n_def = 2 if random.random() < dual_prob else 1
    g_def_types = random.sample(TYPES, n_def)
    g_atk_type  = random.choice(TYPES)
    g_answer    = get_effectiveness(g_atk_type, g_def_types)
    g_feedback  = None
    g_anim_in   = 0.0

def start_game(difficulty):
    global g_score,g_streak,g_best_streak,g_total,g_correct,g_lives
    g_score=g_streak=g_best_streak=g_total=g_correct=0
    g_lives=MAX_LIVES
    new_question(difficulty)

# ═══════════════════════════════════════════════════════════════════
#  SCREEN DRAW FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

# ── MENU ──────────────────────────────────────────────────────────
def draw_menu(surf, t):
    draw_bg(surf); stars.draw(surf)

    # Animated title
    text = "PokéTypes"
    total = F_TITLE.size(text)[0]
    x = WIDTH//2 - total//2
    for i, ch in enumerate(text):
        a  = t*2 + i*0.45
        c  = (int(128+127*math.sin(a)),
              int(128+127*math.sin(a+2.1)),
              int(128+127*math.sin(a+4.2)))
        cs = F_TITLE.render(ch, True, c)
        yo = int(6*math.sin(t*2.5+i*0.55))
        surf.blit(cs, (x, 80+yo)); x += cs.get_width()

    sub = F_SUB.render("Maitrise des types -- Attaque & Defense", True, GREY)
    surf.blit(sub, sub.get_rect(centerx=WIDTH//2, y=168))

    # Highscore panel
    pw,ph=330,74; px=WIDTH//2-pw//2; py=210
    p=pygame.Surface((pw,ph),pygame.SRCALPHA)
    pygame.draw.rect(p,(20,20,60,185),(0,0,pw,ph),border_radius=12)
    ga=int(70+40*math.sin(t*2))
    pygame.draw.rect(p,(*GOLD,ga),(0,0,pw,ph),width=2,border_radius=12)
    surf.blit(p,(px,py))
    lbl=F_SMALL.render("Meilleur score", True, GOLD)
    surf.blit(lbl, lbl.get_rect(centerx=WIDTH//2, y=py+9))
    val=F_SCORE.render(str(high_score), True, WHITE)
    surf.blit(val, val.get_rect(centerx=WIDTH//2, y=py+36))

    btn_play.draw(surf); btn_diff.draw(surf); btn_quit.draw(surf)

    footer=F_SMALL.render("(c) 2025 PokeTypes Studio  |  v2.0", True, (55,65,95))
    surf.blit(footer, footer.get_rect(centerx=WIDTH//2, y=HEIGHT-20))

# ── GAME ──────────────────────────────────────────────────────────
def draw_panel(surf, label, cx, cy, types, t):
    pw,ph=330,200; px=cx-pw//2; py=cy-ph//2
    card=pygame.Surface((pw,ph),pygame.SRCALPHA)
    pygame.draw.rect(card,(20,22,60,210),(0,0,pw,ph),border_radius=18)
    surf.blit(card,(px,py))
    bc = TYPE_COL.get(types[0], ACCENT) if types else ACCENT
    ga = int(100+40*math.sin(t*2))
    pygame.draw.rect(surf,(*bc,ga),pygame.Rect(px,py,pw,ph),width=2,border_radius=18)
    lbl = F_LABEL.render(label, True, GREY)
    surf.blit(lbl, lbl.get_rect(centerx=cx, y=py+12))
    if len(types)==1:
        type_badge(surf, types[0], cx, cy+10)
    elif len(types)==2:
        type_badge(surf, types[0], cx, cy-14)
        type_badge(surf, types[1], cx, cy+50)

def draw_vs(surf, cx, cy, t):
    a   = int(180+75*math.sin(t*3))
    col = (a, a//2, 255)
    vs  = F_FEED.render("VS", True, col)
    surf.blit(vs, vs.get_rect(center=(cx,cy)))

def draw_lives_hud(surf, lives, right_x, y):
    hw  = 22; gap = 10
    total_w = MAX_LIVES*(hw*2+gap)
    sx = right_x - total_w
    for i in range(MAX_LIVES):
        draw_heart(surf, sx + i*(hw*2+gap) + hw, y, i < lives, hw)

def draw_score_bar(surf):
    acc = int(100*g_correct/g_total) if g_total else 0
    txt = F_SCORE.render(
        f"Score : {g_score}   Streak : {g_streak}   {acc}%   Q.{g_total}",
        True, WHITE)
    surf.blit(txt, txt.get_rect(centerx=WIDTH//2-60, y=10))

def draw_feedback_overlay(surf):
    if not g_feedback: return
    alpha = int(255 * min(1, g_fb_timer*2))
    s = pygame.Surface((WIDTH, 60), pygame.SRCALPHA)
    s.fill((*g_fb_col, min(50, alpha//2)))
    surf.blit(s, (0, HEIGHT//2-30))
    txt = F_FEED.render(g_fb_msg, True, g_fb_col)
    surf.blit(txt, txt.get_rect(center=(WIDTH//2, HEIGHT//2)))

def draw_game(surf, t, difficulty):
    draw_bg(surf); stars.draw(surf)

    ease    = min(1.0, g_anim_in)
    slide_y = int((1-ease)*55)

    draw_score_bar(surf)
    draw_lives_hud(surf, g_lives, WIDTH-10, 8)

    # ATTAQUE gauche | DEFENSE droite
    atk_cx  = WIDTH//4
    def_cx  = 3*WIDTH//4
    panel_cy= 258 + slide_y

    draw_panel(surf, "ATTAQUE", atk_cx, panel_cy, [g_atk_type], t)
    draw_panel(surf, "DEFENSE", def_cx, panel_cy, g_def_types,  t)
    draw_vs(surf, WIDTH//2, panel_cy, t)

    q = F_LABEL.render("Quelle est l'efficacite de l'attaque sur la defense ?", True, GREY)
    surf.blit(q, q.get_rect(centerx=WIDTH//2, y=395))

    waiting = (g_feedback is None)
    for b in mult_btns: b.draw(surf, disabled=not waiting)

    draw_feedback_overlay(surf)
    btn_back.draw(surf)
    btn_help.draw(surf)

    dc  = DIFF_COLS[DIFFICULTIES.index(difficulty)]
    dtx = F_SMALL.render(f"Mode : {difficulty}", True, dc)
    surf.blit(dtx, dtx.get_rect(right=WIDTH-10, y=12))

# ── HELP OVERLAY ──────────────────────────────────────────────────
def draw_help(surf):
    ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    ov.fill((0,0,0,215))
    surf.blit(ov, (0,0))
    if CHART_IMG:
        iw, ih = CHART_IMG.get_size()
        surf.blit(CHART_IMG, ((WIDTH-iw)//2, (HEIGHT-ih)//2))
    else:
        msg = F_MED.render("type_chart.png introuvable", True, RED_ERR)
        surf.blit(msg, msg.get_rect(center=(WIDTH//2, HEIGHT//2)))
    close = F_SMALL.render("Appuyez sur H, Echap ou cliquez pour fermer", True, GREY)
    surf.blit(close, close.get_rect(centerx=WIDTH//2, y=HEIGHT-26))

# ── GAME OVER ─────────────────────────────────────────────────────
def draw_gameover(surf, t, difficulty):
    draw_bg(surf); stars.draw(surf)

    # Animated title
    tc = (int(200+55*math.sin(t*2)), 60, 80)
    title = F_BIG.render("GAME OVER", True, tc)
    surf.blit(title, title.get_rect(centerx=WIDTH//2, y=55))

    # Stats panel
    pw,ph = 570,295; px=WIDTH//2-pw//2; py=128
    p = pygame.Surface((pw,ph), pygame.SRCALPHA)
    pygame.draw.rect(p,(18,22,55,225),(0,0,pw,ph),border_radius=18)
    pygame.draw.rect(p,(*ACCENT,80),(0,0,pw,ph),width=2,border_radius=18)
    surf.blit(p,(px,py))

    acc       = int(100*g_correct/g_total) if g_total else 0
    is_record = g_score > high_score

    rows = [
        ("Score de la partie",
         str(g_score) + ("  NOUVEAU RECORD !" if is_record else ""),
         GOLD if is_record else WHITE),
        ("Meilleur score", str(max(g_score, high_score)), GOLD),
        ("Questions repondues", str(g_total),             ACCENT),
        ("Precision",           f"{acc} %",               GRN_OK if acc>=70 else RED_ERR),
        ("Meilleure serie",     str(g_best_streak),       (255,160,60)),
    ]
    row_h = 52
    for i,(lbl,val,col) in enumerate(rows):
        ry = py+10 + i*row_h
        lt = F_SCORE.render(lbl, True, BLACK)
        vt = F_SCORE.render(val,  True, col)
        surf.blit(lt, (px+28, ry+row_h//2-lt.get_height()//2))
        surf.blit(vt, (px+pw-28-vt.get_width(), ry+row_h//2-vt.get_height()//2))
        if i < len(rows)-1:
            pygame.draw.line(surf,(40,50,90),(px+18,ry+row_h-1),(px+pw-18,ry+row_h-1))

    btn_retry.draw(surf)
    btn_menu2.draw(surf)

    dc  = DIFF_COLS[DIFFICULTIES.index(difficulty)]
    dtx = F_SMALL.render(f"Mode : {difficulty}", True, dc)
    surf.blit(dtx, dtx.get_rect(centerx=WIDTH//2, y=HEIGHT-20))

# ═══════════════════════════════════════════════════════════════════
#  MAIN LOOP
# ═══════════════════════════════════════════════════════════════════
STATE      = "menu"    # menu | game | gameover | help
prev_state = "game"
t          = 0.0
difficulty = "NORMAL"
start_game(difficulty)

while True:
    dt = clock.tick(60) / 1000.0
    t += dt
    mx, my = pygame.mouse.get_pos()

    btn_diff.label  = f"Difficulte : {DIFFICULTIES[diff_idx]}"
    btn_diff.accent = DIFF_COLS[diff_idx]
    difficulty      = DIFFICULTIES[diff_idx]

    # ── Events ────────────────────────────────────────────────────
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if STATE in ("help",):       STATE = prev_state
                elif STATE == "game":        STATE = "menu"
                elif STATE == "gameover":    STATE = "menu"
                else:                        pygame.quit(); sys.exit()
            if event.key == pygame.K_h:
                if STATE == "help":          STATE = prev_state
                elif STATE == "game":        prev_state="game"; STATE="help"

        # Close help on any click
        if STATE == "help" and event.type == pygame.MOUSEBUTTONDOWN:
            STATE = prev_state

        # MENU events
        if STATE == "menu":
            if btn_play.clicked(event):
                play(SFX_CLICK); start_game(difficulty); STATE="game"
            if btn_diff.clicked(event):
                play(SFX_CLICK); diff_idx=(diff_idx+1)%len(DIFFICULTIES)
            if btn_quit.clicked(event):
                play(SFX_CLICK); pygame.quit(); sys.exit()

        # GAME events
        elif STATE == "game":
            if btn_back.clicked(event):
                play(SFX_CLICK); STATE="menu"
            if btn_help.clicked(event):
                play(SFX_CLICK); prev_state="game"; STATE="help"

            if g_feedback is None:
                for i, btn in enumerate(mult_btns):
                    if btn.clicked(event):
                        chosen = MULTS[i]
                        g_total += 1
                        if chosen == g_answer:
                            g_correct   += 1
                            g_streak    += 1
                            g_best_streak= max(g_best_streak, g_streak)
                            pts          = int(100*(1 + 0.5*g_streak))
                            g_score     += pts
                            g_feedback   = "correct"
                            g_fb_msg     = f"CORRECT !  +{pts} pts"
                            g_fb_col     = GRN_OK
                            btn.trigger_flash(GRN_OK)
                            play(SFX_CORRECT)
                        else:
                            g_streak  = 0
                            g_lives  -= 1
                            play(SFX_GAMEOVER if g_lives <= 0 else SFX_LOSE_HP)
                            g_feedback = "wrong"
                            g_fb_msg   = f"C'etait {MULT_LABEL[g_answer]}"
                            g_fb_col   = RED_ERR
                            btn.trigger_flash(RED_ERR)
                            mult_btns[MULTS.index(g_answer)].trigger_flash(GRN_OK)
                        g_fb_timer = 1.2

        # GAMEOVER events
        elif STATE == "gameover":
            if btn_retry.clicked(event):
                play(SFX_CLICK); start_game(difficulty); STATE="game"
            if btn_menu2.clicked(event):
                play(SFX_CLICK); STATE="menu"

    # ── Update ────────────────────────────────────────────────────
    stars.update()

    if STATE == "menu":
        btn_play.update(mx,my,dt)
        btn_diff.update(mx,my,dt)
        btn_quit.update(mx,my,dt)

    elif STATE == "game":
        g_anim_in += dt * 3.0
        btn_back.update(mx,my,dt)
        btn_help.update(mx,my,dt)
        for b in mult_btns: b.update(mx,my,dt)

        if g_feedback is not None:
            g_fb_timer -= dt
            if g_fb_timer <= 0:
                if g_feedback == "wrong" and g_lives <= 0:
                    high_score = max(high_score, g_score)
                    STATE = "gameover"
                else:
                    g_feedback = None
                    new_question(difficulty)

    elif STATE == "gameover":
        btn_retry.update(mx,my,dt)
        btn_menu2.update(mx,my,dt)

    # ── Draw ──────────────────────────────────────────────────────
    if STATE == "menu":
        draw_menu(screen, t)
    elif STATE == "game":
        draw_game(screen, t, difficulty)
        if STATE == "game": pass   # help drawn below
    elif STATE == "gameover":
        draw_gameover(screen, t, difficulty)

    if STATE == "help":
        draw_game(screen, t, difficulty)
        draw_help(screen)

    pygame.display.flip()