/*
 * ============================================================
 *  LEVEL UP - Sistema Inteligente de Monitoramento de Saude
 *  Plataforma: ESP32 + Simulacao Wokwi
 * ============================================================
 *
 *  Tres Pilares:
 *    1. Monitoramento Continuo via Wearables
 *       - Frequencia cardiaca (potenciometro simulando sensor)
 *       - Nivel de atividade fisica (potenciometro simulando acelerometro)
 *       - Temperatura corporal (DHT22)
 *
 *    2. Check-up Digital com Inteligencia Artificial
 *       - Triagem adaptativa com perguntas ponderadas
 *       - Cruzamento de sintomas com sinais vitais
 *       - Geracao de score de risco e relatorio preliminar
 *
 *    3. Gamificacao e Engajamento
 *       - Sistema de pontos por habitos saudaveis
 *       - Niveis e ranks progressivos
 *       - Recompensas por checkups e metas atingidas
 *
 *  Componentes:
 *    - ESP32 DevKit V1
 *    - Display OLED SSD1306 128x64 (I2C)
 *    - Sensor DHT22 (temperatura e umidade)
 *    - 2x Potenciometros (simulam sensores wearable)
 *    - 3x LEDs (verde/amarelo/vermelho) - status de saude
 *    - Buzzer - alarme para situacoes criticas
 *    - 2x Botoes - navegacao e interacao
 *
 *  Autores: Nicolas Araujo, Pedro Ivson, Gabriel Lima
 * ============================================================
 */

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <DHT.h>

/* ======================== PINOS ======================== */
#define HEART_RATE_PIN  34
#define ACTIVITY_PIN    35
#define DHT_PIN         4
#define GREEN_LED       25
#define YELLOW_LED      26
#define RED_LED         27
#define BUZZER_PIN      33
#define BTN_MENU        18
#define BTN_SELECT      19

/* ===================== DISPLAY OLED ==================== */
#define SCREEN_WIDTH  128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

/* ======================== DHT22 ======================== */
#define DHT_TYPE DHT22
DHT dht(DHT_PIN, DHT_TYPE);

/* ==================== ESTRUTURAS ======================= */

struct HealthData {
  int heartRate;
  float temperature;
  float humidity;
  int activityLevel;
  int steps;
  int sleepQuality;
};

struct GameData {
  int points;
  int level;
  int dailyStreak;
  int totalCheckups;
  char rank[20];
};

struct CheckupData {
  int currentQuestion;
  int answers[10];
  int riskScore;
  bool completed;
  bool pointsAwarded;
};

/* ==================== TELAS (ENUM) ===================== */
enum Screen {
  SCREEN_DASHBOARD,
  SCREEN_VITALS,
  SCREEN_CHECKUP,
  SCREEN_GAMIFICATION,
  SCREEN_ALERT,
  SCREEN_COUNT
};

/* ================= VARIAVEIS GLOBAIS =================== */
HealthData health;
GameData game;
CheckupData checkup;
Screen currentScreen = SCREEN_DASHBOARD;

unsigned long lastSensorRead = 0;
unsigned long lastDisplayUpdate = 0;
unsigned long lastPointAward = 0;
unsigned long lastMenuPress = 0;
unsigned long lastSelectPress = 0;

const unsigned long SENSOR_INTERVAL  = 2000;
const unsigned long DISPLAY_INTERVAL = 500;
const unsigned long POINT_INTERVAL   = 30000;
const unsigned long DEBOUNCE_DELAY   = 300;

/* ============= PERGUNTAS DO CHECK-UP =================== */
const char* questions[] = {
  "Dor no peito?",
  "Falta de ar?",
  "Tontura frequente?",
  "Dor de cabeca?",
  "Fadiga excessiva?",
  "Febre recente?",
  "Palpitacoes?",
  "Insonia?"
};
const int weights[] = {20, 15, 10, 5, 8, 12, 18, 7};
const int NUM_QUESTIONS = 8;

