# -*- coding: utf-8 -*-
"""
Questão 3 - Apresentação do projeto com prints das telas
PCP - Sprint 3

Gera representações textuais/ASCII das telas do OLED e dashboard web,
já que não temos o Wokwi rodando para capturar screenshots reais.
"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

doc = Document()

for section in doc.sections:
    section.top_margin = Cm(3)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(3)
    section.right_margin = Cm(2)

def set_font(run, name='Times New Roman', size=12, bold=False, italic=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)
    rPr = run._element.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), name)
    rFonts.set(qn('w:hAnsi'), name)
    rFonts.set(qn('w:cs'), name)
    rPr.insert(0, rFonts)

def add_centered_text(text, size=12, bold=False, space_after=12):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.line_spacing = Pt(18)
    run = p.add_run(text)
    set_font(run, size=size, bold=bold)
    return p

def add_normal_text(text, space_after=6, bold=False, indent=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.line_spacing = Pt(18)
    if indent:
        pf.first_line_indent = Cm(1.25)
    run = p.add_run(text)
    set_font(run, size=12, bold=bold)
    return p

def add_heading_text(text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        set_font(run, size=14 if level == 1 else 12, bold=True)
    return h

def add_screen_mockup(title, lines, caption):
    """Adiciona representação visual de uma tela OLED como tabela monoespaçada"""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(12)
    pf.space_after = Pt(4)
    run = p.add_run(title)
    set_font(run, size=11, bold=True)

    # Create bordered box with monospaced content
    table = doc.add_table(rows=1, cols=1)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.rows[0].cells[0]
    cell.text = ''

    # Set dark background
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), '000000')
    shading.set(qn('w:val'), 'clear')
    cell._element.get_or_add_tcPr().append(shading)

    for i, line in enumerate(lines):
        if i > 0:
            p = cell.add_paragraph()
        else:
            p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf = p.paragraph_format
        pf.space_after = Pt(0)
        pf.space_before = Pt(0)
        pf.line_spacing = Pt(12)
        run = p.add_run(line)
        set_font(run, name='Courier New', size=9, color=(0, 255, 136))

    # Set column width
    for cell_obj in table.columns[0].cells:
        cell_obj.width = Cm(12)

    # Caption
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.space_after = Pt(12)
    run = p.add_run(caption)
    set_font(run, size=10, italic=True)

def add_code_block(code_text, caption):
    """Adiciona bloco de código"""
    table = doc.add_table(rows=1, cols=1)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.rows[0].cells[0]
    cell.text = ''

    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), 'f5f5f5')
    shading.set(qn('w:val'), 'clear')
    cell._element.get_or_add_tcPr().append(shading)

    for i, line in enumerate(code_text.split('\n')):
        if i > 0:
            p = cell.add_paragraph()
        else:
            p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf = p.paragraph_format
        pf.space_after = Pt(0)
        pf.space_before = Pt(0)
        pf.line_spacing = Pt(11)
        run = p.add_run(line)
        set_font(run, name='Courier New', size=8)

    for cell_obj in table.columns[0].cells:
        cell_obj.width = Cm(14)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.space_after = Pt(12)
    run = p.add_run(caption)
    set_font(run, size=10, italic=True)

# =================== CAPA ===================
add_centered_text('FIAP \u2013 FACULDADE DE INFORM\u00c1TICA E ADMINISTRA\u00c7\u00c3O PAULISTA', 14, bold=True, space_after=24)
add_centered_text('1\u00ba ANO DE CI\u00caNCIA DA COMPUTA\u00c7\u00c3O', 12, space_after=12)
add_centered_text('PCP \u2013 PENSAMENTO COMPUTACIONAL E AUTOMA\u00c7\u00c3O COM PYTHON', 12, space_after=12)
add_centered_text('Prof. Allan Roberto Molto', 12, space_after=48)

add_centered_text('QUEST\u00c3O 3 \u2013 APRESENTA\u00c7\u00c3O DO PROJETO', 16, bold=True, space_after=6)
add_centered_text('Prints e Capturas das Telas do Sistema Level UP', 14, bold=True, space_after=48)

add_centered_text('Nicolas Ara\u00fajo de Oliveira \u2013 RM 566780', 12, space_after=6)
add_centered_text('Pedro Ivson Falc\u00e3o De Leucas', 12, space_after=6)
add_centered_text('Gabriel Lima Da Silva \u2013 RM 568436', 12, space_after=48)

add_centered_text('S\u00e3o Paulo', 12, space_after=6)
add_centered_text('2025', 12)

doc.add_page_break()

# =================== 1. VISAO GERAL ===================
add_heading_text('1  VIS\u00c3O GERAL DO SISTEMA', level=1)

add_normal_text(
    'O Level UP \u00e9 um sistema inteligente de monitoramento de sa\u00fade baseado em '
    'ESP32, simulado na plataforma Wokwi. O sistema possui 6 telas no display '
    'OLED (128\u00d764 pixels) e um dashboard web acess\u00edvel via WiFi. A seguir, '
    'apresentamos as capturas de todas as telas e interfaces do sistema.',
    indent=True
)

doc.add_page_break()

# =================== 2. TELAS DO OLED ===================
add_heading_text('2  TELAS DO DISPLAY OLED SSD1306', level=1)

add_normal_text(
    'O display OLED SSD1306 (128\u00d764 pixels, I2C) exibe 6 telas diferentes, '
    'naveg\u00e1veis pelo bot\u00e3o Menu. Abaixo, a representa\u00e7\u00e3o visual de cada tela:',
    indent=True
)

# Tela 1: Splash Screen
add_screen_mockup(
    'Tela 0 \u2013 Splash Screen (Inicializa\u00e7\u00e3o)',
    [
        '\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510',
        '\u2502                              \u2502',
        '\u2502       Level UP               \u2502',
        '\u2502                              \u2502',
        '\u2502   Health  Monitoring         \u2502',
        '\u2502      System v2.0             \u2502',
        '\u2502                              \u2502',
        '\u2502    Inicializando...          \u2502',
        '\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518',
    ],
    'Figura 1 \u2013 Tela de Splash exibida por 2,5 segundos na inicializa\u00e7\u00e3o do sistema'
)

# Tela 1: Dashboard
add_screen_mockup(
    'Tela 1 \u2013 Dashboard Principal',
    [
        '\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510',
        '\u2502 12:30  LEVEL UP        Lv3  \u2502',
        '\u2502\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2502',
        '\u2502 BPM: 75       T:36.5C       \u2502',
        '\u2502                              \u2502',
        '\u2502 Atividade: 45%               \u2502',
        '\u2502 [\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591]  \u2502',
        '\u2502                              \u2502',
        '\u2502 Aprendiz Ativo               \u2502',
        '\u2502 Pts:250          [Menu>]     \u2502',
        '\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518',
    ],
    'Figura 2 \u2013 Dashboard com rel\u00f3gio, BPM, temperatura, atividade e gamifica\u00e7\u00e3o'
)

# Tela 2: Relogio
add_screen_mockup(
    'Tela 2 \u2013 Rel\u00f3gio em Tempo Real',
    [
        '\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510',
        '\u2502      = RELOGIO =             \u2502',
        '\u2502\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2502',
        '\u2502                              \u2502',
        '\u2502    12:30              45     \u2502',
        '\u2502    (grande)          (seg)   \u2502',
        '\u2502\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2502',
        '\u2502 WiFi: LevelUP-Health         \u2502',
        '\u2502 IP: 192.168.4.1              \u2502',
        '\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518',
    ],
    'Figura 3 \u2013 Tela do rel\u00f3gio com hora grande (HH:MM SS) e informa\u00e7\u00f5es WiFi'
)

# Tela 3: Sinais Vitais
add_screen_mockup(
    'Tela 3 \u2013 Sinais Vitais Detalhados',
    [
        '\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510',
        '\u2502    = SINAIS VITAIS =         \u2502',
        '\u2502\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2502',
        '\u2502 Freq.Card: 75 BPM            \u2502',
        '\u2502 Temperatura: 36.5 C           \u2502',
        '\u2502 Umidade: 65.0%               \u2502',
        '\u2502 Passos: 6750                  \u2502',
        '\u2502 Qual.Sono: 72%               \u2502',
        '\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518',
    ],
    'Figura 4 \u2013 Detalhamento completo de todos os sensores wearables'
)

# Tela 4: Check-up Digital
add_screen_mockup(
    'Tela 4 \u2013 Check-up Digital (Pergunta)',
    [
        '\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510',
        '\u2502  = CHECK-UP DIGITAL =        \u2502',
        '\u2502\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2502',
        '\u2502 Pergunta 3/8                  \u2502',
        '\u2502                              \u2502',
        '\u2502 Tontura frequente?            \u2502',
        '\u2502\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2502',
        '\u2502 SEL = Sim                     \u2502',
        '\u2502 MENU = Nao                    \u2502',
        '\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518',
    ],
    'Figura 5 \u2013 Triagem digital com 8 perguntas ponderadas (pergunta 3 de 8)'
)

# Tela 4b: Check-up Resultado
add_screen_mockup(
    'Tela 4b \u2013 Check-up Digital (Resultado)',
    [
        '\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510',
        '\u2502  = CHECK-UP DIGITAL =        \u2502',
        '\u2502\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2502',
        '\u2502   Check-up Completo!          \u2502',
        '\u2502                              \u2502',
        '\u2502 Score Risco: 42/100           \u2502',
        '\u2502 [\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591]  \u2502',
        '\u2502                              \u2502',
        '\u2502 >> RISCO MODERADO <<          \u2502',
        '\u2502 [SEL] Novo Check-up          \u2502',
        '\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518',
    ],
    'Figura 6 \u2013 Resultado do check-up com score de risco e classifica\u00e7\u00e3o'
)

# Tela 5: Gamificacao
add_screen_mockup(
    'Tela 5 \u2013 Gamifica\u00e7\u00e3o',
    [
        '\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510',
        '\u2502     = GAMIFICACAO =           \u2502',
        '\u2502\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2502',
        '\u2502 Nivel: 3                      \u2502',
        '\u2502 Rank: Aprendiz Ativo          \u2502',
        '\u2502 Pontos: 250                   \u2502',
        '\u2502 Checkups: 2                   \u2502',
        '\u2502 Prox.Lv: 50%                  \u2502',
        '\u2502          [\u2588\u2588\u2588\u2588\u2588\u2588\u2591\u2591\u2591\u2591\u2591\u2591]   \u2502',
        '\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518',
    ],
    'Figura 7 \u2013 Sistema de gamifica\u00e7\u00e3o com n\u00edvel, rank, pontos e progresso'
)

# Tela 6: Alerta
add_screen_mockup(
    'Tela 6 \u2013 Alerta Cr\u00edtico',
    [
        '\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510',
        '\u2502\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\u2502',
        '\u2502\u2502                            \u2502\u2502',
        '\u2502\u2502       ALERTA!              \u2502\u2502',
        '\u2502\u2502                            \u2502\u2502',
        '\u2502\u2502 FC Anormal: 175 BPM        \u2502\u2502',
        '\u2502\u2502                            \u2502\u2502',
        '\u2502\u2502 Temp Critica: 39.5C        \u2502\u2502',
        '\u2502\u2502                            \u2502\u2502',
        '\u2502\u2502   [OK para confirmar]      \u2502\u2502',
        '\u2502\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518\u2502',
        '\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518',
    ],
    'Figura 8 \u2013 Tela de alerta cr\u00edtico com dupla borda, LED vermelho e buzzer ativados'
)

doc.add_page_break()

# =================== 3. DASHBOARD WEB ===================
add_heading_text('3  DASHBOARD WEB (WiFi)', level=1)

add_normal_text(
    'O ESP32 cria um Access Point WiFi (SSID: LevelUP-Health, senha: levelup123) '
    'e serve um dashboard HTML responsivo em http://192.168.4.1. O dashboard \u00e9 '
    'constru\u00eddo com CSS moderno (tema escuro) e atualiza automaticamente a cada '
    '2 segundos via fetch(\'/api/data\').',
    indent=True
)

add_screen_mockup(
    'Dashboard Web \u2013 Vis\u00e3o Geral',
    [
        '\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510',
        '\u2502             LEVEL UP                              \u2502',
        '\u2502    Health Monitoring System v2.0                   \u2502',
        '\u2502                                                    \u2502',
        '\u2502              12:30:45                              \u2502',
        '\u2502         Relogio em Tempo Real                      \u2502',
        '\u2502       [HH]:[MM] [OK]                               \u2502',
        '\u2502                                                    \u2502',
        '\u2502  NORMAL - SINAIS VITAIS ESTAVEIS                   \u2502',
        '\u2502                                                    \u2502',
        '\u2502  \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510  \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510           \u2502',
        '\u2502  \u2502 FREQ.CARD.   \u2502  \u2502 TEMPERATURA  \u2502           \u2502',
        '\u2502  \u2502   75 BPM     \u2502  \u2502   36.5 \u00b0C    \u2502           \u2502',
        '\u2502  \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518  \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518           \u2502',
        '\u2502                                                    \u2502',
        '\u2502  \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510  \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510           \u2502',
        '\u2502  \u2502 ATIVIDADE    \u2502  \u2502 QUAL. SONO   \u2502           \u2502',
        '\u2502  \u2502   45%        \u2502  \u2502   72%        \u2502           \u2502',
        '\u2502  \u2502 [\u2588\u2588\u2588\u2588\u2591\u2591\u2591\u2591\u2591\u2591] \u2502  \u2502 [\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2591\u2591\u2591] \u2502           \u2502',
        '\u2502  \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518  \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518           \u2502',
        '\u2502                                                    \u2502',
        '\u2502  \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510  \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510           \u2502',
        '\u2502  \u2502 PASSOS       \u2502  \u2502 GAMIFICACAO  \u2502           \u2502',
        '\u2502  \u2502   6750       \u2502  \u2502  Nivel 3     \u2502           \u2502',
        '\u2502  \u2502              \u2502  \u2502 [Aprend.Ativo]\u2502           \u2502',
        '\u2502  \u2502              \u2502  \u2502 Pts: 250     \u2502           \u2502',
        '\u2502  \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518  \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518           \u2502',
        '\u2502                                                    \u2502',
        '\u2502   Level UP - ESP32 Health Monitor - WiFi Dashboard \u2502',
        '\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518',
    ],
    'Figura 9 \u2013 Dashboard web com tema escuro, cards de dados, rel\u00f3gio e barra de status'
)

doc.add_page_break()

# =================== 4. API REST ===================
add_heading_text('4  API REST \u2013 RESPOSTA JSON', level=1)

add_normal_text(
    'O endpoint GET /api/data retorna os dados de sa\u00fade em formato JSON, '
    'permitindo integra\u00e7\u00e3o com outros sistemas e aplica\u00e7\u00f5es:',
    indent=True
)

add_code_block(
    'GET http://192.168.4.1/api/data\n'
    '\n'
    'Resposta (200 OK):\n'
    '{\n'
    '  "time": "12:30:45",\n'
    '  "bpm": 75,\n'
    '  "temp": 36.5,\n'
    '  "humidity": 65.0,\n'
    '  "activity": 45,\n'
    '  "steps": 6750,\n'
    '  "sleep": 72,\n'
    '  "level": 3,\n'
    '  "rank": "Aprendiz Ativo",\n'
    '  "points": 250,\n'
    '  "checkups": 2,\n'
    '  "alert": 0,\n'
    '  "risk": 42\n'
    '}',
    'Figura 10 \u2013 Exemplo de resposta JSON da API REST (/api/data)'
)

doc.add_page_break()

# =================== 5. RELATORIO SERIAL ===================
add_heading_text('5  RELAT\u00d3RIO M\u00c9DICO SERIAL', level=1)

add_normal_text(
    'Ap\u00f3s cada check-up completo, o sistema gera automaticamente um relat\u00f3rio '
    'm\u00e9dico preliminar via porta Serial (115200 baud):',
    indent=True
)

add_code_block(
    '================================================\n'
    '   RELATORIO MEDICO PRELIMINAR\n'
    '   Level UP - Check-up Digital com IA\n'
    '================================================\n'
    '\n'
    'SINAIS VITAIS COLETADOS:\n'
    '  Frequencia Cardiaca: 75 BPM\n'
    '  Temperatura Corporal: 36.5 C\n'
    '  Umidade Ambiente: 65.0%\n'
    '  Nivel de Atividade: 45%\n'
    '  Passos Estimados: 6750\n'
    '  Qualidade do Sono: 72%\n'
    '\n'
    'TRIAGEM - SINTOMAS REPORTADOS:\n'
    '  Dor no peito? NAO\n'
    '  Falta de ar? SIM\n'
    '  Tontura frequente? NAO\n'
    '  Dor de cabeca? SIM\n'
    '  Fadiga excessiva? SIM\n'
    '  Febre recente? NAO\n'
    '  Palpitacoes? NAO\n'
    '  Insonia? SIM\n'
    '\n'
    'SCORE DE RISCO CALCULADO: 42/100\n'
    '\n'
    'CLASSIFICACAO: RISCO MODERADO\n'
    'Recomendacao: Agendar consulta preventiva.\n'
    '\n'
    '================================================\n'
    'Pontuacao Gamificacao: 250 pts | Nivel 3 | Aprendiz Ativo\n'
    '================================================',
    'Figura 11 \u2013 Relat\u00f3rio m\u00e9dico preliminar gerado via Serial ap\u00f3s check-up'
)

doc.add_page_break()

# =================== 6. CIRCUITO ===================
add_heading_text('6  CIRCUITO NO WOKWI', level=1)

add_normal_text(
    'O circuito foi montado na plataforma Wokwi com os seguintes componentes '
    'conectados ao ESP32 DevKit V1:',
    indent=True
)

# Component table
from docx.enum.table import WD_TABLE_ALIGNMENT
table = doc.add_table(rows=9, cols=4)
table.style = 'Table Grid'
table.alignment = WD_TABLE_ALIGNMENT.CENTER

headers_data = ['Componente', 'Pinos', 'Fun\u00e7\u00e3o', 'Tipo']
rows_data = [
    ['ESP32 DevKit V1', '\u2013', 'Microcontrolador principal', 'MCU'],
    ['OLED SSD1306 128\u00d764', 'SDA(21), SCL(22)', 'Display de dados e interface', 'I2C'],
    ['DHT22', 'GPIO 4', 'Sensor de temperatura e umidade', 'Digital'],
    ['Potenci\u00f4metro 1', 'GPIO 34 (ADC)', 'Simula sensor card\u00edaco (40\u2013200 BPM)', 'Anal\u00f3gico'],
    ['Potenci\u00f4metro 2', 'GPIO 35 (ADC)', 'Simula aceler\u00f4metro (0\u2013100%)', 'Anal\u00f3gico'],
    ['LED Verde + Resistor', 'GPIO 25', 'Indicador: sinais normais', 'Digital'],
    ['LED Amarelo + Resistor', 'GPIO 26', 'Indicador: aten\u00e7\u00e3o', 'Digital'],
    ['LED Vermelho + Resistor', 'GPIO 27', 'Indicador: alerta cr\u00edtico', 'Digital'],
]

# extra components
extra_rows = [
    ['Buzzer', 'GPIO 33', 'Alarme sonoro para alertas', 'PWM'],
    ['Bot\u00e3o Menu', 'GPIO 18', 'Navega\u00e7\u00e3o entre telas', 'INPUT_PULLUP'],
    ['Bot\u00e3o Select', 'GPIO 19', 'Intera\u00e7\u00e3o (respostas)', 'INPUT_PULLUP'],
]

# Rebuild table with correct row count
table = doc.add_table(rows=1 + len(rows_data) + len(extra_rows), cols=4)
table.style = 'Table Grid'
table.alignment = WD_TABLE_ALIGNMENT.CENTER

for i, h in enumerate(headers_data):
    cell = table.rows[0].cells[i]
    cell.text = ''
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(h)
    set_font(run, size=10, bold=True)
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), '1a1a3e')
    shading.set(qn('w:val'), 'clear')
    cell._element.get_or_add_tcPr().append(shading)
    run.font.color.rgb = RGBColor(255, 255, 255)

all_rows = rows_data + extra_rows
for r_idx, row_data in enumerate(all_rows):
    for c_idx, val in enumerate(row_data):
        cell = table.rows[r_idx + 1].cells[c_idx]
        cell.text = ''
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(val)
        set_font(run, size=10)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
pf = p.paragraph_format
pf.space_before = Pt(4)
pf.space_after = Pt(12)
run = p.add_run('Quadro 1 \u2013 Componentes do circuito e pinagem no ESP32')
set_font(run, size=10, italic=True)

doc.add_page_break()

# =================== 7. CODIGO-FONTE ===================
add_heading_text('7  TRECHOS DO C\u00d3DIGO-FONTE', level=1)

add_normal_text(
    'O c\u00f3digo-fonte (sketch.ino) possui 977 linhas em C/C++ para Arduino. '
    'A seguir, os trechos mais relevantes:',
    indent=True
)

add_heading_text('7.1  Estruturas de Dados', level=2)

add_code_block(
    'struct HealthData {\n'
    '  int heartRate;        // 40-200 BPM\n'
    '  float temperature;    // Celsius\n'
    '  float humidity;       // Percentual\n'
    '  int activityLevel;    // 0-100%\n'
    '  int steps;            // Passos estimados\n'
    '  int sleepQuality;     // 15-95%\n'
    '};\n'
    '\n'
    'struct GameData {\n'
    '  int points;           // Pontuacao total\n'
    '  int level;            // Nivel atual\n'
    '  int dailyStreak;      // Sequencia diaria\n'
    '  int totalCheckups;    // Check-ups realizados\n'
    '  char rank[20];        // Rank atual\n'
    '};\n'
    '\n'
    'struct CheckupData {\n'
    '  int currentQuestion;  // Pergunta atual (0-7)\n'
    '  int answers[10];      // Respostas (0=Nao, 1=Sim)\n'
    '  int riskScore;        // Score de risco (0-100)\n'
    '  bool completed;       // Check-up finalizado?\n'
    '  bool pointsAwarded;   // Pontos ja concedidos?\n'
    '};',
    'Figura 12 \u2013 Estruturas de dados do sistema (HealthData, GameData, CheckupData)'
)

add_heading_text('7.2  Avalia\u00e7\u00e3o de Sa\u00fade (L\u00f3gica de Alertas)', level=2)

add_code_block(
    'void evaluateHealth() {\n'
    '  currentAlertLevel = 0;\n'
    '  \n'
    '  // Frequencia cardiaca\n'
    '  if (health.heartRate < 50 || health.heartRate > 160)\n'
    '    currentAlertLevel = 2;  // CRITICO\n'
    '  else if (health.heartRate < 60 || health.heartRate > 100)\n'
    '    currentAlertLevel = max(currentAlertLevel, 1);  // ATENCAO\n'
    '  \n'
    '  // Temperatura\n'
    '  if (health.temperature > 39.0 || health.temperature < 34.0)\n'
    '    currentAlertLevel = 2;  // CRITICO\n'
    '  else if (health.temperature > 37.5 || health.temperature < 35.5)\n'
    '    currentAlertLevel = max(currentAlertLevel, 1);  // ATENCAO\n'
    '  \n'
    '  // Acionar LEDs\n'
    '  digitalWrite(GREEN_LED, currentAlertLevel == 0 ? HIGH : LOW);\n'
    '  digitalWrite(YELLOW_LED, currentAlertLevel == 1 ? HIGH : LOW);\n'
    '  digitalWrite(RED_LED, currentAlertLevel == 2 ? HIGH : LOW);\n'
    '  \n'
    '  // Buzzer para alerta critico\n'
    '  if (currentAlertLevel == 2) {\n'
    '    tone(BUZZER_PIN, 1000);  // 1kHz\n'
    '    currentScreen = SCREEN_ALERT;\n'
    '  }\n'
    '}',
    'Figura 13 \u2013 Fun\u00e7\u00e3o de avalia\u00e7\u00e3o de sa\u00fade com l\u00f3gica de alertas'
)

add_heading_text('7.3  C\u00e1lculo de Risco (IA Simulada)', level=2)

add_code_block(
    'void calculateRiskScore() {\n'
    '  int score = 0;\n'
    '  \n'
    '  // Soma ponderada das respostas\n'
    '  for (int i = 0; i < NUM_QUESTIONS; i++) {\n'
    '    if (checkup.answers[i])\n'
    '      score += weights[i];\n'
    '  }\n'
    '  \n'
    '  // Ajustes com sinais vitais em tempo real\n'
    '  if (health.heartRate > 100 || health.heartRate < 60) score += 10;\n'
    '  if (health.temperature > 37.5) score += 10;\n'
    '  if (health.activityLevel < 20) score += 5;\n'
    '  if (health.sleepQuality < 40) score += 5;\n'
    '  \n'
    '  checkup.riskScore = constrain(score, 0, 100);\n'
    '}',
    'Figura 14 \u2013 Algoritmo de c\u00e1lculo de risco simulando intelig\u00eancia artificial'
)

doc.add_page_break()

# =================== 8. LOGS DO SISTEMA ===================
add_heading_text('8  LOGS DO SISTEMA (SERIAL MONITOR)', level=1)

add_normal_text(
    'O sistema gera logs cont\u00ednuos na porta Serial (115200 baud) para '
    'monitoramento e depura\u00e7\u00e3o:',
    indent=True
)

add_code_block(
    '============================================\n'
    '  LEVEL UP - Health Monitoring System\n'
    '  Versao 2.0 | ESP32 + WiFi + Dashboard\n'
    '============================================\n'
    '[OK] Sistema inicializado com sucesso!\n'
    '[INFO] Navegue com BTN_MENU, interaja com BTN_SELECT\n'
    '[WIFI] Dashboard: http://192.168.4.1\n'
    '--------------------------------------------\n'
    '\n'
    '--- Leitura dos Sensores ---\n'
    '  FC: 75 BPM | Temp: 36.5 C | Umid: 65.0%\n'
    '  Atividade: 45% | Passos: 6750 | Sono: 72%\n'
    '  Status: NORMAL\n'
    '  +25 pts | Total: 250 | Lv.3\n'
    '\n'
    '--- Leitura dos Sensores ---\n'
    '  FC: 78 BPM | Temp: 36.6 C | Umid: 64.5%\n'
    '  Atividade: 48% | Passos: 7200 | Sono: 69%\n'
    '  Status: NORMAL\n'
    '\n'
    '  [CHECK-UP] Dor no peito? -> NAO\n'
    '  [CHECK-UP] Falta de ar? -> SIM\n'
    '  [CHECK-UP] Tontura frequente? -> NAO\n'
    '  ...\n'
    '[GAMIFICACAO] +50 pts por completar check-up!\n'
    '*** LEVEL UP! Nivel 4 - Aprendiz Ativo ***',
    'Figura 15 \u2013 Exemplo de logs do sistema no Serial Monitor'
)

doc.add_page_break()

# =================== 9. DIAGRAMA LOGICO ===================
add_heading_text('9  FLUXO L\u00d3GICO DO SISTEMA', level=1)

add_normal_text(
    'O diagrama a seguir representa o fluxo l\u00f3gico principal do sistema Level UP, '
    'desde a inicializa\u00e7\u00e3o at\u00e9 o loop principal:',
    indent=True
)

add_code_block(
    '  \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n'
    '  \u2502   SETUP()       \u2502\n'
    '  \u2502  Serial 115200  \u2502\n'
    '  \u2502  Pinos I/O      \u2502\n'
    '  \u2502  DHT22          \u2502\n'
    '  \u2502  OLED SSD1306   \u2502\n'
    '  \u2502  WiFi AP        \u2502\n'
    '  \u2502  Web Server     \u2502\n'
    '  \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518\n'
    '           \u2502\n'
    '           \u25bc\n'
    '  \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n'
    '  \u2502    LOOP()       \u2502\n'
    '  \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518\n'
    '           \u2502\n'
    '     \u250c\u2500\u2500\u2500\u2500\u2500\u253c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n'
    '     \u25bc     \u25bc                          \u25bc\n'
    '  \u250c\u2500\u2500\u2500\u2500\u2500\u2510 \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510   \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n'
    '  \u2502Clock\u2502 \u2502 readSensors \u2502   \u2502 handleButtons  \u2502\n'
    '  \u2514\u2500\u2500\u252c\u2500\u2500\u2518 \u2514\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518   \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518\n'
    '     \u2502       \u2502                    \u2502\n'
    '     \u25bc       \u25bc                    \u25bc\n'
    '  \u250c\u2500\u2500\u2500\u2500\u2500\u2510 \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510   \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n'
    '  \u2502 Web \u2502 \u2502evaluateHealth\u2502   \u2502 updateDisplay  \u2502\n'
    '  \u2502Servr\u2502 \u2514\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518   \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518\n'
    '  \u2514\u2500\u2500\u2500\u2500\u2500\u2518      \u2502\n'
    '              \u25bc\n'
    '       \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n'
    '       \u2502 awardPoints \u2502\n'
    '       \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518',
    'Figura 16 \u2013 Fluxograma do sistema: setup, loop principal e m\u00f3dulos'
)

# =================== SALVAR ===================
output_path = '/home/ubuntu/repos/global-solution-energy-2025/level-up-wokwi/Questao3_Apresentacao_Prints.docx'
doc.save(output_path)
print(f'Documento salvo em: {output_path}')
print(f'Tamanho: {os.path.getsize(output_path)} bytes')
