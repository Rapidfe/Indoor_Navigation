char roads[][18] = {{0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0},
{0,0,0,0,0,0,1,1,1,1,0,0,1,1,0,0,0,0},
{0,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,0},
{0,1,0,0,0,0,1,1,1,1,1,0,1,1,0,1,1,0},
{0,1,0,0,0,0,1,1,0,1,1,0,1,1,0,1,1,0},
{0,1,0,0,0,0,1,1,0,0,1,0,1,1,0,1,1,0},
{0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0},
{0,0,0,0,1,1,1,1,0,0,1,1,1,1,1,1,1,0},
{0,0,0,0,1,1,1,1,0,0,0,0,0,1,0,0,1,0},
{0,0,0,1,1,0,0,1,0,0,0,0,0,1,0,0,1,0},
{0,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,0},
{0,1,1,1,1,0,0,1,1,0,0,0,0,1,1,1,1,0},
{0,0,0,1,1,1,0,1,1,0,0,0,0,1,1,1,1,0},
{0,0,0,0,1,1,0,1,1,1,1,1,1,1,1,1,1,0},
{0,0,0,0,1,1,0,1,1,0,0,1,1,1,0,0,1,0},
{0,1,1,0,1,1,1,1,1,0,0,1,1,1,0,0,1,0},
{0,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,0},
{0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0}};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(19, OUTPUT); pinMode(2, OUTPUT); pinMode(3, OUTPUT);
  pinMode(4, OUTPUT); pinMode(5, OUTPUT); pinMode(6, OUTPUT);
  pinMode(7, OUTPUT); pinMode(8, OUTPUT); pinMode(9, OUTPUT);
  pinMode(10, OUTPUT); pinMode(11, OUTPUT); pinMode(12, OUTPUT);
  pinMode(13, OUTPUT); pinMode(14, OUTPUT); pinMode(15, OUTPUT);
  pinMode(16, OUTPUT); pinMode(17, OUTPUT); pinMode(18, OUTPUT);
  pinMode(31, OUTPUT); pinMode(32, OUTPUT); pinMode(33, OUTPUT);
  pinMode(34, OUTPUT); pinMode(35, OUTPUT); pinMode(36, OUTPUT);
  pinMode(37, OUTPUT); pinMode(38, OUTPUT); pinMode(39, OUTPUT);
  pinMode(40, OUTPUT); pinMode(41, OUTPUT); pinMode(42, OUTPUT);
  pinMode(43, OUTPUT); pinMode(44, OUTPUT); pinMode(45, OUTPUT);
  pinMode(46, OUTPUT); pinMode(47, OUTPUT); pinMode(48, OUTPUT);
  for(int i=1; i<19; i++){
    digitalWrite(i+1, HIGH);
  }
}

boolean myMap[10][18][18];
int nowNum = -1;
unsigned long blinkTime;
int blinkdiv;
int showing = 10;
long par;
void loop() {
  // put your main code here, to run repeatedly:
  //Serial.flush();
  if( Serial.available() ){
    char a = Serial.read();
    while( a=='a' ){
      for(nowNum=0; nowNum<10; nowNum++){
        for(int i=0; i<18; i++){
          for(int j=0; j<18;){
            if( Serial.available() ){
              par = Serial.parseInt();
              myMap[nowNum][i][j] = par? true:false;
              j++;
            }
          }
          Serial.println('x');
        }
      }
      a = 'b';
      blinkTime = millis();
      showing = 0;
    }
    if( a=='c' ){
      nowNum = -2; 
    }
  }
  /*
  for(int i=0; i<18; i++){
    for(int j=0; j<18; j++){
      if( arr[i][j] )
        digitalWrite(j+31, HIGH);
      else
        digitalWrite(j+31, LOW);
    }
    digitalWrite(i==0? 19:i+1, LOW);
    delay(1);
    digitalWrite(i==0? 19:i+1, HIGH);
  }
  */
  
  /*for(int i=1; i<19; i++){
    digitalWrite(i+1, LOW);
  }
  for(int i=0; i<18; i++){
    digitalWrite(i+31, HIGH);
    delay(1);
    digitalWrite(i+31, LOW);
  }*/

  blinkdiv = (millis()-blinkTime)/150;
  if( showing<9 ){
    if( blinkdiv>=13 ){
      blinkTime = millis();
      showing++;
    }
  }
  if(nowNum<0){
    for(int i=0; i<18; i++){
      for(int j=17; j>=0; j--){
        int tmp = 17-j;
        if( roads[j][i] ){
          if( nowNum==-2 ){
            if( blinkdiv>3 && blinkdiv%2==0 && myMap[showing][j][i] )
              digitalWrite(tmp+31, HIGH);
            else
              digitalWrite(tmp+31, LOW);
          }else{
            digitalWrite(tmp+31, LOW);
          }
        }else{
          digitalWrite(tmp+31, HIGH);
        }
      }
      digitalWrite(i==0? 19:i+1, LOW);
      delay(0.8);
      digitalWrite(i==0? 19:i+1, HIGH);
    }
  }
}