/* ======================= SETUP ========================= */
void setup() {
  Serial.begin(115200);
  Serial.println();
  Serial.println("============================================");
  Serial.println("  LEVEL UP - Health Monitoring System");
  Serial.println("  Versao 1.0 | Plataforma ESP32");
  Serial.println("============================================");

  pinMode(GREEN_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(BTN_MENU, INPUT_PULLUP);
  pinMode(BTN_SELECT, INPUT_PULLUP);

  dht.begin();

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("[ERRO] Falha ao inicializar display OLED");
    for (;;);
  }

  showSplashScreen();
  initGameData();
  resetCheckup();

  Serial.println("[OK] Sistema inicializado com sucesso!");
  Serial.println("[INFO] Navegue com BTN_MENU, interaja com BTN_SELECT");
  Serial.println("--------------------------------------------\n");
}

/* ======================= LOOP ========================== */
void loop() {
  unsigned long now = millis();

  if (now - lastSensorRead >= SENSOR_INTERVAL) {
    readSensors();
    evaluateHealth();
    awardPoints(now);
    lastSensorRead = now;
  }

  handleButtons(now);

  if (now - lastDisplayUpdate >= DISPLAY_INTERVAL) {
    updateDisplay();
    lastDisplayUpdate = now;
  }
}

/* ================ TELA DE SPLASH ======================= */
void showSplashScreen() {
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(14, 4);
  display.println("Level UP");
  display.setTextSize(1);
  display.setCursor(12, 28);
  display.println("Health  Monitoring");
  display.setCursor(28, 40);
  display.println("System v1.0");

  display.drawRect(0, 0, 128, 64, SSD1306_WHITE);

  display.setCursor(16, 54);
  display.println("Inicializando...");
  display.display();
  delay(2500);
}

/* ============= INICIALIZACAO GAMIFICACAO ================ */
void initGameData() {
  game.points = 0;
  game.level = 1;
  game.dailyStreak = 0;
  game.totalCheckups = 0;
  strcpy(game.rank, "Iniciante");
}

/* ================ LEITURA DE SENSORES ================== */
void readSensors() {
  int rawHR = analogRead(HEART_RATE_PIN);
  health.heartRate = map(rawHR, 0, 4095, 40, 200);

  int rawActivity = analogRead(ACTIVITY_PIN);
  health.activityLevel = map(rawActivity, 0, 4095, 0, 100);
  health.steps = map(rawActivity, 0, 4095, 0, 15000);

  float t = dht.readTemperature();
  float h = dht.readHumidity();
  if (!isnan(t)) health.temperature = t;
  if (!isnan(h)) health.humidity = h;

  health.sleepQuality = map(health.activityLevel, 0, 100, 95, 15);

  Serial.println("--- Leitura dos Sensores ---");
  Serial.print("  FC: ");
  Serial.print(health.heartRate);
  Serial.print(" BPM | Temp: ");
  Serial.print(health.temperature, 1);
  Serial.print(" C | Umid: ");
  Serial.print(health.humidity, 1);
  Serial.println("%");
  Serial.print("  Atividade: ");
  Serial.print(health.activityLevel);
  Serial.print("% | Passos: ");
  Serial.print(health.steps);
  Serial.print(" | Sono: ");
  Serial.print(health.sleepQuality);
  Serial.println("%");
}

/* ============ AVALIACAO DE SAUDE + LEDS ================ */
void evaluateHealth() {
  int alertLevel = 0;

  if (health.heartRate < 50 || health.heartRate > 160) {
    alertLevel = 2;
  } else if (health.heartRate < 60 || health.heartRate > 100) {
    alertLevel = max(alertLevel, 1);
  }

  if (health.temperature > 39.0 || health.temperature < 34.0) {
    alertLevel = 2;
  } else if (health.temperature > 37.5 || health.temperature < 35.5) {
    alertLevel = max(alertLevel, 1);
  }

  digitalWrite(GREEN_LED, alertLevel == 0 ? HIGH : LOW);
  digitalWrite(YELLOW_LED, alertLevel == 1 ? HIGH : LOW);
  digitalWrite(RED_LED, alertLevel == 2 ? HIGH : LOW);

  if (alertLevel == 2) {
    if ((millis() / 500) % 2 == 0) {
      tone(BUZZER_PIN, 1000);
    } else {
      noTone(BUZZER_PIN);
    }
    if (currentScreen != SCREEN_ALERT) {
      currentScreen = SCREEN_ALERT;
      Serial.println("!!! ALERTA CRITICO ATIVADO !!!");
    }
  } else {
    noTone(BUZZER_PIN);
  }

  const char* statusLabels[] = {"NORMAL", "ATENCAO", "CRITICO"};
  Serial.print("  Status: ");
  Serial.println(statusLabels[alertLevel]);
}

