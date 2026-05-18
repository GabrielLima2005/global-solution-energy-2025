# -*- coding: utf-8 -*-
"""
Gerador do vídeo pitch COMPLETO do Level UP (~1 minuto).
Combina todas as 7 cenas em um único MP4 dinâmico com:
- Transições suaves entre cenas
- Texto animado (fade-in, slide-up, sequencial)
- Barra de progresso no rodapé
- Marcação de tempo por cena
- Resolução 1920x1080 @ 30fps

Integrantes atualizados:
- Gabriel Lima da Silva
- João Carmo Cassu de Castro
- Luiz Gustavo de Almeida
- Nicolas Araujo de Oliveira
- Matheus Costa Cutrim
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import math
import os

try:
    from moviepy import VideoClip, concatenate_videoclips
    MOVIEPY_V2 = True
except ImportError:
    from moviepy.editor import VideoClip, concatenate_videoclips
    MOVIEPY_V2 = False

# =================== CONFIG ===================
WIDTH, HEIGHT = 1920, 1080
FPS = 30
OUTPUT_DIR = '/home/ubuntu/repos/global-solution-energy-2025/level-up-wokwi'

# Scene durations (seconds) - total ~62s
SCENES = [
    {'name': 'Abertura',     'dur': 8},   # 0:00 - 0:08
    {'name': 'Level UP',     'dur': 7},   # 0:08 - 0:15
    {'name': 'Pilar 1',      'dur': 10},  # 0:15 - 0:25
    {'name': 'Pilar 2',      'dur': 10},  # 0:25 - 0:35
    {'name': 'Pilar 3',      'dur': 7},   # 0:35 - 0:42
    {'name': 'Dashboard',    'dur': 8},   # 0:42 - 0:50
    {'name': 'Encerramento', 'dur': 12},  # 0:50 - 1:02
]

TOTAL_DUR = sum(s['dur'] for s in SCENES)
TRANSITION = 0.8  # seconds for cross-fade transitions

# =================== FONTS ===================
def get_font(size, bold=False):
    paths = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

# =================== DRAWING HELPERS ===================
def ease_out(t):
    return 1 - (1 - min(1, max(0, t))) ** 3

def ease_in_out(t):
    t = min(1, max(0, t))
    return 4*t*t*t if t < 0.5 else 1 - (-2*t + 2)**3 / 2

def lerp(a, b, t):
    return a + (b - a) * t

def alpha_fade(t, fade_in=0.5, hold_end=None, fade_out_start=None, dur=5.0):
    """Flexible alpha: fade in, hold, fade out"""
    if hold_end is None:
        hold_end = dur - 1.0
    if fade_out_start is None:
        fade_out_start = hold_end
    if t < fade_in:
        return ease_out(t / fade_in)
    elif t < fade_out_start:
        return 1.0
    elif t < dur:
        return ease_out((dur - t) / (dur - fade_out_start))
    return 0.0

def gradient_bg(draw, c_top, c_bot):
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(lerp(c_top[0], c_bot[0], t))
        g = int(lerp(c_top[1], c_bot[1], t))
        b = int(lerp(c_top[2], c_bot[2], t))
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

def text_centered(draw, text, y, font, color=(255,255,255), alpha=1.0):
    bbox = draw.textbbox((0,0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (WIDTH - tw) // 2
    c = tuple(int(v * alpha) for v in color)
    draw.text((x, y), text, font=font, fill=c)

def text_at(draw, text, x, y, font, color=(255,255,255), alpha=1.0):
    c = tuple(int(v * alpha) for v in color)
    draw.text((x, y), text, font=font, fill=c)

def draw_progress_bar(draw, progress, alpha=0.6):
    """Draw thin progress bar at bottom of screen"""
    bar_h = 4
    y = HEIGHT - bar_h
    bg = tuple(int(30 * alpha) for _ in range(3))
    draw.rectangle([(0, y), (WIDTH, HEIGHT)], fill=bg)
    w = int(WIDTH * progress)
    if w > 0:
        c = tuple(int(v * alpha) for v in (0, 200, 150))
        draw.rectangle([(0, y), (w, HEIGHT)], fill=c)

def draw_time_badge(draw, time_text, alpha=0.7):
    """Draw time badge top-right"""
    font = get_font(14)
    bbox = draw.textbbox((0,0), time_text, font=font)
    tw = bbox[2] - bbox[0]
    x = WIDTH - tw - 40
    y = 20
    bg = tuple(int(v * alpha * 0.2) for v in (0, 200, 150))
    border = tuple(int(v * alpha * 0.4) for v in (0, 200, 150))
    draw.rounded_rectangle((x - 15, y - 5, x + tw + 15, y + 25), radius=15,
                           fill=bg, outline=border, width=1)
    text_at(draw, time_text, x, y, font, color=(0, 200, 150), alpha=alpha)


# =================== SCENE 1: ABERTURA (0:00 - 0:08) ===================
def scene_abertura(t, dur):
    img = Image.new('RGB', (WIDTH, HEIGHT), (0,0,0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (10, 5, 20), (0, 0, 0))

    # Particle-like dots for atmosphere
    if t > 0.3:
        for i in range(20):
            px = int((WIDTH * 0.2) + (i * 73 + t * 30) % (WIDTH * 0.6))
            py = int((HEIGHT * 0.3) + (i * 97 + t * 15) % (HEIGHT * 0.4))
            dot_a = 0.05 + 0.03 * math.sin(t * 2 + i)
            c = tuple(int(255 * dot_a) for _ in range(3))
            draw.ellipse((px-2, py-2, px+2, py+2), fill=c)

    # "60%" number - dramatic fade in
    num_a = ease_out(min(1, t / 1.2))
    font_big = get_font(200, bold=True)
    color_60 = (255, max(50, int(100 - 30 * num_a)), 30)
    # Glow effect
    if num_a > 0.3:
        glow_a = num_a * 0.15
        for dx in [-3, 0, 3]:
            for dy in [-3, 0, 3]:
                if dx == 0 and dy == 0:
                    continue
                text_centered(draw, '60%', 220 + dy, get_font(200, bold=True),
                              color=(255, 80, 0), alpha=glow_a)
    text_centered(draw, '60%', 220, font_big, color=color_60, alpha=num_a)

    # Subtitle - slide up
    if t > 1.0:
        sub_a = ease_out(min(1, (t - 1.0) / 0.8))
        offset = int(30 * (1 - sub_a))
        text_centered(draw, 'das doenças crônicas poderiam ser', 470 + offset,
                      get_font(40), alpha=sub_a)
        text_centered(draw, 'evitadas com monitoramento adequado', 525 + offset,
                      get_font(42, bold=True), alpha=sub_a)

    # Question text
    if t > 2.5:
        q_a = ease_out(min(1, (t - 2.5) / 0.8))
        text_centered(draw, 'E se pudéssemos mudar isso?', 620, get_font(30),
                      color=(0, 200, 150), alpha=q_a)

    # Source
    if t > 3.5:
        s_a = ease_out(min(1, (t - 3.5) / 0.6))
        text_centered(draw, 'Fonte: Organização Mundial da Saúde (OMS)', 700,
                      get_font(18), color=(130, 130, 140), alpha=s_a)

    return img


# =================== SCENE 2: LEVEL UP LOGO (0:08 - 0:15) ===================
def scene_levelup(t, dur):
    img = Image.new('RGB', (WIDTH, HEIGHT), (0,0,0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (10, 22, 40), (10, 10, 26))

    # Decorative lines
    if t > 0.3:
        line_a = ease_out(min(1, (t - 0.3) / 0.5)) * 0.08
        for i in range(5):
            y_line = 200 + i * 150
            c = tuple(int(v * line_a) for v in (0, 200, 150))
            draw.line([(0, y_line), (WIDTH, y_line)], fill=c, width=1)

    # Logo - scale/bounce effect
    logo_a = ease_out(min(1, t / 0.7))
    slide_y = int(40 * (1 - ease_out(min(1, t / 0.6))))
    text_centered(draw, 'Level UP', 240 + slide_y, get_font(140, bold=True),
                  color=(0, 200, 150), alpha=logo_a)

    # Version
    if t > 0.4:
        v_a = ease_out(min(1, (t - 0.4) / 0.5)) * logo_a
        text_centered(draw, 'Health Monitoring System v2.0', 420,
                      get_font(30), color=(160, 170, 190), alpha=v_a)

    # Tagline with border
    if t > 1.0:
        tag_a = ease_out(min(1, (t - 1.0) / 0.6))
        tag_text = 'Cuidado proativo, inteligente e centrado no paciente'
        font_tag = get_font(24)
        bbox = draw.textbbox((0,0), tag_text, font=font_tag)
        tw = bbox[2] - bbox[0]
        bx = (WIDTH - tw) // 2 - 25
        border_c = tuple(int(v * tag_a) for v in (0, 200, 150))
        draw.rounded_rectangle((bx, 500, bx + tw + 50, 548), radius=25,
                               outline=border_c, width=2)
        text_centered(draw, tag_text, 512, font_tag, color=(0, 200, 150), alpha=tag_a)

    # Three pillars preview
    if t > 2.0:
        pill_a = ease_out(min(1, (t - 2.0) / 0.6))
        pillars = ['Monitoramento', 'Check-up Digital', 'Gamificação']
        icons = ['●', '◆', '★']
        colors = [(0, 200, 150), (167, 139, 250), (251, 191, 36)]
        for i, (name, icon, color) in enumerate(zip(pillars, icons, colors)):
            cx = WIDTH // 2 - 300 + i * 300
            text_at(draw, icon, cx - 5, 610, get_font(20), color=color, alpha=pill_a)
            bbox = draw.textbbox((0,0), name, font=get_font(18))
            nw = bbox[2] - bbox[0]
            text_at(draw, name, cx - nw//2 + 10, 640, get_font(18),
                    color=(180, 180, 190), alpha=pill_a)

    # Brand line
    if t > 3.0:
        br_a = ease_out(min(1, (t - 3.0) / 0.5))
        text_centered(draw, 'Uma evolução estratégica da plataforma Blua — CarePlus', 720,
                      get_font(20), color=(100, 110, 130), alpha=br_a)

    return img


# =================== SCENE 3: PILAR 1 - MONITORAMENTO (0:15 - 0:25) ===================
def scene_pilar1(t, dur):
    img = Image.new('RGB', (WIDTH, HEIGHT), (0,0,0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (10, 30, 10), (10, 10, 26))

    # Header
    h_a = ease_out(min(1, t / 0.5))
    text_centered(draw, 'P I L A R   1', 100, get_font(22),
                  color=(0, 200, 150), alpha=h_a)
    text_centered(draw, 'Monitoramento Contínuo', 140, get_font(58, bold=True), alpha=h_a)

    # Subtitle
    if t > 0.5:
        sub_a = ease_out(min(1, (t - 0.5) / 0.5))
        text_centered(draw, 'Sensores wearables coletando dados em tempo real', 220,
                      get_font(22), color=(150, 180, 150), alpha=sub_a)

    # LEDs with glow animation
    led_data = [
        ((0, 255, 68), 'Normal', '< 100 BPM', 1.0),
        ((255, 204, 0), 'Atenção', '100-120 BPM', 1.5),
        ((255, 51, 51), 'Crítico', '> 120 BPM', 2.0),
    ]
    for color, label, desc, start in led_data:
        if t > start:
            la = ease_out(min(1, (t - start) / 0.4))
            i = led_data.index((color, label, desc, start))
            cx = WIDTH // 2 - 200 + i * 200
            cy = 350
            r = 45
            # Pulsing glow
            pulse = 0.7 + 0.3 * math.sin((t - start) * 3)
            glow_r = r + 15
            glow_c = tuple(int(v * la * 0.2 * pulse) for v in color)
            draw.ellipse((cx-glow_r, cy-glow_r, cx+glow_r, cy+glow_r), fill=glow_c)
            fill = tuple(int(v * la) for v in color)
            draw.ellipse((cx-r, cy-r, cx+r, cy+r), fill=fill)
            # Label
            bbox = draw.textbbox((0,0), label, font=get_font(16, bold=True))
            lw = bbox[2] - bbox[0]
            text_at(draw, label, cx - lw//2, cy + 55, get_font(16, bold=True),
                    color=(200, 200, 200), alpha=la)
            bbox2 = draw.textbbox((0,0), desc, font=get_font(13))
            dw = bbox2[2] - bbox2[0]
            text_at(draw, desc, cx - dw//2, cy + 78, get_font(13),
                    color=(130, 130, 140), alpha=la)

    # Sensor data cards
    sensors = [
        ('Frequência Cardíaca', '75 BPM', (255, 77, 77), '40-200 BPM'),
        ('Temperatura', '36.5 °C', (0, 163, 255), 'DHT22'),
        ('Atividade Física', '45%', (0, 200, 150), '0-100%'),
        ('Qualidade do Sono', '72%', (167, 139, 250), 'Wearable'),
    ]
    card_start = 3.0
    for i, (name, value, color, sub) in enumerate(sensors):
        delay = card_start + i * 0.2
        if t > delay:
            ca = ease_out(min(1, (t - delay) / 0.4))
            cx = WIDTH // 2 - 430 + i * 225
            cy = 500
            cw, ch = 210, 120
            bg = tuple(int(v * ca * 0.08) for v in (255, 255, 255))
            border = tuple(int(v * ca * 0.15) for v in color)
            draw.rounded_rectangle((cx, cy, cx+cw, cy+ch), radius=12, fill=bg, outline=border, width=1)
            text_at(draw, name, cx+15, cy+12, get_font(14), color=(170, 180, 190), alpha=ca)
            text_at(draw, value, cx+15, cy+40, get_font(32, bold=True), color=color, alpha=ca)
            text_at(draw, sub, cx+15, cy+85, get_font(12), color=(110, 110, 120), alpha=ca)

    # Buzzer mention
    if t > 5.0:
        bz_a = ease_out(min(1, (t - 5.0) / 0.5))
        text_centered(draw, '🔊 Buzzer ativa em situações críticas — alerta sonoro imediato', 670,
                      get_font(18), color=(255, 100, 100), alpha=bz_a)

    return img


# =================== SCENE 4: PILAR 2 - CHECK-UP (0:25 - 0:35) ===================
def scene_pilar2(t, dur):
    img = Image.new('RGB', (WIDTH, HEIGHT), (0,0,0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (30, 18, 60), (10, 10, 26))

    h_a = ease_out(min(1, t / 0.5))
    text_centered(draw, 'P I L A R   2', 80, get_font(22), color=(167, 139, 250), alpha=h_a)
    text_centered(draw, 'Check-up Digital com IA', 120, get_font(54, bold=True), alpha=h_a)

    if t > 0.5:
        sub_a = ease_out(min(1, (t - 0.5) / 0.5))
        text_centered(draw, '8 perguntas de triagem adaptativa + sinais vitais = Score de Risco', 195,
                      get_font(20), color=(140, 130, 170), alpha=sub_a)

    # Check-up box with animated questions
    if t > 1.0:
        box_a = ease_out(min(1, (t - 1.0) / 0.5))
        bx, by = WIDTH//2 - 300, 260
        bw, bh = 600, 220
        fill = tuple(int(v * box_a * 0.4) for v in (15, 10, 30))
        border = tuple(int(v * box_a) for v in (167, 139, 250))
        draw.rounded_rectangle((bx, by, bx+bw, by+bh), radius=16, fill=fill, outline=border, width=2)

        # Animated question cycling
        questions = [
            ('1/8', 'Dor de cabeça frequente?'),
            ('2/8', 'Dificuldade para dormir?'),
            ('3/8', 'Tontura frequente?'),
            ('4/8', 'Falta de ar ao se exercitar?'),
            ('5/8', 'Dor no peito?'),
        ]
        q_idx = min(len(questions)-1, int((t - 1.0) / 1.5))
        q_num, q_text = questions[q_idx]

        text_at(draw, f'CHECK-UP DIGITAL — Pergunta {q_num}', bx+30, by+20,
                get_font(16), color=(167, 139, 250), alpha=box_a)
        # Question fades in
        q_local_t = (t - 1.0) % 1.5
        q_a = ease_out(min(1, q_local_t / 0.3)) * box_a
        text_at(draw, q_text, bx+30, by+60, get_font(30), alpha=q_a)

        # Buttons
        btn_y = by + 130
        green = tuple(int(v * box_a) for v in (0, 200, 150))
        draw.rounded_rectangle((bx+30, btn_y, bx+180, btn_y+50), radius=10, fill=green)
        text_at(draw, 'SIM', bx+80, btn_y+12, get_font(20, bold=True), color=(0,0,0), alpha=box_a)

        gray = tuple(int(v * box_a * 0.15) for v in (255,255,255))
        draw.rounded_rectangle((bx+210, btn_y, bx+380, btn_y+50), radius=10, fill=gray,
                               outline=tuple(int(v*box_a*0.3) for v in (255,255,255)), width=1)
        text_at(draw, 'NÃO', bx+270, btn_y+12, get_font(20, bold=True), alpha=box_a)

        # Weight indicator
        text_at(draw, f'Peso: {[15, 10, 12, 20, 25][q_idx]}pts', bx+420, btn_y+15,
                get_font(14), color=(130, 120, 160), alpha=box_a)

    # Risk score animation
    if t > 4.0:
        r_a = ease_out(min(1, (t - 4.0) / 0.6))
        # Score filling up
        fill_pct = min(0.42, 0.42 * ease_out(min(1, (t - 4.0) / 1.5)))
        bar_x, bar_y = WIDTH//2 - 250, 530
        bar_w, bar_h = 350, 28
        bg_bar = tuple(int(v * r_a * 0.15) for v in (255, 255, 255))
        draw.rounded_rectangle((bar_x, bar_y, bar_x+bar_w, bar_y+bar_h), radius=14, fill=bg_bar)
        fill_w = int(bar_w * fill_pct)
        if fill_w > 2:
            for px in range(fill_w):
                pt = px / bar_w
                r = int(lerp(0, 255, pt) * r_a)
                g = int(lerp(200, 180, pt) * r_a)
                b = int(lerp(150, 0, pt) * r_a)
                draw.line([(bar_x+px, bar_y+3), (bar_x+px, bar_y+bar_h-3)], fill=(r,g,b))

        score_val = int(42 * ease_out(min(1, (t - 4.0) / 1.5)))
        text_at(draw, f'{score_val}/100', bar_x + bar_w + 20, bar_y - 5,
                get_font(34, bold=True), color=(255, 204, 0), alpha=r_a)

    # Classification
    if t > 5.5:
        cl_a = ease_out(min(1, (t - 5.5) / 0.5))
        text_centered(draw, 'Classificação: RISCO MODERADO', 590,
                      get_font(22, bold=True), color=(255, 204, 0), alpha=cl_a)
        text_centered(draw, 'Relatório médico gerado automaticamente via Serial', 625,
                      get_font(16), color=(130, 130, 150), alpha=cl_a)

    # Three outputs
    if t > 6.5:
        out_a = ease_out(min(1, (t - 6.5) / 0.5))
        outputs = ['Score 0-100', 'Classificação', 'Relatório Médico']
        for i, txt in enumerate(outputs):
            cx = WIDTH//2 - 280 + i * 250
            bg_c = tuple(int(v * out_a * 0.1) for v in (167, 139, 250))
            border_c = tuple(int(v * out_a * 0.3) for v in (167, 139, 250))
            draw.rounded_rectangle((cx, 680, cx+210, 720), radius=10,
                                   fill=bg_c, outline=border_c, width=1)
            bbox = draw.textbbox((0,0), txt, font=get_font(16, bold=True))
            tw = bbox[2] - bbox[0]
            text_at(draw, txt, cx + (210-tw)//2, 690, get_font(16, bold=True),
                    color=(167, 139, 250), alpha=out_a)

    return img


# =================== SCENE 5: PILAR 3 - GAMIFICAÇÃO (0:35 - 0:42) ===================
def scene_pilar3(t, dur):
    img = Image.new('RGB', (WIDTH, HEIGHT), (0,0,0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (30, 26, 0), (10, 10, 26))

    h_a = ease_out(min(1, t / 0.5))
    text_centered(draw, 'P I L A R   3', 120, get_font(22), color=(251, 191, 36), alpha=h_a)
    text_centered(draw, 'Gamificação', 160, get_font(60, bold=True), alpha=h_a)

    if t > 0.5:
        sub_a = ease_out(min(1, (t - 0.5) / 0.5))
        text_centered(draw, 'Pontos, níveis e ranks incentivam hábitos saudáveis', 245,
                      get_font(22), color=(180, 170, 120), alpha=sub_a)

    # Animated counter cards
    stats = [
        ('Nível', 3, (251, 191, 36)),
        ('Pontos', 250, (0, 200, 150)),
        ('Check-ups', 2, (167, 139, 250)),
    ]
    for i, (label, target, color) in enumerate(stats):
        start = 1.0 + i * 0.3
        if t > start:
            ca = ease_out(min(1, (t - start) / 0.4))
            # Counter animation
            count_t = min(1, (t - start) / 1.0)
            current = int(target * ease_out(count_t))
            cx = WIDTH//2 - 300 + i * 260
            cy = 320
            cw, ch = 230, 130
            bg = tuple(int(v * ca * 0.08) for v in color)
            border = tuple(int(v * ca * 0.3) for v in color)
            draw.rounded_rectangle((cx, cy, cx+cw, cy+ch), radius=16, fill=bg, outline=border, width=1)
            val_text = str(current)
            font_val = get_font(52, bold=True)
            bbox = draw.textbbox((0,0), val_text, font=font_val)
            vw = bbox[2] - bbox[0]
            text_at(draw, val_text, cx + (cw-vw)//2, cy+18, font_val, color=color, alpha=ca)
            font_lbl = get_font(16)
            bbox2 = draw.textbbox((0,0), label, font=font_lbl)
            lw = bbox2[2] - bbox2[0]
            text_at(draw, label, cx + (cw-lw)//2, cy+85, font_lbl, color=(150,150,160), alpha=ca)

    # Rank progression with highlight animation
    if t > 2.5:
        ra = ease_out(min(1, (t - 2.5) / 0.6))
        ranks = ['Iniciante', 'Aprendiz Ativo', 'Guerreiro Fit', 'Expert Vital', 'Mestre Saúde']
        colors = [(150,150,150), (0,200,150), (251,191,36), (167,139,250), (255,77,77)]
        font_r = get_font(15, bold=True)
        widths = []
        for r in ranks:
            bbox = draw.textbbox((0,0), r, font=font_r)
            widths.append(bbox[2] - bbox[0] + 40)
        total = sum(widths) + (len(ranks)-1) * 35
        sx = (WIDTH - total) // 2
        for i, (rank, color, w) in enumerate(zip(ranks, colors, widths)):
            # Highlight current rank with glow
            highlight = (i == 2)  # Guerreiro Fit
            fill_a = 0.2 if highlight else 0.1
            bg_c = tuple(int(v * ra * fill_a) for v in color)
            border_c = tuple(int(v * ra * (0.6 if highlight else 0.3)) for v in color)
            bw = 2 if highlight else 1
            draw.rounded_rectangle((sx, 510, sx+w, 548), radius=20,
                                   fill=bg_c, outline=border_c, width=bw)
            text_at(draw, rank, sx+20, 518, font_r, color=color, alpha=ra)
            sx += w
            if i < len(ranks) - 1:
                text_at(draw, '→', sx+10, 516, get_font(18), color=(80,80,90), alpha=ra)
                sx += 35

    # Impact stat
    if t > 3.5:
        imp_a = ease_out(min(1, (t - 3.5) / 0.5))
        text_centered(draw, 'Aumento de até 30% na adesão ao tratamento', 610,
                      get_font(24), color=(251, 191, 36), alpha=imp_a)
        text_centered(draw, '+50 pontos por check-up completo   •   +10 pontos por vitais saudáveis', 650,
                      get_font(16), color=(150, 150, 130), alpha=imp_a)

    return img


# =================== SCENE 6: DASHBOARD WEB (0:42 - 0:50) ===================
def scene_dashboard(t, dur):
    img = Image.new('RGB', (WIDTH, HEIGHT), (0,0,0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (0, 26, 46), (10, 10, 26))

    h_a = ease_out(min(1, t / 0.5))
    text_centered(draw, 'W I F I   A C C E S S   P O I N T   +   W E B   S E R V E R', 70,
                  get_font(18), color=(0, 163, 255), alpha=h_a)
    text_centered(draw, 'Dashboard em Tempo Real', 105, get_font(50, bold=True), alpha=h_a)

    # Dashboard mockup with entrance animation
    if t > 0.6:
        da = ease_out(min(1, (t - 0.6) / 0.5))
        dx, dy = WIDTH//2 - 380, 185
        dw, dh = 760, 470
        slide = int(30 * (1 - da))
        dy += slide
        bg = tuple(int(v * da) for v in (17, 24, 39))
        border = tuple(int(v * da * 0.3) for v in (0, 163, 255))
        draw.rounded_rectangle((dx, dy, dx+dw, dy+dh), radius=16, fill=bg, outline=border, width=2)

        # Header
        text_centered(draw, 'LEVEL UP', dy+18, get_font(24, bold=True), color=(0,200,150), alpha=da)
        text_centered(draw, 'Health Monitoring System v2.0', dy+48, get_font(13), color=(100,110,130), alpha=da)

        # Status
        if t > 1.0:
            st_a = ease_out(min(1, (t - 1.0) / 0.3)) * da
            st_fill = tuple(int(v * st_a * 0.15) for v in (0, 200, 150))
            draw.rounded_rectangle((dx+30, dy+75, dx+dw-30, dy+105), radius=8, fill=st_fill)
            text_centered(draw, 'NORMAL — SINAIS VITAIS ESTÁVEIS', dy+80,
                          get_font(15, bold=True), color=(0,200,150), alpha=st_a)

        # Cards appearing one by one
        cards = [
            ('Freq. Cardíaca', '75 BPM', (255, 77, 77)),
            ('Temperatura', '36.5 °C', (0, 163, 255)),
            ('Atividade', '45%', (0, 200, 150)),
            ('Qual. Sono', '72%', (167, 139, 250)),
            ('Passos', '6.750', (251, 191, 36)),
            ('Gamificação', 'Lv.3 ★', (0, 200, 150)),
        ]
        for i, (name, val, color) in enumerate(cards):
            delay = 1.3 + i * 0.2
            if t > delay:
                ca = ease_out(min(1, (t - delay) / 0.3)) * da
                col, row = i % 3, i // 3
                cx = dx + 30 + col * 235
                cy = dy + 120 + row * 140
                cw, ch = 225, 125
                card_bg = tuple(int(v * ca * 0.08) for v in (255,255,255))
                card_border = tuple(int(v * ca * 0.12) for v in (255,255,255))
                draw.rounded_rectangle((cx, cy, cx+cw, cy+ch), radius=10,
                                       fill=card_bg, outline=card_border, width=1)
                text_at(draw, name, cx+15, cy+15, get_font(14), color=(150,160,170), alpha=ca)
                text_at(draw, val, cx+15, cy+50, get_font(32, bold=True), color=color, alpha=ca)

        # API endpoint hint
        if t > 3.5:
            api_a = ease_out(min(1, (t - 3.5) / 0.4)) * da
            text_at(draw, 'API: GET /api/data → JSON', dx+30, dy+dh-35,
                    get_font(12), color=(80,90,110), alpha=api_a)
            text_at(draw, 'Auto-refresh: 2s', dx+dw-170, dy+dh-35,
                    get_font(12), color=(80,90,110), alpha=api_a)

    # WiFi info
    if t > 4.0:
        wa = ease_out(min(1, (t - 4.0) / 0.5))
        items = [
            ('SSID: LevelUP-Health', (0, 163, 255)),
            ('Senha: levelup123', (0, 163, 255)),
            ('http://192.168.4.1', (0, 200, 150)),
        ]
        font_w = get_font(16)
        widths = []
        for txt, _ in items:
            bbox = draw.textbbox((0,0), txt, font=font_w)
            widths.append(bbox[2] - bbox[0] + 40)
        total = sum(widths) + (len(items)-1) * 15
        sx = (WIDTH - total) // 2
        for (txt, color), w in zip(items, widths):
            bg_c = tuple(int(v * wa * 0.1) for v in color)
            border_c = tuple(int(v * wa * 0.3) for v in color)
            draw.rounded_rectangle((sx, 695, sx+w, 730), radius=10,
                                   fill=bg_c, outline=border_c, width=1)
            text_at(draw, txt, sx+20, 700, font_w, color=color, alpha=wa)
            sx += w + 15

    return img


# =================== SCENE 7: ENCERRAMENTO (0:50 - 1:02) ===================
def scene_encerramento(t, dur):
    img = Image.new('RGB', (WIDTH, HEIGHT), (0,0,0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (13, 26, 45), (0, 0, 0))

    # Subtle particle field
    for i in range(30):
        px = int((i * 67 + t * 20) % WIDTH)
        py = int((i * 101 + t * 8) % HEIGHT)
        dot_a = 0.04 + 0.02 * math.sin(t * 1.5 + i * 0.5)
        c = tuple(int(v * dot_a) for v in (0, 200, 150))
        draw.ellipse((px-1, py-1, px+1, py+1), fill=c)

    # Logo with glow
    logo_a = ease_out(min(1, t / 0.8))
    # Glow
    glow_a = logo_a * 0.1
    for offset in [(-2,-2), (2,-2), (-2,2), (2,2)]:
        text_centered(draw, 'Level UP', 130 + offset[1], get_font(120, bold=True),
                      color=(0, 200, 150), alpha=glow_a)
    text_centered(draw, 'Level UP', 130, get_font(120, bold=True),
                  color=(0, 200, 150), alpha=logo_a)

    # Slogan
    if t > 0.8:
        sl_a = ease_out(min(1, (t - 0.8) / 0.6))
        text_centered(draw, 'Sua saúde, seu jogo, seu nível!', 290,
                      get_font(34), color=(220, 225, 235), alpha=sl_a)

    # Impact metrics
    metrics = [
        ('-20%', 'Redução de custos\nassistenciais', (0, 200, 150)),
        ('+30%', 'Aumento da adesão\nao tratamento', (0, 163, 255)),
        ('+25%', 'Produtividade\nclínica', (167, 139, 250)),
    ]
    for i, (val, desc, color) in enumerate(metrics):
        delay = 1.5 + i * 0.3
        if t > delay:
            ma = ease_out(min(1, (t - delay) / 0.4))
            cx = WIDTH//2 - 370 + i * 290
            cy = 380
            cw, ch = 260, 130
            bg = tuple(int(v * ma * 0.05) for v in (255,255,255))
            border_c = tuple(int(v * ma * 0.1) for v in (255,255,255))
            draw.rounded_rectangle((cx, cy, cx+cw, cy+ch), radius=14,
                                   fill=bg, outline=border_c, width=1)
            text_at(draw, val, cx+20, cy+15, get_font(40, bold=True), color=color, alpha=ma)
            for j, line in enumerate(desc.split('\n')):
                text_at(draw, line, cx+20, cy+70+j*22, get_font(16), color=(170,175,185), alpha=ma)

    # For CarePlus line
    if t > 3.0:
        cp_a = ease_out(min(1, (t - 3.0) / 0.5))
        text_centered(draw, 'Para a CarePlus: inovação em saúde, cuidado centrado no paciente', 545,
                      get_font(18), color=(100, 130, 160), alpha=cp_a)

    # Team credits - UPDATED
    if t > 4.0:
        cr_a = ease_out(min(1, (t - 4.0) / 0.8))
        # Divider line
        line_c = tuple(int(v * cr_a * 0.2) for v in (255,255,255))
        draw.line([(WIDTH//2 - 200, 590), (WIDTH//2 + 200, 590)], fill=line_c, width=1)

        text_centered(draw, 'Equipe', 605, get_font(16),
                      color=(100, 110, 130), alpha=cr_a)

        members = [
            'Gabriel Lima da Silva',
            'João Carmo Cassu de Castro',
            'Luiz Gustavo de Almeida',
            'Nicolas Araujo de Oliveira',
            'Matheus Costa Cutrim',
        ]
        for i, name in enumerate(members):
            delay_m = 4.0 + i * 0.15
            if t > delay_m:
                m_a = ease_out(min(1, (t - delay_m) / 0.3)) * cr_a
                text_centered(draw, name, 635 + i * 28, get_font(18, bold=True),
                              color=(190, 195, 205), alpha=m_a)

    # Institution
    if t > 6.0:
        inst_a = ease_out(min(1, (t - 6.0) / 0.5))
        text_centered(draw, 'FIAP — 1º Ano Ciência da Computação — PCP Sprint 3 — 2025', 810,
                      get_font(14), color=(80, 85, 100), alpha=inst_a)

    # Final fade to black
    if t > dur - 2.0:
        fade = 1 - ease_out((dur - t) / 2.0)
        overlay = Image.new('RGB', (WIDTH, HEIGHT), (0,0,0))
        img = Image.blend(img, overlay, fade * 0.8)

    return img


# =================== MAIN: COMBINE ALL SCENES ===================
def make_full_video():
    """Generate the complete pitch video with transitions"""

    scene_funcs = [
        scene_abertura,
        scene_levelup,
        scene_pilar1,
        scene_pilar2,
        scene_pilar3,
        scene_dashboard,
        scene_encerramento,
    ]

    # Calculate scene time offsets
    offsets = []
    t_offset = 0
    for s in SCENES:
        offsets.append(t_offset)
        t_offset += s['dur']

    def make_frame(t):
        # Determine which scene we're in
        elapsed = 0
        scene_idx = 0
        for i, s in enumerate(SCENES):
            if t < elapsed + s['dur']:
                scene_idx = i
                break
            elapsed += s['dur']
        else:
            scene_idx = len(SCENES) - 1

        local_t = t - offsets[scene_idx]
        dur = SCENES[scene_idx]['dur']

        # Generate current scene
        img = scene_funcs[scene_idx](local_t, dur)

        # Cross-fade transition at scene boundaries
        if local_t < TRANSITION and scene_idx > 0:
            # Blend with end of previous scene
            prev_dur = SCENES[scene_idx - 1]['dur']
            prev_local_t = prev_dur - (TRANSITION - local_t)
            prev_img = scene_funcs[scene_idx - 1](prev_local_t, prev_dur)
            blend = ease_in_out(local_t / TRANSITION)
            img = Image.blend(prev_img, img, blend)

        # Add overlays
        draw = ImageDraw.Draw(img)
        progress = t / TOTAL_DUR
        draw_progress_bar(draw, progress, alpha=0.5)

        # Time badge
        mins = int(t) // 60
        secs = int(t) % 60
        draw_time_badge(draw, f'{mins}:{secs:02d}', alpha=0.6)

        return np.array(img)

    print(f'Gerando vídeo pitch completo ({TOTAL_DUR}s)...')
    clip = VideoClip(make_frame, duration=TOTAL_DUR)
    output_path = os.path.join(OUTPUT_DIR, 'Video_Pitch_LevelUP.mp4')
    clip.write_videofile(output_path, fps=FPS, codec='libx264',
                         audio=False, logger='bar',
                         preset='medium', bitrate='6000k')
    clip.close()
    size = os.path.getsize(output_path)
    print(f'\nVídeo salvo: {output_path}')
    print(f'Tamanho: {size // 1024} KB ({size // (1024*1024)} MB)')
    print(f'Duração: {TOTAL_DUR}s ({TOTAL_DUR//60}:{TOTAL_DUR%60:02d})')
    return output_path


if __name__ == '__main__':
    make_full_video()
