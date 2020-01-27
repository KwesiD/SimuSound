/*
  Mifare RC522 Basic test program
  Prints out the tag id when in range
  
  PINOUT:

   RC522 MODULE    UNO     MEGA
   SDA(SS)         D10     D53
   SCK             D13     D52
   MOSI            D11     D51
   MISO            D12     D50
   PQ              Not Connected
   GND             GND     GND
   RST             D9      D9
   3.3V            3.3V    3.3V

*/

/**
 * https://www.instructables.com/id/ESP32-With-RFID-Access-Control/
 */

 
#include <SPI.h>
#include <MFRC522.h>
#include <String.h> 

#define RFID_SS  21//10
#define RFID_RST 22//9

//String getUID(void);

MFRC522 rfid( RFID_SS, RFID_RST );

void setup() {
  SPI.begin();
  Serial.begin(115200);
  rfid.begin();
  Serial.println("Start");
}

void loop() {
  //Serial.println(getUID());
  String uid = getUID();
  if(!uid.equals("")){
    Serial.println(uid);
  }
}

String getUID(){
  byte data[MAX_LEN];
  byte uid[5];
  //String hexValues[5];
  String hex = "";
  if ( rfid.requestTag( MF1_REQIDL, data ) == MI_OK ) {
    if ( rfid.antiCollision( data ) == MI_OK ) {
      memcpy( uid, data, 5 );
      //return uid;
      for ( int i = 0; i < 5; i++ ) {
        hex += String(uid[i],HEX);
      }
//      for(int i = 0;i < 5;i++){
//        hex += hexValues[i];
//      }
      return hex;
    }
  }
  return "";
}
