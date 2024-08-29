//#include <Servo.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2);

//Servo servo;
#define red A0
#define green A1

char received = 0; 

void setup()
{
    Serial.begin(9600);
  pinMode(green, OUTPUT);
  pinMode(red, OUTPUT);
    lcd.init();
  lcd.backlight();
  lcd.setCursor(0,0);
lcd.print("  Welcome   "); 
 lcd.setCursor(0,1);
lcd.print("No.Plate detector  ");
  //servo.attach(9);
  delay(2000);
  lcd.clear();
 
}

void loop()
{ 
if (Serial.available() > 0)
    {
        received = Serial.read();
        Serial.println(received);
        delay(1000);
        if (received == '1')
        {  
            Serial.println("authorised vehicle");  
                lcd.setCursor(0,0);
              lcd.print("authorised vehicle");          
            digitalWrite(red,LOW);
            digitalWrite(green,HIGH);
           // servo.write(90);
        }
      else if(received == '2')
        {
            Serial.println("Un-authorised vehicle"); 
                lcd.setCursor(0,0);
              lcd.print("Un-authorised vehicle"); 
            digitalWrite(red,HIGH);
            digitalWrite(green,LOW);
             //servo.write(0);
        }
        else
        {
            Serial.println("No vehicle");
            lcd.setCursor(0,0);
              lcd.print("No vehicle");  
            digitalWrite(red,LOW);
            digitalWrite(green,LOW);
             //servo.write(180);
          }
  }
}

 
