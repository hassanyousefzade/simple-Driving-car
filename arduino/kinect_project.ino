void setup() {
  // put your setup code here, to run once:
int i;
pinMode(3,OUTPUT);
pinMode(4,OUTPUT);
pinMode(5,OUTPUT);
pinMode(6,OUTPUT);
Serial.begin(9600);
Serial.print("residam");
khamosh();

}
int a;
int  k;
int x;
void loop() {


while(Serial.available()>0)
{
  golo();
  
  k=Serial.read();
  Serial.print(k);
  //a= k.toFloat();
  
  if(k==2)
  {
    x=-1;
  }
  if(k==1)
  {
    x=1;
    Serial.print("ok");
  }
  teta(abs(k),x);
}
}
void gardeshrast()
{
digitalWrite(3,HIGH);

digitalWrite(4,HIGH);

digitalWrite(5,HIGH);

analogWrite(6,120);
delay(100);
khamosh();
}

void aghab()
{
digitalWrite(3,HIGH);

digitalWrite(4,LOW);

digitalWrite(5,LOW);

digitalWrite(6,HIGH);
delay(4000);
Serial.print("residam");
khamosh();
}

void golo()
{
Serial.print("golo");
analogWrite(3,195);

digitalWrite(4,HIGH);

digitalWrite(5,HIGH);

analogWrite(6,195);
}

void khamosh()
{
digitalWrite(3,LOW);

digitalWrite(4,LOW);

digitalWrite(5,LOW);

digitalWrite(6,LOW);
}

void gardeshcahp()
{
analogWrite(3,120);

digitalWrite(4,HIGH);

digitalWrite(5,HIGH);

digitalWrite(6,HIGH);
delay(100);
khamosh();
}
void teta(int teta,int k)
{


int alpha;

int i;

alpha=int((teta*3)/30);

for(i=0;i<alpha;i++)
{

  if(k==-1)
  {
    gardeshrast();
  }
  if(k==1)
  {
    gardeshcahp();
  }

}

}



 
