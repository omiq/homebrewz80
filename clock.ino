#define AUTO  A0
#define CLOCKLED 5
#define BUTTON_PIN 7

// Initialize the speed to OFF
int speed = 0;
int oldSpeed = 0;
int steps = 0;

void sleep(int sleep_time)
{
  long start_time = millis();

  while(millis() < start_time + sleep_time)
  {
    // do nothing
  }
}

// Tick the clock
void toggle_clock()
{
  digitalWrite(CLOCKLED, HIGH);
  sleep(10);
  digitalWrite(CLOCKLED, LOW);
  sleep(10);
}

// Single increment of the clock
void single_step()
{
  toggle_clock();
  Serial.print("STEP ");
  Serial.println(steps);
  steps++;
  sleep(500);
}


void setup() {

  // set up the pins and the event listeners
  pinMode(CLOCKLED, OUTPUT);  
  pinMode(BUTTON_PIN, INPUT);
  pinMode(AUTO, INPUT);

  // initialize serial communication 
  Serial.begin(115200);

  // Output the status of the buttons/switches
  Serial.print("POT: ");
  Serial.println(analogRead(AUTO));

  Serial.print("STEP: ");
  Serial.println(digitalRead(BUTTON_PIN));

}

void loop()
{

  // What is the pot set to?
  speed = analogRead(AUTO);
  
  if(abs(speed-oldSpeed)>30) {

    oldSpeed = speed;

    if(speed > 1000) 
    {
      // Manual stepping listener
      Serial.println("AUTO OFF");

    }
    else
    {
      // Set the speed to the trim pot
      Serial.print("POT: ");
      Serial.println(speed);
    }

  }
  else
  {
      sleep(10);

      if(speed > 1000) {
        if(digitalRead(BUTTON_PIN))
        {
          single_step();
        }
      } else {
        sleep(speed);
        toggle_clock();
      }
  } 
}

