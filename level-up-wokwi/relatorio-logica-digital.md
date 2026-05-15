# Relatorio de Logica Digital - Sprint 03
## Projeto Level UP - Sistema Inteligente de Monitoramento de Saude

**Autores:** Nicolas Araujo de Oliveira (RM 566780), Pedro Ivson Falcao De Leucas, Gabriel Lima Da Silva (RM 568436)

**Disciplina:** Logica Digital Aplicada

---

## 1. Introducao

Este relatorio apresenta a modelagem logica do sistema **Level UP**, um monitor de saude baseado em ESP32 simulado no Wokwi. O sistema possui tres subsistemas principais com logica digital bem definida:

1. **Sistema de Alertas de Saude** — controla LEDs (verde/amarelo/vermelho) e buzzer com base em faixas de frequencia cardiaca e temperatura
2. **Sistema de Gamificacao** — determina se o paciente ganha pontos com base em indicadores saudaveis
3. **Sistema de Classificacao de Risco** — classifica o risco do check-up digital em tres niveis

Iremos modelar cada subsistema como expressoes booleanas, simplificar usando algebra booleana e mapas de Karnaugh, e provar a equivalencia entre os modelos original e simplificado com tabelas verdade.

---

## 2. Sistema 1: Logica de Alertas de Saude (LEDs + Buzzer)

### 2.1 Descricao do Funcionamento

O sistema avalia continuamente dois sinais vitais e aciona indicadores visuais/sonoros:

- **Frequencia Cardiaca (FC):**
  - CRITICO: FC < 50 ou FC > 160
  - ATENCAO: FC < 60 ou FC > 100 (quando nao critico)
  - NORMAL: 60 <= FC <= 100

- **Temperatura (T):**
  - CRITICO: T < 34.0 ou T > 39.0
  - ATENCAO: T < 35.5 ou T > 37.5 (quando nao critico)
  - NORMAL: 35.5 <= T <= 37.5

### 2.2 Variaveis Booleanas de Entrada

Definimos 4 variaveis binarias que representam a classificacao dos sensores:

| Variavel | Significado | Condicao |
|----------|-------------|----------|
| A | FC em faixa critica | FC < 50 OR FC > 160 |
| B | FC em faixa de atencao | (50 <= FC < 60) OR (100 < FC <= 160), ou seja: FC fora do normal mas nao critica |
| C | Temperatura em faixa critica | T < 34.0 OR T > 39.0 |
| D | Temperatura em faixa de atencao | (34.0 <= T < 35.5) OR (37.5 < T <= 39.0) |

**Restricoes importantes:**
- A e B sao mutuamente exclusivos (A . B = 0): a FC nao pode ser critica e de atencao ao mesmo tempo
- C e D sao mutuamente exclusivos (C . D = 0): a temperatura nao pode ser critica e de atencao ao mesmo tempo

### 2.3 Saidas do Sistema

| Saida | Significado | Componente |
|-------|-------------|------------|
| R | LED Vermelho (alerta critico) | RED_LED |
| Y | LED Amarelo (atencao) | YELLOW_LED |
| G | LED Verde (normal) | GREEN_LED |
| Z | Buzzer (alarme sonoro) | BUZZER_PIN |

### 2.4 Expressoes Logicas Originais

Extraidas diretamente do codigo `evaluateHealth()` no `sketch.ino`:

```
R = A + C
Y = A' . C' . (B + D)
G = A' . B' . C' . D'
Z = A + C
```

Onde:
- `+` representa OR
- `.` representa AND
- `'` representa NOT (complemento)

**Objetivo:** O LED vermelho e o buzzer ativam quando QUALQUER sinal vital esta critico. O LED amarelo ativa quando NENHUM esta critico mas ALGUM esta em atencao. O LED verde ativa apenas quando TODOS os sinais estao normais.

### 2.5 Tabela Verdade Original