/* ============ SISTEMA DE PONTUACAO ===================== */
void awardPoints(unsigned long now) {
  if (now - lastPointAward < POINT_INTERVAL) return;
  lastPointAward = now;

  int earned = 0;

  if (health.heartRate >= 60 && health.heartRate <= 100) earned += 10;
  if (health.activityLevel > 30) earned += 5;
  if (health.activityLevel > 60) earned += 10;
  if (health.temperature >= 36.0 && health.temperature <= 37.5) earned += 5;
  if (health.sleepQuality > 70) earned += 5;

  game.points += earned;

  int newLevel = (game.points / 100) + 1;
  if (newLevel > game.level) {
    game.level = newLevel;
    updateRank();
    Serial.print("*** LEVEL UP! Nivel ");
    Serial.print(game.level);
    Serial.print(" - ");
    Serial.print(game.rank);
    Serial.println(" ***");
  }

  if (earned > 0) {
    Serial.print("  +");
    Serial.print(earned);
    Serial.print(" pts | Total: ");
    Serial.print(game.points);
    Serial.print(" | Lv.");
    Serial.println(game.level);
  }
}

/* ============ ATUALIZACAO DE RANK ====================== */
void updateRank() {
  if (game.level >= 10)     strcpy(game.rank, "Mestre Saude");
  else if (game.level >= 7) strcpy(game.rank, "Expert Vital");
  else if (game.level >= 5) strcpy(game.rank, "Guerreiro Fit");
  else if (game.level >= 3) strcpy(game.rank, "Aprendiz Ativo");
  else                      strcpy(game.rank, "Iniciante");
}

/* ============ CONTROLE DOS BOTOES ====================== */
void handleButtons(unsigned long now) {
  if (digitalRead(BTN_MENU) == LOW && (now - lastMenuPress > DEBOUNCE_DELAY)) {
    lastMenuPress = now;

    if (currentScreen == SCREEN_CHECKUP && !checkup.completed) {
      advanceCheckup(false);
    } else if (currentScreen == SCREEN_ALERT) {
      currentScreen = SCREEN_DASHBOARD;
      noTone(BUZZER_PIN);
    } else {
      currentScreen = (Screen)((currentScreen + 1) % SCREEN_COUNT);
      if (currentScreen == SCREEN_ALERT) currentScreen = SCREEN_DASHBOARD;
    }
  }

  if (digitalRead(BTN_SELECT) == LOW && (now - lastSelectPress > DEBOUNCE_DELAY)) {
    lastSelectPress = now;

    if (currentScreen == SCREEN_CHECKUP) {
      if (checkup.completed) {
        resetCheckup();
      } else {
        advanceCheckup(true);
      }
    } else if (currentScreen == SCREEN_ALERT) {
      currentScreen = SCREEN_DASHBOARD;
      noTone(BUZZER_PIN);
    }
  }
}

/* ============ ATUALIZACAO DO DISPLAY =================== */
void updateDisplay() {
  display.clearDisplay();

  switch (currentScreen) {
    case SCREEN_DASHBOARD:    drawDashboard();    break;
    case SCREEN_VITALS:       drawVitals();       break;
    case SCREEN_CHECKUP:      drawCheckup();      break;
    case SCREEN_GAMIFICATION: drawGamification(); break;
    case SCREEN_ALERT:        drawAlert();        break;
    default: break;
  }

  display.display();
}

/* ============ TELA: DASHBOARD ========================== */
void drawDashboard() {
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);

  display.setCursor(20, 0);
  display.println("== LEVEL UP ==");
  display.drawFastHLine(0, 9, 128, SSD1306_WHITE);

  display.setCursor(0, 13);
  display.print("BPM: ");
  display.print(health.heartRate);

  display.setCursor(70, 13);
  display.print("T:");
  display.print(health.temperature, 1);
  display.print("C");

  display.setCursor(0, 25);
  display.print("Atividade: ");
  display.print(health.activityLevel);
  display.print("%");
  drawProgressBar(0, 35, 128, 7, health.activityLevel);

  display.setCursor(0, 46);
  display.print("Lv.");
  display.print(game.level);
  display.print(" ");
  display.print(game.rank);

  display.setCursor(0, 56);
  display.print("Pts:");
  display.print(game.points);

  display.setCursor(78, 56);
  display.print("[Menu>]");
}

