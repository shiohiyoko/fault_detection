/****************************************************************************/	
//	Function: Measure the measure the Surrounding temperature around the sensor
//			  and the temperature of the target which is in front of the sensor.
//			  And print the result on the serial monitor.
//	Hardware: Grove - Infrared Temperature Sensor
//	Arduino IDE: Arduino-1.0
//	Author:	 Bruce.Qin	
//	Date: 	 Nov 28,2011
//	Version: v1.0 modified by FrankieChu at Jan 24,2013
//	by www.seeedstudio.com
//
//  This library is free software; you can redistribute it and/or
//  modify it under the terms of the GNU Lesser General Public
//  License as published by the Free Software Foundation; either
//  version 2.1 of the License, or (at your option) any later version.
//
//  This library is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
//  Lesser General Public License for more details.
//
//  You should have received a copy of the GNU Lesser General Public
//  License along with this library; if not, write to the Free Software
//  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
//
/******************************************************************************/

#include <math.h>
#include <XBee.h>


#define SUR_TEMP_PIN A0 // Analog input pin connect to temperature sensor SUR pin
#define OBJ_TEMP_PIN A1 // Analog input pin connect to temperature sensor OBJ pin
float temp_calibration=0;       //this parameter was used to calibrate the temperature
//float objt_calibration=0.000; //this parameter was used to calibrate the object temperature
float temperature_range=10;    //we make a map of temperature-voltage according to sensor datasheet. 10 is the temperature step when sensor and 
                               //object distance is 9CM.
float offset_vol=0.014;        //this parameter was used to set the mid level voltage,when put the sensor in normal environment after 10 min,
                               //the sensor output 0.For example,the surrounding temperature is 29??????but the result is 27??? via the sensor,
                               //you should set the reerence to 0.520 or more,according to your sensor to change.
                               //the unit is V
float tempValue = 0; 
float objtValue= 0;  
float current_temp=0;
float temp=0;
float temp1=0;
float temp2=0;
unsigned int temp3=0;
const float reference_vol=0.500;
unsigned char clear_num=0;//when use lcd to display
float R=0;
float voltage=0;
float final_temp=0;

// xbee parameters
XBee xbee = XBee();


// current parameters
const float FACTOR = 30;
const float VMIN = 0.96;
const float VMAX = 3.92;

const float ADCV = 5.0;

long res[100]={
                 318300,302903,288329,274533,261471,249100,237381,226276,215750,205768,
                 196300,187316,178788,170691,163002,155700,148766,142183,135936,130012,
                 124400,119038,113928,109059,104420,100000,95788,91775,87950,84305,
                 80830,77517,74357,71342,68466,65720,63098,60595,58202,55916,
                 53730,51645,49652,47746,45924,44180,42511,40912,39380,37910,
                 36500,35155,33866,32631,31446,30311,29222,28177,27175,26213,
                 25290,24403,23554,22738,21955,21202,20479,19783,19115,18472,
                 17260,16688,16138,15608,15098,14608,14135,13680,13242,12819,
                 12412,12020,11642,11278,10926,10587,10260,9945,9641,9347,
                 9063,8789,8525,8270,8023,7785,7555,7333,7118,6911};
                 
float obj [13][12]={
/*0*/             { 0,-0.274,-0.58,-0.922,-1.301,-1.721,-2.183,-2.691,-3.247,-3.854,-4.516,-5.236}, //
/*1*/             { 0.271,0,-0.303,-0.642,-1.018,-1.434,-1.894,-2.398,-2.951,-3.556,-4.215,-4.931},  //???surrounding temperature,from -10,0,10,...100
/*2*/             { 0.567,0.3,0,-0.335,-0.708,-1.121,-1.577,-2.078,-2.628,-3.229,-3.884,-4.597},   //???object temperature,from -10,0,10,...110
/*3*/             { 0.891,0.628,0.331,0,-0.369,-0.778,-1.23,-1.728,-2.274,-2.871,-3.523,-4.232},
/*4*/             { 1.244,0.985,0.692,0.365,0,-0.405,-0.853,-1.347,-1.889,-2.482,-3.13,-3.835},
/*5*/             { 1.628,1.372,1.084,0.761,0.401,0,-0.444,-0.933,-1.47,-2.059,-2.702,-3.403},
/*6*/             { 2.043,1.792,1.509,1.191,0.835,0.439,0,-0.484,-1.017,-1.601,-2.24,-2.936},
/*7*/             { 2.491,2.246,1.968,1.655,1.304,0.913,0.479,0,-0.528,-1.107,-1.74,-2.431},
/*8*/             { 2.975,2.735,2.462,2.155,1.809,1.424,0.996,0.522,0,-0.573,-1.201,-1.887},
/*9*/             { 3.495,3.261,2.994,2.692,2.353,1.974,1.552,1.084,0.568,0,-0.622,-1.301},
/*10*/            { 4.053,3.825,3.565,3.27,2.937,2.564,2.148,1.687,1.177,0.616,0,-0.673},
/*11*/            { 4.651,4.43,4.177,3.888,3.562,3.196,2.787,2.332,1.829,1.275,0.666,0},
/*12*/            { 5.29,5.076,4.83,4.549,4.231,3.872,3.47,3.023,2.527,1.98,1.379,0.72}
};

