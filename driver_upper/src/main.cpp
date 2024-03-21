// подключаем библиотеки 
#include <Arduino.h>
#include <GParser.h>
#include <AsyncStream.h>
#include <Config.h>
#include <GyverFilters.h>
#include <LiquidCrystal_I2C.h>

AsyncStream<100> serial(&Serial, '\n');
AsyncStream<100> serial1(&Serial1, '\n');
AsyncStream<100> serial2(&Serial2, '\n');
LiquidCrystal_I2C lcd(0x27,20,4);  // set the LCD address to 0x27 for a 16 chars and 2 line display

uint32_t turnTimer;
int ledState = LOW;

void setup() {
  Serial.begin(BITRATE);

  // подключение сериала для общения с роботом 
  Serial1.setRX(UART_0_RX);
  Serial1.setTX(UART_0_TX);
  Serial1.begin(BITRATE);
  pinMode(UART_COM, OUTPUT);
  digitalWrite(UART_COM, LOW);

  // подключение сериала для общения с постом управления 
  Serial2.setRX(UART_1_RX);
  Serial2.setTX(UART_1_TX);
  Serial2.begin(BITRATE);

  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(19, OUTPUT);

  lcd.init();
  lcd.backlight();
  lcd.setCursor(1,1);
  lcd.print("Hello SoftAcademic");
  delay(1000);
}

void loop() {
  // если данные получены (ретранслятор)
  if (serial2.available()) {     

    digitalWrite(UART_COM, HIGH);
    delay(5);
    Serial1.println(serial2.buf);  
    Serial.println(serial2.buf);
    delay(5);
    digitalWrite(UART_COM, LOW);  

  }

  if (serial1.available()) {     
    // GParser data = GParser(serial1.buf, ' ');
    Serial.println(serial1.buf); 
    lcd.setCursor(0,1);
    lcd.print(serial1.buf);
    // lcd.print(" ");
    // lcd.print(data[1]);
    // lcd.print(" ");
    // lcd.print(data[2]);
    
    lcd.setCursor(0,2);
    lcd.print(" ");
    lcd.setCursor(0,3);
    lcd.print(" ");
  }

  // мигалка для индикации работы 
  if (millis()- turnTimer >= 500){
    turnTimer = millis();

    if (ledState == LOW) ledState = HIGH;
    else ledState = LOW;

    digitalWrite(LED_BUILTIN, ledState);
   }
}


void loop1(){

  
}