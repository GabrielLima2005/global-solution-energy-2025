# SmartEnergyOffice 🚀

Este projeto foi desenvolvido com o objetivo de analisar o consumo energético de um escritório e criar uma solução simples e sustentável para reduzir desperdícios, utilizando análise de dados, automação IoT (simulada) e uma simulação do uso de energia solar.

---

## 📌 Objetivo do Projeto
- Analisar dados de consumo de energia (dataset simulado).
- Identificar horários e equipamentos que geram maior desperdício.
- Criar uma automação simples para reduzir o consumo desnecessário.
- Simular o impacto da energia solar durante o dia.
- Relacionar a solução ao **futuro do trabalho** e sustentabilidade.

---

## 📁 Estrutura do Repositório

SmartEnergyOffice/
│

│   ├── analise_consumo.ipynb

│   ├── automacao_iot.py

│   ├── simulacao_solar.ipynb

│   └── consumo_simulado.csv

│

└── README.md




---

## 📊 Descrição dos Arquivos

### **📌 consumo_simulado.csv**
Arquivo com 24 registros, um para cada hora do dia, contendo:
- Iluminação (kWh)  
- Ar-condicionado (kWh)  
- Computadores (kWh)  
- Outros equipamentos (kWh)

### **📌 analise_consumo.ipynb**
Notebook que:
- Carrega o dataset  
- Calcula o consumo total por hora  
- Gera um gráfico simples  
- Identifica desperdício após o horário comercial

### **📌 automacao_iot.py**
Simulação de automações que poderiam existir em um escritório:
- Desligar luzes após às 20h  
- Reduzir o ar-condicionado quando o ambiente já estiver frio  

Representa um **protótipo de IoT inteligente**.

### **📌 simulacao_solar.ipynb**
Mostra como a energia solar reduziria o consumo de energia do escritório durante o dia.

---

## 📈 Resultados do Projeto

### 🔍 **Principais descobertas**
- O maior consumo ocorre entre **09h e 14h**, principalmente por causa do ar-condicionado e computadores.
- Após as **20h**, ainda existe consumo desnecessário — indicando desperdício.

### ⚙️ **Impacto das soluções criadas**
- **Automação IoT simulada** → economia estimada entre **10% e 20%**  
- **Simulação da energia solar** → redução de até **80% do uso da rede no pico**  

---

## 🌱 Conexão com o Futuro do Trabalho
Ambientes de trabalho modernos exigem:
- eficiência energética  
- automação  
- sustentabilidade  
- redução de custos  

Este projeto mostra como soluções simples podem deixar ambientes mais inteligentes, econômicos e preparados para o futuro.

---

## ▶️ Como Executar

1. Baixe o repositório.
2. Execute:
   - `analise_consumo.ipynb` → análise dos dados  
   - `automacao_iot.py` → simulação IoT  
   - `simulacao_solar.ipynb` → simulação da energia solar  


---

## ✔️ Tecnologias Utilizadas
- Python  
- Pandas  
- Matplotlib  
- Jupyter Notebook  

---

Projeto desenvolvido para fins de estudo e aplicação prática de análise de dados e sustentabilidade.

---

## Level UP - Sistema Inteligente de Monitoramento de Saude

O **Level UP** e uma evolucao estrategica que transforma a experiencia de saude corporativa em um modelo mais inteligente, proativo e centrado no paciente. O projeto e simulado no **Wokwi** utilizando **ESP32**.

### Tres Pilares

1. **Monitoramento Continuo via Wearables** - Frequencia cardiaca, atividade fisica, temperatura corporal
2. **Check-up Digital com IA** - Triagem adaptativa com score de risco automatizado
3. **Gamificacao** - Pontos, niveis e ranks para engajamento em habitos saudaveis

### Componentes do Circuito (Wokwi)

| Componente | Funcao |
|---|---|
| ESP32 DevKit V1 | Microcontrolador principal |
| OLED SSD1306 128x64 | Display de dados e interface |
| DHT22 | Sensor de temperatura e umidade |
| 2x Potenciometros | Simulam sensor cardiaco e acelerometro |
| 3x LEDs (Verde/Amarelo/Vermelho) | Indicadores de status de saude |
| Buzzer | Alarme para alertas criticos |
| 2x Botoes | Navegacao e interacao |

### Como Executar no Wokwi

1. Acesse [wokwi.com](https://wokwi.com)
2. Crie um novo projeto ESP32
3. Copie o conteudo de `level-up-wokwi/diagram.json` para o arquivo de diagrama
4. Copie o conteudo de `level-up-wokwi/sketch.ino` para o arquivo de codigo
5. Instale as bibliotecas listadas em `level-up-wokwi/libraries.txt`
6. Execute a simulacao

### Navegacao

- **BTN_MENU (azul)**: Navegar entre telas (Dashboard, Vitais, Check-up, Gamificacao)
- **BTN_SELECT (verde)**: Interagir (responder perguntas do check-up, confirmar alertas)

### Arquivos

- `level-up-wokwi/diagram.json` - Circuito completo do Wokwi
- `level-up-wokwi/sketch.ino` - Codigo Arduino para ESP32
- `level-up-wokwi/libraries.txt` - Bibliotecas necessarias

---

Nicolas Araujo de Oliveira RM 566780

Pedro Ivson Falcao De Leucas RM 

Gabriel Lima Da Silva RM 568436