/* ============ TELA: SINAIS VITAIS ====================== */
void drawVitals() {
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);

  display.setCursor(8, 0);
  display.println("= SINAIS VITAIS =");
  display.drawFastHLine(0, 9, 128, SSD1306_WHITE);

  display.setCursor(0, 13);
  display.print("Freq.Card: ");
  display.print(health.heartRate);
  display.println(" BPM");

  display.setCursor(0, 23);
  display.print("Temperatura: ");
  display.print(health.temperature, 1);
  display.println(" C");

  display.setCursor(0, 33);
  display.print("Umidade: ");
  display.print(health.humidity, 1);
  display.println("%");

  display.setCursor(0, 43);
  display.print("Passos: ");
  display.println(health.steps);

  display.setCursor(0, 53);
  display.print("Qual.Sono: ");
  display.print(health.sleepQuality);
  display.println("%");
}

/* ============ TELA: CHECK-UP DIGITAL =================== */
void drawCheckup() {
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);

  display.setCursor(4, 0);
  display.println("= CHECK-UP DIGITAL =");
  display.drawFastHLine(0, 9, 128, SSD1306_WHITE);

  if (checkup.completed) {
    if (!checkup.pointsAwarded) {
      game.points += 50;
      game.totalCheckups++;
      checkup.pointsAwarded = true;
      Serial.println("[GAMIFICACAO] +50 pts por completar check-up!");
      printMedicalReport();
    }

    display.setCursor(8, 14);
    display.println("Check-up Completo!");

    display.setCursor(0, 26);
    display.print("Score Risco: ");
    display.print(checkup.riskScore);
    display.println("/100");

    drawProgressBar(0, 37, 128, 7, checkup.riskScore);

    display.setCursor(0, 48);
    if (checkup.riskScore < 30) {
      display.println(">> BAIXO RISCO <<");
    } else if (checkup.riskScore < 60) {
      display.println(">> RISCO MODERADO <<");
    } else {
      display.println(">> ALTO RISCO! <<");
    }

    display.setCursor(4, 57);
    display.println("[SEL] Novo Check-up");
  } else {
    display.setCursor(0, 13);
    display.print("Pergunta ");
    display.print(checkup.currentQuestion + 1);
    display.print("/");
    display.println(NUM_QUESTIONS);

    display.setCursor(0, 27);
    display.println(questions[checkup.currentQuestion]);

    display.drawFastHLine(0, 42, 128, SSD1306_WHITE);
    display.setCursor(0, 46);
    display.println("SEL = Sim");
    display.setCursor(0, 56);
    display.println("MENU = Nao");
  }
}

/* ============ TELA: GAMIFICACAO ======================== */
void drawGamification() {
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);

  display.setCursor(12, 0);
  display.println("= GAMIFICACAO =");
  display.drawFastHLine(0, 9, 128, SSD1306_WHITE);

  display.setCursor(0, 13);
  display.print("Nivel: ");
  display.println(game.level);

  display.setCursor(0, 23);
  display.print("Rank: ");
  display.println(game.rank);

  display.setCursor(0, 33);
  display.print("Pontos: ");
  display.println(game.points);

  display.setCursor(0, 43);
  display.print("Checkups: ");
  display.println(game.totalCheckups);

  int progressToNext = game.points % 100;
  display.setCursor(0, 53);
  display.print("Prox.Lv: ");
  display.print(progressToNext);
  display.print("%");
  drawProgressBar(64, 53, 60, 7, progressToNext);
}

/* ============ TELA: ALERTA CRITICO ===================== */
void drawAlert() {
  display.drawRect(0, 0, 128, 64, SSD1306_WHITE);
  display.drawRect(2, 2, 124, 60, SSD1306_WHITE);

  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(16, 6);
  display.println("ALERTA!");

  display.setTextSize(1);

  if (health.heartRate > 160 || health.heartRate < 50) {
    display.setCursor(4, 28);
    display.print("FC Anormal: ");
    display.print(health.heartRate);
    display.println(" BPM");
  }

  if (health.temperature > 39.0 || health.temperature < 34.0) {
    display.setCursor(4, 40);
    display.print("Temp Critica: ");
    display.print(health.temperature, 1);
    display.println("C");
  }

  display.setCursor(8, 52);
  display.println("[OK para confirmar]");
}

