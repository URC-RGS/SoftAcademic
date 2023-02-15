#include "Arduino.h"
#include <Wire.h>
#include "MS5837.h"
#include <Adafruit_NeoPixel.h>


struct OutData_MS5837
{
    float dept;
    float term;
};

class TNPA_Neopix 
/* Класс описывающий взаимодействие с отладочными адресными светодиодами */
{
  private:
    int pin_neopix, // пин для подключения адресной светодиодной ленты 
        output_power, // мощность светодиодов 
        number_led; // колли
  
  public:
    TNPA_Neopix (int neo_pin_neopix, int neo_output_power, int neo_number_led){
        setConfig(neo_pin_neopix, neo_output_power, neo_number_led);
      }
    
    void setConfig(int neo_pin_neopix, int neo_output_power, int neo_number_led)
    {
        pin_neopix = neo_pin_neopix;
        output_power = neo_output_power;
        number_led = neo_number_led;
        Adafruit_NeoPixel pixels(number_led, pin_neopix);
        pixels.clear();

        for(int i=0; i<number_led; i++) { 

          pixels.setPixelColor(i, pixels.Color(0, 0, 255));

          pixels.show();  

          delay(200);
        }
  
        for(int i=0; i<number_led; i++) { 

          pixels.setPixelColor(i, pixels.Color(0, 255, 0));

          pixels.show();  

          delay(200);
        }

        for(int i=0; i<number_led; i++) { 

          pixels.setPixelColor(i, pixels.Color(255, 0, 0));

          pixels.show();  

          delay(200);
        }

        for(int i=0; i<number_led; i++) { 

          pixels.setPixelColor(i, pixels.Color(0, 0, 255)); 

        }

        pixels.show();  
        delay(500);

        for(int i=0; i<number_led; i++) { 

          pixels.setPixelColor(i, pixels.Color(0, 255, 0)); 

        }
        pixels.show();  
        delay(500);

        for(int i=0; i<number_led; i++) { 

          pixels.setPixelColor(i, pixels.Color(255, 0, 0)); 

        }
        pixels.show();  
        delay(500);

        for(int i=0; i<number_led; i++) { 

          pixels.setPixelColor(i, pixels.Color(0, 0, 0)); 

        }
        pixels.show();  
        

    }

    void show_debag_motor(int data[6])
    {
      // TODO доделать вфвод на светодиодную ленту 
      Serial.print("motor_0 - ");
      Serial.println(data[0]);

      Serial.print("motor_1 - ");
      Serial.println(data[1]);

      Serial.print("motor_2 - ");
      Serial.println(data[2]);

      Serial.print("motor_3 - ");
      Serial.println(data[3]);

      Serial.print("motor_4 - ");
      Serial.println(data[4]);
      
      Serial.print("motor_5 - ");
      Serial.println(data[5]);

    }
};

class TNPA_Depth_and_term
{   
    private:
        MS5837 sensor;
        float defolt_depth;

    public:
        TNPA_Depth_and_term()
        {
            setConfig();
        }

        void setConfig() 
        {
            Wire.begin();

            while (!sensor.init()) 
            {
                Serial.println("Init failed!");
                Serial.println("Are SDA/SCL connected correctly?");
                Serial.println("Blue Robotics Bar30: White=SDA, Green=SCL");
                Serial.println("\n\n\n");
                delay(5000);
            }

            sensor.setModel(MS5837::MS5837_30BA);
            sensor.setFluidDensity(997);
            sensor.read();
            defolt_depth = sensor.depth();
        }
            

        OutData_MS5837 reqiest()
        {
            OutData_MS5837 OutData;
            sensor.read();
            OutData.dept = abs(sensor.depth() - defolt_depth);
            OutData.term = sensor.temperature();
            return OutData;
        }
};

void setup() {
  // put your setup code here, to run once:
  TNPA_Neopix neo(23,100,1);
}


void loop()
{
  
}