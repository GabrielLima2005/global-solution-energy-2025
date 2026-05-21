# Roteiro de Apresentacao - Monitoramento de Temperatura de Servidor IoT

## Tempo estimado: 8 a 12 minutos

---

## 1. INTRODUCAO (2 minutos)

### O que falar:

> "Bom dia/boa tarde, professor. Nosso projeto eh o **Sistema de Monitoramento de Temperatura de um Servidor**, utilizando IoT."

> "O problema que estamos resolvendo eh o seguinte: servidores precisam operar em temperaturas controladas, geralmente entre 18 e 27 graus. Quando a temperatura sobe demais, pode causar travamentos, perda de dados e ate queimar componentes."

> "Nossa solucao usa um ESP32 com sensor de temperatura que monitora o servidor em tempo real e alerta o administrador de forma remota, pela internet."

---

## 2. COMPONENTES DO CIRCUITO (2 minutos)

### Mostrar no Wokwi e explicar cada componente:

| Componente | O que falar |
|-----------|-------------|
| **ESP32** | "Esse eh nosso microcontrolador principal. Ele tem WiFi integrado, que permite o monitoramento remoto." |
| **DHT22** | "Esse eh o sensor de temperatura e umidade. Ele faz a leitura a cada 2 segundos." |
| **LCD 16x2** | "Esse display mostra a temperatura e o status em tempo real, pra quem ta perto do servidor." |
| **LED Verde** | "Acende quando a temperatura ta normal, abaixo de 25 graus." |
| **LED Amarelo** | "Acende quando ta em alerta, entre 25 e 35 graus." |
| **LED Vermelho** | "Acende quando ta critico, acima de 35 graus." |
| **Buzzer** | "Dispara um alarme sonoro quando a temperatura ta critica, pra chamar atencao imediata." |

---

## 3. DEMONSTRACAO NO WOKWI (4 minutos)

### Passo a passo da demonstracao:

**Passo 1 - Iniciar simulacao:**
> "Vou iniciar a simulacao. Reparem que o ESP32 conecta no WiFi e mostra o IP no display."

**Passo 2 - Mostrar funcionamento normal:**
> "Com a temperatura em 22 graus, o LED verde ta aceso e o status mostra NORMAL no LCD."

**Passo 3 - Simular alerta (subir para 30C):**
> "Agora vou aumentar a temperatura clicando no sensor... Reparem que o LED amarelo acendeu e o status mudou para ALERTA."

**Passo 4 - Simular critico (subir para 40C):**
> "Subindo mais a temperatura... Agora o LED vermelho acendeu e o buzzer ta tocando. Isso indica que o servidor precisa de atencao imediata."

**Passo 5 - Mostrar pagina web (se possivel):**
> "Alem do monitoramento local, o ESP32 serve uma pagina web. Qualquer pessoa na rede pode acessar pelo navegador e ver a temperatura em tempo real, sem precisar estar perto do servidor."

---

## 4. EXPLICACAO DO CODIGO (2 minutos)

### Pontos principais para mencionar:

> "O codigo esta organizado em funcoes separadas:"

1. **`lerSensor()`** - "Faz a leitura do DHT22 a cada 2 segundos"
2. **`avaliarTemperatura()`** - "Compara com os limites e decide qual LED acender"
3. **`atualizarLCD()`** - "Mostra os dados no display"
4. **`atenderClienteWeb()`** - "Serve a pagina HTML pra monitoramento remoto"

> "Usamos 3 bibliotecas: DHTesp pro sensor, LiquidCrystal_I2C pro display, e WiFi pra conexao de rede."

---

## 5. APLICACAO NO MUNDO REAL (1 minuto)

> "Num cenario real, esse sistema poderia ser expandido com:"
> - "Envio de alertas por email ou Telegram quando a temperatura sobe"
> - "Armazenamento de historico na nuvem usando ThingSpeak ou Firebase"
> - "Controle automatico do ar-condicionado da sala de servidores"
> - "Varios sensores espalhados em diferentes pontos do rack"

---

## 6. CONCLUSAO (1 minuto)

> "Resumindo: nosso projeto resolve o problema de monitoramento de temperatura de servidores de forma simples, usando IoT. O sistema avisa tanto localmente pelos LEDs e buzzer, quanto remotamente pela pagina web. Eh uma solucao de baixo custo que pode prevenir danos serios aos equipamentos."

> "Alguma duvida?"

---

## DICAS PARA A APRESENTACAO

- Deixe o Wokwi ja aberto antes de comecar
- Teste a simulacao antes da apresentacao pra garantir que funciona
- Fale devagar nas partes tecnicas
- Se o professor perguntar sobre o WiFi: "No Wokwi usamos a rede simulada Wokwi-GUEST. Na vida real, configurariamos com a rede do escritorio"
- Se perguntar sobre custo: "Um ESP32 custa em torno de R$30-50, e o DHT22 cerca de R$15-20. O sistema completo sairia por menos de R$100"
- Se perguntar sobre alcance: "Como usa WiFi, funciona em qualquer lugar que tenha rede, inclusive pela internet se configurar um servidor"

---

## PERGUNTAS QUE O PROFESSOR PODE FAZER

| Pergunta | Resposta sugerida |
|----------|-------------------|
| Por que ESP32 e nao Arduino? | "Porque o ESP32 ja tem WiFi integrado, que eh essencial pro monitoramento remoto." |
| Por que DHT22 e nao DHT11? | "O DHT22 tem maior precisao (0.5C vs 2C) e maior faixa de medicao." |
| Como funciona o I2C do LCD? | "I2C usa apenas 2 fios (SDA e SCL) pra comunicacao, economizando pinos do ESP32." |
| E se cair a internet? | "Os alertas locais (LEDs e buzzer) continuam funcionando normalmente, so o acesso remoto fica indisponivel." |
| Qual a frequencia de leitura? | "A cada 2 segundos. Pode ser ajustado no codigo conforme a necessidade." |
| Como seria em producao? | "Usariamos MQTT pra enviar dados a um broker, e um dashboard como Grafana pra visualizacao." |
