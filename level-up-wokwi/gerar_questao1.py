# -*- coding: utf-8 -*-
"""
Questão 1 - Descrição completa do projeto Level UP com Care Plus
PCP - Sprint 3
"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

doc = Document()

# =================== MARGENS ABNT ===================
for section in doc.sections:
    section.top_margin = Cm(3)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(3)
    section.right_margin = Cm(2)

# =================== FUNCOES AUXILIARES ===================
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

def add_centered_text(text, size=12, bold=False, space_after=12, space_before=0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(space_before)
    pf.line_spacing = Pt(18)
    run = p.add_run(text)
    set_font(run, size=size, bold=bold)
    return p

def add_normal_text(text, space_after=6, bold=False, indent=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(0)
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

def add_bullet(text, level=0):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.space_after = Pt(4)
    pf.line_spacing = Pt(18)
    if level > 0:
        pf.left_indent = Cm(1.5 * (level + 1))
    p.clear()
    run = p.add_run(text)
    set_font(run, size=12)
    return p

def add_table(headers, rows):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Header
    for i, h in enumerate(headers):
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
    # Data rows
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = ''
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(str(val))
            set_font(run, size=10)
    return table

# =================== CAPA ===================
add_centered_text('FIAP \u2013 FACULDADE DE INFORM\u00c1TICA E ADMINISTRA\u00c7\u00c3O PAULISTA', 14, bold=True, space_after=24)
add_centered_text('1\u00ba ANO DE CI\u00caNCIA DA COMPUTA\u00c7\u00c3O', 12, bold=False, space_after=12)
add_centered_text('PCP \u2013 PENSAMENTO COMPUTACIONAL E AUTOMA\u00c7\u00c3O COM PYTHON', 12, bold=False, space_after=12)
add_centered_text('Prof. Allan Roberto Molto', 12, bold=False, space_after=48)

add_centered_text('QUEST\u00c3O 1 \u2013 DESCRI\u00c7\u00c3O COMPLETA DO PROJETO', 16, bold=True, space_after=6)
add_centered_text('Level UP \u2013 BluaDiagnostics', 14, bold=True, space_after=6)
add_centered_text('Check-up Digital e Prescri\u00e7\u00e3o Inteligente', 12, space_after=48)

add_centered_text('Nicolas Ara\u00fajo de Oliveira \u2013 RM 566780', 12, space_after=6)
add_centered_text('Pedro Ivson Falc\u00e3o De Leucas', 12, space_after=6)
add_centered_text('Gabriel Lima Da Silva \u2013 RM 568436', 12, space_after=48)

add_centered_text('S\u00e3o Paulo', 12, space_after=6)
add_centered_text('2025', 12, space_after=0)

doc.add_page_break()

# =================== 1. INTRODUCAO ===================
add_heading_text('1  INTRODU\u00c7\u00c3O', level=1)

add_normal_text(
    'O projeto Level UP \u00e9 uma evolu\u00e7\u00e3o estrat\u00e9gica da plataforma Blua da Care Plus, '
    'que transforma a experi\u00eancia de sa\u00fade corporativa em um modelo mais inteligente, '
    'proativo e centrado no paciente. Atualmente, o modelo tradicional ainda apresenta '
    'lacunas importantes: aus\u00eancia de monitoramento cont\u00ednuo, baixa ades\u00e3o entre '
    'consultas e uma triagem digital pouco estruturada.',
    indent=True
)

add_normal_text(
    'Segundo a Organiza\u00e7\u00e3o Mundial da Sa\u00fade (OMS), cerca de 60% das doen\u00e7as cr\u00f4nicas '
    'poderiam ser evitadas com monitoramento e preven\u00e7\u00e3o adequados. Al\u00e9m disso, '
    'estudos da McKinsey indicam que solu\u00e7\u00f5es digitais podem reduzir custos '
    'assistenciais em at\u00e9 20%. Diante desse cen\u00e1rio, o Level UP se apoia em tr\u00eas '
    'pilares fundamentais: monitoramento cont\u00ednuo via wearables, check-up digital '
    'com intelig\u00eancia artificial e engajamento por gamifica\u00e7\u00e3o.',
    indent=True
)

add_normal_text(
    'O sistema foi prototipado utilizando ESP32 simulado na plataforma Wokwi, '
    'integrando sensores de sa\u00fade (DHT22, potenci\u00f4metros), display OLED SSD1306, '
    'LEDs indicadores, buzzer de alerta, WiFi Access Point e Web Server com '
    'dashboard HTML responsivo em tempo real.',
    indent=True
)

doc.add_page_break()

# =================== 2. DADOS DE ENTRADA ===================
add_heading_text('2  DADOS DE ENTRADA \u2013 INTEGRA\u00c7\u00c3O COM IA E WEARABLES', level=1)

add_normal_text(
    'O sistema Level UP recebe dados de m\u00faltiplas fontes, simulando a integra\u00e7\u00e3o '
    'inteligente com wearables e sistemas de intelig\u00eancia artificial. Os dados de '
    'entrada s\u00e3o categorizados em tr\u00eas grupos principais:',
    indent=True
)

add_heading_text('2.1  Dados de Sensores Wearables (Monitoramento Cont\u00ednuo)', level=2)

add_table(
    ['Dado de Entrada', 'Sensor/Fonte', 'Faixa de Valores', 'Frequ\u00eancia de Coleta'],
    [
        ['Frequ\u00eancia Card\u00edaca (BPM)', 'Potenci\u00f4metro (simula sensor PPG/\u00f3ptico)', '40\u2013200 BPM', 'A cada 2 segundos'],
        ['N\u00edvel de Atividade F\u00edsica', 'Potenci\u00f4metro (simula aceler\u00f4metro)', '0\u2013100%', 'A cada 2 segundos'],
        ['Temperatura Corporal', 'DHT22 (sensor real de temperatura)', '15\u201350 \u00b0C', 'A cada 2 segundos'],
        ['Umidade Ambiente', 'DHT22 (sensor real de umidade)', '0\u2013100%', 'A cada 2 segundos'],
        ['Passos Estimados', 'Derivado do n\u00edvel de atividade', '0\u201315.000 passos', 'A cada 2 segundos'],
        ['Qualidade do Sono', 'Derivado inversamente da atividade', '15\u201395%', 'A cada 2 segundos'],
    ]
)

p = doc.add_paragraph()
pf = p.paragraph_format
pf.space_before = Pt(4)
pf.space_after = Pt(12)
run = p.add_run('Quadro 1 \u2013 Dados de entrada dos sensores wearables')
set_font(run, size=10, italic=True)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

add_heading_text('2.2  Dados de Triagem Digital (Check-up com IA)', level=2)

add_normal_text(
    'O check-up digital simula um sistema de triagem com intelig\u00eancia artificial '
    'que adapta perguntas conforme as respostas do paciente. O sistema utiliza 8 '
    'perguntas ponderadas, cada uma com um peso espec\u00edfico que reflete a gravidade '
    'cl\u00ednica do sintoma:',
    indent=True
)

add_table(
    ['Pergunta', 'Peso', 'Tipo de Resposta'],
    [
        ['Dor no peito?', '20', 'Sim/N\u00e3o'],
        ['Falta de ar?', '15', 'Sim/N\u00e3o'],
        ['Tontura frequente?', '10', 'Sim/N\u00e3o'],
        ['Dor de cabe\u00e7a?', '5', 'Sim/N\u00e3o'],
        ['Fadiga excessiva?', '8', 'Sim/N\u00e3o'],
        ['Febre recente?', '12', 'Sim/N\u00e3o'],
        ['Palpita\u00e7\u00f5es?', '18', 'Sim/N\u00e3o'],
        ['Ins\u00f4nia?', '7', 'Sim/N\u00e3o'],
    ]
)

p = doc.add_paragraph()
pf = p.paragraph_format
pf.space_before = Pt(4)
pf.space_after = Pt(12)
run = p.add_run('Quadro 2 \u2013 Perguntas da triagem digital com pesos')
set_font(run, size=10, italic=True)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

add_normal_text(
    'Al\u00e9m das respostas do question\u00e1rio, o sistema cruza automaticamente os '
    'dados com os sinais vitais coletados em tempo real, adicionando pontos de '
    'risco adicionais:',
    indent=True
)

add_bullet('FC fora de 60\u2013100 BPM: +10 pontos de risco')
add_bullet('Temperatura acima de 37,5 \u00b0C: +10 pontos de risco')
add_bullet('N\u00edvel de atividade abaixo de 20%: +5 pontos de risco')
add_bullet('Qualidade do sono abaixo de 40%: +5 pontos de risco')

add_heading_text('2.3  Dados de Intera\u00e7\u00e3o do Usu\u00e1rio', level=2)

add_bullet('Navega\u00e7\u00e3o entre telas via bot\u00e3o Menu (6 telas dispon\u00edveis)')
add_bullet('Respostas do check-up via bot\u00e3o Select (Sim) ou Menu (N\u00e3o)')
add_bullet('Ajuste de hor\u00e1rio via interface web (/api/settime?h=HH&m=MM)')
add_bullet('Conex\u00e3o WiFi para acesso ao dashboard (SSID: LevelUP-Health)')

doc.add_page_break()

# =================== 3. ANALISE DOS DADOS ===================
add_heading_text('3  AN\u00c1LISE DOS DADOS \u2013 PROCESSAMENTO E L\u00d3GICA', level=1)

add_normal_text(
    'O processamento dos dados no Level UP ocorre em tempo real, utilizando '
    'algoritmos embarcados no ESP32 que analisam continuamente os sinais vitais '
    'e geram respostas inteligentes. A an\u00e1lise \u00e9 dividida em tr\u00eas m\u00f3dulos:',
    indent=True
)

add_heading_text('3.1  M\u00f3dulo de Avalia\u00e7\u00e3o de Sa\u00fade (evaluateHealth)', level=2)

add_normal_text(
    'Este m\u00f3dulo analisa os sinais vitais coletados e classifica o estado de '
    'sa\u00fade em tr\u00eas n\u00edveis de alerta, utilizando l\u00f3gica booleana com limiares '
    'cl\u00ednicos pr\u00e9-definidos:',
    indent=True
)

add_table(
    ['Condi\u00e7\u00e3o', 'N\u00edvel de Alerta', 'A\u00e7\u00e3o do Sistema'],
    [
        ['FC entre 60\u2013100 BPM e Temp entre 35,5\u201337,5 \u00b0C', 'NORMAL (0)', 'LED verde aceso'],
        ['FC entre 50\u201360 ou 100\u2013160 BPM; Temp entre 34\u201335,5 ou 37,5\u201339 \u00b0C', 'ATEN\u00c7\u00c3O (1)', 'LED amarelo aceso'],
        ['FC < 50 ou > 160 BPM; Temp < 34 ou > 39 \u00b0C', 'CR\u00cdTICO (2)', 'LED vermelho + Buzzer + Tela de Alerta autom\u00e1tica'],
    ]
)

p = doc.add_paragraph()
pf = p.paragraph_format
pf.space_before = Pt(4)
pf.space_after = Pt(12)
run = p.add_run('Quadro 3 \u2013 N\u00edveis de alerta e a\u00e7\u00f5es do sistema')
set_font(run, size=10, italic=True)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

add_heading_text('3.2  M\u00f3dulo de C\u00e1lculo de Risco (calculateRiskScore)', level=2)

add_normal_text(
    'Ap\u00f3s a conclus\u00e3o do check-up digital, o sistema calcula um score de risco '
    'de 0 a 100, combinando as respostas do question\u00e1rio (multiplicadas pelos '
    'pesos) com os sinais vitais em tempo real. O algoritmo funciona como uma '
    'IA simplificada que cruza m\u00faltiplas vari\u00e1veis para gerar um diagn\u00f3stico '
    'preliminar:',
    indent=True
)

add_normal_text('Score = \u03a3(Resposta_i \u00d7 Peso_i) + Ajustes_Sinais_Vitais', bold=True)

add_table(
    ['Faixa de Score', 'Classifica\u00e7\u00e3o', 'Recomenda\u00e7\u00e3o'],
    [
        ['0\u201329', 'BAIXO RISCO', 'Manter h\u00e1bitos saud\u00e1veis'],
        ['30\u201359', 'RISCO MODERADO', 'Agendar consulta preventiva'],
        ['60\u2013100', 'ALTO RISCO', 'Consulta m\u00e9dica URGENTE'],
    ]
)

p = doc.add_paragraph()
pf = p.paragraph_format
pf.space_before = Pt(4)
pf.space_after = Pt(12)
run = p.add_run('Quadro 4 \u2013 Classifica\u00e7\u00e3o de risco e recomenda\u00e7\u00f5es')
set_font(run, size=10, italic=True)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

add_heading_text('3.3  M\u00f3dulo de Gamifica\u00e7\u00e3o (awardPoints)', level=2)

add_normal_text(
    'O sistema de gamifica\u00e7\u00e3o analisa continuamente os sinais vitais (a cada 30 '
    'segundos) e premia o usu\u00e1rio por manter h\u00e1bitos saud\u00e1veis:',
    indent=True
)

add_table(
    ['Condi\u00e7\u00e3o Saud\u00e1vel', 'Pontos Ganhos'],
    [
        ['FC entre 60\u2013100 BPM', '+10 pontos'],
        ['Atividade f\u00edsica > 30%', '+5 pontos'],
        ['Atividade f\u00edsica > 60%', '+10 pontos adicionais'],
        ['Temperatura entre 36,0\u201337,5 \u00b0C', '+5 pontos'],
        ['Qualidade do sono > 70%', '+5 pontos'],
        ['Check-up completo', '+50 pontos (b\u00f4nus)'],
    ]
)

p = doc.add_paragraph()
pf = p.paragraph_format
pf.space_before = Pt(4)
pf.space_after = Pt(12)
run = p.add_run('Quadro 5 \u2013 Sistema de pontua\u00e7\u00e3o por h\u00e1bitos saud\u00e1veis')
set_font(run, size=10, italic=True)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

add_normal_text(
    'Os n\u00edveis evoluem a cada 100 pontos, e os ranks progridem conforme o n\u00edvel:',
    indent=True
)

add_table(
    ['N\u00edvel', 'Rank', 'Pontua\u00e7\u00e3o Necess\u00e1ria'],
    [
        ['1\u20132', 'Iniciante', '0\u2013199 pontos'],
        ['3\u20134', 'Aprendiz Ativo', '200\u2013399 pontos'],
        ['5\u20136', 'Guerreiro Fit', '400\u2013599 pontos'],
        ['7\u20139', 'Expert Vital', '600\u2013899 pontos'],
        ['10+', 'Mestre Sa\u00fade', '900+ pontos'],
    ]
)

p = doc.add_paragraph()
pf = p.paragraph_format
pf.space_before = Pt(4)
pf.space_after = Pt(12)
run = p.add_run('Quadro 6 \u2013 Sistema de n\u00edveis e ranks da gamifica\u00e7\u00e3o')
set_font(run, size=10, italic=True)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_page_break()

# =================== 4. SAIDA DOS DADOS ===================
add_heading_text('4  SA\u00cdDA DOS DADOS \u2013 RESULTADOS E BENEF\u00cdCIOS', level=1)

add_normal_text(
    'O sistema Level UP gera m\u00faltiplas sa\u00eddas de dados, proporcionando benef\u00edcios '
    'diretos tanto para o paciente quanto para a equipe m\u00e9dica e a CarePlus:',
    indent=True
)

add_heading_text('4.1  Sa\u00eddas Visuais em Tempo Real (OLED)', level=2)

add_normal_text(
    'O display OLED SSD1306 de 128\u00d764 pixels apresenta 6 telas de informa\u00e7\u00e3o, '
    'naveg\u00e1veis por bot\u00e3o:',
    indent=True
)

add_bullet('Dashboard: vis\u00e3o geral com rel\u00f3gio, BPM, temperatura, atividade e gamifica\u00e7\u00e3o')
add_bullet('Rel\u00f3gio: hora em formato grande (HH:MM SS) com informa\u00e7\u00f5es WiFi')
add_bullet('Sinais Vitais: detalhamento completo de todos os sensores')
add_bullet('Check-up Digital: triagem interativa com 8 perguntas ponderadas')
add_bullet('Gamifica\u00e7\u00e3o: n\u00edvel, rank, pontos e progresso para pr\u00f3ximo n\u00edvel')
add_bullet('Alerta: tela autom\u00e1tica para situa\u00e7\u00f5es cr\u00edticas com dupla borda')

add_heading_text('4.2  Sa\u00eddas F\u00edsicas (LEDs e Buzzer)', level=2)

add_bullet('LED Verde: sinais vitais normais \u2013 paciente saud\u00e1vel')
add_bullet('LED Amarelo: aten\u00e7\u00e3o \u2013 valores ligeiramente fora do normal')
add_bullet('LED Vermelho + Buzzer: alerta cr\u00edtico \u2013 interven\u00e7\u00e3o necess\u00e1ria')

add_heading_text('4.3  Sa\u00eddas Digitais (Dashboard Web e API)', level=2)

add_normal_text(
    'O ESP32 cria um Access Point WiFi (SSID: LevelUP-Health) e serve um '
    'dashboard HTML responsivo em http://192.168.4.1 com atualiza\u00e7\u00e3o autom\u00e1tica '
    'a cada 2 segundos. Al\u00e9m disso, disponibiliza uma API REST:',
    indent=True
)

add_bullet('GET /api/data \u2013 retorna todos os dados de sa\u00fade em formato JSON')
add_bullet('GET /api/settime?h=HH&m=MM \u2013 permite ajustar o rel\u00f3gio remotamente')

add_heading_text('4.4  Relat\u00f3rio M\u00e9dico Preliminar (Serial)', level=2)

add_normal_text(
    'Ap\u00f3s cada check-up completo, o sistema gera automaticamente um relat\u00f3rio '
    'm\u00e9dico preliminar via porta Serial contendo: sinais vitais coletados, '
    'sintomas reportados, score de risco calculado, classifica\u00e7\u00e3o '
    '(Baixo/Moderado/Alto Risco) e recomenda\u00e7\u00e3o cl\u00ednica.',
    indent=True
)

add_heading_text('4.5  Benef\u00edcios para o Paciente e a CarePlus', level=2)

add_table(
    ['Benef\u00edcio', 'Descri\u00e7\u00e3o', 'Impacto Esperado'],
    [
        ['Detec\u00e7\u00e3o precoce de riscos', 'Monitoramento cont\u00ednuo identifica altera\u00e7\u00f5es antes que se agravem', 'Redu\u00e7\u00e3o de 30\u201340% em interna\u00e7\u00f5es evit\u00e1veis'],
        ['Triagem inteligente', 'Check-up digital com IA gera ficha preliminar autom\u00e1tica', 'Aumento de 25% na produtividade cl\u00ednica'],
        ['Engajamento cont\u00ednuo', 'Gamifica\u00e7\u00e3o incentiva h\u00e1bitos saud\u00e1veis entre consultas', 'Aumento de 30% na ades\u00e3o ao tratamento'],
        ['Acesso remoto em tempo real', 'Dashboard web acess\u00edvel por qualquer dispositivo via WiFi', 'Democratiza\u00e7\u00e3o do acesso \u00e0 informa\u00e7\u00e3o de sa\u00fade'],
        ['Prescri\u00e7\u00e3o orientada por dados', 'Relat\u00f3rio com sinais vitais + sintomas para o m\u00e9dico', 'Prescri\u00e7\u00e3o mais assertiva e personalizada'],
        ['Redu\u00e7\u00e3o de custos', 'Preven\u00e7\u00e3o > tratamento; menos emerg\u00eancias, mais preven\u00e7\u00e3o', 'Economia de at\u00e9 20% em custos assistenciais'],
    ]
)

p = doc.add_paragraph()
pf = p.paragraph_format
pf.space_before = Pt(4)
pf.space_after = Pt(12)
run = p.add_run('Quadro 7 \u2013 Benef\u00edcios do sistema para paciente e CarePlus')
set_font(run, size=10, italic=True)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_page_break()

# =================== 5. COMPONENTES DESEJADOS ===================
add_heading_text('5  ATENDIMENTO AOS COMPONENTES DESEJADOS', level=1)

add_heading_text('5.1  Ferramenta de Check-up Digital Simples e Visual', level=2)

add_normal_text(
    'O Level UP implementa um check-up digital completo com 8 perguntas '
    'ponderadas, exibidas no display OLED de forma simples e visual. O paciente '
    'responde "Sim" ou "N\u00e3o" pressionando bot\u00f5es f\u00edsicos. Ao final, o sistema '
    'exibe o score de risco (0\u2013100), a classifica\u00e7\u00e3o (Baixo/Moderado/Alto) e '
    'uma barra de progresso visual. A IA simulada compara as respostas com '
    'padr\u00f5es cl\u00ednicos (pesos predefinidos) e gera sinais de alerta autom\u00e1ticos.',
    indent=True
)

add_heading_text('5.2  Prot\u00f3tipo de Interface de Prescri\u00e7\u00e3o Integrada ao Hist\u00f3rico', level=2)

add_normal_text(
    'O relat\u00f3rio m\u00e9dico gerado via Serial funciona como um prot\u00f3tipo de '
    'prescri\u00e7\u00e3o integrada. Ele combina os sinais vitais coletados em tempo real '
    'com os sintomas reportados no check-up, gerando uma ficha completa com '
    'classifica\u00e7\u00e3o de risco e recomenda\u00e7\u00e3o cl\u00ednica. O dashboard web complementa '
    'essa funcionalidade, oferecendo acesso remoto ao hist\u00f3rico de dados do '
    'paciente via API REST (/api/data).',
    indent=True
)

add_heading_text('5.3  Integra\u00e7\u00e3o com Wearables e Dados Externos', level=2)

add_normal_text(
    'O sistema simula a integra\u00e7\u00e3o com wearables utilizando potenci\u00f4metros '
    '(sensor card\u00edaco e aceler\u00f4metro) e sensor DHT22 (temperatura/umidade). '
    'Os dados s\u00e3o coletados a cada 2 segundos e transmitidos via WiFi para o '
    'dashboard web, simulando o fluxo de dados que ocorreria com wearables '
    'reais (smartwatch, pulseiras fitness, etc.).',
    indent=True
)

doc.add_page_break()

# =================== 6. CONCLUSAO ===================
add_heading_text('6  CONCLUS\u00c3O', level=1)

add_normal_text(
    'O projeto Level UP demonstra como a tecnologia pode transformar o cuidado '
    'de sa\u00fade de reativo para proativo. Atrav\u00e9s da integra\u00e7\u00e3o inteligente de '
    'sensores wearables, intelig\u00eancia artificial para triagem e gamifica\u00e7\u00e3o '
    'para engajamento, o sistema cria uma jornada de cuidado cont\u00ednua, '
    'preventiva e centrada no paciente.',
    indent=True
)

add_normal_text(
    'Para a CarePlus, o Level UP representa tr\u00eas benef\u00edcios diretos: redu\u00e7\u00e3o '
    'de custos assistenciais (prevenindo complica\u00e7\u00f5es com monitoramento cont\u00ednuo), '
    'aumento da satisfa\u00e7\u00e3o dos benefici\u00e1rios (com uma experi\u00eancia de sa\u00fade mais '
    'completa e engajante) e fortalecimento da proposta de valor da empresa '
    'como refer\u00eancia em inova\u00e7\u00e3o em sa\u00fade digital.',
    indent=True
)

add_normal_text(
    'O prot\u00f3tipo funcional simulado no Wokwi valida a viabilidade t\u00e9cnica da '
    'solu\u00e7\u00e3o, demonstrando que \u00e9 poss\u00edvel criar um dispositivo de monitoramento '
    'inteligente com hardware acess\u00edvel (ESP32) e software embarcado eficiente, '
    'pronto para evoluir para uma solu\u00e7\u00e3o de produ\u00e7\u00e3o com wearables reais e '
    'integra\u00e7\u00e3o com a plataforma Blua.',
    indent=True
)

# =================== SALVAR ===================
output_path = '/home/ubuntu/repos/global-solution-energy-2025/level-up-wokwi/Questao1_Descricao_Projeto.docx'
doc.save(output_path)
print(f'Documento salvo em: {output_path}')
print(f'Tamanho: {os.path.getsize(output_path)} bytes')
