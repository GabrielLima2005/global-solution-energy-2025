/*
 * ============================================================
 *  LEVEL UP - Sistema Inteligente de Monitoramento de Saude
 *  Plataforma: ESP32 + Simulacao Wokwi
 *  Versao 2.0 - Com Relogio, WiFi e Dashboard Web
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
 *  Novidades v2.0:
 *    - Relogio em tempo real (software clock)
 *    - WiFi Access Point integrado
 *    - Web Server com Dashboard HTML responsivo
 *    - API REST para dados de saude (/api/data)
 *    - Endpoint para ajustar relogio (/api/settime?h=HH&m=MM)
 *    - Nova tela de relogio no OLED
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
#include <WiFi.h>
#include <WebServer.h>

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

/* ===================== WIFI + WEB ====================== */
const char* ap_ssid = "LevelUP-Health";
const char* ap_pass = "levelup123";
WebServer server(80);

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
  SCREEN_CLOCK,
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
int currentAlertLevel = 0;

unsigned long lastSensorRead = 0;
unsigned long lastDisplayUpdate = 0;
unsigned long lastPointAward = 0;
unsigned long lastMenuPress = 0;
unsigned long lastSelectPress = 0;

const unsigned long SENSOR_INTERVAL  = 2000;
const unsigned long DISPLAY_INTERVAL = 500;
const unsigned long POINT_INTERVAL   = 30000;
const unsigned long DEBOUNCE_DELAY   = 300;

/* ================== RELOGIO SOFTWARE =================== */
int clockH = 12;
int clockM = 0;
int clockS = 0;
unsigned long lastClockTick = 0;

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