Considerando as restricoes A.B=0 e C.D=0, as combinacoes impossiveis sao marcadas com "X" (don't care):

| # | A | B | C | D | R | Y | G | Z | Observacao |
|---|---|---|---|---|---|---|---|---|------------|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | FC normal, Temp normal |
| 1 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | FC normal, Temp atencao |
| 2 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 | FC normal, Temp critica |
| 3 | 0 | 0 | 1 | 1 | X | X | X | X | Impossivel (C.D=0) |
| 4 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | FC atencao, Temp normal |
| 5 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | FC atencao, Temp atencao |
| 6 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 1 | FC atencao, Temp critica |
| 7 | 0 | 1 | 1 | 1 | X | X | X | X | Impossivel (C.D=0) |
| 8 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | FC critica, Temp normal |
| 9 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | FC critica, Temp atencao |
| 10 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 1 | FC critica, Temp critica |
| 11 | 1 | 0 | 1 | 1 | X | X | X | X | Impossivel (C.D=0) |
| 12 | 1 | 1 | 0 | 0 | X | X | X | X | Impossivel (A.B=0) |
| 13 | 1 | 1 | 0 | 1 | X | X | X | X | Impossivel (A.B=0) |
| 14 | 1 | 1 | 1 | 0 | X | X | X | X | Impossivel (A.B=0) |
| 15 | 1 | 1 | 1 | 1 | X | X | X | X | Impossivel (A.B=0, C.D=0) |

### 2.6 Simplificacao por Algebra Booleana

#### Saida R (LED Vermelho):
```
Original:  R = A + C
```
Ja esta na forma minima. Nao ha como simplificar uma soma de duas variaveis.

#### Saida Z (Buzzer):
```
Original:  Z = A + C
Observacao: Z = R (saidas identicas!)
```
**Simplificacao:** Eliminamos a expressao redundante. O buzzer pode compartilhar o mesmo sinal logico do LED vermelho, economizando uma porta logica.

#### Saida Y (LED Amarelo):
```
Original:  Y = A' . C' . (B + D)
```

Aplicando a Lei de De Morgan: A' . C' = (A + C)'

```
Y = (A + C)' . (B + D)
Y = R' . (B + D)
```

**Simplificacao:** Substituimos `A' . C'` por `R'`, reutilizando o sinal ja calculado para o LED vermelho. Isso elimina duas portas NOT e uma porta AND de 2 entradas, substituindo por uma unica porta NOT sobre R.

**Prova da equivalencia:**
```
R = A + C
R' = (A + C)' = A' . C'  (De Morgan)

Portanto:
R' . (B + D) = A' . C' . (B + D)  ✓
```

#### Saida G (LED Verde):
```
Original:  G = A' . B' . C' . D'
```

Podemos reescrever usando as saidas ja calculadas:
```
G = (A + B + C + D)'
```

Ou, de forma mais eficiente:
```
G = R' . Y' . (nenhuma condicao de atencao sem alerta)
```

Na verdade, como R, Y e G sao mutuamente exclusivos e exaustivos (exatamente um LED esta ligado):
```
G = (R + Y)'
G = R' . Y'
```

**Prova da equivalencia:**
```
R + Y = (A + C) + (A' . C' . (B + D))
     = (A + C) + ((A + C)' . (B + D))

Pela lei X + X'Y = X + Y:
     = (A + C) + (B + D)
     = A + B + C + D

Portanto:
G = (R + Y)' = (A + B + C + D)' = A' . B' . C' . D'  ✓
```

### 2.7 Expressoes Simplificadas (Sistema de Alertas)

```
R = A + C
Z = R                    (reuso do sinal R)
Y = R' . (B + D)         (substituicao de A'.C' por R')
G = (R + Y)'             (derivado das outras saidas)
```

### 2.8 Mapas de Karnaugh

#### Mapa de Karnaugh para R (LED Vermelho):

```
          CD
AB    00  01  11  10
  00 | 0 | 0 | X | 1 |
  01 | 0 | 0 | X | 1 |
  11 | X | X | X | X |
  10 | 1 | 1 | X | 1 |
```

Agrupamentos:
- Grupo 1: A=1 (toda a linha A=1,B=0) → termo: A
- Grupo 2: C=1 (toda a coluna C=1,D=0) → termo: C
- R(min) = A + C ✓

#### Mapa de Karnaugh para Y (LED Amarelo):

```
          CD
AB    00  01  11  10
  00 | 0 | 1 | X | 0 |
  01 | 1 | 1 | X | 0 |
  11 | X | X | X | X |
  10 | 0 | 0 | X | 0 |
```

Agrupamentos (aproveitando don't cares):
- Grupo 1: A'C'D (celulas 01 e 05, expandindo com don't cares 03 e 07) → D . A' (ou D . C' considerando restricao)
  - Celulas: (0,0,0,1), (0,1,0,1), com don't cares (0,0,1,1), (0,1,1,1)
  - Agrupamento: A=0, D=1 → A' . D
- Grupo 2: A'C'B (celulas 04 e 05, expandindo com don't cares 12 e 13) → B . C'
  - Celulas: (0,1,0,0), (0,1,0,1), com don't cares (1,1,0,0), (1,1,0,1)
  - Agrupamento: B=1, C=0 → B . C'

Y(min) = A' . D + B . C'

Verificacao (com restricoes A.B=0, C.D=0):
```
A'.D + B.C' 
= A'.D.(C+C') + B.C'.(A+A')
= A'.D.C + A'.D.C' + A.B.C' + A'.B.C'
```
Como C.D=0, temos A'.D.C = 0. Como A.B=0, temos A.B.C' = 0.
```
= A'.D.C' + A'.B.C'
= A'.C'.(D + B)
= A'.C'.(B + D) ✓
```

As tres formas sao equivalentes. A forma A'.C'.(B+D) = R'.(B+D) e a mais eficiente em hardware.

#### Mapa de Karnaugh para G (LED Verde):

```
          CD
AB    00  01  11  10
  00 | 1 | 0 | X | 0 |
  01 | 0 | 0 | X | 0 |
  11 | X | X | X | X |
  10 | 0 | 0 | X | 0 |
```

Agrupamento:
- Unica celula com valor 1: (0,0,0,0)
- G(min) = A' . B' . C' . D' ✓

### 2.9 Tabela Verdade Comparativa — Original vs Simplificado

| # | A | B | C | D | R(orig) | R(simp) | Y(orig) | Y(simp) | G(orig) | G(simp) | Z(orig) | Z(simp) |
|---|---|---|---|---|---------|---------|---------|---------|---------|---------|---------|---------|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 |
| 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| 2 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 1 |
| 4 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| 5 | 0 | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| 6 | 0 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 1 |
| 8 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 1 |
| 9 | 1 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 1 |
| 10 | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 1 |

**Resultado: Todas as saidas sao identicas em todos os 9 cenarios validos. Os modelos sao equivalentes.** ✓

### 2.10 Diagrama Logico

#### Circuito Original (7 portas):
```
A ──────────────┐
                ├─ OR ──── R (LED Vermelho)
C ──────────────┘

A ── NOT ──┐
           ├─ AND ──┐
C ── NOT ──┘        │
                    ├─ AND ──── Y (LED Amarelo)
B ────────┐         │
          ├─ OR ───┘
D ────────┘

A ── NOT ──┐
           │
B ── NOT ──┼─ AND4 ──── G (LED Verde)
           │
C ── NOT ──┤
           │
D ── NOT ──┘

A ──────────────┐
                ├─ OR ──── Z (Buzzer)
C ──────────────┘
```
**Total: 4 NOT + 2 AND + 2 OR = 8 portas, com sinais redundantes**

#### Circuito Simplificado (5 portas):
```
A ────────┐
          ├─ OR ──── R (LED Vermelho)
C ────────┘     │
                └──── Z (Buzzer) [mesmo fio]
                │
                └─ NOT ──── R'
                            │
B ────────┐                 │
          ├─ OR ───┐        │
D ────────┘        ├─ AND ──── Y (LED Amarelo)
                   │            │
              R' ──┘            │
                                │
R ────────┐                     │
          ├─ NOR ──── G (LED Verde)
Y ────────┘
```
**Total: 1 NOT + 1 AND + 2 OR + 1 NOR = 5 portas, sem redundancia**

**Economia: 3 portas logicas eliminadas (reducao de 37.5%)**

---

## 3. Sistema 2: Logica de Gamificacao (Pontos)

### 3.1 Descricao do Funcionamento

O sistema avalia se o paciente merece pontos de gamificacao com base em 5 condicoes de saude saudavel. Cada condicao contribui pontos independentes.

### 3.2 Variaveis Booleanas de Entrada

| Variavel | Significado | Condicao | Pontos |
|----------|-------------|----------|--------|
| P1 | FC esta normal | 60 <= FC <= 100 | +10 |
| P2 | Atividade moderada | Atividade > 30% | +5 |
| P3 | Atividade intensa | Atividade > 60% | +10 |
| P4 | Temperatura normal | 36.0 <= T <= 37.5 | +5 |
| P5 | Boa qualidade de sono | Sono > 70% | +5 |

**Restricao:** P3 → P2 (se atividade > 60%, entao necessariamente > 30%). Portanto P3 . P2' = 0 (impossivel).

### 3.3 Saida: Ganha Pontos (GP)

```
Original: GP = P1 + P2 + P3 + P4 + P5
```

O paciente ganha algum ponto se QUALQUER condicao saudavel for verdadeira.

### 3.4 Tabela Verdade (Parcial — Cenarios Relevantes)

Como temos 5 variaveis (32 linhas), apresentamos os cenarios representativos:

| P1 | P2 | P3 | P4 | P5 | GP | Cenario |
|----|----|----|----|----|----|----|
| 0 | 0 | 0 | 0 | 0 | 0 | Nenhuma condicao saudavel — 0 pontos |
| 1 | 0 | 0 | 0 | 0 | 1 | Apenas FC normal — +10 pts |
| 0 | 1 | 0 | 0 | 0 | 1 | Apenas atividade moderada — +5 pts |
| 0 | 1 | 1 | 0 | 0 | 1 | Atividade intensa — +15 pts |
| 0 | 0 | 0 | 1 | 0 | 1 | Apenas temp normal — +5 pts |
| 0 | 0 | 0 | 0 | 1 | 1 | Apenas bom sono — +5 pts |
| 1 | 1 | 1 | 1 | 1 | 1 | Todas condicoes saudaveis — +35 pts |
| 0 | 0 | 1 | 0 | 0 | X | Impossivel (P3→P2) |

### 3.5 Simplificacao

A expressao `GP = P1 + P2 + P3 + P4 + P5` ja esta na forma minima (soma de literais).

Porem, considerando a restricao P3 → P2:
```
P1 + P2 + P3 + P4 + P5
```
Como P3=1 implica P2=1, o termo P3 e absorvido por P2 (Teorema da Absorcao: X + X.Y = X, e aqui P2 + P3 = P2 pois P3 ⊆ P2):

```
GP(simplificado) = P1 + P2 + P4 + P5
```

**Simplificacao: Eliminamos a variavel P3 da expressao GP, reduzindo de 5 para 4 entradas.**

### 3.6 Prova de Equivalencia

Para todos os casos validos (onde P3 → P2):

| P1 | P2 | P3 | P4 | P5 | GP(orig) = P1+P2+P3+P4+P5 | GP(simp) = P1+P2+P4+P5 | Igual? |
|----|----|----|----|----|---------------------------|------------------------|--------|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | ✓ |
| 0 | 0 | 0 | 0 | 1 | 1 | 1 | ✓ |
| 0 | 0 | 0 | 1 | 0 | 1 | 1 | ✓ |
| 0 | 0 | 0 | 1 | 1 | 1 | 1 | ✓ |
| 0 | 1 | 0 | 0 | 0 | 1 | 1 | ✓ |
| 0 | 1 | 0 | 0 | 1 | 1 | 1 | ✓ |
| 0 | 1 | 0 | 1 | 0 | 1 | 1 | ✓ |
| 0 | 1 | 0 | 1 | 1 | 1 | 1 | ✓ |
| 0 | 1 | 1 | 0 | 0 | 1 | 1 | ✓ |
| 0 | 1 | 1 | 0 | 1 | 1 | 1 | ✓ |
| 0 | 1 | 1 | 1 | 0 | 1 | 1 | ✓ |
| 0 | 1 | 1 | 1 | 1 | 1 | 1 | ✓ |
| 1 | 0 | 0 | 0 | 0 | 1 | 1 | ✓ |
| 1 | 0 | 0 | 0 | 1 | 1 | 1 | ✓ |
| 1 | 0 | 0 | 1 | 0 | 1 | 1 | ✓ |
| 1 | 0 | 0 | 1 | 1 | 1 | 1 | ✓ |
| 1 | 1 | 0 | 0 | 0 | 1 | 1 | ✓ |
| 1 | 1 | 0 | 0 | 1 | 1 | 1 | ✓ |
| 1 | 1 | 0 | 1 | 0 | 1 | 1 | ✓ |
| 1 | 1 | 0 | 1 | 1 | 1 | 1 | ✓ |
| 1 | 1 | 1 | 0 | 0 | 1 | 1 | ✓ |
| 1 | 1 | 1 | 0 | 1 | 1 | 1 | ✓ |
| 1 | 1 | 1 | 1 | 0 | 1 | 1 | ✓ |
| 1 | 1 | 1 | 1 | 1 | 1 | 1 | ✓ |

**Nota:** As linhas com P3=1 e P2=0 sao impossiveis pela restricao e foram omitidas.

**Resultado: As saidas sao identicas em todos os cenarios validos. Os modelos sao equivalentes.** ✓

---

## 4. Sistema 3: Logica de Classificacao de Risco (Check-up Digital)

### 4.1 Descricao do Funcionamento

Apos o check-up de 8 perguntas, o sistema classifica o risco do paciente em tres niveis com base no score calculado.

### 4.2 Variaveis Booleanas de Entrada

Simplificamos para 2 variaveis que representam as faixas do score:

| Variavel | Significado | Condicao |
|----------|-------------|----------|
| S1 | Score >= 30 | Ultrapassou limiar de baixo risco |
| S2 | Score >= 60 | Ultrapassou limiar de risco moderado |

**Restricao:** S2 → S1 (se score >= 60, entao >= 30). Portanto S2 . S1' = 0.

### 4.3 Saidas do Sistema

| Saida | Significado | Condicao |
|-------|-------------|----------|
| LO | Baixo Risco | Score < 30 |
| MO | Risco Moderado | 30 <= Score < 60 |
| HI | Alto Risco | Score >= 60 |

### 4.4 Expressoes Logicas Originais

```
HI = S2
MO = S1 . S2'
LO = S1' . S2'
```

### 4.5 Tabela Verdade Original

| # | S1 | S2 | LO | MO | HI | Classificacao |
|---|----|----|----|----|----|----|
| 0 | 0 | 0 | 1 | 0 | 0 | Baixo Risco (score < 30) |
| 1 | 1 | 0 | 0 | 1 | 0 | Risco Moderado (30 <= score < 60) |
| 2 | 0 | 1 | X | X | X | Impossivel (S2→S1) |
| 3 | 1 | 1 | 0 | 0 | 1 | Alto Risco (score >= 60) |

### 4.6 Simplificacao por Algebra Booleana

```
Original:
  HI = S2
  MO = S1 . S2'
  LO = S1' . S2'
```

Observando que HI, MO e LO sao mutuamente exclusivos e exaustivos:
```
LO + MO + HI = 1  (para todas as entradas validas)
```

Portanto:
```
Simplificado:
  HI = S2
  MO = S1 . HI'       (substituicao: S2' = HI')
  LO = (HI + MO)'     (derivado: unica classificacao restante)
```

**Prova:**
```
(HI + MO)' = (S2 + S1.S2')' 
           = (S2 + S1)' . (S2 + S2')'    [Distributiva]

Mais simples: S2 + S1.S2' = S2 + S1     [Absorcao: X + X'Y = X + Y]

Portanto: LO = (S2 + S1)' = S1'.S2' ✓
```

### 4.7 Tabela Verdade Comparativa

| S1 | S2 | HI(orig) | HI(simp) | MO(orig) | MO(simp) | LO(orig) | LO(simp) |
|----|----|----------|----------|----------|----------|----------|----------|
| 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 |
| 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |

**Resultado: Todas as saidas sao identicas em todos os cenarios validos. Os modelos sao equivalentes.** ✓

---

## 5. Resumo das Simplificacoes

### 5.1 Sistema de Alertas (Principal)

| Saida | Expressao Original | Expressao Simplificada | Metodo |
|-------|--------------------|------------------------|--------|
| R (LED Vermelho) | A + C | A + C | Ja minima |
| Z (Buzzer) | A + C | R (reuso de sinal) | Eliminacao de redundancia |
| Y (LED Amarelo) | A' . C' . (B + D) | R' . (B + D) | De Morgan + substituicao |
| G (LED Verde) | A' . B' . C' . D' | (R + Y)' | Derivacao por exclusao |

**Economia total: Reducao de 8 para 5 portas logicas (37.5%)**

### 5.2 Sistema de Gamificacao

| Saida | Expressao Original | Expressao Simplificada | Metodo |
|-------|--------------------|------------------------|--------|
| GP (Ganha Pontos) | P1 + P2 + P3 + P4 + P5 | P1 + P2 + P4 + P5 | Absorcao (P3 ⊆ P2) |

**Economia: Reducao de 1 variavel de entrada (porta OR de 5 → 4 entradas)**

### 5.3 Sistema de Classificacao de Risco

| Saida | Expressao Original | Expressao Simplificada | Metodo |
|-------|--------------------|------------------------|--------|
| HI (Alto Risco) | S2 | S2 | Ja minima |
| MO (Risco Moderado) | S1 . S2' | S1 . HI' | Substituicao de sinal |
| LO (Baixo Risco) | S1' . S2' | (HI + MO)' | Derivacao por exclusao |

**Economia: Reutilizacao de sinais ja calculados, eliminando portas NOT duplicadas**

---

## 6. Conclusao

Este relatorio demonstrou a modelagem completa da logica digital do projeto Level UP em tres subsistemas. Para cada um:

1. **Modelamos** as expressoes booleanas originais a partir do codigo-fonte (`sketch.ino`)
2. **Simplificamos** usando algebra booleana (Leis de De Morgan, Teorema da Absorcao, eliminacao de redundancia) e mapas de Karnaugh com condicoes don't care
3. **Provamos a equivalencia** com tabelas verdade comparativas, confirmando que todas as saidas sao identicas em 100% dos cenarios validos

As simplificacoes resultaram em:
- **37.5% menos portas logicas** no sistema de alertas
- **Eliminacao de variavel redundante** no sistema de gamificacao
- **Reutilizacao eficiente de sinais** no sistema de classificacao de risco

Essas otimizacoes sao aplicaveis tanto em implementacao com portas logicas discretas quanto no firmware embarcado, contribuindo para menor consumo de energia e maior eficiencia computacional do ESP32.

---

**Projeto:** Level UP - Sistema Inteligente de Monitoramento de Saude v2.0

**Plataforma:** ESP32 + Wokwi | WiFi + Dashboard Web

**Repositorio:** github.com/GabrielLima2005/global-solution-energy-2025
