int c = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("Hola");
  delay(1000);
}

void loop() {
  Serial.println(c);
  c ++;
  delay(10);
}
