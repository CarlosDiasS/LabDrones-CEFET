#include <SoftwareSerial.h>

SoftwareSerial Seriall(2, 3); // RX no pino 2, TX no pino 3

long dist; //retorno em metros 
int strenght;
int check;
int uart[9];
int i;

const int HEADER = 0x59;

void setup() {
  Serial.begin(115200);  // Porta serial para monitoramento
  Seriall.begin(115200);
}

void loop() {
  
  if (Seriall.available()) {
    //Serial.println("comunicando com o lidar..");
    // Verifica o cabeçalho
    if (Seriall.read() == HEADER) {
      uart[0] = HEADER; 
      if (Seriall.read() == HEADER) {
        uart[1] = HEADER; 

        for (i = 2; i < 9; i++) {
          uart[i] = Seriall.read();
        }

        //padrao sbus que soma os valores de todos os canais 
        //check = uart[0] + uart[1] + uart[2] + uart[3] + uart[4] + uart[5] + uart[6] + uart[7];

        // Verifica se o checksum é válido
        if (uart[8] == (check & 0xff)) {
          // Calcula a distância e a força (strength) a partir dos dados lidos
          dist = uart[2] + uart[3] ;
          strenght = uart[4] + uart[5];

          // Imprime os resultados na serial principal para monitoramento
          Serial.print("Distância = ");
          Serial.print(dist);
          Serial.print('\t');
          Serial.print("Força = ");
          Serial.print(strenght);
          Serial.print("\n");

          delay(200); // Pequena pausa antes de ler novamente
        }
      }
    }
  }
}