void setup() 
{
	Serial.begin(115200); // initialize serial communications at 9600 bps
	analogReference(INTERNAL);//set the refenrence voltage 1.1V,the distinguishability can up to 1mV.
	//analogReference(INTERNAL1V1);//(mega only)set the refenrence voltage 1.1V,the distinguishability can up to 1mV.
  xbee.setSerial(Serial);
}

void loop()
{
//	measureSurTemp();//measure the /Surrounding temperature around the sensor
	final_temp = measureObjectTemp();
  sendMsg();
}

float binSearch(long x)// this function used for measure the surrounding temperature
{
	int low,mid,high;
	low=0;
	//mid=0;
	high=100;
	while (low<=high)
	{
		mid=(low+high)/2;
		if(x<res[mid])
			low= mid+1;
		else//(x>res[mid])
			high=mid-1;
	}
	return mid;
}

float arraysearch(float x,float y)//x is the surrounding temperature,y is the object temperature
{
	int i=0;
	float tem_coefficient=100;//Magnification of 100 times	
	i=(x/10)+1;//Ambient temperature			
	voltage=(float)y/tem_coefficient;//the original voltage		
	//Serial.print("sensor voltage:\t");		
	//Serial.print(voltage,5);	
	//Serial.print("V");			
	for(temp3=0;temp3<13;temp3++)		
	{			
		if((voltage>obj[temp3][i])&&(voltage<obj[temp3+1][i]))				
		{			
			return temp3;					
		}			
	}
}
float measureSurTemp()
{  
	unsigned char i=0;
	float current_temp1=0;	  
	int signal=0;	  
	tempValue=0;

	for(i=0;i<10;i++)       //	  
	{		  
		tempValue+= analogRead(SUR_TEMP_PIN); 		  
		delay(10); 	  
	}	  
	tempValue=tempValue/10;	  
	temp = tempValue*1.1/1023;	  
	R=2000000*temp/(2.50-temp);	  
	signal=binSearch(R);	  
	current_temp=signal-1+temp_calibration+(res[signal-1]-R)/(res[signal-1]-res[signal]);
	Serial.print("Surrounding temperature:");
	Serial.print(current_temp);
	return current_temp;
}

float measureObjectTemp()
{
	unsigned char i=0;  
	unsigned char j=0;  
	float sur_temp=0;  
	unsigned int array_temp=0;  
	float temp1,temp2; 
	objtValue=0;	
	for(i=0;i<10;i++)
	{
		objtValue+= analogRead(OBJ_TEMP_PIN); 
		delay(10); 
    }
	objtValue=objtValue/10;//Averaging processing     
	temp1=objtValue*1.1/1023;//+objt_calibration; 
	sur_temp=temp1-(reference_vol+offset_vol);             
//	Serial.print("\t");/
	array_temp=arraysearch(current_temp,sur_temp*1000);        
	temp2=current_temp;        
	temp1=(temperature_range*voltage)/(obj[array_temp+1][(int)(temp2/10)+1]-obj[array_temp][(int)(temp2/10)+1]);        
	return temp2+temp1;
}

int vibration(){
  return analogRead(A2);
}

float getCorrients()
{
  float volt;
  float corrients;
  float sum = 0;
  long tempo = millis();
  int counter = 0;

  while(millis() - tempo < 500)
  {
    volt = analogRead(A4) * ADCV / 1023.0;
    corrients = fmap(volt, VMIN, VMAX, -FACTOR, FACTOR);

    sum += sq(corrients);
    counter = counter + 1;
    delay(1);
  }

  corrients = sqrt(sum/counter);
  return(corrients);
}

float fmap(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max-out_min) / (in_max - in_min) + out_min;
}


void sendMsg(){
  int temp = static_cast<int>(final_temp*100);
  int vib = vibration();
  int current = static_cast<int>(getCorrients());
  
  uint8_t payload[6]; 
//  Serial.println(temp);
  payload[0] = temp >> 8 & 0xFF;
  payload[1] = temp & 0xFF;
  payload[2] = vib >> 8 & 0xFF;
  payload[3] = vib & 0xFF;
  payload[4] = current >> 8 & 0xFF;
  payload[5] = current & 0xFF;
  
    // Specify the address of the remote XBee (this is the SH + SL)
  XBeeAddress64 addr64 = XBeeAddress64(0x0013a200, 0x41268089);
  
  // Create a TX Request
  ZBTxRequest zbTx = ZBTxRequest(addr64, payload, sizeof(payload));
  
  // Send your request
  xbee.send(zbTx);
}
