/*
  AnalogReadSerial

  Reads an analog input on pin 0, prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/AnalogReadSerial
*/

// the setup routine runs once when you press reset:

const int up = 12;
const int down = 11;
const int cw = 10;
const int ccw = 9;

void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  pinMode(up, OUTPUT);
  pinMode(down, OUTPUT);
  pinMode(cw, OUTPUT);
  pinMode(ccw, OUTPUT);
}

// the loop routine runs over and over again forever:

int valor_alvo_elevacao = 90;
int valor_alvo_azimute = 180;
int valor_corrente_elevacao = 90;
int valor_corrente_azimute = 90; 
String gcode = ""; 
int temp1 = 0;
int temp2 = 0;
int temp3 = 0;
int temp4 = 0;
int temp5 = 0;
int temp6 = 0;
int convergencia;
int convergencia2;
String parar = ""; 
int ultimo_valor_corrente_elevacao;
int ultimo_valor_corrente_azimute;


  
void loop() {
  digitalWrite(up, HIGH);
  digitalWrite(down, HIGH);
  digitalWrite(cw, HIGH);
  digitalWrite(ccw, HIGH);
  

  // read the input on analog pin 0
  Serial.println("Entre com gcode");  
  while (Serial.available() == 0){} //Wait for user input  }  
  gcode = Serial.readString(); //Reading the Input string from Serial port.
  Serial.println(gcode); 

  comando = gcode.remove(2);
  Serial.println(comando);

  /*temp1 = (gcode[3]-48)*100;
  temp2 = (gcode[4]-48)*10;
  temp3 = gcode[5]-48;
  valor_alvo_elevacao = temp1 + temp2 + temp3;

  temp4 = (gcode[6]-48)*100;
  temp5 = (gcode[7]-48)*10;
  temp6 = gcode[8]-48;
  valor_alvo_azimute = temp4 + temp5 + temp6;
  

  Serial.println("recebido mensagem: ok"); 

  convergencia = 0;
  convergencia2 = 0;
  while (convergencia < 6 && ultimo_valor_corrente_elevacao != valor_alvo_elevacao){
  
  int sensorValue_elevacao = analogRead(A0);
  valor_corrente_elevacao = map(sensorValue_elevacao, 2, 1004, 0, 180);
 

        if(valor_alvo_elevacao < valor_corrente_elevacao){
          digitalWrite(up, HIGH);
          digitalWrite(down, LOW);   
          
                                                        }
          
        if(valor_alvo_elevacao > valor_corrente_elevacao){
          digitalWrite(up, LOW);
          digitalWrite(down, HIGH);
          
                                                          }
                                                          
        if(valor_alvo_elevacao == valor_corrente_elevacao){
          digitalWrite(up, HIGH);
          digitalWrite(down, HIGH);
          convergencia = convergencia +1;
        }
        delay(10);
        ultimo_valor_corrente_elevacao = valor_corrente_elevacao;
                                                  }

////////////Azimute

while (convergencia2 < 6 && ultimo_valor_corrente_azimute != valor_alvo_azimute){
      int sensorValue_azimute = analogRead(A1);
      valor_corrente_azimute = map(sensorValue_azimute, 124, 1012, 0, 360);
      
        if(valor_alvo_azimute < valor_corrente_azimute){
          digitalWrite(cw, HIGH);
          digitalWrite(ccw, LOW);   
          
                                                        }
          
        if(valor_alvo_azimute > valor_corrente_azimute){
          digitalWrite(cw, LOW);
          digitalWrite(ccw, HIGH);
          
                                                          }
                                                          
        if(valor_alvo_azimute == valor_corrente_azimute){
          digitalWrite(cw, HIGH);
          digitalWrite(ccw, HIGH);
          convergencia2 = convergencia2 +1;
        }
        
       
        delay(10);
        ultimo_valor_corrente_azimute = valor_corrente_azimute;  
                        }
  Serial.println("ok");     */

}