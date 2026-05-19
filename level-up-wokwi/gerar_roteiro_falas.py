# -*- coding: utf-8 -*-
"""
Gera o documento Word com o roteiro de falas para o vídeo pitch de 3 minutos.
Cada cena tem: tempo, título, fala sugerida, e dicas de entonação.
"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

OUTPUT = '/home/ubuntu/repos/global-solution-energy-2025/level-up-wokwi/Roteiro_Falas_Video_3min.docx'

def create_doc():
    doc = Document()

    # Page setup
    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2)

    # Title
    title = doc.add_heading('Roteiro de Falas — Vídeo Pitch Level UP (3 min)', level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Subtitle
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('Disciplina: PCP – Pensamento Computacional e Automação com Python')
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(80, 80, 80)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('Prof. Sandro | FIAP — 1º Ano Ciência da Computação — 2026')
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(80, 80, 80)

    doc.add_paragraph()

    # Instructions
    p = doc.add_paragraph()
    run = p.add_run('INSTRUÇÕES GERAIS:')
    run.bold = True
    run.font.size = Pt(11)
    doc.add_paragraph('• Fale de forma clara, pausada e com confiança.', style='List Bullet')
    doc.add_paragraph('• Cada cena tem um tempo sugerido — pratique para encaixar.', style='List Bullet')
    doc.add_paragraph('• O vídeo visual já está pronto (Video_Pitch_3min_LevelUP.mp4). Grave apenas o áudio e sobreponha.', style='List Bullet')
    doc.add_paragraph('• Alternativamente, grave a tela + narração juntos em um app de gravação.', style='List Bullet')
    doc.add_paragraph('• Dica: use fones com microfone em ambiente silencioso.', style='List Bullet')
    doc.add_paragraph('• Duração total: exatamente 3 minutos (180 segundos).', style='List Bullet')

    doc.add_paragraph()
    doc.add_paragraph('─' * 60)
    doc.add_paragraph()

    # ===== SECTION 1 =====
    h = doc.add_heading('SEÇÃO 1 — Apresentação da Proposta do Projeto (~1 min 12s)', level=1)

    # Scene 1
    add_scene(doc,
        num=1, title='Abertura / Título',
        time='0:00 – 0:08', duration='8 segundos',
        fala=(
            'Olá! Somos alunos do primeiro ano de Ciência da Computação da FIAP '
            'e apresentamos o Level UP — um sistema inteligente de monitoramento de saúde '
            'desenvolvido como evolução estratégica da plataforma Blua, da CarePlus.'
        ),
        dica='Tom animado e acolhedor. Fale seu nome ou diga "somos a equipe..."'
    )

    # Scene 2
    add_scene(doc,
        num=2, title='O Problema',
        time='0:08 – 0:22', duration='14 segundos',
        fala=(
            'Hoje, a saúde corporativa ainda funciona de forma reativa. '
            'Não existe monitoramento contínuo, a adesão entre consultas é baixa, '
            'a triagem digital é pouco estruturada, e os custos assistenciais são elevados. '
            'Segundo a OMS, sessenta por cento das doenças crônicas poderiam ser evitadas '
            'com monitoramento e prevenção adequados.'
        ),
        dica='Tom sério, enfatize "sessenta por cento" com pausa antes.'
    )

    # Scene 3
    add_scene(doc,
        num=3, title='A Solução — Level UP',
        time='0:22 – 0:32', duration='10 segundos',
        fala=(
            'Para resolver isso, criamos o Level UP, que se apoia em três pilares: '
            'monitoramento contínuo via wearables, check-up digital com inteligência artificial, '
            'e gamificação para engajamento. '
            'Estudos da McKinsey indicam que soluções digitais podem reduzir custos em até vinte por cento.'
        ),
        dica='Tom confiante. Enumere os pilares com clareza.'
    )

    # Scene 4
    add_scene(doc,
        num=4, title='Pilar 1 — Monitoramento Contínuo',
        time='0:32 – 0:46', duration='14 segundos',
        fala=(
            'O primeiro pilar é o monitoramento contínuo. '
            'Integramos sensores que medem frequência cardíaca, temperatura corporal, '
            'nível de atividade física e qualidade do sono — tudo em tempo real. '
            'LEDs indicam o status: verde para normal, amarelo para atenção, '
            'e vermelho com buzzer para situações críticas. '
            'Isso permite identificar riscos precocemente e agir antes que o problema se agrave.'
        ),
        dica='Fale com ritmo, dê uma breve pausa entre cada sensor mencionado.'
    )

    # Scene 5
    add_scene(doc,
        num=5, title='Pilar 2 — Check-up Digital com IA',
        time='0:46 – 1:00', duration='14 segundos',
        fala=(
            'O segundo pilar é o check-up digital com inteligência artificial. '
            'São oito perguntas de triagem adaptativa, cada uma com peso diferente. '
            'O sistema cruza as respostas com os sinais vitais e gera um score de risco '
            'de zero a cem, classificando automaticamente em baixo, moderado ou alto. '
            'Um relatório preliminar é gerado para o médico, aumentando a produtividade clínica.'
        ),
        dica='Enfatize "oito perguntas" e "score de risco de zero a cem".'
    )

    # Scene 6
    add_scene(doc,
        num=6, title='Pilar 3 — Gamificação',
        time='1:00 – 1:12', duration='12 segundos',
        fala=(
            'O terceiro pilar é a gamificação. '
            'O paciente ganha pontos por manter sinais vitais saudáveis e completar check-ups. '
            'A cada cem pontos sobe de nível, passando por cinco ranks: de Iniciante até Mestre Saúde. '
            'Estudos mostram que estratégias de engajamento podem aumentar a adesão ao tratamento '
            'em até trinta por cento.'
        ),
        dica='Tom motivador. Enfatize "trinta por cento" no final.'
    )

    doc.add_paragraph()
    doc.add_paragraph('─' * 60)
    doc.add_paragraph()

    # ===== SECTION 2 =====
    h = doc.add_heading('SEÇÃO 2 — Cronograma e Especificações (~30s)', level=1)

    # Scene 7
    add_scene(doc,
        num=7, title='Cronograma das Etapas',
        time='1:12 – 1:28', duration='16 segundos',
        fala=(
            'Nosso cronograma está dividido em quatro fases. '
            'Na Sprint um, entre março e abril de dois mil e vinte e seis, '
            'definimos o projeto e montamos o circuito com sensores, LEDs e display OLED. '
            'Na Sprint dois, adicionamos WiFi, dashboard web e API REST. '
            'Na Sprint três, atual, desenvolvemos o relatório de lógica digital, '
            'documentação ABNT e este vídeo pitch. '
            'Para o futuro, planejamos app mobile, integração com wearables reais e IA preditiva.'
        ),
        dica='Fale com ritmo ágil mas claro. Enumere as sprints com pausas breves.'
    )

    # Scene 8
    add_scene(doc,
        num=8, title='Especificações de Hardware e Software',
        time='1:28 – 1:42', duration='14 segundos',
        fala=(
            'No hardware, utilizamos um ESP32 DevKit V1 como microcontrolador principal, '
            'display OLED SSD1306 de cento e vinte e oito por sessenta e quatro pixels, '
            'sensor DHT22 para temperatura e umidade, '
            'dois potenciômetros simulando sensores wearable, '
            'três LEDs com resistores de proteção, buzzer e dois botões de navegação. '
            'No software, programamos em C++ com Arduino IDE, '
            'usando bibliotecas Adafruit para o display, WiFi e WebServer do ESP32, '
            'e HTML, CSS e JavaScript para o dashboard.'
        ),
        dica='Fale fluido, não precisa detalhar cada resistor. Foque nos componentes principais.'
    )

    doc.add_paragraph()
    doc.add_paragraph('─' * 60)
    doc.add_paragraph()

    # ===== SECTION 3 =====
    h = doc.add_heading('SEÇÃO 3 — Descrição do Software (~42s)', level=1)

    # Scene 9
    add_scene(doc,
        num=9, title='Arquitetura do Software',
        time='1:42 – 1:56', duration='14 segundos',
        fala=(
            'O software tem novecentas e setenta e sete linhas em C++ '
            'e está organizado em seis módulos principais: '
            'leitura de sensores a cada dois segundos, '
            'avaliação de saúde com lógica booleana simplificada, '
            'check-up digital com perguntas ponderadas, '
            'gamificação com sistema de pontos e níveis, '
            'WiFi e web server com dashboard embutido em PROGMEM, '
            'e display OLED com seis telas diferentes e refresh a cada quinhentos milissegundos.'
        ),
        dica='Enumere os módulos com clareza. Não precisa ser técnico demais.'
    )

    # Scene 10
    add_scene(doc,
        num=10, title='Telas OLED',
        time='1:56 – 2:10', duration='14 segundos',
        fala=(
            'O display OLED apresenta seis telas, navegáveis pelo botão Menu. '
            'A tela Dashboard mostra BPM, temperatura e nível do jogador. '
            'A tela Relógio exibe a hora em formato grande com informações do WiFi. '
            'Sinais Vitais detalha todos os sensores. '
            'O Check-up Digital apresenta as perguntas interativas. '
            'Gamificação mostra pontos, nível e rank atual. '
            'E a tela de Alerta aparece automaticamente quando há risco crítico, '
            'acompanhada do buzzer sonoro.'
        ),
        dica='Fale de forma descritiva, como se mostrasse cada tela.'
    )

    # Scene 11
    add_scene(doc,
        num=11, title='Dashboard Web',
        time='2:10 – 2:24', duration='14 segundos',
        fala=(
            'O ESP32 cria sua própria rede WiFi chamada LevelUP-Health. '
            'Ao conectar, o usuário acessa o dashboard web no endereço cento e noventa e dois '
            'ponto cento e sessenta e oito ponto quatro ponto um. '
            'O dashboard tem tema escuro, exibe todos os dados de saúde em cards coloridos, '
            'e atualiza automaticamente a cada dois segundos via API REST. '
            'Também é possível ajustar o relógio diretamente pela interface web.'
        ),
        dica='Fale o IP com clareza. Enfatize "atualiza automaticamente".'
    )

    doc.add_paragraph()
    doc.add_paragraph('─' * 60)
    doc.add_paragraph()

    # ===== SECTION 4 =====
    h = doc.add_heading('SEÇÃO 4 — Hardware / Protótipo Wokwi (~36s)', level=1)

    # Scene 12
    add_scene(doc,
        num=12, title='Circuito Wokwi — Protótipo',
        time='2:24 – 2:40', duration='16 segundos',
        fala=(
            'Nosso protótipo foi desenvolvido no simulador Wokwi. '
            'O circuito conta com quatorze componentes e vinte e nove conexões. '
            'No centro temos o ESP32. À esquerda, o display OLED conectado via I2C, '
            'o sensor DHT22 e os dois potenciômetros. '
            'À direita, os três LEDs de status com resistores de proteção, '
            'o buzzer e os dois botões de interação. '
            'O mesmo código pode ser carregado diretamente em um ESP32 real — '
            'é um protótipo funcional completo.'
        ),
        dica='Tom técnico mas acessível. Enfatize "protótipo funcional completo".'
    )

    # Scene 13
    add_scene(doc,
        num=13, title='Encerramento',
        time='2:40 – 3:00', duration='20 segundos',
        fala=(
            'Em resumo, o Level UP transforma o cuidado de reativo para proativo, '
            'com potencial de reduzir custos assistenciais em vinte por cento, '
            'aumentar a adesão ao tratamento em trinta por cento, '
            'e melhorar a produtividade clínica em vinte e cinco por cento. '
            'Para a CarePlus, isso significa inovação em saúde centrada no paciente. '
            'Obrigado pela atenção! Somos: Gabriel Lima da Silva, '
            'João Carmo Cassu de Castro, Luiz Gustavo de Almeida, '
            'Nicolas Araujo de Oliveira e Matheus Costa Cutrim. '
            'FIAP, primeiro ano de Ciência da Computação, dois mil e vinte e seis. Muito obrigado!'
        ),
        dica='Tom conclusivo e animado. Termine com energia e sorriso na voz.'
    )

    doc.add_paragraph()
    doc.add_paragraph('─' * 60)
    doc.add_paragraph()

    # Final tips
    h = doc.add_heading('DICAS FINAIS PARA GRAVAÇÃO', level=1)
    tips = [
        'Pratique lendo em voz alta 2-3 vezes antes de gravar.',
        'Use cronômetro para verificar se cada cena cabe no tempo.',
        'Se sobrar tempo em alguma cena, faça uma pausa natural — não acelere.',
        'Grave em ambiente silencioso, preferencialmente com fone/headset.',
        'Pode dividir a narração entre membros da equipe (1 pessoa por seção funciona bem).',
        'Após gravar, sobreponha o áudio ao Video_Pitch_3min_LevelUP.mp4 no editor.',
        'Exporte em 1080p e faça upload no YouTube como "não listado" ou "público".',
        'Poste o link do YouTube no sistema de entrega da FIAP.',
    ]
    for tip in tips:
        doc.add_paragraph(tip, style='List Bullet')

    doc.add_paragraph()

    # Word count estimate
    p = doc.add_paragraph()
    run = p.add_run('ESTATÍSTICAS DO ROTEIRO:')
    run.bold = True
    doc.add_paragraph('• Total de palavras na narração: ~650 palavras', style='List Bullet')
    doc.add_paragraph('• Velocidade recomendada: ~130 palavras/minuto (ritmo calmo e claro)', style='List Bullet')
    doc.add_paragraph('• Duração estimada da narração: ~3 minutos', style='List Bullet')
    doc.add_paragraph('• Seção mais longa: Encerramento (20s) — pode dividir entre 2 pessoas', style='List Bullet')

    doc.save(OUTPUT)
    print(f'Roteiro salvo: {OUTPUT}')
    print(f'Tamanho: {os.path.getsize(OUTPUT) // 1024} KB')


def add_scene(doc, num, title, time, duration, fala, dica):
    """Add a scene to the document"""
    # Scene header
    p = doc.add_paragraph()
    run = p.add_run(f'CENA {num} — {title}')
    run.bold = True
    run.font.size = Pt(13)
    run.font.color.rgb = RGBColor(0, 100, 80)

    # Time info
    p = doc.add_paragraph()
    run = p.add_run(f'⏱ Tempo: {time}  |  Duração: {duration}')
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(100, 100, 100)

    # Speech
    p = doc.add_paragraph()
    run = p.add_run('FALA: ')
    run.bold = True
    run.font.size = Pt(11)
    run = p.add_run(f'"{fala}"')
    run.font.size = Pt(11)
    run.italic = True

    # Tip
    p = doc.add_paragraph()
    run = p.add_run(f'💡 Dica: {dica}')
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(80, 80, 120)

    doc.add_paragraph()


if __name__ == '__main__':
    create_doc()