/* ============= PAGINA HTML (PROGMEM) =================== */
const char PAGE_HTML[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Level UP - Health Dashboard</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',Tahoma,sans-serif;background:#0f0f1a;color:#e0e0e0;min-height:100vh}
.hdr{text-align:center;padding:18px;background:linear-gradient(135deg,#1a1a3e,#16213e);border-bottom:2px solid #00ff88}
.hdr h1{color:#00ff88;font-size:1.8em;letter-spacing:2px}
.hdr p{color:#888;font-size:0.85em;margin-top:4px}
.clk-box{text-align:center;padding:24px 10px;background:#111128}
.clk{font-size:4.5em;font-weight:700;color:#00ff88;font-family:'Courier New',monospace;text-shadow:0 0 20px rgba(0,255,136,0.3)}
.clk-lbl{color:#666;font-size:0.85em;margin-top:4px}
.st-bar{text-align:center;padding:10px;font-weight:700;font-size:1em;letter-spacing:1px}
.st-ok{background:#1b5e20;color:#a5d6a7}
.st-warn{background:#e65100;color:#ffe0b2}
.st-crit{background:#b71c1c;color:#ffcdd2;animation:pulse 1s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.6}}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;padding:18px;max-width:960px;margin:0 auto}
.card{background:#16213e;border-radius:12px;padding:18px;border-left:4px solid;transition:transform 0.2s}
.card:hover{transform:translateY(-2px)}
.card h3{font-size:0.75em;text-transform:uppercase;letter-spacing:1px;opacity:0.6;margin-bottom:8px}
.card .v{font-size:2.2em;font-weight:700}
.card .u{font-size:0.65em;opacity:0.5;margin-left:3px}
.c-hr{border-color:#ff6b6b}.c-hr .v{color:#ff6b6b}
.c-tp{border-color:#ffd93d}.c-tp .v{color:#ffd93d}
.c-ac{border-color:#6bcb77}.c-ac .v{color:#6bcb77}
.c-sl{border-color:#4d96ff}.c-sl .v{color:#4d96ff}
.c-st{border-color:#cc65fe}.c-st .v{color:#cc65fe}
.c-gm{border-color:#ff6b9d}.c-gm .v{color:#ff6b9d}
.bar{height:7px;background:#1a1a3e;border-radius:4px;margin-top:10px;overflow:hidden}
.bf{height:100%;border-radius:4px;transition:width 0.5s ease}
.bg .bf{background:linear-gradient(90deg,#00ff88,#00cc6a)}
.bb .bf{background:linear-gradient(90deg,#4d96ff,#2979ff)}
.bp .bf{background:linear-gradient(90deg,#ff6b9d,#ff4081)}
.badge{display:inline-block;background:#2a2a5e;padding:3px 10px;border-radius:16px;font-size:0.8em;margin-top:6px;color:#ff6b9d}
.ft{text-align:center;padding:14px;color:#444;font-size:0.75em;border-top:1px solid #1a1a3e;margin-top:16px}
.tf{text-align:center;padding:10px;background:#111128}
.tf input{width:50px;padding:4px;background:#1a1a3e;color:#00ff88;border:1px solid #333;border-radius:4px;text-align:center;font-size:1em}
.tf button{padding:5px 16px;background:#00ff88;color:#0f0f1a;border:none;border-radius:4px;cursor:pointer;font-weight:700;margin-left:8px}
.tf button:hover{background:#00cc6a}
</style>
</head>
<body>
<div class="hdr">
<h1>LEVEL UP</h1>
<p>Health Monitoring System v2.0</p>
</div>
<div class="clk-box">
<div class="clk" id="clk">--:--:--</div>
<div class="clk-lbl">Relogio em Tempo Real</div>
</div>
<div class="tf">
<label>Ajustar: </label>
<input type="number" id="sh" min="0" max="23" placeholder="HH">
<span style="color:#666">:</span>
<input type="number" id="sm" min="0" max="59" placeholder="MM">
<button onclick="setT()">OK</button>
</div>
<div class="st-bar st-ok" id="st">Conectando...</div>
<div class="grid">
<div class="card c-hr">
<h3>Frequencia Cardiaca</h3>
<div><span class="v" id="bpm">--</span><span class="u">BPM</span></div>
</div>
<div class="card c-tp">
<h3>Temperatura</h3>
<div><span class="v" id="tmp">--</span><span class="u">&deg;C</span></div>
</div>
<div class="card c-ac">
<h3>Atividade Fisica</h3>
<div><span class="v" id="act">--</span><span class="u">%</span></div>
<div class="bar bg"><div class="bf" id="ab" style="width:0%"></div></div>
</div>
<div class="card c-sl">
<h3>Qualidade do Sono</h3>
<div><span class="v" id="slp">--</span><span class="u">%</span></div>
<div class="bar bb"><div class="bf" id="sb" style="width:0%"></div></div>
</div>
<div class="card c-st">
<h3>Passos</h3>
<div><span class="v" id="stp">--</span></div>
</div>
<div class="card c-gm">
<h3>Gamificacao</h3>
<div><span class="v" id="lv">--</span></div>
<div class="badge" id="rk">--</div>
<div style="margin-top:8px;font-size:0.85em">Pontos: <strong id="pt">0</strong></div>
<div style="font-size:0.8em;color:#888;margin-top:3px">Checkups: <span id="ck">0</span></div>
<div class="bar bp"><div class="bf" id="lb" style="width:0%"></div></div>
</div>
</div>
<div class="ft">Level UP - ESP32 Health Monitor - WiFi Dashboard</div>
<script>
function u(){
fetch('/api/data').then(function(r){return r.json()}).then(function(d){
document.getElementById('clk').textContent=d.time;
document.getElementById('bpm').textContent=d.bpm;
document.getElementById('tmp').textContent=d.temp;
document.getElementById('act').textContent=d.activity;
document.getElementById('ab').style.width=d.activity+'%';
document.getElementById('slp').textContent=d.sleep;
document.getElementById('sb').style.width=d.sleep+'%';
document.getElementById('stp').textContent=d.steps;
document.getElementById('lv').textContent='Nivel '+d.level;
document.getElementById('rk').textContent=d.rank;
document.getElementById('pt').textContent=d.points;
document.getElementById('ck').textContent=d.checkups;
document.getElementById('lb').style.width=(d.points%100)+'%';
var s=document.getElementById('st');
if(d.alert===2){s.className='st-bar st-crit';s.textContent='ALERTA CRITICO - SINAIS ANORMAIS';}
else if(d.alert===1){s.className='st-bar st-warn';s.textContent='ATENCAO - VALORES FORA DO NORMAL';}
else{s.className='st-bar st-ok';s.textContent='NORMAL - SINAIS VITAIS ESTAVEIS';}
}).catch(function(){});}
function setT(){
var h=document.getElementById('sh').value;
var m=document.getElementById('sm').value;
if(h!==''&&m!=='')fetch('/api/settime?h='+h+'&m='+m).then(function(){u();});
}
setInterval(u,2000);u();
</script>
</body>
</html>
)rawliteral";

/* ======================= SETUP ========================= */
void setup() {
  Serial.begin(115200);
  Serial.println();
  Serial.println("============================================");
  Serial.println("  LEVEL UP - Health Monitoring System");
  Serial.println("  Versao 2.0 | ESP32 + WiFi + Dashboard");
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
  setupWiFi();
  setupWebServer();

  Serial.println("[OK] Sistema inicializado com sucesso!");
  Serial.println("[INFO] Navegue com BTN_MENU, interaja com BTN_SELECT");
  Serial.print("[WIFI] Dashboard: http://");
  Serial.println(WiFi.softAPIP());
  Serial.println("--------------------------------------------\n");
}

/* ======================= LOOP ========================== */
void loop() {
  unsigned long now = millis();

  updateClock();
  server.handleClient();

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

/* ================ CONFIGURACAO WIFI ==================== */
void setupWiFi() {
  Serial.print("[WIFI] Criando Access Point: ");
  Serial.println(ap_ssid);
  WiFi.softAP(ap_ssid, ap_pass);
  Serial.print("[WIFI] IP do AP: ");
  Serial.println(WiFi.softAPIP());
}

/* ============= CONFIGURACAO WEB SERVER ================= */
void setupWebServer() {
  server.on("/", handleRoot);
  server.on("/api/data", handleApiData);
  server.on("/api/settime", handleSetTime);
  server.begin();
  Serial.println("[WEB] Servidor HTTP iniciado na porta 80");
}

/* ============= HANDLER: PAGINA PRINCIPAL =============== */
void handleRoot() {
  server.send_P(200, "text/html", PAGE_HTML);
}

/* ============= HANDLER: API DE DADOS =================== */
void handleApiData() {
  char timeStr[9];
  sprintf(timeStr, "%02d:%02d:%02d", clockH, clockM, clockS);

  String json = "{";
  json += "\"time\":\"";
  json += timeStr;
  json += "\",\"bpm\":";
  json += String(health.heartRate);
  json += ",\"temp\":";
  json += String(health.temperature, 1);
  json += ",\"humidity\":";
  json += String(health.humidity, 1);
  json += ",\"activity\":";
  json += String(health.activityLevel);
  json += ",\"steps\":";
  json += String(health.steps);
  json += ",\"sleep\":";
  json += String(health.sleepQuality);
  json += ",\"level\":";
  json += String(game.level);
  json += ",\"rank\":\"";
  json += String(game.rank);
  json += "\",\"points\":";
  json += String(game.points);
  json += ",\"checkups\":";
  json += String(game.totalCheckups);
  json += ",\"alert\":";
  json += String(currentAlertLevel);
  json += ",\"risk\":";
  json += String(checkup.riskScore);
  json += "}";

  server.send(200, "application/json", json);
}

/* ============= HANDLER: AJUSTAR RELOGIO ================ */
void handleSetTime() {
  if (server.hasArg("h") && server.hasArg("m")) {
    clockH = server.arg("h").toInt() % 24;
    clockM = server.arg("m").toInt() % 60;
    clockS = 0;
    Serial.print("[RELOGIO] Horario ajustado: ");
    char buf[9];
    sprintf(buf, "%02d:%02d:%02d", clockH, clockM, clockS);
    Serial.println(buf);
    server.send(200, "application/json", "{\"ok\":true}");
  } else {
    server.send(400, "application/json", "{\"error\":\"Envie ?h=HH&m=MM\"}");
  }
}

/* ================ RELOGIO SOFTWARE ===================== */
void updateClock() {
  if (millis() - lastClockTick >= 1000) {
    lastClockTick = millis();
    clockS++;
    if (clockS >= 60) {
      clockS = 0;
      clockM++;
    }
    if (clockM >= 60) {
      clockM = 0;
      clockH++;
    }
    if (clockH >= 24) {
      clockH = 0;
    }
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
  display.setCursor(20, 40);
  display.println("System v2.0");

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
  currentAlertLevel = 0;

  if (health.heartRate < 50 || health.heartRate > 160) {
    currentAlertLevel = 2;
  } else if (health.heartRate < 60 || health.heartRate > 100) {
    currentAlertLevel = max(currentAlertLevel, 1);
  }

  if (health.temperature > 39.0 || health.temperature < 34.0) {
    currentAlertLevel = 2;
  } else if (health.temperature > 37.5 || health.temperature < 35.5) {
    currentAlertLevel = max(currentAlertLevel, 1);
  }

  digitalWrite(GREEN_LED, currentAlertLevel == 0 ? HIGH : LOW);
  digitalWrite(YELLOW_LED, currentAlertLevel == 1 ? HIGH : LOW);
  digitalWrite(RED_LED, currentAlertLevel == 2 ? HIGH : LOW);

  if (currentAlertLevel == 2) {
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
  Serial.println(statusLabels[currentAlertLevel]);
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
    case SCREEN_CLOCK:        drawClockScreen();  break;
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

  char timeStr[6];
  sprintf(timeStr, "%02d:%02d", clockH, clockM);
  display.setCursor(0, 0);
  display.print(timeStr);

  display.setCursor(40, 0);
  display.print("LEVEL UP");

  display.setCursor(104, 0);
  display.print("Lv");
  display.print(game.level);
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
  display.print(game.rank);

  display.setCursor(0, 56);
  display.print("Pts:");
  display.print(game.points);

  display.setCursor(78, 56);
  display.print("[Menu>]");
}

/* ============ TELA: RELOGIO ============================ */
void drawClockScreen() {
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);

  display.setCursor(28, 0);
  display.println("= RELOGIO =");
  display.drawFastHLine(0, 9, 128, SSD1306_WHITE);

  display.setTextSize(3);
  char hm[6];
  sprintf(hm, "%02d:%02d", clockH, clockM);
  display.setCursor(4, 16);
  display.print(hm);

  display.setTextSize(2);
  char sec[3];
  sprintf(sec, "%02d", clockS);
  display.setCursor(100, 20);
  display.print(sec);

  display.setTextSize(1);
  display.drawFastHLine(0, 42, 128, SSD1306_WHITE);

  display.setCursor(0, 46);
  display.print("WiFi: ");
  display.println(ap_ssid);

  display.setCursor(0, 56);
  display.print("IP: ");
  display.print(WiFi.softAPIP());
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
