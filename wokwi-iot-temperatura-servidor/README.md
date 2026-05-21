# Sistema de Monitoramento de Temperatura de Servidor - IoT

## Tema 5: Monitoramento remoto de temperatura de servidor com IoT

**FIAP - Trabalho IoT**

---

## Descricao do Projeto

Este projeto simula um sistema de monitoramento remoto de temperatura de um servidor (computador) utilizando IoT. O sistema monitora continuamente a temperatura do ambiente do servidor e alerta o administrador quando a temperatura atinge niveis criticos.

### Problema
Servidores precisam operar em temperaturas controladas (idealmente entre 18C e 27C). Temperaturas elevadas podem causar:
- Travamentos e instabilidade
- Reducao da vida util dos componentes
- Perda de dados
- Desligamento forcado

### Solucao
Sistema IoT que monitora a temperatura em tempo real e:
- Exibe os dados em um display LCD local
- Indica o status por LEDs coloridos (verde/amarelo/vermelho)
- Emite alarme sonoro em situacoes criticas
- Disponibiliza os dados via pagina web (acesso remoto)

---

## Componentes Utilizados

| Componente | Funcao |
|-----------|--------|
| ESP32 DevKit V1 | Microcontrolador com WiFi |
| DHT22 | Sensor de temperatura e umidade |
| LCD 16x2 (I2C) | Display para exibir dados localmente |
| LED Verde | Indica temperatura normal |
| LED Amarelo | Indica alerta de temperatura |
| LED Vermelho | Indica temperatura critica |
| Buzzer | Alarme sonoro para situacoes criticas |
| Resistores 220ohm (x3) | Protecao dos LEDs |

---

## Faixas de Temperatura

| Faixa | Status | Indicador |
|-------|--------|-----------|
| Ate 25C | NORMAL | LED Verde aceso |
| 25C - 35C | ALERTA | LED Amarelo aceso |
| Acima de 35C | CRITICO | LED Vermelho + Buzzer |

---

## Como Simular no Wokwi

1. Acesse [https://wokwi.com](https://wokwi.com)
2. Crie um novo projeto ESP32
3. Copie o conteudo de `sketch.ino` para o editor de codigo
4. Copie o conteudo de `diagram.json` para o editor de diagrama (aba "diagram.json")
5. Clique em "Play" para iniciar a simulacao
6. No sensor DHT22, clique nele para alterar a temperatura manualmente e testar os alertas

### Ou use o link direto:
- Importe o projeto pelo Wokwi usando os arquivos deste repositorio

---

## Funcionamento

1. O ESP32 inicializa e conecta ao WiFi
2. A cada 2 segundos, le a temperatura e umidade do DHT22
3. Avalia a temperatura e atualiza os indicadores:
   - **LED Verde**: Tudo OK, temperatura segura
   - **LED Amarelo**: Atencao, temperatura subindo
   - **LED Vermelho + Buzzer**: Critico! Acao necessaria
4. Exibe os dados no LCD local
5. Serve uma pagina web com os dados em tempo real

---

## Estrutura dos Arquivos

```
wokwi-iot-temperatura-servidor/
├── sketch.ino        # Codigo fonte do ESP32
├── diagram.json      # Diagrama do circuito para o Wokwi
├── wokwi.toml        # Configuracao do projeto Wokwi
└── README.md         # Este arquivo
```

---

## Tecnologias

- **Plataforma**: ESP32
- **Linguagem**: C/C++ (Arduino Framework)
- **Comunicacao**: WiFi (HTTP Server)
- **Protocolo**: HTTP (pagina web para monitoramento remoto)
- **Simulador**: Wokwi

---

## Bibliotecas Utilizadas

- `DHTesp` - Leitura do sensor DHT22
- `LiquidCrystal_I2C` - Controle do display LCD via I2C
- `WiFi` - Conexao WiFi do ESP32

---

## Aplicacao no Mundo Real

Em um cenario real, este sistema poderia ser expandido com:
- Envio de alertas por email/SMS/Telegram
- Armazenamento de dados em nuvem (ThingSpeak, Firebase)
- Dashboard com historico de temperaturas
- Controle automatico do ar-condicionado da sala de servidores
- Multiplos sensores em diferentes pontos do rack

---

## Autor

**Gabriel Lima** - FIAP 2025
