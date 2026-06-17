// Variables to track state
bool ledState = LOW;
int userValue = 0;

void setup() {
  // Initialize Serial communication at 9600 baud
  Serial.begin(9600);
  
  // Initialize the onboard LED pin
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, ledState);
}

void loop() {
  // Check if data has been sent from the computer
  if (Serial.available() > 0) {
    // Read the incoming string until a newline character
    String command = Serial.readStringUntil('\n');
    command.trim(); // Remove any trailing whitespace or \r

    // --- COMMAND: Toggle LED ---
    if (command == "LED_TOGGLE") {
      ledState = !ledState;
      digitalWrite(LED_BUILTIN, ledState);
      Serial.println("LED Toggled");
    } 
    
    // --- COMMAND: Query LED State ---
    else if (command == "LED_STATE") {
      Serial.println(ledState ? "ON" : "OFF");
    } 
    
    // --- COMMAND: Read Voltage from A0 ---
    else if (command == "READ_A0") {
      int rawValue = analogRead(A0);
      float voltage = rawValue * (5.0 / 1023.0); // Convert raw 0-1023 to 0-5V
      Serial.println(voltage);
    } 
    
    // --- COMMAND: Set User Value (Format: "SET_VAL:123") ---
    else if (command.startsWith("SET_VAL:")) {
      String valString = command.substring(8); // Get everything after "SET_VAL:"
      userValue = valString.toInt();
      Serial.print("Value set to: ");
      Serial.println(userValue);
    } 
    
    // --- COMMAND: Get User Value ---
    else if (command == "GET_VAL") {
      Serial.println(userValue);
    } 
    
    else {
      Serial.println("Unknown Command");
    }
  }
}
