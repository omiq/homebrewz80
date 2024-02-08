
#include <LCD-I2C.h>
#define IOREQ 2
#define CLOCK 12

int data_pins[8] = { 4, 5, 6, 7, 8, 9, 10, 11 };
LCD_I2C lcd(0x27, 16, 2);  // Default address of most PCF8574 modules, change according

char read_data() {
  char data = 0b00000000;
  data |= (digitalRead(4) << (0));
  data |= (digitalRead(5) << (1));
  data |= (digitalRead(6) << (2));
  data |= (digitalRead(7) << (3));
  data |= (digitalRead(8) << (4));
  data |= (digitalRead(9) << (5));
  data |= (digitalRead(10) << (6));
  data |= (digitalRead(11) << (7));

  return data;
}

void output_lcd() 
{
  char data;
  char buffer[32];
  delay(10);
  data = read_data();
  sprintf(buffer, "%c", data);
  lcd.print(buffer);

  while(digitalRead(IOREQ) == 0)
  {
      digitalWrite(LED_BUILTIN, 0);
  }

  digitalWrite(LED_BUILTIN, 1);
}

void setup() {

  // Init the LCD
  lcd.begin();
  lcd.display();
  lcd.backlight();
  pinMode(LED_BUILTIN, OUTPUT);
  
  // Pins
  for (int p = 0; p < 8; p++) {
    pinMode(p, INPUT);
  }

  // This will fire our IRQ handler any time the pin goes low
  pinMode(IOREQ, INPUT);

  // Sync with the clock
  pinMode(CLOCK, INPUT);

  // Wanted to do this but it didn't work  
  // attachInterrupt(0, output_lcd, FALLING);

  // Clear the screen and output message
  lcd.clear();
  lcd.print("Z80 Started");
  lcd.setCursor(0, 1);
  lcd.print("Waiting ...");
  digitalWrite(LED_BUILTIN, 0);
  delay(500);
  lcd.clear();
}


void loop() {

  if (digitalRead(CLOCK) == 1)
  {

    while(digitalRead(CLOCK) == 1) {}
    

    if(digitalRead(IOREQ) == 0) 
    {
      output_lcd(); 
    } 
    
   
  }
}
