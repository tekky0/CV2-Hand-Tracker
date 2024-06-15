
int gauge = 0;

void setup() {
  Serial.begin(9600);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(6, OUTPUT);
  
}
void loop() {
     if (Serial.available() > 0) {
  gauge = 0;
        String data = Serial.readStringUntil('\n');  // Read data until newline character
        Serial.print("Received data: ");
        Serial.println(data);  // Print received data

        // Example: Parse received data as integers
        int finger1 = data.substring(0, 1).toInt();
        int finger2 = data.substring(2, 3).toInt();
        int finger3 = data.substring(4, 5).toInt();
        int finger4 = data.substring(6, 7).toInt();
        int finger5 = data.substring(8, 9).toInt();

        if (finger1 == 1) {
          digitalWrite(7, HIGH);
          gauge += 1;
          
        }
        else{
          digitalWrite(7, LOW);
          gauge -= 1;
          
        }if (finger2 == 1) {
            digitalWrite(5, HIGH);
            gauge += 1;
          
        }
        else{
          digitalWrite(5, LOW);
          gauge -= 1;
          
        }if (finger3 == 1) {
            digitalWrite(4, HIGH);
            gauge += 1;
        }
        else{
          digitalWrite(4, LOW);
          gauge -= 1;
          
        }if (finger4 == 1) {
            digitalWrite(3, HIGH);
            gauge += 1;
        }
        else{
          digitalWrite(3, LOW);
          gauge -= 1;
          
        }if (finger5 == 1) {
            digitalWrite(2, HIGH);
            gauge += 1;
        }
        else{
          digitalWrite(2, LOW);
          gauge -= 1;
        }
        int brightness = map(gauge, 0, 5, 0, 255);
        analogWrite(6, brightness);
        
    }
}
