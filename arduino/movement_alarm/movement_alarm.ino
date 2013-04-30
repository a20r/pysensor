
int power_pin = 12;
int value_pin = 7;
boolean new_bool = true;

void setup() {
  Serial.begin(9600);
  pinMode(power_pin, OUTPUT);
  pinMode(value_pin, INPUT);
  digitalWrite(power_pin, HIGH);
    
}

void loop() {
  if ((digitalRead(value_pin) == HIGH) && new_bool) {
    Serial.write('\x00');
    delay(100);
    Serial.write("MOTION");
    delay(100);
    Serial.write("\x01\x02");
    delay(100);
    Serial.flush();
    new_bool = false;
  } else if (digitalRead(value_pin) == LOW && !new_bool) {
      new_bool = true;
      Serial.write('\x00');
      delay(100);
      Serial.write("MOTIONENDED");
      delay(100);
      Serial.write("\x01\x02");
      delay(100);
      Serial.flush();
  }
}

