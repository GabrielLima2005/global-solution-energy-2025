// ============================================================
// Sistema de Monitoramento de Temperatura de Servidor - IoT
// FIAP - Trabalho IoT (Tema 5)
// Plataforma: ESP32 + DHT22 + LCD I2C + LEDs + Buzzer
// Simulador: Wokwi (https://wokwi.com)
// ============================================================

#include <DHTesp.h>
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>

// === Pinos ===
#define DHT_PIN       15    // Sensor DHT22
#define LED_VERDE     2     // LED verde - temperatura OK
#define LED_AMARELO   4     // LED amarelo - alerta
#define LED_VERMELHO  5     // LED vermelho - critico
#define BUZZER_PIN    18    // Buzzer para alarme

// === Limites de temperatura (graus Celsius) ===
#define TEMP_NORMAL_MAX   25.0  // Ate 25C = normal
#define TEMP_ALERTA_MAX   35.0  // 25C - 35C = alerta
// Acima de 35C = critico

// === Objetos ===
DHTesp dht;
LiquidCrystal_I2C lcd(0x27, 16, 2);  // LCD 16x2 endereco I2C 0x27

// === WiFi (simulado no Wokwi) ===
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// === Variaveis ===
float temperatura = 0;
float umidade = 0;
String status_servidor = "";
unsigned long ultimaLeitura = 0;
const long intervaloLeitura = 2000;  // Leitura a cada 2 segundos

// === Servidor Web ===
WiFiServer server(80);

void setup() {
  Serial.begin(115200);
  Serial.println("=== Monitor de Temperatura de Servidor ===");
  Serial.println("Inicializando...");

  // Configurar pinos
  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_AMARELO, OUTPUT);
  pinMode(LED_VERMELHO, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  // Inicializar DHT22
  dht.setup(DHT_PIN, DHTesp::DHT22);
  Serial.println("[OK] Sensor DHT22 inicializado");

  // Inicializar LCD
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Monitor Servidor");
  lcd.setCursor(0, 1);
  lcd.print("Iniciando...");
  Serial.println("[OK] LCD inicializado");

  // Conectar WiFi
  WiFi.begin(ssid, password);
  Serial.print("Conectando WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("[OK] WiFi conectado - IP: ");
  Serial.println(WiFi.localIP());

  // Iniciar servidor web
  server.begin();
  Serial.println("[OK] Servidor web iniciado na porta 80");

  // Mostrar IP no LCD
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("IP:");
  lcd.setCursor(0, 1);
  lcd.print(WiFi.localIP());
  delay(3000);

  Serial.println("=== Sistema pronto! ===\n");
}

void loop() {
  unsigned long agora = millis();

  // Leitura periodica do sensor
  if (agora - ultimaLeitura >= intervaloLeitura) {
    ultimaLeitura = agora;
    lerSensor();
    avaliarTemperatura();
    atualizarLCD();
    imprimirSerial();
  }

  // Atender clientes web
  atenderClienteWeb();
}

void lerSensor() {
  TempAndHumidity dados = dht.getTempAndHumidity();

  if (dht.getStatus() != 0) {
    Serial.println("[ERRO] Falha na leitura do sensor!");
    return;
  }

  temperatura = dados.temperature;
  umidade = dados.humidity;
}

void avaliarTemperatura() {
  if (temperatura <= TEMP_NORMAL_MAX) {
    // NORMAL - temperatura segura
    status_servidor = "NORMAL";
    digitalWrite(LED_VERDE, HIGH);
    digitalWrite(LED_AMARELO, LOW);
    digitalWrite(LED_VERMELHO, LOW);
    noTone(BUZZER_PIN);

  } else if (temperatura <= TEMP_ALERTA_MAX) {
    // ALERTA - temperatura elevada
    status_servidor = "ALERTA";
    digitalWrite(LED_VERDE, LOW);
    digitalWrite(LED_AMARELO, HIGH);
    digitalWrite(LED_VERMELHO, LOW);
    noTone(BUZZER_PIN);

  } else {
    // CRITICO - temperatura perigosa
    status_servidor = "CRITICO!";
    digitalWrite(LED_VERDE, LOW);
    digitalWrite(LED_AMARELO, LOW);
    digitalWrite(LED_VERMELHO, HIGH);
    tone(BUZZER_PIN, 1000);  // Alarme sonoro
  }
}

void atualizarLCD() {
  lcd.clear();

  // Linha 1: Temperatura e Umidade
  lcd.setCursor(0, 0);
  lcd.print("T:");
  lcd.print(temperatura, 1);
  lcd.print("C ");
  lcd.print("U:");
  lcd.print(umidade, 0);
  lcd.print("%");

  // Linha 2: Status
  lcd.setCursor(0, 1);
  lcd.print("Status: ");
  lcd.print(status_servidor);
}

void imprimirSerial() {
  Serial.print("Temp: ");
  Serial.print(temperatura, 1);
  Serial.print(" C | Umid: ");
  Serial.print(umidade, 0);
  Serial.print("% | Status: ");
  Serial.println(status_servidor);
}

void atenderClienteWeb() {
  WiFiClient client = server.available();
  if (!client) return;

  String request = client.readStringUntil('\r');
  client.flush();

  // Resposta HTML
  String html = "<!DOCTYPE html><html><head>";
  html += "<meta charset='UTF-8'>";
  html += "<meta http-equiv='refresh' content='5'>";
  html += "<title>Monitor de Temperatura - Servidor</title>";
  html += "<style>";
  html += "body{font-family:Arial;text-align:center;padding:20px;background:#1a1a2e;color:white;}";
  html += ".card{background:#16213e;border-radius:15px;padding:30px;margin:20px auto;max-width:400px;}";
  html += ".temp{font-size:48px;font-weight:bold;}";
  html += ".normal{color:#00ff88;} .alerta{color:#ffaa00;} .critico{color:#ff3333;}";
  html += "h1{color:#4fc3f7;}";
  html += "</style></head><body>";
  html += "<h1>Monitor de Temperatura do Servidor</h1>";
  html += "<div class='card'>";
  html += "<p class='temp'>" + String(temperatura, 1) + " &deg;C</p>";
  html += "<p>Umidade: " + String(umidade, 0) + "%</p>";

  // Cor do status baseada na condicao
  String corStatus = "normal";
  if (status_servidor == "ALERTA") corStatus = "alerta";
  else if (status_servidor == "CRITICO!") corStatus = "critico";

  html += "<p class='" + corStatus + "' style='font-size:24px;font-weight:bold;'>";
  html += status_servidor + "</p>";
  html += "</div>";
  html += "<p>Atualiza automaticamente a cada 5 segundos</p>";
  html += "<p><small>FIAP - IoT - Monitoramento de Servidor</small></p>";
  html += "</body></html>";

  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html; charset=utf-8");
  client.println("Connection: close");
  client.println();
  client.println(html);
  client.stop();
}
