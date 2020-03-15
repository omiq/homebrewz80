#include <Eventually.h>

EvtManager mgr;
#define FAST_SLOW_MODE 2
#define AUTO  3
#define CLOCKLED 5
#define BUTTON_PIN 7



void sleep(int sleep_time)
{
  long start_time = millis();

  while(millis() < start_time + sleep_time)
  {
    // do nothing
  }
}


void toggle_clock()
{


      PORTD |= 0b00100000; // sets digital pin 5 HIGH
        sleep(10);
      PORTD &= 0b00000000; // sets digital pin 5 LOW
        sleep(10);

}

bool single_step()
{

  toggle_clock();

  return false;            // tells event manager to continue
}



void manual_auto()
{
  mgr.resetContext();
  if(digitalRead(AUTO)) 
  {

    if(digitalRead(FAST_SLOW_MODE) )
    { mgr.addListener(new EvtTimeListener(1, true, (EvtAction)toggle_clock)); }
    else 
    { mgr.addListener(new EvtTimeListener(1000, true, (EvtAction)toggle_clock)); }
  }
  else
  {
    mgr.addListener(new EvtPinListener(BUTTON_PIN,(EvtAction)single_step)); // Manual stepping listener
  }
}

void setup() {

  // set up the pins and the event listeners
  pinMode(CLOCKLED, OUTPUT);  
  pinMode(BUTTON_PIN, INPUT);

  // Set up interupts for when toggles change
  attachInterrupt(0, manual_auto, CHANGE);
  attachInterrupt(1, manual_auto, CHANGE);
  
  // Manual or automatic clock
  manual_auto(); 


}

USE_EVENTUALLY_LOOP(mgr) // Uses this instead of the usual loop() function.
