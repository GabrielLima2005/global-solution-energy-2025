#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from docx import Document
from docx.shared import Pt, Cm, RGBColor
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

style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)
style.paragraph_format.line_spacing = 1.5
style.paragraph_format.space_after = Pt(0)
style.paragraph_format.space_before = Pt(0)

for i in range(1, 4):
    hs = doc.styles[f'Heading {i}']
    hs.font.name = 'Times New Roman'
    hs.font.bold = True
    hs.font.color.rgb = RGBColor(0, 0, 0)
    hs.paragraph_format.line_spacing = 1.5
    hs.paragraph_format.space_before = Pt(12)
    hs.paragraph_format.space_after = Pt(6)
    hs.font.size = Pt([14, 13, 12][i-1])

def add_centered_text(text, size=12, bold=False, space_before=0, space_after=0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.bold = bold
    return p

def add_normal_text(text, bold=False, indent_first=True, space_after=6):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(space_after)
    if indent_first:
        p.paragraph_format.first_line_indent = Cm(1.25)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.bold = bold
    return p

def add_equation(text, space_after=6):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(6)
    run = p.add_run(text)
    run.font.name = 'Courier New'
    run.font.size = Pt(11)
    run.bold = True
    return p

def add_table(headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(header)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        run.bold = True
        shading = OxmlElement('w:shd')
        shading.set(qn('w:fill'), 'D9E2F3')
        shading.set(qn('w:val'), 'clear')
        cell._tc.get_or_add_tcPr().append(shading)
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = ''
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(str(val))
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10)
    if col_widths:
        for i, w in enumerate(col_widths):
            for row in table.rows:
                row.cells[i].width = Cm(w)
    doc.add_paragraph()
    return table

def add_caption(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10)
    run.italic = True

# === CAPA ===
for _ in range(4):
    doc.add_paragraph()
add_centered_text('FIAP - FACULDADE DE INFORM\u00c1TICA E ADMINISTRA\u00c7\u00c3O PAULISTA', 14, bold=True, space_after=24)
add_centered_text('CURSO DE ENGENHARIA DE SOFTWARE / SISTEMAS', 12, space_after=48)
for _ in range(2):
    doc.add_paragraph()
add_centered_text('RELAT\u00d3RIO DE L\u00d3GICA DIGITAL', 16, bold=True, space_after=6)
add_centered_text('SPRINT 03', 14, bold=True, space_after=24)
add_centered_text('Projeto Level UP - Sistema Inteligente de', 14, space_after=0)
add_centered_text('Monitoramento de Sa\u00fade', 14, space_after=48)
for _ in range(3):
    doc.add_paragraph()
add_centered_text('Nicolas Ara\u00fajo de Oliveira - RM 566780', 12, space_after=6)
add_centered_text('Pedro Ivson Falc\u00e3o De Leucas', 12, space_after=6)
add_centered_text('Gabriel Lima Da Silva - RM 568436', 12, space_after=48)
for _ in range(2):
    doc.add_paragraph()
add_centered_text('S\u00e3o Paulo', 12, space_after=6)
add_centered_text('2025', 12)
doc.add_page_break()

# === SUM\u00c1RIO ===
add_centered_text('SUM\u00c1RIO', 14, bold=True, space_after=24)
sumario_items = [
    ('1', 'INTRODU\u00c7\u00c3O', '3'),
    ('2', 'SISTEMA DE ALERTAS DE SA\u00daDE (LEDS + BUZZER)', '4'),
    ('2.1', 'Descri\u00e7\u00e3o do Funcionamento', '4'),
    ('2.2', 'Vari\u00e1veis Booleanas de Entrada', '4'),
    ('2.3', 'Sa\u00eddas do Sistema', '5'),
    ('2.4', 'Express\u00f5es L\u00f3gicas Originais', '5'),
    ('2.5', 'Tabela Verdade Original', '6'),
    ('2.6', 'Simplifica\u00e7\u00e3o por \u00c1lgebra Booleana', '7'),
    ('2.7', 'Mapas de Karnaugh', '8'),
    ('2.8', 'Express\u00f5es Simplificadas', '9'),
    ('2.9', 'Diagramas L\u00f3gicos', '9'),
    ('2.10', 'Tabela Verdade Comparativa', '10'),
    ('3', 'SISTEMA DE GAMIFICA\u00c7\u00c3O (PONTOS)', '11'),
    ('3.1', 'Descri\u00e7\u00e3o e Vari\u00e1veis', '11'),
    ('3.2', 'Simplifica\u00e7\u00e3o', '12'),
    ('3.3', 'Prova de Equival\u00eancia', '12'),
    ('4', 'SISTEMA DE CLASSIFICA\u00c7\u00c3O DE RISCO', '13'),
    ('4.1', 'Descri\u00e7\u00e3o e Vari\u00e1veis', '13'),
    ('4.2', 'Simplifica\u00e7\u00e3o', '14'),
    ('4.3', 'Prova de Equival\u00eancia', '14'),
    ('5', 'RESUMO DAS SIMPLIFICA\u00c7\u00d5ES', '15'),
    ('6', 'CONCLUS\u00c3O', '16'),
    ('', 'REFER\u00caNCIAS', '17'),
]
for num, title, page in sumario_items:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.5
    if num and '.' not in num:
        run = p.add_run(f'{num}  {title}')
        run.bold = True
    elif num:
        run = p.add_run(f'  {num}  {title}')
    else:
        run = p.add_run(f'{title}')
        run.bold = True
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run2 = p.add_run(f'  {"." * 40}  {page}')
    run2.font.name = 'Times New Roman'
    run2.font.size = Pt(12)
doc.add_page_break()

# === 1. INTRODU\u00c7\u00c3O ===
doc.add_heading('1  INTRODU\u00c7\u00c3O', level=1)
add_normal_text(
    'Este relat\u00f3rio apresenta a modelagem e simplifica\u00e7\u00e3o da l\u00f3gica digital do sistema '
    'Level UP, um monitor inteligente de sa\u00fade baseado em ESP32 simulado na plataforma Wokwi. '
    'O trabalho atende aos requisitos da Sprint 03, aplicando conceitos de l\u00f3gica digital '
    'ao projeto em desenvolvimento.'
)
add_normal_text(
    'O sistema Level UP possui tr\u00eas subsistemas principais com l\u00f3gica digital bem definida, '
    'que ser\u00e3o analisados neste relat\u00f3rio:'
)
items_intro = [
    'Sistema de Alertas de Sa\u00fade \u2014 controla LEDs (verde, amarelo e vermelho) e buzzer com base em faixas de frequ\u00eancia card\u00edaca e temperatura corporal;',
    'Sistema de Gamifica\u00e7\u00e3o \u2014 determina se o paciente ganha pontos com base em indicadores de sa\u00fade saud\u00e1veis;',
    'Sistema de Classifica\u00e7\u00e3o de Risco \u2014 classifica o resultado do check-up digital em tr\u00eas n\u00edveis de risco (baixo, moderado e alto).'
]
for item in items_intro:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Cm(2)
    run = p.add_run('\u2022 ' + item)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
add_normal_text(
    'Para cada subsistema, iremos: (a) modelar as express\u00f5es booleanas originais extra\u00eddas '
    'diretamente do c\u00f3digo-fonte; (b) aplicar t\u00e9cnicas de simplifica\u00e7\u00e3o utilizando \u00e1lgebra '
    'booleana e mapas de Karnaugh; e (c) provar a equival\u00eancia entre os modelos original e '
    'simplificado por meio de tabelas verdade comparativas.'
)
add_normal_text(
    'O c\u00f3digo-fonte analisado encontra-se no arquivo sketch.ino do projeto, desenvolvido '
    'em linguagem C/C++ para a plataforma Arduino (ESP32). As express\u00f5es booleanas foram '
    'extra\u00eddas das fun\u00e7\u00f5es evaluateHealth(), awardPoints() e calculateRiskScore().'
)
doc.add_page_break()

# === 2. SISTEMA DE ALERTAS ===
doc.add_heading('2  SISTEMA DE ALERTAS DE SA\u00daDE (LEDS + BUZZER)', level=1)
doc.add_heading('2.1  Descri\u00e7\u00e3o do Funcionamento', level=2)
add_normal_text(
    'O sistema de alertas avalia continuamente dois sinais vitais do paciente e aciona '
    'indicadores visuais (LEDs) e sonoros (buzzer) de acordo com a gravidade detectada. '
    'O objetivo \u00e9 fornecer feedback imediato sobre o estado de sa\u00fade, classificando-o em '
    'tr\u00eas n\u00edveis: Normal, Aten\u00e7\u00e3o e Cr\u00edtico.'
)
add_normal_text(
    'A frequ\u00eancia card\u00edaca (FC) \u00e9 classificada em tr\u00eas faixas: Cr\u00edtico quando FC < 50 ou '
    'FC > 160 BPM; Aten\u00e7\u00e3o quando FC < 60 ou FC > 100 BPM (fora da faixa normal, mas n\u00e3o '
    'cr\u00edtico); e Normal quando 60 \u2264 FC \u2264 100 BPM.'
)
add_normal_text(
    'A temperatura corporal (T) segue classifica\u00e7\u00e3o an\u00e1loga: Cr\u00edtico quando T < 34,0 ou '
    'T > 39,0 graus Celsius; Aten\u00e7\u00e3o quando T < 35,5 ou T > 37,5 graus (fora do normal, '
    'mas n\u00e3o cr\u00edtico); e Normal quando 35,5 \u2264 T \u2264 37,5 graus Celsius.'
)

doc.add_heading('2.2  Vari\u00e1veis Booleanas de Entrada', level=2)
add_normal_text(
    'Para modelar a l\u00f3gica do sistema de alertas, definimos quatro vari\u00e1veis bin\u00e1rias que '
    'representam a classifica\u00e7\u00e3o dos sensores:', space_after=12
)
add_caption('Quadro 1 \u2014 Vari\u00e1veis de entrada do Sistema de Alertas')
add_table(
    ['Vari\u00e1vel', 'Significado', 'Condi\u00e7\u00e3o'],
    [
        ['A', 'FC em faixa cr\u00edtica', 'FC < 50 OR FC > 160'],
        ['B', 'FC em faixa de aten\u00e7\u00e3o', '(50 \u2264 FC < 60) OR (100 < FC \u2264 160)'],
        ['C', 'Temp. em faixa cr\u00edtica', 'T < 34,0 OR T > 39,0'],
        ['D', 'Temp. em faixa de aten\u00e7\u00e3o', '(34,0 \u2264 T < 35,5) OR (37,5 < T \u2264 39,0)'],
    ],
    col_widths=[2, 4, 6]
)
add_caption('Fonte: Elaborado pelos autores (2025)')
add_normal_text(
    'Restri\u00e7\u00f5es importantes: As vari\u00e1veis A e B s\u00e3o mutuamente exclusivas (A \u00b7 B = 0), '
    'pois a frequ\u00eancia card\u00edaca n\u00e3o pode estar simultaneamente em faixa cr\u00edtica e de aten\u00e7\u00e3o. '
    'Da mesma forma, C e D s\u00e3o mutuamente exclusivas (C \u00b7 D = 0). Essas restri\u00e7\u00f5es geram '
    'condi\u00e7\u00f5es "don\'t care" na tabela verdade e nos mapas de Karnaugh.'
)

doc.add_heading('2.3  Sa\u00eddas do Sistema', level=2)
add_caption('Quadro 2 \u2014 Sa\u00eddas do Sistema de Alertas')
add_table(
    ['Sa\u00edda', 'Significado', 'Componente F\u00edsico'],
    [
        ['R', 'LED Vermelho (alerta cr\u00edtico)', 'RED_LED (GPIO 4)'],
        ['Y', 'LED Amarelo (aten\u00e7\u00e3o)', 'YELLOW_LED (GPIO 16)'],
        ['G', 'LED Verde (normal)', 'GREEN_LED (GPIO 17)'],
        ['Z', 'Buzzer (alarme sonoro)', 'BUZZER_PIN (GPIO 18)'],
    ],
    col_widths=[2, 5, 5]
)
add_caption('Fonte: Elaborado pelos autores (2025)')

doc.add_heading('2.4  Express\u00f5es L\u00f3gicas Originais', level=2)
add_normal_text(
    'As express\u00f5es booleanas foram extra\u00eddas diretamente da fun\u00e7\u00e3o evaluateHealth() no '
    'arquivo sketch.ino. Utilizamos a nota\u00e7\u00e3o onde "+" representa a opera\u00e7\u00e3o OR, "\u00b7" '
    'representa AND, e o ap\u00f3strofo ("\'" ) representa NOT (complemento):'
)
add_equation('R = A + C')
add_equation("Y = A' \u00b7 C' \u00b7 (B + D)")
add_equation("G = A' \u00b7 B' \u00b7 C' \u00b7 D'")
add_equation('Z = A + C')
add_normal_text(
    'O objetivo desta l\u00f3gica \u00e9: o LED vermelho (R) e o buzzer (Z) ativam quando QUALQUER '
    'sinal vital est\u00e1 em n\u00edvel cr\u00edtico. O LED amarelo (Y) ativa quando NENHUM sinal est\u00e1 '
    'cr\u00edtico mas ALGUM est\u00e1 em faixa de aten\u00e7\u00e3o. O LED verde (G) ativa somente quando TODOS '
    'os sinais vitais est\u00e3o na faixa normal.'
)
doc.add_page_break()

doc.add_heading('2.5  Tabela Verdade Original', level=2)
add_normal_text(
    'A tabela verdade a seguir apresenta todas as 16 combina\u00e7\u00f5es poss\u00edveis das 4 vari\u00e1veis '
    'de entrada. As combina\u00e7\u00f5es onde A\u00b7B=1 ou C\u00b7D=1 s\u00e3o marcadas como "X" (don\'t care), '
    'pois representam cen\u00e1rios fisicamente imposs\u00edveis:', indent_first=False, space_after=12
)
add_caption('Quadro 3 \u2014 Tabela Verdade Original do Sistema de Alertas')
add_table(
    ['#', 'A', 'B', 'C', 'D', 'R', 'Y', 'G', 'Z', 'Observa\u00e7\u00e3o'],
    [
        ['0',  '0', '0', '0', '0', '0', '0', '1', '0', 'FC normal, Temp normal'],
        ['1',  '0', '0', '0', '1', '0', '1', '0', '0', 'FC normal, Temp aten\u00e7\u00e3o'],
        ['2',  '0', '0', '1', '0', '1', '0', '0', '1', 'FC normal, Temp cr\u00edtica'],
        ['3',  '0', '0', '1', '1', 'X', 'X', 'X', 'X', 'Imposs\u00edvel (C\u00b7D=0)'],
        ['4',  '0', '1', '0', '0', '0', '1', '0', '0', 'FC aten\u00e7\u00e3o, Temp normal'],
        ['5',  '0', '1', '0', '1', '0', '1', '0', '0', 'FC aten\u00e7\u00e3o, Temp aten\u00e7\u00e3o'],
        ['6',  '0', '1', '1', '0', '1', '0', '0', '1', 'FC aten\u00e7\u00e3o, Temp cr\u00edtica'],
        ['7',  '0', '1', '1', '1', 'X', 'X', 'X', 'X', 'Imposs\u00edvel (C\u00b7D=0)'],
        ['8',  '1', '0', '0', '0', '1', '0', '0', '1', 'FC cr\u00edtica, Temp normal'],
        ['9',  '1', '0', '0', '1', '1', '0', '0', '1', 'FC cr\u00edtica, Temp aten\u00e7\u00e3o'],
        ['10', '1', '0', '1', '0', '1', '0', '0', '1', 'FC cr\u00edtica, Temp cr\u00edtica'],
        ['11', '1', '0', '1', '1', 'X', 'X', 'X', 'X', 'Imposs\u00edvel (C\u00b7D=0)'],
        ['12', '1', '1', '0', '0', 'X', 'X', 'X', 'X', 'Imposs\u00edvel (A\u00b7B=0)'],
        ['13', '1', '1', '0', '1', 'X', 'X', 'X', 'X', 'Imposs\u00edvel (A\u00b7B=0)'],
        ['14', '1', '1', '1', '0', 'X', 'X', 'X', 'X', 'Imposs\u00edvel (A\u00b7B=0)'],
        ['15', '1', '1', '1', '1', 'X', 'X', 'X', 'X', 'Imposs\u00edvel (A\u00b7B=0, C\u00b7D=0)'],
    ]
)
add_caption('Fonte: Elaborado pelos autores (2025)')
doc.add_page_break()

doc.add_heading('2.6  Simplifica\u00e7\u00e3o por \u00c1lgebra Booleana', level=2)
add_normal_text('Sa\u00edda R (LED Vermelho):', bold=True, indent_first=False)
add_equation('Original:  R = A + C')
add_normal_text(
    'A express\u00e3o j\u00e1 est\u00e1 na forma m\u00ednima. Uma soma (OR) de duas vari\u00e1veis n\u00e3o pode ser '
    'mais simplificada.'
)
add_normal_text('Sa\u00edda Z (Buzzer):', bold=True, indent_first=False)
add_equation('Original:  Z = A + C')
add_equation('Simplificado:  Z = R  (reuso do sinal)')
add_normal_text(
    'Observamos que Z \u00e9 id\u00eantico a R. Portanto, o buzzer pode compartilhar o mesmo sinal '
    'l\u00f3gico do LED vermelho, eliminando uma porta l\u00f3gica redundante.'
)
add_normal_text('Sa\u00edda Y (LED Amarelo):', bold=True, indent_first=False)
add_equation("Original:  Y = A' \u00b7 C' \u00b7 (B + D)")
add_normal_text(
    "Aplicando a Lei de De Morgan, sabemos que A' \u00b7 C' = (A + C)'. Como R = A + C, "
    "temos que A' \u00b7 C' = R'. Portanto:"
)
add_equation("Simplificado:  Y = R' \u00b7 (B + D)")
add_normal_text(
    'Esta substitui\u00e7\u00e3o elimina duas portas NOT e uma porta AND de 2 entradas, substituindo '
    'por uma \u00fanica porta NOT sobre o sinal R j\u00e1 calculado.'
)
add_normal_text('Prova da equival\u00eancia (Y):', bold=True, indent_first=False)
add_equation('R = A + C')
add_equation("R' = (A + C)' = A' \u00b7 C'   [Lei de De Morgan]")
add_equation("R' \u00b7 (B + D) = A' \u00b7 C' \u00b7 (B + D)   [Q.E.D.]")
add_normal_text('Sa\u00edda G (LED Verde):', bold=True, indent_first=False)
add_equation("Original:  G = A' \u00b7 B' \u00b7 C' \u00b7 D'")
add_normal_text(
    'Como R, Y e G s\u00e3o mutuamente exclusivos e exaustivos (exatamente um LED deve estar '
    'ligado a qualquer momento), podemos derivar G a partir das outras sa\u00eddas:'
)
add_equation("R + Y = (A + C) + (A' \u00b7 C' \u00b7 (B + D))")
add_normal_text(
    "Aplicando o Teorema da Absor\u00e7\u00e3o (X + X'\u00b7Y = X + Y):", indent_first=False
)
add_equation('R + Y = (A + C) + (B + D) = A + B + C + D')
add_normal_text('Portanto:', indent_first=False)
add_equation("Simplificado:  G = (R + Y)' = R' \u00b7 Y'")
add_normal_text('Prova:', indent_first=False)
add_equation("(R + Y)' = (A + B + C + D)' = A' \u00b7 B' \u00b7 C' \u00b7 D'   [Q.E.D.]")
doc.add_page_break()

doc.add_heading('2.7  Mapas de Karnaugh', level=2)
add_normal_text(
    'A seguir, apresentamos os mapas de Karnaugh para cada sa\u00edda. As c\u00e9lulas marcadas com '
    '"X" representam condi\u00e7\u00f5es don\'t care (combina\u00e7\u00f5es imposs\u00edveis pelas restri\u00e7\u00f5es '
    'A\u00b7B=0 e C\u00b7D=0), que podem ser aproveitadas para simplifica\u00e7\u00e3o.'
)
add_normal_text('Mapa de Karnaugh para R (LED Vermelho):', bold=True, indent_first=False, space_after=6)
add_caption('Quadro 4 \u2014 Mapa de Karnaugh: R (LED Vermelho)')
add_table(
    ['AB \\ CD', '00', '01', '11', '10'],
    [['00', '0', '0', 'X', '1'], ['01', '0', '0', 'X', '1'],
     ['11', 'X', 'X', 'X', 'X'], ['10', '1', '1', 'X', '1']],
    col_widths=[3, 2, 2, 2, 2]
)
add_caption('Fonte: Elaborado pelos autores (2025)')
add_normal_text(
    'Agrupamentos identificados: Grupo 1 cobre toda a linha A=1 (termo A); Grupo 2 cobre '
    'toda a coluna C=1 (termo C). Resultado: R(m\u00edn) = A + C.'
)
add_normal_text('Mapa de Karnaugh para Y (LED Amarelo):', bold=True, indent_first=False, space_after=6)
add_caption('Quadro 5 \u2014 Mapa de Karnaugh: Y (LED Amarelo)')
add_table(
    ['AB \\ CD', '00', '01', '11', '10'],
    [['00', '0', '1', 'X', '0'], ['01', '1', '1', 'X', '0'],
     ['11', 'X', 'X', 'X', 'X'], ['10', '0', '0', 'X', '0']],
    col_widths=[3, 2, 2, 2, 2]
)
add_caption('Fonte: Elaborado pelos autores (2025)')
add_normal_text(
    "Agrupamentos: Grupo 1 (A'D, aproveitando don't cares) e Grupo 2 (BC', aproveitando "
    "don't cares). Y(m\u00edn) = A'\u00b7D + B\u00b7C' = A'\u00b7C'\u00b7(B+D) = R'\u00b7(B+D)."
)
add_normal_text('Mapa de Karnaugh para G (LED Verde):', bold=True, indent_first=False, space_after=6)
add_caption('Quadro 6 \u2014 Mapa de Karnaugh: G (LED Verde)')
add_table(
    ['AB \\ CD', '00', '01', '11', '10'],
    [['00', '1', '0', 'X', '0'], ['01', '0', '0', 'X', '0'],
     ['11', 'X', 'X', 'X', 'X'], ['10', '0', '0', 'X', '0']],
    col_widths=[3, 2, 2, 2, 2]
)
add_caption('Fonte: Elaborado pelos autores (2025)')
add_normal_text(
    "\u00danica c\u00e9lula com valor 1: posi\u00e7\u00e3o (A=0, B=0, C=0, D=0). N\u00e3o h\u00e1 agrupamento poss\u00edvel. "
    "G(m\u00edn) = A'\u00b7B'\u00b7C'\u00b7D'."
)
doc.add_page_break()

doc.add_heading('2.8  Express\u00f5es Simplificadas', level=2)
add_caption('Quadro 7 \u2014 Compara\u00e7\u00e3o das Express\u00f5es: Sistema de Alertas')
add_table(
    ['Sa\u00edda', 'Express\u00e3o Original', 'Express\u00e3o Simplificada', 'M\u00e9todo'],
    [
        ['R', 'A + C', 'A + C', 'J\u00e1 m\u00ednima'],
        ['Z', 'A + C', 'R (reuso)', 'Elimina\u00e7\u00e3o redund\u00e2ncia'],
        ['Y', "A'\u00b7C'\u00b7(B+D)", "R'\u00b7(B+D)", 'De Morgan + subst.'],
        ['G', "A'\u00b7B'\u00b7C'\u00b7D'", "(R+Y)'", 'Deriva\u00e7\u00e3o por exclus\u00e3o'],
    ],
    col_widths=[2, 4, 4, 4]
)
add_caption('Fonte: Elaborado pelos autores (2025)')

doc.add_heading('2.9  Diagramas L\u00f3gicos', level=2)
add_normal_text('Circuito Original (8 portas l\u00f3gicas):', bold=True, indent_first=False)
add_normal_text(
    "O circuito original utiliza: 4 portas NOT (para A', B', C', D'), 2 portas AND "
    "(para A'\u00b7C' e para o produto final de Y, e para G com AND de 4 entradas), e 2 portas "
    "OR (para R=A+C e Z=A+C, e para B+D). Total: 8 portas com sinais redundantes.",
    indent_first=False
)
add_normal_text('Circuito Simplificado (5 portas l\u00f3gicas):', bold=True, indent_first=False)
add_normal_text(
    "O circuito simplificado utiliza: 1 porta OR (R = A+C), 1 porta NOT (R' a partir de R), "
    "1 porta OR (B+D), 1 porta AND (Y = R'\u00b7(B+D)), e 1 porta NOR (G = (R+Y)'). O sinal Z "
    "\u00e9 conectado diretamente a R (mesmo fio). Total: 5 portas, sem redund\u00e2ncia.",
    indent_first=False
)
add_normal_text(
    'Economia: Redu\u00e7\u00e3o de 8 para 5 portas l\u00f3gicas, representando uma redu\u00e7\u00e3o de 37,5% '
    'na complexidade do circuito.',
    bold=True
)
doc.add_page_break()

doc.add_heading('2.10  Tabela Verdade Comparativa \u2014 Original vs Simplificado', level=2)
add_normal_text(
    'A tabela a seguir compara as sa\u00eddas do modelo original e do modelo simplificado para '
    'todas as combina\u00e7\u00f5es v\u00e1lidas de entrada (excluindo as condi\u00e7\u00f5es imposs\u00edveis):', space_after=12
)
add_caption('Quadro 8 \u2014 Tabela Verdade Comparativa: Sistema de Alertas')
add_table(
    ['#', 'A', 'B', 'C', 'D', 'R(orig)', 'R(simp)', 'Y(orig)', 'Y(simp)', 'G(orig)', 'G(simp)', 'Z(orig)', 'Z(simp)'],
    [
        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0'],
        ['1', '0', '0', '0', '1', '0', '0', '1', '1', '0', '0', '0', '0'],
        ['2', '0', '0', '1', '0', '1', '1', '0', '0', '0', '0', '1', '1'],
        ['4', '0', '1', '0', '0', '0', '0', '1', '1', '0', '0', '0', '0'],
        ['5', '0', '1', '0', '1', '0', '0', '1', '1', '0', '0', '0', '0'],
        ['6', '0', '1', '1', '0', '1', '1', '0', '0', '0', '0', '1', '1'],
        ['8', '1', '0', '0', '0', '1', '1', '0', '0', '0', '0', '1', '1'],
        ['9', '1', '0', '0', '1', '1', '1', '0', '0', '0', '0', '1', '1'],
        ['10', '1', '0', '1', '0', '1', '1', '0', '0', '0', '0', '1', '1'],
    ]
)
add_caption('Fonte: Elaborado pelos autores (2025)')
add_normal_text(
    'Resultado: Todas as sa\u00eddas do modelo simplificado s\u00e3o id\u00eanticas \u00e0s do modelo original '
    'em todos os 9 cen\u00e1rios v\u00e1lidos. Os modelos s\u00e3o comprovadamente equivalentes.',
    bold=True
)
doc.add_page_break()

# === 3. GAMIFICA\u00c7\u00c3O ===
doc.add_heading('3  SISTEMA DE GAMIFICA\u00c7\u00c3O (PONTOS)', level=1)
doc.add_heading('3.1  Descri\u00e7\u00e3o e Vari\u00e1veis', level=2)
add_normal_text(
    'O sistema de gamifica\u00e7\u00e3o avalia periodicamente (a cada 30 segundos) se o paciente '
    'merece pontos de recompensa com base em cinco condi\u00e7\u00f5es de sa\u00fade saud\u00e1vel. Cada '
    'condi\u00e7\u00e3o contribui pontos de forma independente. A l\u00f3gica foi extra\u00edda da fun\u00e7\u00e3o '
    'awardPoints() no sketch.ino.'
)
add_caption('Quadro 9 \u2014 Vari\u00e1veis de Entrada do Sistema de Gamifica\u00e7\u00e3o')
add_table(
    ['Vari\u00e1vel', 'Significado', 'Condi\u00e7\u00e3o', 'Pontos'],
    [
        ['P1', 'FC est\u00e1 normal', '60 \u2264 FC \u2264 100', '+10'],
        ['P2', 'Atividade moderada', 'Atividade > 30%', '+5'],
        ['P3', 'Atividade intensa', 'Atividade > 60%', '+10'],
        ['P4', 'Temperatura normal', '36,0 \u2264 T \u2264 37,5', '+5'],
        ['P5', 'Boa qualidade de sono', 'Sono > 70%', '+5'],
    ],
    col_widths=[2, 4, 4, 2]
)
add_caption('Fonte: Elaborado pelos autores (2025)')
add_normal_text(
    'Restri\u00e7\u00e3o importante: P3 implica P2 (P3 \u2192 P2). Se a atividade \u00e9 superior a 60%, '
    'necessariamente \u00e9 superior a 30%. Portanto, a combina\u00e7\u00e3o P3=1 com P2=0 \u00e9 imposs\u00edvel '
    "(P3 \u00b7 P2' = 0)."
)
add_normal_text('Express\u00e3o original para "Ganha Pontos" (GP):', bold=True, indent_first=False)
add_equation('GP = P1 + P2 + P3 + P4 + P5')
add_normal_text(
    'O paciente ganha alguma pontua\u00e7\u00e3o se QUALQUER condi\u00e7\u00e3o saud\u00e1vel for verdadeira.'
)

doc.add_heading('3.2  Simplifica\u00e7\u00e3o', level=2)
add_normal_text(
    'Aplicando o Teorema da Absor\u00e7\u00e3o: como P3 \u2192 P2, toda vez que P3=1 temos P2=1. '
    'Portanto, o termo P3 \u00e9 absorvido por P2 na opera\u00e7\u00e3o OR (X + X\u00b7Y = X). '
    'Formalmente: P2 + P3 = P2 (pois P3 est\u00e1 contido em P2).'
)
add_equation('GP(original)     = P1 + P2 + P3 + P4 + P5')
add_equation('GP(simplificado) = P1 + P2 + P4 + P5')
add_normal_text(
    'Simplifica\u00e7\u00e3o: Eliminamos a vari\u00e1vel P3 da express\u00e3o GP, reduzindo de uma porta OR '
    'de 5 entradas para uma porta OR de 4 entradas.'
)
doc.add_page_break()

doc.add_heading('3.3  Prova de Equival\u00eancia', level=2)
add_normal_text(
    'A tabela verdade a seguir compara as sa\u00eddas do modelo original e simplificado para '
    'todas as combina\u00e7\u00f5es v\u00e1lidas (omitindo linhas onde P3=1 e P2=0, por serem imposs\u00edveis):', space_after=12
)
add_caption('Quadro 10 \u2014 Tabela Verdade Comparativa: Sistema de Gamifica\u00e7\u00e3o')
gam_rows = []
for p1 in range(2):
    for p2 in range(2):
        for p3 in range(2):
            if p3 == 1 and p2 == 0:
                continue
            for p4 in range(2):
                for p5 in range(2):
                    orig = p1 | p2 | p3 | p4 | p5
                    simp = p1 | p2 | p4 | p5
                    gam_rows.append([str(p1), str(p2), str(p3), str(p4), str(p5), str(orig), str(simp), 'ok' if orig == simp else 'ERRO'])
add_table(['P1', 'P2', 'P3', 'P4', 'P5', 'GP(orig)', 'GP(simp)', 'Igual?'], gam_rows)
add_caption('Fonte: Elaborado pelos autores (2025)')
add_normal_text(
    'Resultado: As sa\u00eddas s\u00e3o id\u00eanticas em todas as 24 combina\u00e7\u00f5es v\u00e1lidas. '
    'Os modelos s\u00e3o comprovadamente equivalentes.',
    bold=True
)
doc.add_page_break()

# === 4. CLASSIFICA\u00c7\u00c3O DE RISCO ===
doc.add_heading('4  SISTEMA DE CLASSIFICA\u00c7\u00c3O DE RISCO (CHECK-UP DIGITAL)', level=1)
doc.add_heading('4.1  Descri\u00e7\u00e3o e Vari\u00e1veis', level=2)
add_normal_text(
    'Ap\u00f3s o paciente completar o check-up digital de 8 perguntas, o sistema calcula um '
    'score de risco (0 a 100) e classifica o resultado em tr\u00eas n\u00edveis. A l\u00f3gica foi extra\u00edda '
    'da fun\u00e7\u00e3o calculateRiskScore() e do trecho de classifica\u00e7\u00e3o no sketch.ino.'
)
add_normal_text(
    'Para a modelagem booleana, simplificamos para 2 vari\u00e1veis que representam os limiares '
    'de decis\u00e3o do score:', space_after=12
)
add_caption('Quadro 11 \u2014 Vari\u00e1veis de Entrada do Sistema de Classifica\u00e7\u00e3o')
add_table(
    ['Vari\u00e1vel', 'Significado', 'Condi\u00e7\u00e3o'],
    [
        ['S1', 'Score \u2265 30', 'Ultrapassou limiar de baixo risco'],
        ['S2', 'Score \u2265 60', 'Ultrapassou limiar de risco moderado'],
    ],
    col_widths=[2, 4, 6]
)
add_caption('Fonte: Elaborado pelos autores (2025)')
add_normal_text(
    'Restri\u00e7\u00e3o: S2 implica S1 (S2 \u2192 S1). Se o score \u00e9 \u2265 60, necessariamente \u00e9 \u2265 30. '
    "Portanto S2 \u00b7 S1' = 0 (imposs\u00edvel)."
)
add_caption('Quadro 12 \u2014 Sa\u00eddas do Sistema de Classifica\u00e7\u00e3o')
add_table(
    ['Sa\u00edda', 'Significado', 'Condi\u00e7\u00e3o'],
    [
        ['LO', 'Baixo Risco', 'Score < 30'],
        ['MO', 'Risco Moderado', '30 \u2264 Score < 60'],
        ['HI', 'Alto Risco', 'Score \u2265 60'],
    ],
    col_widths=[2, 4, 6]
)
add_caption('Fonte: Elaborado pelos autores (2025)')
add_normal_text('Express\u00f5es l\u00f3gicas originais:', bold=True, indent_first=False)
add_equation('HI = S2')
add_equation("MO = S1 \u00b7 S2'")
add_equation("LO = S1' \u00b7 S2'")

doc.add_heading('4.2  Simplifica\u00e7\u00e3o', level=2)
add_normal_text(
    'Observando que HI, MO e LO s\u00e3o mutuamente exclusivos e exaustivos (exatamente uma '
    'classifica\u00e7\u00e3o \u00e9 ativa por vez), podemos simplificar por substitui\u00e7\u00e3o de sinais:'
)
add_equation('Simplificado:')
add_equation('HI = S2')
add_equation("MO = S1 \u00b7 HI'       [substitui\u00e7\u00e3o: S2' = HI']")
add_equation("LO = (HI + MO)'     [deriva\u00e7\u00e3o por exclus\u00e3o]")
add_normal_text('Prova da equival\u00eancia para LO:', bold=True, indent_first=False)
add_equation("HI + MO = S2 + S1\u00b7S2'")
add_equation("= S2 + S1    [Absor\u00e7\u00e3o: X + X'\u00b7Y = X + Y]")
add_equation("LO = (S2 + S1)' = S1' \u00b7 S2'    [Q.E.D.]")
doc.add_page_break()

doc.add_heading('4.3  Prova de Equival\u00eancia', level=2)
add_caption('Quadro 13 \u2014 Tabela Verdade Comparativa: Sistema de Classifica\u00e7\u00e3o')
add_table(
    ['S1', 'S2', 'HI(orig)', 'HI(simp)', 'MO(orig)', 'MO(simp)', 'LO(orig)', 'LO(simp)', 'Igual?'],
    [
        ['0', '0', '0', '0', '0', '0', '1', '1', 'ok'],
        ['1', '0', '0', '0', '1', '1', '0', '0', 'ok'],
        ['0', '1', 'X', 'X', 'X', 'X', 'X', 'X', 'Imposs\u00edvel'],
        ['1', '1', '1', '1', '0', '0', '0', '0', 'ok'],
    ]
)
add_caption('Fonte: Elaborado pelos autores (2025)')
add_normal_text(
    'Resultado: Todas as sa\u00eddas s\u00e3o id\u00eanticas nos 3 cen\u00e1rios v\u00e1lidos. '
    'Os modelos s\u00e3o comprovadamente equivalentes.',
    bold=True
)
doc.add_page_break()

# === 5. RESUMO ===
doc.add_heading('5  RESUMO DAS SIMPLIFICA\u00c7\u00d5ES', level=1)
add_caption('Quadro 14 \u2014 Resumo: Sistema de Alertas')
add_table(
    ['Sa\u00edda', 'Original', 'Simplificada', 'M\u00e9todo'],
    [
        ['R (LED Vermelho)', 'A + C', 'A + C', 'J\u00e1 m\u00ednima'],
        ['Z (Buzzer)', 'A + C', 'R (reuso)', 'Elimina\u00e7\u00e3o redund\u00e2ncia'],
        ['Y (LED Amarelo)', "A'\u00b7C'\u00b7(B+D)", "R'\u00b7(B+D)", 'De Morgan + subst.'],
        ['G (LED Verde)', "A'\u00b7B'\u00b7C'\u00b7D'", "(R+Y)'", 'Deriva\u00e7\u00e3o exclus\u00e3o'],
    ]
)
add_caption('Fonte: Elaborado pelos autores (2025)')
add_normal_text('Economia no Sistema de Alertas: Redu\u00e7\u00e3o de 8 para 5 portas l\u00f3gicas (37,5%).', bold=True)

add_caption('Quadro 15 \u2014 Resumo: Sistema de Gamifica\u00e7\u00e3o')
add_table(
    ['Sa\u00edda', 'Original', 'Simplificada', 'M\u00e9todo'],
    [['GP (Ganha Pts)', 'P1+P2+P3+P4+P5', 'P1+P2+P4+P5', 'Absor\u00e7\u00e3o (P3 \u2286 P2)']],
)
add_caption('Fonte: Elaborado pelos autores (2025)')
add_normal_text('Economia no Sistema de Gamifica\u00e7\u00e3o: Redu\u00e7\u00e3o de 1 vari\u00e1vel de entrada (OR 5 \u2192 OR 4).', bold=True)

add_caption('Quadro 16 \u2014 Resumo: Sistema de Classifica\u00e7\u00e3o de Risco')
add_table(
    ['Sa\u00edda', 'Original', 'Simplificada', 'M\u00e9todo'],
    [
        ['HI (Alto Risco)', 'S2', 'S2', 'J\u00e1 m\u00ednima'],
        ['MO (Moderado)', "S1\u00b7S2'", "S1\u00b7HI'", 'Subst. de sinal'],
        ['LO (Baixo Risco)', "S1'\u00b7S2'", "(HI+MO)'", 'Deriva\u00e7\u00e3o exclus\u00e3o'],
    ]
)
add_caption('Fonte: Elaborado pelos autores (2025)')
add_normal_text(
    'Economia no Sistema de Classifica\u00e7\u00e3o: Reutiliza\u00e7\u00e3o de sinais j\u00e1 calculados, '
    'eliminando portas NOT duplicadas.',
    bold=True
)
doc.add_page_break()

# === 6. CONCLUS\u00c3O ===
doc.add_heading('6  CONCLUS\u00c3O', level=1)
add_normal_text(
    'Este relat\u00f3rio demonstrou a modelagem completa da l\u00f3gica digital do projeto Level UP '
    'em tr\u00eas subsistemas distintos. Para cada subsistema, o trabalho foi conduzido em tr\u00eas '
    'etapas rigorosas, conforme solicitado no enunciado da Sprint 03.'
)
add_normal_text(
    'Na primeira etapa, modelamos as express\u00f5es booleanas originais, extraindo-as '
    'diretamente do c\u00f3digo-fonte (sketch.ino) das fun\u00e7\u00f5es evaluateHealth(), awardPoints() '
    'e calculateRiskScore(). Cada vari\u00e1vel de entrada foi cuidadosamente definida a partir '
    'das condi\u00e7\u00f5es l\u00f3gicas presentes no c\u00f3digo, e as restri\u00e7\u00f5es de exclus\u00e3o m\u00fatua foram '
    'identificadas e formalizadas.'
)
add_normal_text(
    'Na segunda etapa, aplicamos t\u00e9cnicas de simplifica\u00e7\u00e3o utilizando \u00e1lgebra booleana '
    '(Leis de De Morgan, Teorema da Absor\u00e7\u00e3o, elimina\u00e7\u00e3o de redund\u00e2ncia) e mapas de '
    'Karnaugh com condi\u00e7\u00f5es don\'t care. As simplifica\u00e7\u00f5es resultaram em redu\u00e7\u00f5es '
    'significativas: 37,5% menos portas l\u00f3gicas no sistema de alertas, elimina\u00e7\u00e3o de '
    'vari\u00e1vel redundante no sistema de gamifica\u00e7\u00e3o, e reutiliza\u00e7\u00e3o eficiente de sinais '
    'no sistema de classifica\u00e7\u00e3o de risco.'
)
add_normal_text(
    'Na terceira etapa, provamos a equival\u00eancia entre os modelos original e simplificado '
    'por meio de tabelas verdade comparativas. Em todos os cen\u00e1rios v\u00e1lidos de todos os '
    'tr\u00eas subsistemas, as sa\u00eddas dos modelos original e simplificado s\u00e3o id\u00eanticas, '
    'confirmando matematicamente a corre\u00e7\u00e3o das simplifica\u00e7\u00f5es realizadas.'
)
add_normal_text(
    'Essas otimiza\u00e7\u00f5es s\u00e3o aplic\u00e1veis tanto em implementa\u00e7\u00e3o com portas l\u00f3gicas discretas '
    '(circuitos digitais) quanto no firmware embarcado do ESP32, contribuindo para menor '
    'consumo de energia, menor lat\u00eancia de processamento e maior efici\u00eancia computacional '
    'do sistema Level UP.'
)
doc.add_page_break()

# === REFER\u00caNCIAS ===
add_centered_text('REFER\u00caNCIAS', 14, bold=True, space_after=24)
refs = [
    'FLOYD, Thomas L. Sistemas digitais: fundamentos e aplica\u00e7\u00f5es. 9. ed. Porto Alegre: Bookman, 2007.',
    'IDOETA, Ivan V.; CAPUANO, Francisco G. Elementos de eletr\u00f4nica digital. 42. ed. S\u00e3o Paulo: \u00c9rica, 2019.',
    'KARNAUGH, Maurice. The map method for synthesis of combinational logic circuits. Transactions of the American Institute of Electrical Engineers, Part I: Communication and Electronics, v. 72, n. 5, p. 593-599, 1953.',
    'TOCCI, Ronald J.; WIDMER, Neal S.; MOSS, Gregory L. Sistemas digitais: princ\u00edpios e aplica\u00e7\u00f5es. 12. ed. S\u00e3o Paulo: Pearson Education, 2018.',
    'ESPRESSIF SYSTEMS. ESP32 Technical Reference Manual. Version 5.0. Shanghai: Espressif Systems, 2024. Dispon\u00edvel em: https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf. Acesso em: 10 maio 2025.',
    'ARDUINO. Arduino Language Reference. Dispon\u00edvel em: https://www.arduino.cc/reference/en/. Acesso em: 10 maio 2025.',
    'WOKWI. Wokwi ESP32 Simulator Documentation. Dispon\u00edvel em: https://docs.wokwi.com/. Acesso em: 10 maio 2025.',
]
for ref in refs:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(ref)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)

# === SALVAR ===
output_path = '/home/ubuntu/repos/global-solution-energy-2025/level-up-wokwi/Relatorio_Logica_Digital_Sprint03_ABNT.docx'
doc.save(output_path)
print(f'Relat\u00f3rio salvo em: {output_path}')
print(f'Tamanho: {os.path.getsize(output_path)} bytes')