/* ============ BARRA DE PROGRESSO ======================= */
void drawProgressBar(int x, int y, int w, int h, int percent) {
  percent = constrain(percent, 0, 100);
  display.drawRect(x, y, w, h, SSD1306_WHITE);
  int fillWidth = ((w - 2) * percent) / 100;
  if (fillWidth > 0) {
    display.fillRect(x + 1, y + 1, fillWidth, h - 2, SSD1306_WHITE);
  }
}

/* ============ AVANCAR CHECK-UP ========================= */
void advanceCheckup(bool answer) {
  checkup.answers[checkup.currentQuestion] = answer ? 1 : 0;

  Serial.print("  [CHECK-UP] ");
  Serial.print(questions[checkup.currentQuestion]);
  Serial.print(" -> ");
  Serial.println(answer ? "SIM" : "NAO");

  checkup.currentQuestion++;

  if (checkup.currentQuestion >= NUM_QUESTIONS) {
    calculateRiskScore();
    checkup.completed = true;
  }
}

/* ============ CALCULO DE RISCO (IA SIMULADA) =========== */
void calculateRiskScore() {
  int score = 0;

  for (int i = 0; i < NUM_QUESTIONS; i++) {
    if (checkup.answers[i]) {
      score += weights[i];
    }
  }

  if (health.heartRate > 100 || health.heartRate < 60) score += 10;
  if (health.temperature > 37.5) score += 10;
  if (health.activityLevel < 20) score += 5;
  if (health.sleepQuality < 40) score += 5;

  checkup.riskScore = constrain(score, 0, 100);
}

/* ============ RESETAR CHECK-UP ========================= */
void resetCheckup() {
  checkup.currentQuestion = 0;
  checkup.completed = false;
  checkup.pointsAwarded = false;
  checkup.riskScore = 0;
  memset(checkup.answers, 0, sizeof(checkup.answers));
}

/* ============ RELATORIO MEDICO SERIAL ================== */
void printMedicalReport() {
  Serial.println();
  Serial.println("================================================");
  Serial.println("   RELATORIO MEDICO PRELIMINAR");
  Serial.println("   Level UP - Check-up Digital com IA");
  Serial.println("================================================");
  Serial.println();
  Serial.println("SINAIS VITAIS COLETADOS:");
  Serial.print("  Frequencia Cardiaca: ");
  Serial.print(health.heartRate);
  Serial.println(" BPM");
  Serial.print("  Temperatura Corporal: ");
  Serial.print(health.temperature, 1);
  Serial.println(" C");
  Serial.print("  Umidade Ambiente: ");
  Serial.print(health.humidity, 1);
  Serial.println("%");
  Serial.print("  Nivel de Atividade: ");
  Serial.print(health.activityLevel);
  Serial.println("%");
  Serial.print("  Passos Estimados: ");
  Serial.println(health.steps);
  Serial.print("  Qualidade do Sono: ");
  Serial.print(health.sleepQuality);
  Serial.println("%");
  Serial.println();
  Serial.println("TRIAGEM - SINTOMAS REPORTADOS:");
  for (int i = 0; i < NUM_QUESTIONS; i++) {
    Serial.print("  ");
    Serial.print(questions[i]);
    Serial.print(" ");
    Serial.println(checkup.answers[i] ? "SIM" : "NAO");
  }
  Serial.println();
  Serial.print("SCORE DE RISCO CALCULADO: ");
  Serial.print(checkup.riskScore);
  Serial.println("/100");
  Serial.println();
  if (checkup.riskScore < 30) {
    Serial.println("CLASSIFICACAO: BAIXO RISCO");
    Serial.println("Recomendacao: Manter habitos saudaveis.");
  } else if (checkup.riskScore < 60) {
    Serial.println("CLASSIFICACAO: RISCO MODERADO");
    Serial.println("Recomendacao: Agendar consulta preventiva.");
  } else {
    Serial.println("CLASSIFICACAO: ALTO RISCO");
    Serial.println("Recomendacao: Consulta medica URGENTE.");
  }
  Serial.println();
  Serial.println("================================================");
  Serial.print("Pontuacao Gamificacao: ");
  Serial.print(game.points);
  Serial.print(" pts | Nivel ");
  Serial.print(game.level);
  Serial.print(" | ");
  Serial.println(game.rank);
  Serial.println("================================================");
  Serial.println();
}
