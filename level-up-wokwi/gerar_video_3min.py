# -*- coding: utf-8 -*-
"""
Gerador do vídeo pitch de 3 MINUTOS para Prof. Sandro.
Requisitos:
  1. Breve apresentação da proposta do projeto (~1 min)
  2. Cronograma + especificação do hardware e softwares (~40s)
  3. Breve descrição do software desenvolvido (~1 min)
  4. Hardware desenvolvido / protótipo Wokwi (~20s + encerramento)

Total: ~3 min (180s)
Resolução: 1920x1080 @ 30fps, H.264, sem áudio

Equipe:
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
    from moviepy import VideoClip
except ImportError:
    from moviepy.editor import VideoClip

# =================== CONFIG ===================
WIDTH, HEIGHT = 1920, 1080
FPS = 30
OUTPUT_DIR = '/home/ubuntu/repos/global-solution-energy-2025/level-up-wokwi'

# Scene durations - total 180s (3:00)
SCENES = [
    {'name': 'Abertura',             'dur': 8},    # 0:00 - 0:08
    {'name': 'Problema',             'dur': 14},   # 0:08 - 0:22
    {'name': 'Solução Level UP',     'dur': 10},   # 0:22 - 0:32
    {'name': 'Pilar 1',              'dur': 14},   # 0:32 - 0:46
    {'name': 'Pilar 2',              'dur': 14},   # 0:46 - 1:00
    {'name': 'Pilar 3',              'dur': 12},   # 1:00 - 1:12
    # --- Seção 2: Cronograma + Specs ---
    {'name': 'Cronograma',           'dur': 16},   # 1:12 - 1:28
    {'name': 'Specs Hardware',       'dur': 14},   # 1:28 - 1:42
    # --- Seção 3: Software ---
    {'name': 'Arquitetura Software', 'dur': 14},   # 1:42 - 1:56
    {'name': 'Telas OLED',           'dur': 14},   # 1:56 - 2:10
    {'name': 'Dashboard Web',        'dur': 14},   # 2:10 - 2:24
    # --- Seção 4: Hardware Wokwi ---
    {'name': 'Circuito Wokwi',       'dur': 16},   # 2:24 - 2:40
    {'name': 'Encerramento',         'dur': 20},   # 2:40 - 3:00
]

TOTAL_DUR = sum(s['dur'] for s in SCENES)
TRANSITION = 0.6

# =================== FONTS ===================
_font_cache = {}
def get_font(size, bold=False):
    key = (size, bold)
    if key in _font_cache:
        return _font_cache[key]
    paths = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
    ]
    for p in paths:
        if os.path.exists(p):
            f = ImageFont.truetype(p, size)
            _font_cache[key] = f
            return f
    f = ImageFont.load_default()
    _font_cache[key] = f
    return f

# =================== DRAWING HELPERS ===================
def ease_out(t):
    return 1 - (1 - min(1, max(0, t))) ** 3

def ease_in_out(t):
    t = min(1, max(0, t))
    return 4*t*t*t if t < 0.5 else 1 - (-2*t + 2)**3 / 2

def lerp(a, b, t):
    return a + (b - a) * t

def gradient_bg(draw, c_top, c_bot):
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(lerp(c_top[0], c_bot[0], t))
        g = int(lerp(c_top[1], c_bot[1], t))
        b = int(lerp(c_top[2], c_bot[2], t))
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

def text_c(draw, text, y, font, color=(255,255,255), alpha=1.0):
    bbox = draw.textbbox((0,0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (WIDTH - tw) // 2
    c = tuple(int(v * alpha) for v in color)
    draw.text((x, y), text, font=font, fill=c)

def text_at(draw, text, x, y, font, color=(255,255,255), alpha=1.0):
    c = tuple(int(v * alpha) for v in color)
    draw.text((x, y), text, font=font, fill=c)

def draw_progress_bar(draw, progress, section_name, alpha=0.7):
    bar_h = 6
    y = HEIGHT - bar_h - 30
    # Background
    bg = tuple(int(20 * alpha) for _ in range(3))
    draw.rectangle([(0, y), (WIDTH, y + bar_h)], fill=bg)
    w = int(WIDTH * progress)
    if w > 0:
        c = tuple(int(v * alpha) for v in (0, 200, 150))
        draw.rectangle([(0, y), (w, y + bar_h)], fill=c)
    # Section label
    font = get_font(13)
    text_at(draw, section_name, 30, HEIGHT - 25, font, color=(80, 90, 110), alpha=alpha)
    # Time
    total_s = int(TOTAL_DUR * progress)
    mins = total_s // 60
    secs = total_s % 60
    time_text = f'{mins}:{secs:02d} / {TOTAL_DUR//60}:{TOTAL_DUR%60:02d}'
    bbox = draw.textbbox((0,0), time_text, font=font)
    tw = bbox[2] - bbox[0]
    text_at(draw, time_text, WIDTH - tw - 30, HEIGHT - 25, font, color=(80, 90, 110), alpha=alpha)

def draw_section_badge(draw, section_num, section_title, alpha=0.8):
    font = get_font(13)
    text = f'SEÇÃO {section_num}/4 — {section_title}'
    bbox = draw.textbbox((0,0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = WIDTH - tw - 40
    y = 18
    bg = tuple(int(v * alpha * 0.15) for v in (0, 200, 150))
    border = tuple(int(v * alpha * 0.3) for v in (0, 200, 150))
    draw.rounded_rectangle((x-12, y-4, x+tw+12, y+20), radius=12, fill=bg, outline=border, width=1)
    text_at(draw, text, x, y, font, color=(0, 200, 150), alpha=alpha)

def particles(draw, t, count=25, color=(255,255,255), alpha_base=0.04):
    for i in range(count):
        px = int((i * 73 + t * 18) % WIDTH)
        py = int((i * 97 + t * 10) % HEIGHT)
        a = alpha_base + 0.02 * math.sin(t * 1.5 + i)
        c = tuple(int(v * a) for v in color)
        draw.ellipse((px-1, py-1, px+1, py+1), fill=c)

def rounded_card(draw, x, y, w, h, color, alpha, radius=14):
    bg = tuple(int(v * alpha * 0.08) for v in (255,255,255))
    border = tuple(int(v * alpha * 0.2) for v in color)
    draw.rounded_rectangle((x, y, x+w, y+h), radius=radius, fill=bg, outline=border, width=1)


# ==================================================================================
#  SEÇÃO 1: APRESENTAÇÃO DA PROPOSTA (~1 min) — Cenas 1-6
# ==================================================================================

def scene_abertura(t, dur):
    """Cena 1: Tela título (0:00 - 0:08)"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (0,0,0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (8, 15, 35), (0, 0, 0))
    particles(draw, t, 30, (0, 200, 150))

    # Institution
    inst_a = ease_out(min(1, t / 0.5))
    text_c(draw, 'FIAP — Faculdade de Informática e Administração Paulista', 80,
           get_font(20), color=(100, 110, 140), alpha=inst_a)
    text_c(draw, '1º Ano — Ciência da Computação — 2025', 110,
           get_font(16), color=(80, 90, 120), alpha=inst_a)

    # Title
    if t > 0.3:
        t_a = ease_out(min(1, (t - 0.3) / 0.7))
        slide = int(30 * (1 - t_a))
        text_c(draw, 'Level UP', 250 + slide, get_font(130, bold=True),
               color=(0, 200, 150), alpha=t_a)

    if t > 0.8:
        s_a = ease_out(min(1, (t - 0.8) / 0.5))
        text_c(draw, 'Sistema Inteligente de Monitoramento de Saúde', 420,
               get_font(30), color=(180, 190, 210), alpha=s_a)

    if t > 1.3:
        v_a = ease_out(min(1, (t - 1.3) / 0.5))
        text_c(draw, 'Versão 2.0 — ESP32 + WiFi + Dashboard Web', 470,
               get_font(20), color=(120, 130, 155), alpha=v_a)

    # CarePlus context
    if t > 2.5:
        cp_a = ease_out(min(1, (t - 2.5) / 0.6))
        border_c = tuple(int(v * cp_a * 0.3) for v in (0, 163, 255))
        draw.rounded_rectangle((WIDTH//2 - 320, 540, WIDTH//2 + 320, 590), radius=20,
                               outline=border_c, width=1)
        text_c(draw, 'Evolução estratégica da plataforma Blua — CarePlus', 555,
               get_font(22), color=(0, 163, 255), alpha=cp_a)

    # Team names
    if t > 4.0:
        cr_a = ease_out(min(1, (t - 4.0) / 0.6))
        members = [
            'Gabriel Lima da Silva',
            'João Carmo Cassu de Castro',
            'Luiz Gustavo de Almeida',
            'Nicolas Araujo de Oliveira',
            'Matheus Costa Cutrim',
        ]
        text_c(draw, 'Equipe:', 650, get_font(14), color=(90, 100, 120), alpha=cr_a)
        for i, name in enumerate(members):
            text_c(draw, name, 675 + i * 24, get_font(16, bold=True),
                   color=(160, 170, 190), alpha=cr_a)

    return img


def scene_problema(t, dur):
    """Cena 2: Contexto do problema (0:08 - 0:22)"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (0,0,0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (25, 5, 10), (5, 0, 0))

    h_a = ease_out(min(1, t / 0.5))
    text_c(draw, 'O PROBLEMA', 60, get_font(20), color=(255, 80, 80), alpha=h_a)
    text_c(draw, 'Saúde Corporativa: modelo reativo e fragmentado', 95,
           get_font(42, bold=True), alpha=h_a)

    # Problem points appearing
    problems = [
        ('Ausência de monitoramento contínuo', 'Pacientes só são avaliados em consultas esporádicas', (255, 77, 77)),
        ('Baixa adesão entre consultas', 'Sem incentivo para manter hábitos saudáveis diariamente', (255, 153, 51)),
        ('Triagem digital pouco estruturada', 'Check-ups genéricos sem adaptação ao perfil do paciente', (255, 204, 0)),
        ('Custos assistenciais elevados', 'Doenças crônicas detectadas tarde = tratamento mais caro', (200, 100, 100)),
    ]
    for i, (title, desc, color) in enumerate(problems):
        delay = 1.0 + i * 1.5
        if t > delay:
            pa = ease_out(min(1, (t - delay) / 0.5))
            y = 200 + i * 110
            # Icon dot
            dot_c = tuple(int(v * pa) for v in color)
            draw.ellipse((200, y+8, 218, y+26), fill=dot_c)
            text_at(draw, title, 240, y, get_font(26, bold=True), color=color, alpha=pa)
            text_at(draw, desc, 240, y+35, get_font(18), color=(150, 140, 140), alpha=pa)

    # OMS statistic
    if t > 8.0:
        stat_a = ease_out(min(1, (t - 8.0) / 0.8))
        bg_c = tuple(int(v * stat_a * 0.08) for v in (255, 80, 80))
        draw.rounded_rectangle((WIDTH//2 - 400, 660, WIDTH//2 + 400, 740), radius=16, fill=bg_c)
        text_c(draw, '60% das doenças crônicas poderiam ser evitadas', 670,
               get_font(28, bold=True), color=(255, 100, 100), alpha=stat_a)
        text_c(draw, 'Fonte: Organização Mundial da Saúde (OMS)', 710,
               get_font(16), color=(130, 100, 100), alpha=stat_a)

    return img


def scene_solucao(t, dur):
    """Cena 3: Solução Level UP (0:22 - 0:32)"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (0,0,0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (10, 22, 40), (5, 10, 20))
    particles(draw, t, 20, (0, 200, 150))

    h_a = ease_out(min(1, t / 0.5))
    text_c(draw, 'A SOLUÇÃO', 60, get_font(20), color=(0, 200, 150), alpha=h_a)
    text_c(draw, 'Level UP — Três Pilares', 95, get_font(50, bold=True), alpha=h_a)

    if t > 0.5:
        sub_a = ease_out(min(1, (t - 0.5) / 0.5))
        text_c(draw, 'Cuidado proativo, inteligente e centrado no paciente', 175,
               get_font(22), color=(150, 170, 190), alpha=sub_a)

    # Three pillars
    pillars = [
        ('PILAR 1', 'Monitoramento\nContínuo', 'Wearables + sensores\nem tempo real',
         (0, 200, 150), '●'),
        ('PILAR 2', 'Check-up Digital\ncom IA', 'Triagem adaptativa +\nscore de risco',
         (167, 139, 250), '◆'),
        ('PILAR 3', 'Gamificação', 'Pontos, níveis e ranks\npara engajamento',
         (251, 191, 36), '★'),
    ]
    for i, (label, title, desc, color, icon) in enumerate(pillars):
        delay = 1.5 + i * 1.0
        if t > delay:
            pa = ease_out(min(1, (t - delay) / 0.5))
            cx = WIDTH//2 - 480 + i * 380
            cy = 280
            cw, ch = 350, 340
            bg = tuple(int(v * pa * 0.06) for v in (255,255,255))
            border_c = tuple(int(v * pa * 0.25) for v in color)
            draw.rounded_rectangle((cx, cy, cx+cw, cy+ch), radius=20, fill=bg, outline=border_c, width=2)
            # Icon
            text_c_x = cx + cw//2
            icon_font = get_font(50)
            bbox = draw.textbbox((0,0), icon, font=icon_font)
            iw = bbox[2] - bbox[0]
            text_at(draw, icon, text_c_x - iw//2, cy+25, icon_font, color=color, alpha=pa)
            # Label
            font_lbl = get_font(14)
            bbox = draw.textbbox((0,0), label, font=font_lbl)
            lw = bbox[2] - bbox[0]
            text_at(draw, label, text_c_x - lw//2, cy+90, font_lbl, color=color, alpha=pa)
            # Title
            for j, line in enumerate(title.split('\n')):
                font_t = get_font(24, bold=True)
                bbox = draw.textbbox((0,0), line, font=font_t)
                tw = bbox[2] - bbox[0]
                text_at(draw, line, text_c_x - tw//2, cy+120 + j*30, font_t, alpha=pa)
            # Desc
            for j, line in enumerate(desc.split('\n')):
                font_d = get_font(16)
                bbox = draw.textbbox((0,0), line, font=font_d)
                dw = bbox[2] - bbox[0]
                text_at(draw, line, text_c_x - dw//2, cy+210 + j*24, font_d,
                        color=(140, 150, 170), alpha=pa)

    # McKinsey stat
    if t > 6.0:
        mk_a = ease_out(min(1, (t - 6.0) / 0.5))
        text_c(draw, 'Soluções digitais podem reduzir custos assistenciais em até 20% — McKinsey', 680,
               get_font(18), color=(100, 130, 160), alpha=mk_a)

    return img


def scene_pilar1(t, dur):
    """Cena 4: Pilar 1 — Monitoramento Contínuo (0:32 - 0:46)"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (0,0,0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (10, 30, 15), (5, 10, 15))

    h_a = ease_out(min(1, t / 0.5))
    text_c(draw, 'P I L A R   1', 55, get_font(20), color=(0, 200, 150), alpha=h_a)
    text_c(draw, 'Monitoramento Contínuo via Wearables', 90, get_font(44, bold=True), alpha=h_a)

    if t > 0.5:
        sub_a = ease_out(min(1, (t - 0.5) / 0.5))
        text_c(draw, 'Sensores coletam dados em tempo real e alertam sobre riscos', 155,
               get_font(20), color=(140, 170, 150), alpha=sub_a)

    # Sensor data cards
    sensors = [
        ('Frequência Cardíaca', '40–200 BPM', 'Potenciômetro\n(simula wearable)', (255, 77, 77)),
        ('Temperatura Corporal', '0–50 °C', 'DHT22\n(sensor real)', (0, 163, 255)),
        ('Nível de Atividade', '0–100%', 'Potenciômetro\n(simula acelerômetro)', (0, 200, 150)),
        ('Qualidade do Sono', '0–100%', 'Derivado da\natividade noturna', (167, 139, 250)),
    ]
    for i, (name, range_val, sensor, color) in enumerate(sensors):
        delay = 1.0 + i * 0.8
        if t > delay:
            ca = ease_out(min(1, (t - delay) / 0.4))
            col = i % 2
            row = i // 2
            cx = WIDTH//2 - 480 + col * 490
            cy = 210 + row * 175
            cw, ch = 460, 155
            rounded_card(draw, cx, cy, cw, ch, color, ca)
            text_at(draw, name, cx+20, cy+15, get_font(22, bold=True), color=color, alpha=ca)
            text_at(draw, f'Faixa: {range_val}', cx+20, cy+50, get_font(18), alpha=ca)
            for j, line in enumerate(sensor.split('\n')):
                text_at(draw, line, cx+20, cy+85 + j*22, get_font(15), color=(120, 130, 140), alpha=ca)

    # Alert system
    if t > 5.0:
        al_a = ease_out(min(1, (t - 5.0) / 0.5))
        text_c(draw, 'Sistema de Alertas', 590, get_font(22, bold=True),
               color=(255, 200, 0), alpha=al_a)
        leds = [
            ('LED Verde', 'Normal', (0, 255, 68)),
            ('LED Amarelo', 'Atenção', (255, 204, 0)),
            ('LED Vermelho', 'Crítico', (255, 51, 51)),
            ('Buzzer', 'Alarme sonoro', (200, 100, 100)),
        ]
        for i, (name, desc, color) in enumerate(leds):
            delay_l = 5.5 + i * 0.3
            if t > delay_l:
                la = ease_out(min(1, (t - delay_l) / 0.3)) * al_a
                cx = WIDTH//2 - 400 + i * 210
                cy = 635
                dot_c = tuple(int(v * la) for v in color)
                draw.ellipse((cx+10, cy, cx+30, cy+20), fill=dot_c)
                text_at(draw, name, cx+40, cy-2, get_font(14, bold=True), color=color, alpha=la)
                text_at(draw, desc, cx+40, cy+18, get_font(12), color=(130,130,140), alpha=la)

    return img


def scene_pilar2(t, dur):
    """Cena 5: Pilar 2 — Check-up Digital (0:46 - 1:00)"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (0,0,0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (25, 15, 45), (10, 5, 20))

    h_a = ease_out(min(1, t / 0.5))
    text_c(draw, 'P I L A R   2', 55, get_font(20), color=(167, 139, 250), alpha=h_a)
    text_c(draw, 'Check-up Digital com Inteligência Artificial', 90,
           get_font(44, bold=True), alpha=h_a)

    if t > 0.5:
        sub_a = ease_out(min(1, (t - 0.5) / 0.5))
        text_c(draw, '8 perguntas de triagem adaptativa + cruzamento com sinais vitais', 155,
               get_font(20), color=(140, 130, 170), alpha=sub_a)

    # Question flow
    questions = [
        ('1', 'Dor no peito?', 20),
        ('2', 'Falta de ar?', 15),
        ('3', 'Tontura frequente?', 10),
        ('4', 'Dor de cabeça?', 5),
        ('5', 'Fadiga excessiva?', 8),
        ('6', 'Febre recente?', 12),
        ('7', 'Palpitações?', 18),
        ('8', 'Insônia?', 7),
    ]
    # Show questions in a grid
    for i, (num, text, weight) in enumerate(questions):
        delay = 1.0 + i * 0.3
        if t > delay:
            qa = ease_out(min(1, (t - delay) / 0.3))
            col = i % 4
            row = i // 4
            cx = WIDTH//2 - 470 + col * 240
            cy = 210 + row * 120
            cw, ch = 225, 100
            rounded_card(draw, cx, cy, cw, ch, (167, 139, 250), qa)
            text_at(draw, f'Pergunta {num}', cx+15, cy+10, get_font(13),
                    color=(167, 139, 250), alpha=qa)
            text_at(draw, text, cx+15, cy+35, get_font(18, bold=True), alpha=qa)
            text_at(draw, f'Peso: {weight} pts', cx+15, cy+65, get_font(13),
                    color=(120, 110, 140), alpha=qa)

    # Risk score output
    if t > 5.0:
        r_a = ease_out(min(1, (t - 5.0) / 0.6))
        bg_c = tuple(int(v * r_a * 0.08) for v in (255,255,255))
        draw.rounded_rectangle((WIDTH//2 - 350, 470, WIDTH//2 + 350, 590), radius=16, fill=bg_c)
        text_c(draw, 'Score de Risco: 0 a 100', 480, get_font(24, bold=True),
               color=(167, 139, 250), alpha=r_a)
        # Bar filling
        bar_x, bar_y = WIDTH//2 - 250, 525
        bar_w, bar_h = 500, 20
        fill_pct = min(0.42, 0.42 * ease_out(min(1, (t - 5.0) / 1.5)))
        bg_bar = tuple(int(v * r_a * 0.1) for v in (255,255,255))
        draw.rounded_rectangle((bar_x, bar_y, bar_x+bar_w, bar_y+bar_h), radius=10, fill=bg_bar)
        fill_w = int(bar_w * fill_pct)
        if fill_w > 2:
            for px in range(fill_w):
                pt = px / bar_w
                r = int(lerp(0, 255, pt) * r_a)
                g = int(lerp(200, 100, pt) * r_a)
                b = int(lerp(150, 0, pt) * r_a)
                draw.line([(bar_x+px, bar_y+2), (bar_x+px, bar_y+bar_h-2)], fill=(r,g,b))
        score = int(42 * ease_out(min(1, (t - 5.0) / 1.5)))
        text_c(draw, f'Exemplo: {score}/100 — Risco Moderado', 555,
               get_font(16), color=(255, 204, 0), alpha=r_a)

    # Outputs
    if t > 7.5:
        out_a = ease_out(min(1, (t - 7.5) / 0.5))
        outputs = [
            ('Classificação automática', 'Baixo / Moderado / Alto'),
            ('Relatório preliminar', 'Ficha médica via Serial'),
            ('Integração vital', 'BPM e temp. ajustam o score'),
        ]
        for i, (name, desc) in enumerate(outputs):
            cx = WIDTH//2 - 460 + i * 310
            cy = 620
            rounded_card(draw, cx, cy, 290, 75, (167, 139, 250), out_a)
            text_at(draw, name, cx+15, cy+12, get_font(16, bold=True),
                    color=(167, 139, 250), alpha=out_a)
            text_at(draw, desc, cx+15, cy+40, get_font(14), color=(140, 140, 160), alpha=out_a)

    return img


def scene_pilar3(t, dur):
    """Cena 6: Pilar 3 — Gamificação (1:00 - 1:12)"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (0,0,0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (30, 25, 5), (10, 8, 5))

    h_a = ease_out(min(1, t / 0.5))
    text_c(draw, 'P I L A R   3', 55, get_font(20), color=(251, 191, 36), alpha=h_a)
    text_c(draw, 'Gamificação e Engajamento', 90, get_font(48, bold=True), alpha=h_a)

    if t > 0.5:
        sub_a = ease_out(min(1, (t - 0.5) / 0.5))
        text_c(draw, 'Incentivando hábitos saudáveis com pontos, níveis e recompensas', 160,
               get_font(20), color=(180, 170, 120), alpha=sub_a)

    # How points work
    point_rules = [
        ('+10 pts', 'Vitais saudáveis (a cada 30s)', (0, 200, 150)),
        ('+50 pts', 'Check-up completo', (167, 139, 250)),
        ('+5 pts', 'Meta diária de atividade', (0, 163, 255)),
        ('Nível UP', 'A cada 100 pontos', (251, 191, 36)),
    ]
    for i, (pts, desc, color) in enumerate(point_rules):
        delay = 1.0 + i * 0.5
        if t > delay:
            pa = ease_out(min(1, (t - delay) / 0.4))
            cx = WIDTH//2 - 480 + i * 245
            cy = 230
            rounded_card(draw, cx, cy, 230, 100, color, pa)
            text_at(draw, pts, cx+15, cy+15, get_font(28, bold=True), color=color, alpha=pa)
            text_at(draw, desc, cx+15, cy+55, get_font(14), color=(160, 160, 170), alpha=pa)

    # Rank progression
    if t > 3.5:
        ra = ease_out(min(1, (t - 3.5) / 0.6))
        text_c(draw, 'Progressão de Ranks', 370, get_font(22, bold=True), alpha=ra)
        ranks = [
            ('Iniciante', 'Nível 1', (150, 150, 150)),
            ('Aprendiz Ativo', 'Nível 2', (0, 200, 150)),
            ('Guerreiro Fit', 'Nível 3-4', (251, 191, 36)),
            ('Expert Vital', 'Nível 5-7', (167, 139, 250)),
            ('Mestre Saúde', 'Nível 8+', (255, 77, 77)),
        ]
        for i, (rank, req, color) in enumerate(ranks):
            delay_r = 3.5 + i * 0.2
            if t > delay_r:
                rra = ease_out(min(1, (t - delay_r) / 0.3)) * ra
                cx = WIDTH//2 - 460 + i * 190
                cy = 410
                cw = 175
                rounded_card(draw, cx, cy, cw, 80, color, rra)
                font_r = get_font(16, bold=True)
                bbox = draw.textbbox((0,0), rank, font=font_r)
                tw = bbox[2] - bbox[0]
                text_at(draw, rank, cx + (cw-tw)//2, cy+15, font_r, color=color, alpha=rra)
                font_s = get_font(13)
                bbox2 = draw.textbbox((0,0), req, font=font_s)
                sw = bbox2[2] - bbox2[0]
                text_at(draw, req, cx + (cw-sw)//2, cy+45, font_s, color=(130,130,140), alpha=rra)

        # Arrow connectors
        if t > 4.5:
            arr_a = ra * 0.5
            for i in range(4):
                x = WIDTH//2 - 460 + i * 190 + 175 + 3
                c = tuple(int(v * arr_a) for v in (100, 100, 110))
                text_at(draw, '→', x, 440, get_font(20), color=(100, 100, 110), alpha=arr_a)

    # Impact
    if t > 6.0:
        imp_a = ease_out(min(1, (t - 6.0) / 0.5))
        bg_c = tuple(int(v * imp_a * 0.08) for v in (251, 191, 36))
        draw.rounded_rectangle((WIDTH//2 - 380, 540, WIDTH//2 + 380, 620), radius=16, fill=bg_c)
        text_c(draw, 'Estratégias de gamificação podem aumentar a adesão', 550,
               get_font(22, bold=True), color=(251, 191, 36), alpha=imp_a)
        text_c(draw, 'ao tratamento em até 30% (estudos de saúde digital)', 585,
               get_font(18), color=(200, 180, 100), alpha=imp_a)

    return img


# ==================================================================================
#  SEÇÃO 2: CRONOGRAMA + ESPECIFICAÇÕES (~40s) — Cenas 7-8
# ==================================================================================

def scene_cronograma(t, dur):
    """Cena 7: Cronograma das etapas (1:12 - 1:28)"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (0,0,0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (15, 15, 30), (5, 5, 15))

    h_a = ease_out(min(1, t / 0.5))
    text_c(draw, 'CRONOGRAMA DO PROJETO', 55, get_font(20), color=(0, 163, 255), alpha=h_a)
    text_c(draw, 'Etapas Realizadas e Planejadas', 90, get_font(42, bold=True), alpha=h_a)

    # Timeline
    phases = [
        ('Sprint 1', 'MAR-ABR 2025', [
            'Definição do projeto Level UP',
            'Circuito ESP32 no Wokwi',
            'Sensores + LEDs + OLED',
            'Check-up digital (8 perguntas)',
        ], (0, 200, 150), True),
        ('Sprint 2', 'ABR-MAI 2025', [
            'WiFi Access Point',
            'Dashboard Web (HTML/JS)',
            'API REST (/api/data)',
            'Relógio em tempo real',
        ], (0, 163, 255), True),
        ('Sprint 3', 'MAI-JUN 2025', [
            'Relatório lógica digital',
            'Documentação ABNT',
            'Vídeo pitch',
            'Testes e refinamentos',
        ], (251, 191, 36), True),
        ('Futuro', 'JUL+ 2025', [
            'App mobile nativo',
            'Integração wearables reais',
            'IA preditiva (ML)',
            'Validação clínica',
        ], (167, 139, 250), False),
    ]

    for i, (phase, period, items, color, done) in enumerate(phases):
        delay = 0.8 + i * 1.5
        if t > delay:
            pa = ease_out(min(1, (t - delay) / 0.5))
            cx = WIDTH//2 - 480 + i * 245
            cy = 170
            cw, ch = 230, 450
            bg = tuple(int(v * pa * 0.06) for v in (255,255,255))
            border_c = tuple(int(v * pa * 0.25) for v in color)
            draw.rounded_rectangle((cx, cy, cx+cw, cy+ch), radius=14, fill=bg, outline=border_c, width=2)
            # Header
            font_h = get_font(20, bold=True)
            bbox = draw.textbbox((0,0), phase, font=font_h)
            tw = bbox[2] - bbox[0]
            text_at(draw, phase, cx + (cw-tw)//2, cy+15, font_h, color=color, alpha=pa)
            # Period
            font_p = get_font(13)
            bbox = draw.textbbox((0,0), period, font=font_p)
            pw = bbox[2] - bbox[0]
            text_at(draw, period, cx + (cw-pw)//2, cy+45, font_p, color=(120,120,130), alpha=pa)
            # Status
            status = 'CONCLUÍDO' if done else 'PLANEJADO'
            status_c = (0, 200, 150) if done else (167, 139, 250)
            font_s = get_font(11, bold=True)
            bbox = draw.textbbox((0,0), status, font=font_s)
            sw = bbox[2] - bbox[0]
            sc = tuple(int(v * pa * 0.15) for v in status_c)
            sbc = tuple(int(v * pa * 0.4) for v in status_c)
            draw.rounded_rectangle((cx + (cw-sw)//2 - 10, cy+70, cx + (cw+sw)//2 + 10, cy+90),
                                   radius=8, fill=sc, outline=sbc, width=1)
            text_at(draw, status, cx + (cw-sw)//2, cy+73, font_s, color=status_c, alpha=pa)
            # Items
            for j, item in enumerate(items):
                prefix = '✓ ' if done else '○ '
                item_c = (170, 180, 190) if done else (130, 130, 160)
                text_at(draw, prefix + item, cx+15, cy+110 + j*40, get_font(13), color=item_c, alpha=pa)

    return img


def scene_specs(t, dur):
    """Cena 8: Especificações de Hardware e Software (1:28 - 1:42)"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (0,0,0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (15, 20, 25), (5, 8, 15))

    h_a = ease_out(min(1, t / 0.5))
    text_c(draw, 'ESPECIFICAÇÕES TÉCNICAS', 55, get_font(20), color=(0, 200, 150), alpha=h_a)
    text_c(draw, 'Hardware e Software Utilizados', 90, get_font(42, bold=True), alpha=h_a)

    # Hardware column
    if t > 0.5:
        hw_a = ease_out(min(1, (t - 0.5) / 0.5))
        hx = 120
        text_at(draw, 'HARDWARE', hx, 170, get_font(18, bold=True), color=(255, 77, 77), alpha=hw_a)
        hw_items = [
            ('ESP32 DevKit V1', 'Microcontrolador dual-core, WiFi/BT integrado'),
            ('Display OLED SSD1306', '128×64 pixels, comunicação I2C (0x3C)'),
            ('Sensor DHT22', 'Temperatura (-40~80°C) + Umidade (0~100%)'),
            ('2× Potenciômetros', 'Simulam sensores wearable (BPM, atividade)'),
            ('3× LEDs', 'Verde (D25), Amarelo (D26), Vermelho (D27)'),
            ('Buzzer', 'Alarme sonoro para situações críticas (D33)'),
            ('2× Push Buttons', 'Menu (D18) e Select (D19) com pull-up'),
            ('3× Resistores 220Ω', 'Proteção para LEDs'),
        ]
        for i, (name, desc) in enumerate(hw_items):
            delay = 0.8 + i * 0.25
            if t > delay:
                ia = ease_out(min(1, (t - delay) / 0.3)) * hw_a
                y = 210 + i * 50
                text_at(draw, '•', hx, y, get_font(14), color=(255, 77, 77), alpha=ia)
                text_at(draw, name, hx + 20, y, get_font(16, bold=True), alpha=ia)
                text_at(draw, desc, hx + 20, y + 22, get_font(13), color=(130, 140, 150), alpha=ia)

    # Software column
    if t > 3.0:
        sw_a = ease_out(min(1, (t - 3.0) / 0.5))
        sx = WIDTH//2 + 60
        text_at(draw, 'SOFTWARE', sx, 170, get_font(18, bold=True), color=(0, 163, 255), alpha=sw_a)
        sw_items = [
            ('Arduino IDE / Wokwi', 'Plataforma de desenvolvimento'),
            ('C++ (Arduino)', 'Linguagem de programação'),
            ('Adafruit SSD1306', 'Biblioteca do display OLED'),
            ('Adafruit GFX', 'Biblioteca gráfica'),
            ('DHT Sensor Library', 'Leitura do sensor DHT22'),
            ('WiFi.h + WebServer.h', 'Rede e servidor web (ESP32)'),
            ('HTML/CSS/JavaScript', 'Dashboard web responsivo'),
            ('REST API (JSON)', 'Comunicação de dados'),
        ]
        for i, (name, desc) in enumerate(sw_items):
            delay = 3.3 + i * 0.25
            if t > delay:
                ia = ease_out(min(1, (t - delay) / 0.3)) * sw_a
                y = 210 + i * 50
                text_at(draw, '•', sx, y, get_font(14), color=(0, 163, 255), alpha=ia)
                text_at(draw, name, sx + 20, y, get_font(16, bold=True), alpha=ia)
                text_at(draw, desc, sx + 20, y + 22, get_font(13), color=(130, 140, 150), alpha=ia)

    # Divider
    if t > 0.5:
        dv_a = ease_out(min(1, (t - 0.5) / 0.5)) * 0.1
        c = tuple(int(255 * dv_a) for _ in range(3))
        draw.line([(WIDTH//2 + 30, 170), (WIDTH//2 + 30, 620)], fill=c, width=1)

    return img


# ==================================================================================
#  SEÇÃO 3: DESCRIÇÃO DO SOFTWARE (~1 min) — Cenas 9-11
# ==================================================================================

def scene_arquitetura(t, dur):
    """Cena 9: Arquitetura do software (1:42 - 1:56)"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (0,0,0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (15, 15, 30), (5, 5, 18))

    h_a = ease_out(min(1, t / 0.5))
    text_c(draw, 'ARQUITETURA DO SOFTWARE', 55, get_font(20), color=(0, 200, 150), alpha=h_a)
    text_c(draw, 'Estrutura do Código (977 linhas C++)', 90, get_font(42, bold=True), alpha=h_a)

    # Module blocks
    modules = [
        ('Leitura de Sensores', 'readSensors()', 'ADC + DHT22 a cada 2s\nMapeia valores para faixas\nhumanas realistas',
         (255, 77, 77), 1.0),
        ('Avaliação de Saúde', 'evaluateHealth()', 'Classifica: Normal/Atenção/Crítico\nAtiva LEDs e buzzer\nLógica booleana simplificada',
         (255, 204, 0), 2.0),
        ('Check-up Digital', 'checkupProcess()', '8 perguntas ponderadas\nScore 0-100 com vitais\nRelatório médico (Serial)',
         (167, 139, 250), 3.0),
        ('Gamificação', 'awardPoints()', '+10 pts por vitais saudáveis\n+50 pts por check-up\n5 ranks progressivos',
         (251, 191, 36), 4.0),
        ('WiFi + Web Server', 'setupWiFi() / routes', 'AP: LevelUP-Health\nDashboard HTML (PROGMEM)\nAPI REST → JSON',
         (0, 163, 255), 5.0),
        ('Display OLED', 'updateDisplay()', '6 telas com navegação\n128×64 px, I2C\nRefresh a cada 500ms',
         (0, 200, 150), 6.0),
    ]

    for i, (name, func, desc, color, start) in enumerate(modules):
        if t > start:
            ma = ease_out(min(1, (t - start) / 0.5))
            col = i % 3
            row = i // 3
            cx = WIDTH//2 - 510 + col * 340
            cy = 175 + row * 220
            cw, ch = 320, 200
            rounded_card(draw, cx, cy, cw, ch, color, ma, radius=16)
            text_at(draw, name, cx+18, cy+15, get_font(18, bold=True), color=color, alpha=ma)
            text_at(draw, func, cx+18, cy+45, get_font(14), color=(130, 140, 160), alpha=ma)
            for j, line in enumerate(desc.split('\n')):
                text_at(draw, line, cx+18, cy+80 + j*24, get_font(15), alpha=ma)

    # Loop info
    if t > 8.0:
        lo_a = ease_out(min(1, (t - 8.0) / 0.5))
        text_c(draw, 'Loop principal: sensores (2s) → avaliação → display (500ms) → WiFi clients', 640,
               get_font(16), color=(100, 120, 140), alpha=lo_a)

    return img


def scene_telas_oled(t, dur):
    """Cena 10: Telas OLED (1:56 - 2:10)"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (0,0,0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (10, 18, 28), (5, 8, 15))

    h_a = ease_out(min(1, t / 0.5))
    text_c(draw, 'INTERFACE — TELAS OLED (128×64 px)', 55, get_font(20), color=(0, 200, 150), alpha=h_a)
    text_c(draw, '6 Telas com Navegação por Botões', 90, get_font(42, bold=True), alpha=h_a)

    # OLED screen mockups
    screens = [
        ('Dashboard', ['LEVEL UP v2.0  12:00', '─────────────────', 'BPM: 75  ♥ Normal',
                        'Tmp: 36.5°C', 'Ativ: ████░░ 45%', 'Lv.3 Guerreiro Fit'],
         (0, 200, 150)),
        ('Relógio', ['', '   12:00:00', '', 'WiFi: LevelUP-Health',
                      'IP: 192.168.4.1', 'Clientes: 1'],
         (0, 163, 255)),
        ('Sinais Vitais', ['SINAIS VITAIS', '─────────────────', 'FC: 75 BPM  [Normal]',
                           'Temp: 36.5°C [OK]', 'Umid: 65%', 'Ativ: 45% Sono: 72%'],
         (255, 77, 77)),
        ('Check-up', ['CHECK-UP DIGITAL', '─────────────────', 'Pergunta 3/8:',
                      'Tontura frequente?', '', '[SIM]        [NAO]'],
         (167, 139, 250)),
        ('Gamificação', ['GAMIFICACAO', '─────────────────', 'Pontos: 250',
                         'Nivel: 3', 'Rank: Guerreiro Fit', 'Progresso: ████░ 50%'],
         (251, 191, 36)),
        ('Alerta', ['!! ALERTA CRITICO !!', '─────────────────', 'FC: 145 BPM',
                     'ACIMA DO NORMAL!', '', 'Procure atendimento'],
         (255, 51, 51)),
    ]

    for i, (name, lines, color) in enumerate(screens):
        delay = 0.8 + i * 1.0
        if t > delay:
            sa = ease_out(min(1, (t - delay) / 0.4))
            col = i % 3
            row = i // 3
            cx = WIDTH//2 - 510 + col * 340
            cy = 165 + row * 270
            # OLED frame
            frame_c = tuple(int(v * sa * 0.3) for v in color)
            draw.rounded_rectangle((cx, cy, cx+310, cy+250), radius=10,
                                   fill=(0, 0, 0), outline=frame_c, width=2)
            # Screen title
            font_n = get_font(16, bold=True)
            bbox = draw.textbbox((0,0), name, font=font_n)
            nw = bbox[2] - bbox[0]
            text_at(draw, name, cx + (310-nw)//2, cy+8, font_n, color=color, alpha=sa)
            # OLED content (simulated monospace)
            font_m = get_font(14)
            for j, line in enumerate(lines):
                text_at(draw, line, cx+15, cy+40 + j*28, font_m, color=(0, 200, 150), alpha=sa * 0.8)

    # Navigation info
    if t > 8.0:
        nav_a = ease_out(min(1, (t - 8.0) / 0.5))
        text_c(draw, 'Botão Menu (azul) = trocar tela   |   Botão Select (verde) = interagir', 720,
               get_font(18), color=(120, 140, 160), alpha=nav_a)

    return img


def scene_dashboard_web(t, dur):
    """Cena 11: Dashboard Web (2:10 - 2:24)"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (0,0,0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (5, 15, 30), (5, 5, 15))

    h_a = ease_out(min(1, t / 0.5))
    text_c(draw, 'DASHBOARD WEB EM TEMPO REAL', 45, get_font(20), color=(0, 163, 255), alpha=h_a)
    text_c(draw, 'WiFi Access Point + Web Server', 75, get_font(38, bold=True), alpha=h_a)

    # Dashboard mockup
    if t > 0.5:
        da = ease_out(min(1, (t - 0.5) / 0.5))
        dx, dy = WIDTH//2 - 420, 130
        dw, dh = 840, 480
        bg = tuple(int(15 * da) for _ in range(3))
        border = tuple(int(v * da * 0.2) for v in (0, 163, 255))
        draw.rounded_rectangle((dx, dy, dx+dw, dy+dh), radius=16, fill=bg, outline=border, width=2)

        # Browser bar
        bar_bg = tuple(int(v * da) for v in (25, 25, 40))
        draw.rounded_rectangle((dx+5, dy+5, dx+dw-5, dy+35), radius=8, fill=bar_bg)
        text_at(draw, 'http://192.168.4.1', dx+20, dy+10, get_font(13), color=(0,200,150), alpha=da)

        # Header
        text_at(draw, 'LEVEL UP', dx+dw//2 - 40, dy+50, get_font(22, bold=True),
                color=(0, 200, 150), alpha=da)
        text_at(draw, 'Health Monitoring System v2.0', dx+dw//2 - 100, dy+78,
                get_font(12), color=(100,110,130), alpha=da)

        # Clock
        if t > 1.0:
            cl_a = ease_out(min(1, (t - 1.0) / 0.3)) * da
            font_clk = get_font(36, bold=True)
            bbox = draw.textbbox((0,0), '12:00:00', font=font_clk)
            cw_t = bbox[2] - bbox[0]
            text_at(draw, '12:00:00', dx + (dw-cw_t)//2, dy+100, font_clk,
                    color=(0, 200, 150), alpha=cl_a)

        # Status bar
        if t > 1.3:
            st_a = ease_out(min(1, (t - 1.3) / 0.3)) * da
            st_fill = tuple(int(v * st_a * 0.2) for v in (0, 200, 150))
            draw.rounded_rectangle((dx+30, dy+150, dx+dw-30, dy+175), radius=6, fill=st_fill)
            font_st = get_font(13, bold=True)
            st_text = 'NORMAL — SINAIS VITAIS ESTÁVEIS'
            bbox = draw.textbbox((0,0), st_text, font=font_st)
            stw = bbox[2] - bbox[0]
            text_at(draw, st_text, dx + (dw-stw)//2, dy+155, font_st,
                    color=(0, 200, 150), alpha=st_a)

        # Cards
        cards = [
            ('Freq. Cardíaca', '75 BPM', (255, 77, 77)),
            ('Temperatura', '36.5 °C', (255, 204, 0)),
            ('Atividade', '45%', (0, 200, 150)),
            ('Qual. Sono', '72%', (0, 163, 255)),
            ('Passos', '6.750', (167, 139, 250)),
            ('Gamificação', 'Lv.3 ★', (255, 107, 157)),
        ]
        for i, (name, val, color) in enumerate(cards):
            delay = 1.5 + i * 0.2
            if t > delay:
                ca = ease_out(min(1, (t - delay) / 0.3)) * da
                col = i % 3
                row = i // 3
                cx = dx + 30 + col * 260
                cy = dy + 190 + row * 130
                card_w, card_h = 250, 115
                card_bg = tuple(int(v * ca * 0.08) for v in (255,255,255))
                card_border = tuple(int(v * ca * 0.1) for v in (255,255,255))
                draw.rounded_rectangle((cx, cy, cx+card_w, cy+card_h), radius=8,
                                       fill=card_bg, outline=card_border, width=1)
                text_at(draw, name, cx+12, cy+12, get_font(12), color=(150,160,170), alpha=ca)
                text_at(draw, val, cx+12, cy+40, get_font(28, bold=True), color=color, alpha=ca)

    # API info
    if t > 4.0:
        api_a = ease_out(min(1, (t - 4.0) / 0.5))
        api_items = [
            ('GET /api/data', 'Retorna JSON com todos os dados', (0, 200, 150)),
            ('GET /api/settime?h=HH&m=MM', 'Ajusta relógio via web', (0, 163, 255)),
            ('Auto-refresh: 2 segundos', 'fetch() + setInterval()', (167, 139, 250)),
        ]
        for i, (endpoint, desc, color) in enumerate(api_items):
            cx = WIDTH//2 - 460 + i * 310
            cy = 640
            rounded_card(draw, cx, cy, 290, 65, color, api_a)
            text_at(draw, endpoint, cx+12, cy+10, get_font(14, bold=True), color=color, alpha=api_a)
            text_at(draw, desc, cx+12, cy+35, get_font(12), color=(130,140,150), alpha=api_a)

    # WiFi badge
    if t > 5.0:
        wa = ease_out(min(1, (t - 5.0) / 0.5))
        text_c(draw, 'SSID: LevelUP-Health  |  Senha: levelup123  |  IP: 192.168.4.1', 725,
               get_font(16), color=(0, 163, 255), alpha=wa)

    return img


# ==================================================================================
#  SEÇÃO 4: HARDWARE / PROTÓTIPO WOKWI (~20s + encerramento) — Cenas 12-13
# ==================================================================================

def scene_circuito(t, dur):
    """Cena 12: Circuito Wokwi (2:24 - 2:40)"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (0,0,0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (20, 15, 10), (8, 5, 5))

    h_a = ease_out(min(1, t / 0.5))
    text_c(draw, 'PROTÓTIPO — CIRCUITO WOKWI', 45, get_font(20), color=(255, 150, 50), alpha=h_a)
    text_c(draw, 'Hardware Desenvolvido no Simulador', 80, get_font(42, bold=True), alpha=h_a)

    # Circuit schematic drawing
    if t > 0.5:
        ca = ease_out(min(1, (t - 0.5) / 0.5))

        # ESP32 central box
        esp_x, esp_y = WIDTH//2 - 120, 200
        esp_w, esp_h = 240, 350
        esp_bg = tuple(int(v * ca) for v in (20, 30, 50))
        esp_border = tuple(int(v * ca) for v in (0, 200, 150))
        draw.rounded_rectangle((esp_x, esp_y, esp_x+esp_w, esp_y+esp_h), radius=12,
                               fill=esp_bg, outline=esp_border, width=3)
        text_c(draw, 'ESP32', esp_y+15, get_font(24, bold=True), color=(0, 200, 150), alpha=ca)
        text_c(draw, 'DevKit V1', esp_y+45, get_font(14), color=(100, 150, 130), alpha=ca)

        # Pin labels on ESP32
        pins_left = ['D34 (ADC)', 'D35 (ADC)', 'D4', 'D21 (SDA)', 'D22 (SCL)', '3V3', 'GND']
        pins_right = ['D25', 'D26', 'D27', 'D33', 'D18', 'D19', 'GND']
        font_pin = get_font(11)
        for i, pin in enumerate(pins_left):
            py = esp_y + 80 + i * 35
            text_at(draw, pin, esp_x+10, py, font_pin, color=(100,130,120), alpha=ca)
        for i, pin in enumerate(pins_right):
            py = esp_y + 80 + i * 35
            bbox = draw.textbbox((0,0), pin, font=font_pin)
            pw = bbox[2] - bbox[0]
            text_at(draw, pin, esp_x+esp_w-pw-10, py, font_pin, color=(100,130,120), alpha=ca)

    # Connected components
    components = [
        ('OLED SSD1306', '128×64 I2C', (0, 163, 255), 'left', 1.5, 'D21/D22 (I2C)'),
        ('DHT22', 'Temp + Umid', (0, 200, 150), 'left', 2.0, 'D4'),
        ('Pot. BPM', 'Freq. Cardíaca', (255, 150, 50), 'left', 2.5, 'D34 (ADC)'),
        ('Pot. Atividade', 'Nível Ativ.', (255, 200, 50), 'left', 3.0, 'D35 (ADC)'),
        ('LED Verde', '220Ω → Normal', (0, 255, 68), 'right', 3.5, 'D25'),
        ('LED Amarelo', '220Ω → Atenção', (255, 204, 0), 'right', 4.0, 'D26'),
        ('LED Vermelho', '220Ω → Crítico', (255, 51, 51), 'right', 4.5, 'D27'),
        ('Buzzer', 'Alarme Sonoro', (200, 100, 100), 'right', 5.0, 'D33'),
        ('Botão Menu', 'Navegação (azul)', (50, 100, 255), 'right', 5.5, 'D18'),
        ('Botão Select', 'Interação (verde)', (50, 200, 100), 'right', 6.0, 'D19'),
    ]

    left_idx = 0
    right_idx = 0
    for name, desc, color, side, delay, pin in components:
        if t > delay:
            comp_a = ease_out(min(1, (t - delay) / 0.4))
            if side == 'left':
                cx = 80
                cy = 210 + left_idx * 75
                left_idx += 1
                # Connection line to ESP32
                line_c = tuple(int(v * comp_a * 0.3) for v in color)
                draw.line([(cx + 180, cy + 20), (esp_x - 5, cy + 20)], fill=line_c, width=1)
            else:
                cx = WIDTH - 330
                cy = 210 + right_idx * 55
                right_idx += 1
                line_c = tuple(int(v * comp_a * 0.3) for v in color)
                draw.line([(esp_x + esp_w + 5, cy + 15), (cx - 5, cy + 15)], fill=line_c, width=1)

            # Component box
            cw = 200 if side == 'left' else 250
            ch = 55 if side == 'left' else 40
            bg_c = tuple(int(v * comp_a * 0.08) for v in color)
            border_c = tuple(int(v * comp_a * 0.3) for v in color)
            draw.rounded_rectangle((cx, cy, cx+cw, cy+ch), radius=8, fill=bg_c, outline=border_c, width=1)
            text_at(draw, name, cx+10, cy+5, get_font(13, bold=True), color=color, alpha=comp_a)
            text_at(draw, desc, cx+10, cy+25, get_font(11), color=(140,140,150), alpha=comp_a)

    # Total connections
    if t > 8.0:
        tc_a = ease_out(min(1, (t - 8.0) / 0.5))
        text_c(draw, '14 componentes  •  29 conexões  •  Simulação completa no Wokwi', 610,
               get_font(18), color=(255, 150, 50), alpha=tc_a)
        text_c(draw, 'Circuito pronto para carregar em ESP32 real — mesmo código funciona', 645,
               get_font(16), color=(150, 130, 100), alpha=tc_a)

    return img


def scene_encerramento(t, dur):
    """Cena 13: Encerramento (2:40 - 3:00)"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (0,0,0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (13, 26, 45), (0, 0, 0))
    particles(draw, t, 35, (0, 200, 150))

    # Logo
    logo_a = ease_out(min(1, t / 0.8))
    glow_a = logo_a * 0.08
    for dx in [-2, 0, 2]:
        for dy in [-2, 0, 2]:
            if dx == 0 and dy == 0:
                continue
            text_c(draw, 'Level UP', 100 + dy, get_font(110, bold=True),
                   color=(0, 200, 150), alpha=glow_a)
    text_c(draw, 'Level UP', 100, get_font(110, bold=True), color=(0, 200, 150), alpha=logo_a)

    if t > 0.6:
        sl_a = ease_out(min(1, (t - 0.6) / 0.5))
        text_c(draw, 'Sua saúde, seu jogo, seu nível!', 260, get_font(32), alpha=sl_a)

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
            cx = WIDTH//2 - 380 + i * 290
            cy = 340
            cw, ch = 260, 110
            rounded_card(draw, cx, cy, cw, ch, color, ma)
            text_at(draw, val, cx+18, cy+12, get_font(36, bold=True), color=color, alpha=ma)
            for j, line in enumerate(desc.split('\n')):
                text_at(draw, line, cx+18, cy+60+j*20, get_font(15), color=(160,165,175), alpha=ma)

    # CarePlus
    if t > 3.0:
        cp_a = ease_out(min(1, (t - 3.0) / 0.5))
        text_c(draw, 'Evolução estratégica da plataforma Blua — CarePlus', 490,
               get_font(18), color=(100, 130, 160), alpha=cp_a)

    # Team
    if t > 4.0:
        cr_a = ease_out(min(1, (t - 4.0) / 0.7))
        line_c = tuple(int(v * cr_a * 0.2) for v in (255,255,255))
        draw.line([(WIDTH//2 - 200, 530), (WIDTH//2 + 200, 530)], fill=line_c, width=1)
        text_c(draw, 'Equipe', 545, get_font(15), color=(90, 100, 120), alpha=cr_a)
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
                text_c(draw, name, 575 + i * 26, get_font(17, bold=True),
                       color=(180, 185, 200), alpha=m_a)

    # Institution
    if t > 6.0:
        inst_a = ease_out(min(1, (t - 6.0) / 0.5))
        text_c(draw, 'FIAP — 1º Ano Ciência da Computação — PCP Sprint 3 — 2025', 730,
               get_font(14), color=(70, 80, 100), alpha=inst_a)
        text_c(draw, 'Prof. Sandro  |  Prof. Allan Roberto Molto', 755,
               get_font(14), color=(70, 80, 100), alpha=inst_a)

    # Fade to black
    if t > dur - 3.0:
        fade = 1 - ease_out((dur - t) / 3.0)
        overlay = Image.new('RGB', (WIDTH, HEIGHT), (0,0,0))
        img = Image.blend(img, overlay, min(1.0, fade * 0.9))

    return img


# ==================================================================================
#  MAIN: COMBINE ALL SCENES INTO ONE VIDEO
# ==================================================================================
SCENE_FUNCS = [
    scene_abertura,
    scene_problema,
    scene_solucao,
    scene_pilar1,
    scene_pilar2,
    scene_pilar3,
    scene_cronograma,
    scene_specs,
    scene_arquitetura,
    scene_telas_oled,
    scene_dashboard_web,
    scene_circuito,
    scene_encerramento,
]

# Section mapping for the badge
SECTION_MAP = {
    0: (1, 'Proposta do Projeto'),
    1: (1, 'Proposta do Projeto'),
    2: (1, 'Proposta do Projeto'),
    3: (1, 'Proposta do Projeto'),
    4: (1, 'Proposta do Projeto'),
    5: (1, 'Proposta do Projeto'),
    6: (2, 'Cronograma + Especificações'),
    7: (2, 'Cronograma + Especificações'),
    8: (3, 'Descrição do Software'),
    9: (3, 'Descrição do Software'),
    10: (3, 'Descrição do Software'),
    11: (4, 'Hardware / Protótipo Wokwi'),
    12: (4, 'Encerramento'),
}


def make_video():
    offsets = []
    t_offset = 0
    for s in SCENES:
        offsets.append(t_offset)
        t_offset += s['dur']

    def make_frame(t):
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

        img = SCENE_FUNCS[scene_idx](local_t, dur)

        # Cross-fade transition
        if local_t < TRANSITION and scene_idx > 0:
            prev_dur = SCENES[scene_idx - 1]['dur']
            prev_local_t = prev_dur - (TRANSITION - local_t)
            prev_img = SCENE_FUNCS[scene_idx - 1](prev_local_t, prev_dur)
            blend = ease_in_out(local_t / TRANSITION)
            img = Image.blend(prev_img, img, blend)

        # Overlays
        draw = ImageDraw.Draw(img)
        progress = t / TOTAL_DUR
        scene_name = SCENES[scene_idx]['name']
        draw_progress_bar(draw, progress, scene_name, alpha=0.6)

        sec_num, sec_title = SECTION_MAP.get(scene_idx, (1, ''))
        draw_section_badge(draw, sec_num, sec_title, alpha=0.7)

        return np.array(img)

    print(f'Gerando vídeo pitch de 3 minutos ({TOTAL_DUR}s)...')
    print(f'Cenas: {len(SCENES)}')
    for i, s in enumerate(SCENES):
        m = offsets[i] // 60
        sec = offsets[i] % 60
        print(f'  [{i+1:2d}] {m}:{sec:02d} — {s["name"]} ({s["dur"]}s)')
    print()

    clip = VideoClip(make_frame, duration=TOTAL_DUR)
    output_path = os.path.join(OUTPUT_DIR, 'Video_Pitch_3min_LevelUP.mp4')
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
    make_video()
