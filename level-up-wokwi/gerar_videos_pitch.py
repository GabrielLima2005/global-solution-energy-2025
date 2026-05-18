# -*- coding: utf-8 -*-
"""
Gerador de clipes de vídeo para o pitch do Level UP.
Gera 7 vídeos MP4 curtos (5-8s cada) com animações de texto
para usar como inserts durante a gravação do vídeo pitch.
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

# Try to use moviepy v2 API, fall back to v1
try:
    from moviepy import VideoClip, AudioClip, concatenate_videoclips
    MOVIEPY_V2 = True
except ImportError:
    from moviepy.editor import VideoClip, AudioClip, concatenate_videoclips
    MOVIEPY_V2 = False

# =================== CONFIG ===================
WIDTH, HEIGHT = 1920, 1080
FPS = 30
OUTPUT_DIR = '/home/ubuntu/repos/global-solution-energy-2025/level-up-wokwi/videos_pitch'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =================== FONTES ===================
def get_font(size, bold=False):
    """Tenta carregar fonte do sistema"""
    font_paths = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
    ]
    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def get_mono_font(size):
    paths = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf',
    ]
    for path in paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

# =================== HELPERS ===================
def ease_out(t):
    """Ease-out cubic"""
    return 1 - (1 - t) ** 3

def ease_in_out(t):
    """Ease-in-out cubic"""
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - (-2 * t + 2) ** 3 / 2

def lerp(a, b, t):
    return a + (b - a) * t

def fade_alpha(t, fade_in=0.5, fade_out=0.5, duration=5.0):
    """Calculate alpha for fade in/out"""
    if t < fade_in:
        return ease_out(t / fade_in)
    elif t > duration - fade_out:
        return ease_out((duration - t) / fade_out)
    return 1.0

def draw_text_centered(draw, text, y, font, color=(255, 255, 255), alpha=1.0):
    """Draw centered text"""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (WIDTH - tw) // 2
    c = tuple(int(v * alpha) for v in color)
    draw.text((x, y), text, font=font, fill=c)

def draw_text_at(draw, text, x, y, font, color=(255, 255, 255), alpha=1.0):
    c = tuple(int(v * alpha) for v in color)
    draw.text((x, y), text, font=font, fill=c)

def gradient_bg(draw, color_top, color_bot):
    """Draw vertical gradient background"""
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(lerp(color_top[0], color_bot[0], t))
        g = int(lerp(color_top[1], color_bot[1], t))
        b = int(lerp(color_top[2], color_bot[2], t))
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

def draw_rounded_rect(draw, xy, fill, radius=15):
    """Draw rounded rectangle"""
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill)

def make_clip(make_frame_func, duration, filename):
    """Create and save a video clip"""
    def make_frame_array(t):
        img = make_frame_func(t, duration)
        return np.array(img)

    clip = VideoClip(make_frame_array, duration=duration)
    output_path = os.path.join(OUTPUT_DIR, filename)
    clip.write_videofile(output_path, fps=FPS, codec='libx264',
                         audio=False, logger='bar',
                         preset='medium', bitrate='5000k')
    clip.close()
    print(f'  -> {filename} ({os.path.getsize(output_path) // 1024} KB)')
    return output_path


# =================== SLIDE 1: ABERTURA ===================
def slide1_frame(t, dur):
    img = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (10, 5, 20), (0, 0, 0))

    alpha = fade_alpha(t, 0.3, 0.8, dur)

    # "60%" - grande, aparece com fade + scale effect
    num_alpha = min(1.0, t / 1.0) if t < 1.0 else alpha
    font_big = get_font(180, bold=True)
    color_60 = (255, int(77 + 60 * num_alpha), int(30 + 30 * num_alpha))
    draw_text_centered(draw, '60%', 250, font_big, color=color_60, alpha=num_alpha)

    # Subtitle appears after 0.8s
    if t > 0.8:
        sub_alpha = min(1.0, (t - 0.8) / 0.8) * alpha
        font_sub = get_font(42)
        draw_text_centered(draw, 'das doenças crônicas poderiam ser', 480, font_sub, alpha=sub_alpha)
        font_sub_bold = get_font(44, bold=True)
        draw_text_centered(draw, 'evitadas com monitoramento adequado', 540, font_sub_bold, alpha=sub_alpha)

    # Source appears after 2s
    if t > 2.0:
        src_alpha = min(1.0, (t - 2.0) / 0.6) * alpha
        font_src = get_font(20)
        draw_text_centered(draw, 'Fonte: Organização Mundial da Saúde (OMS)', 650, font_src,
                           color=(150, 150, 150), alpha=src_alpha)

    # Subtle pulsing glow effect on the number
    if t < dur - 1:
        import math
        glow = 0.3 + 0.15 * math.sin(t * 2.5)
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx == 0 and dy == 0:
                    continue

    return img


# =================== SLIDE 2: LEVEL UP LOGO ===================
def slide2_frame(t, dur):
    img = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (10, 22, 40), (10, 10, 26))

    alpha = fade_alpha(t, 0.3, 0.8, dur)

    # Logo text slides up
    slide_offset = max(0, 50 * (1 - ease_out(min(1, t / 0.8))))
    logo_y = int(280 + slide_offset)
    font_logo = get_font(130, bold=True)
    logo_alpha = min(1.0, t / 0.6) * alpha
    draw_text_centered(draw, 'Level UP', logo_y, font_logo, color=(0, 200, 150), alpha=logo_alpha)

    # Subtitle
    if t > 0.5:
        sub_alpha = min(1.0, (t - 0.5) / 0.6) * alpha
        font_sub = get_font(32)
        draw_text_centered(draw, 'Health Monitoring System v2.0', 440, font_sub,
                           color=(180, 180, 200), alpha=sub_alpha)

    # Tagline box
    if t > 1.0:
        tag_alpha = min(1.0, (t - 1.0) / 0.6) * alpha
        font_tag = get_font(26)
        text = 'Cuidado proativo, inteligente e centrado no paciente'
        bbox = draw.textbbox((0, 0), text, font=font_tag)
        tw = bbox[2] - bbox[0]
        bx = (WIDTH - tw) // 2 - 30
        c_border = tuple(int(v * tag_alpha) for v in (0, 200, 150))
        draw.rounded_rectangle((bx, 520, bx + tw + 60, 575), radius=30,
                               outline=c_border, width=2)
        draw_text_centered(draw, text, 535, font_tag, color=(0, 200, 150), alpha=tag_alpha)

    # Brand line
    if t > 1.8:
        br_alpha = min(1.0, (t - 1.8) / 0.6) * alpha
        font_br = get_font(22)
        draw_text_centered(draw, 'Uma evolução estratégica da plataforma Blua — CarePlus', 640, font_br,
                           color=(120, 120, 140), alpha=br_alpha)

    return img


# =================== SLIDE 3: PILAR 1 ===================
def slide3_frame(t, dur):
    img = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (10, 26, 10), (10, 10, 26))

    alpha = fade_alpha(t, 0.3, 0.8, dur)

    # Pilar label
    if t > 0.2:
        p_alpha = min(1.0, (t - 0.2) / 0.4) * alpha
        font_label = get_font(22)
        draw_text_centered(draw, 'P I L A R   1', 180, font_label, color=(0, 200, 150), alpha=p_alpha)

    # Title
    if t > 0.4:
        t_alpha = min(1.0, (t - 0.4) / 0.5) * alpha
        font_title = get_font(64, bold=True)
        draw_text_centered(draw, 'Monitoramento Contínuo', 220, font_title, alpha=t_alpha)

    # LEDs appear one by one
    led_colors = [(0, 255, 68), (255, 204, 0), (255, 51, 51)]
    led_labels = ['Normal', 'Atenção', 'Crítico']
    led_start_times = [1.0, 1.5, 2.0]

    for i, (color, label, start) in enumerate(zip(led_colors, led_labels, led_start_times)):
        if t > start:
            led_alpha = min(1.0, (t - start) / 0.4) * alpha
            cx = WIDTH // 2 - 150 + i * 150
            cy = 400
            r = 40
            fill = tuple(int(v * led_alpha) for v in color)
            draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill)
            font_led = get_font(16)
            lbl_bbox = draw.textbbox((0, 0), label, font=font_led)
            lw = lbl_bbox[2] - lbl_bbox[0]
            draw_text_at(draw, label, cx - lw // 2, cy + 50, font_led,
                         color=(180, 180, 180), alpha=led_alpha)

    # Sensor cards
    sensors = [
        ('Freq. Cardíaca', '75 BPM'),
        ('Temperatura', '36.5 °C'),
        ('Atividade', '45%'),
        ('Qual. Sono', '72%'),
    ]
    card_start = 2.5
    if t > card_start:
        card_alpha = min(1.0, (t - card_start) / 0.5) * alpha
        card_w = 200
        total_w = len(sensors) * card_w + (len(sensors) - 1) * 20
        start_x = (WIDTH - total_w) // 2
        for i, (label, value) in enumerate(sensors):
            x = start_x + i * (card_w + 20)
            y = 530
            fill_bg = tuple(int(v * card_alpha) for v in (30, 30, 45))
            draw.rounded_rectangle((x, y, x + card_w, y + 90), radius=12, fill=fill_bg)
            font_lbl = get_font(16)
            draw_text_at(draw, label, x + 15, y + 12, font_lbl,
                         color=(180, 180, 200), alpha=card_alpha)
            font_val = get_font(28, bold=True)
            draw_text_at(draw, value, x + 15, y + 40, font_val,
                         color=(0, 200, 150), alpha=card_alpha)

    return img


# =================== SLIDE 4: PILAR 2 ===================
def slide4_frame(t, dur):
    img = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (26, 16, 64), (10, 10, 26))

    alpha = fade_alpha(t, 0.3, 0.8, dur)

    # Labels
    if t > 0.2:
        p_alpha = min(1.0, (t - 0.2) / 0.4) * alpha
        draw_text_centered(draw, 'P I L A R   2', 150, get_font(22), color=(167, 139, 250), alpha=p_alpha)

    if t > 0.4:
        t_alpha = min(1.0, (t - 0.4) / 0.5) * alpha
        draw_text_centered(draw, 'Check-up Digital com IA', 190, get_font(58, bold=True), alpha=t_alpha)

    # Check-up box
    if t > 1.0:
        box_alpha = min(1.0, (t - 1.0) / 0.5) * alpha
        bx, by = WIDTH // 2 - 280, 310
        bw, bh = 560, 180
        fill_box = tuple(int(v * box_alpha * 0.5) for v in (20, 15, 40))
        border_c = tuple(int(v * box_alpha) for v in (167, 139, 250))
        draw.rounded_rectangle((bx, by, bx + bw, by + bh), radius=16, fill=fill_box, outline=border_c, width=2)

        draw_text_at(draw, 'CHECK-UP DIGITAL — Pergunta 3/8', bx + 30, by + 20,
                     get_font(16), color=(167, 139, 250), alpha=box_alpha)
        draw_text_at(draw, 'Tontura frequente?', bx + 30, by + 55,
                     get_font(28), alpha=box_alpha)

        # Buttons
        btn_y = by + 110
        green = tuple(int(v * box_alpha) for v in (0, 200, 150))
        draw.rounded_rectangle((bx + 30, btn_y, bx + 170, btn_y + 45), radius=8, fill=green)
        draw_text_at(draw, 'SIM (Select)', bx + 50, btn_y + 10, get_font(18, bold=True),
                     color=(0, 0, 0), alpha=box_alpha)

        gray = tuple(int(v * box_alpha * 0.2) for v in (255, 255, 255))
        draw.rounded_rectangle((bx + 200, btn_y, bx + 370, btn_y + 45), radius=8, fill=gray,
                               outline=tuple(int(v * box_alpha * 0.3) for v in (255, 255, 255)), width=1)
        draw_text_at(draw, 'NÃO (Menu)', bx + 225, btn_y + 10, get_font(18, bold=True), alpha=box_alpha)

    # Risk bar
    if t > 2.0:
        risk_alpha = min(1.0, (t - 2.0) / 0.6) * alpha
        bar_x, bar_y = WIDTH // 2 - 200, 560
        bar_w, bar_h = 300, 24
        bg_bar = tuple(int(v * risk_alpha * 0.2) for v in (255, 255, 255))
        draw.rounded_rectangle((bar_x, bar_y, bar_x + bar_w, bar_y + bar_h), radius=12, fill=bg_bar)

        fill_pct = min(0.42, 0.42 * min(1.0, (t - 2.0) / 1.0))
        fill_w = int(bar_w * fill_pct)
        if fill_w > 0:
            # Gradient green to yellow
            for px in range(fill_w):
                pt = px / bar_w
                r = int(lerp(0, 255, pt) * risk_alpha)
                g = int(lerp(200, 204, pt) * risk_alpha)
                b = int(lerp(150, 0, pt) * risk_alpha)
                draw.line([(bar_x + px, bar_y + 2), (bar_x + px, bar_y + bar_h - 2)], fill=(r, g, b))

        # Score text
        draw_text_at(draw, '42/100', bar_x + bar_w + 20, bar_y - 5, get_font(32, bold=True),
                     color=(255, 204, 0), alpha=risk_alpha)

        draw_text_centered(draw, 'Score de Risco → Classificação: RISCO MODERADO', 610, get_font(18),
                           color=(150, 150, 170), alpha=risk_alpha)

    return img


# =================== SLIDE 5: PILAR 3 ===================
def slide5_frame(t, dur):
    img = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (26, 26, 0), (10, 10, 26))

    alpha = fade_alpha(t, 0.3, 0.8, dur)

    if t > 0.2:
        p_alpha = min(1.0, (t - 0.2) / 0.4) * alpha
        draw_text_centered(draw, 'P I L A R   3', 150, get_font(22), color=(251, 191, 36), alpha=p_alpha)

    if t > 0.4:
        t_alpha = min(1.0, (t - 0.4) / 0.5) * alpha
        draw_text_centered(draw, 'Gamificação', 195, get_font(64, bold=True), alpha=t_alpha)

    # Game stat cards
    stats = [('3', 'Nível'), ('250', 'Pontos'), ('2', 'Check-ups')]
    card_start = 1.0
    if t > card_start:
        for i, (val, lbl) in enumerate(stats):
            delay = card_start + i * 0.3
            if t > delay:
                c_alpha = min(1.0, (t - delay) / 0.4) * alpha
                cx = WIDTH // 2 - 240 + i * 220
                cy = 340
                fill_bg = tuple(int(v * c_alpha) for v in (30, 24, 5))
                border_c = tuple(int(v * c_alpha) for v in (251, 191, 36))
                draw.rounded_rectangle((cx, cy, cx + 180, cy + 110), radius=16,
                                       fill=fill_bg, outline=border_c, width=1)
                font_val = get_font(48, bold=True)
                val_bbox = draw.textbbox((0, 0), val, font=font_val)
                vw = val_bbox[2] - val_bbox[0]
                draw_text_at(draw, val, cx + (180 - vw) // 2, cy + 15, font_val,
                             color=(251, 191, 36), alpha=c_alpha)
                font_lbl = get_font(16)
                lbl_bbox = draw.textbbox((0, 0), lbl, font=font_lbl)
                lw = lbl_bbox[2] - lbl_bbox[0]
                draw_text_at(draw, lbl, cx + (180 - lw) // 2, cy + 75, font_lbl,
                             color=(150, 150, 150), alpha=c_alpha)

    # Rank progression
    ranks = ['Iniciante', 'Aprendiz Ativo', 'Guerreiro Fit', 'Expert Vital', 'Mestre Saúde']
    rank_colors = [(150, 150, 150), (0, 200, 150), (251, 191, 36), (167, 139, 250), (255, 77, 77)]
    rank_start = 2.5
    if t > rank_start:
        r_alpha = min(1.0, (t - rank_start) / 0.6) * alpha
        total_w = 0
        font_rank = get_font(16, bold=True)
        rank_widths = []
        for r in ranks:
            bbox = draw.textbbox((0, 0), r, font=font_rank)
            w = bbox[2] - bbox[0] + 40
            rank_widths.append(w)
            total_w += w
        total_w += (len(ranks) - 1) * 40  # arrows space
        sx = (WIDTH - total_w) // 2
        cy = 530
        for i, (rank, color, rw) in enumerate(zip(ranks, rank_colors, rank_widths)):
            fill_c = tuple(int(v * r_alpha * 0.15) for v in color)
            border = tuple(int(v * r_alpha * 0.5) for v in color)
            draw.rounded_rectangle((sx, cy, sx + rw, cy + 36), radius=18, fill=fill_c, outline=border, width=1)
            text_c = tuple(int(v * r_alpha) for v in color)
            draw_text_at(draw, rank, sx + 20, cy + 7, font_rank, color=color, alpha=r_alpha)
            sx += rw
            if i < len(ranks) - 1:
                draw_text_at(draw, '→', sx + 12, cy + 5, get_font(18),
                             color=(100, 100, 100), alpha=r_alpha)
                sx += 40

    # Impact text
    if t > 3.5:
        imp_alpha = min(1.0, (t - 3.5) / 0.5) * alpha
        draw_text_centered(draw, 'Aumento de até 30% na adesão ao tratamento', 620, get_font(24),
                           color=(200, 200, 200), alpha=imp_alpha)

    return img


# =================== SLIDE 6: DASHBOARD ===================
def slide6_frame(t, dur):
    img = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (0, 26, 46), (10, 10, 26))

    alpha = fade_alpha(t, 0.3, 0.8, dur)

    if t > 0.2:
        p_alpha = min(1.0, (t - 0.2) / 0.4) * alpha
        draw_text_centered(draw, 'W I F I   +   W E B   S E R V E R', 100, get_font(20),
                           color=(0, 163, 255), alpha=p_alpha)

    if t > 0.4:
        t_alpha = min(1.0, (t - 0.4) / 0.5) * alpha
        draw_text_centered(draw, 'Dashboard em Tempo Real', 140, get_font(56, bold=True), alpha=t_alpha)

    # Dashboard mockup
    if t > 0.8:
        d_alpha = min(1.0, (t - 0.8) / 0.5) * alpha
        dx, dy = WIDTH // 2 - 370, 240
        dw, dh = 740, 420
        fill_bg = tuple(int(v * d_alpha) for v in (17, 24, 39))
        border = tuple(int(v * d_alpha * 0.3) for v in (0, 163, 255))
        draw.rounded_rectangle((dx, dy, dx + dw, dy + dh), radius=16, fill=fill_bg, outline=border, width=2)

        # Header
        draw_text_centered(draw, 'LEVEL UP', dy + 20, get_font(26, bold=True),
                           color=(0, 200, 150), alpha=d_alpha)
        draw_text_centered(draw, 'Health Monitoring System v2.0', dy + 52,
                           get_font(14), color=(120, 120, 140), alpha=d_alpha)

        # Status bar
        status_fill = tuple(int(v * d_alpha * 0.15) for v in (0, 200, 150))
        draw.rounded_rectangle((dx + 40, dy + 80, dx + dw - 40, dy + 110), radius=8, fill=status_fill)
        draw_text_centered(draw, 'NORMAL — SINAIS VITAIS ESTÁVEIS', dy + 85,
                           get_font(16, bold=True), color=(0, 200, 150), alpha=d_alpha)

        # Data cards grid
        cards = [
            ('Freq. Cardíaca', '75 BPM', (255, 77, 77)),
            ('Temperatura', '36.5 °C', (0, 163, 255)),
            ('Atividade', '45%', (0, 200, 150)),
            ('Qual. Sono', '72%', (167, 139, 250)),
            ('Passos', '6.750', (251, 191, 36)),
            ('Gamificação', 'Lv.3', (0, 200, 150)),
        ]

        for i, (label, value, color) in enumerate(cards):
            card_delay = 1.2 + i * 0.15
            if t > card_delay:
                c_alpha = min(1.0, (t - card_delay) / 0.3) * d_alpha
                col = i % 3
                row = i // 3
                cx = dx + 40 + col * 225
                cy_card = dy + 130 + row * 130
                cw, ch = 210, 110
                card_fill = tuple(int(v * c_alpha * 0.08) for v in (255, 255, 255))
                card_border = tuple(int(v * c_alpha * 0.12) for v in (255, 255, 255))
                draw.rounded_rectangle((cx, cy_card, cx + cw, cy_card + ch), radius=10,
                                       fill=card_fill, outline=card_border, width=1)
                draw_text_at(draw, label, cx + 15, cy_card + 15, get_font(13),
                             color=(150, 150, 170), alpha=c_alpha)
                draw_text_at(draw, value, cx + 15, cy_card + 45, get_font(30, bold=True),
                             color=color, alpha=c_alpha)

    # WiFi info
    if t > 3.0:
        w_alpha = min(1.0, (t - 3.0) / 0.5) * alpha
        wifi_items = [
            ('SSID: LevelUP-Health', (0, 163, 255)),
            ('Senha: levelup123', (0, 163, 255)),
            ('http://192.168.4.1', (0, 163, 255)),
        ]
        total_w = 0
        font_wifi = get_font(16)
        widths = []
        for text, _ in wifi_items:
            bbox = draw.textbbox((0, 0), text, font=font_wifi)
            w = bbox[2] - bbox[0] + 40
            widths.append(w)
            total_w += w
        total_w += (len(wifi_items) - 1) * 20
        sx = (WIDTH - total_w) // 2
        for i, ((text, color), w) in enumerate(zip(wifi_items, widths)):
            fill_c = tuple(int(v * w_alpha * 0.1) for v in color)
            border_c = tuple(int(v * w_alpha * 0.3) for v in color)
            draw.rounded_rectangle((sx, 690, sx + w, 725), radius=10,
                                   fill=fill_c, outline=border_c, width=1)
            draw_text_at(draw, text, sx + 20, 695, font_wifi, color=color, alpha=w_alpha)
            sx += w + 20

    return img


# =================== SLIDE 7: ENCERRAMENTO ===================
def slide7_frame(t, dur):
    img = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, (13, 26, 45), (0, 0, 0))

    alpha = fade_alpha(t, 0.3, 1.5, dur)

    # Logo
    if t > 0.2:
        l_alpha = min(1.0, (t - 0.2) / 0.6) * alpha
        draw_text_centered(draw, 'Level UP', 160, get_font(110, bold=True),
                           color=(0, 200, 150), alpha=l_alpha)

    # Slogan
    if t > 0.8:
        s_alpha = min(1.0, (t - 0.8) / 0.5) * alpha
        draw_text_centered(draw, 'Sua saúde, seu jogo, seu nível!', 310, get_font(36),
                           color=(220, 220, 230), alpha=s_alpha)

    # Impact metrics
    metrics = [
        ('-20%', 'Redução de custos\nassistenciais', (0, 200, 150)),
        ('+30%', 'Aumento da adesão\nao tratamento', (0, 163, 255)),
        ('+25%', 'Produtividade\nclínica', (167, 139, 250)),
    ]
    met_start = 1.5
    for i, (val, desc, color) in enumerate(metrics):
        delay = met_start + i * 0.3
        if t > delay:
            m_alpha = min(1.0, (t - delay) / 0.4) * alpha
            cx = WIDTH // 2 - 340 + i * 280
            cy = 420
            fill_bg = tuple(int(v * m_alpha * 0.06) for v in (255, 255, 255))
            border_c = tuple(int(v * m_alpha * 0.12) for v in (255, 255, 255))
            draw.rounded_rectangle((cx, cy, cx + 240, cy + 130), radius=14,
                                   fill=fill_bg, outline=border_c, width=1)
            draw_text_at(draw, val, cx + 20, cy + 15, get_font(36, bold=True),
                         color=color, alpha=m_alpha)
            font_desc = get_font(15)
            for j, line in enumerate(desc.split('\n')):
                draw_text_at(draw, line, cx + 20, cy + 65 + j * 22, font_desc,
                             color=(180, 180, 190), alpha=m_alpha)

    # Credits
    if t > 3.0:
        cr_alpha = min(1.0, (t - 3.0) / 0.6) * alpha
        credits = [
            'Nicolas Araújo de Oliveira — RM 566780',
            'Pedro Ivson Falcão De Leucas',
            'Gabriel Lima Da Silva — RM 568436',
        ]
        font_cr = get_font(18)
        for i, line in enumerate(credits):
            draw_text_centered(draw, line, 620 + i * 30, font_cr,
                               color=(160, 160, 170), alpha=cr_alpha)

    if t > 4.0:
        inst_alpha = min(1.0, (t - 4.0) / 0.5) * alpha
        draw_text_centered(draw, 'FIAP — 1º Ano Ciência da Computação — PCP Sprint 3 — 2025',
                           740, get_font(14), color=(100, 100, 110), alpha=inst_alpha)

    return img


# =================== MAIN ===================
if __name__ == '__main__':
    print('Gerando vídeos do pitch Level UP...\n')

    slides = [
        ('01_Abertura_60pct.mp4', slide1_frame, 6),
        ('02_LevelUP_Logo.mp4', slide2_frame, 6),
        ('03_Pilar1_Monitoramento.mp4', slide3_frame, 8),
        ('04_Pilar2_Checkup_IA.mp4', slide4_frame, 8),
        ('05_Pilar3_Gamificacao.mp4', slide5_frame, 7),
        ('06_Dashboard_Web.mp4', slide6_frame, 8),
        ('07_Encerramento.mp4', slide7_frame, 8),
    ]

    for i, (filename, frame_func, duration) in enumerate(slides):
        print(f'[{i+1}/7] Gerando {filename} ({duration}s)...')
        make_clip(frame_func, duration, filename)

    print(f'\nTodos os vídeos foram salvos em: {OUTPUT_DIR}')
    total_size = sum(os.path.getsize(os.path.join(OUTPUT_DIR, f)) for f in os.listdir(OUTPUT_DIR) if f.endswith('.mp4'))
    print(f'Tamanho total: {total_size // 1024} KB ({total_size // (1024*1024)} MB)')
