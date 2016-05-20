"""*********************************************
Title:sx1276_7_8 demo code
Current version:v1.0
Function:demo
Processor Arduino
Clock:
Operate freqency:433MHZ band\
Date rate:for programme
modulation: Lora/
deviation:for programme
Transmit one packet data time : Indefinite package
Work mode:
campany:WWW.DORJI.COM
author:DORJI
Contact:
Date:2014-07-02
************************************************"""

import RPi.GPIO as GPIO
import time

from sx1278_function import *

"""*********************************************************
**Parameter table define**
sx1276_7_8FreqTbl = [[0x6C, 0x80, 0x00]] #433MHz
sx1276_7_8PowerTbl = [0xFF,0xFC,0xF9,0xF6]  #20 17 14 11 dbm
sx1276_7_8SpreadFactorTbl = [6,7,8,9,10,11,12]
sx1276_7_8LoRaBwTbl = [0,1,2,3,4,5,6,7,8,9] 
#7.8KHz,10.4KHz,15.6KHz,20.8KHz,31.2KHz,41.7KHz,62.5KHz,125KHz,250KHz,500KHz
*********************************************************"""

# Config
mode = 0x01 #lora mode
Freq_Sel = 0x00 #433M
Power_Sel = 0x00 #
Lora_Rate_Sel = 0x06 #
BandWide_Sel = 0x07
Fsk_Rate_Sel = 0x00

print "reset"
reset_sx1276()

print "config"
sx1276_7_8_Config(mode, Freq_Sel, Power_Sel, Lora_Rate_Sel, BandWide_Sel, Fsk_Rate_Sel)

print "enRX"
sx1276_7_8_LoRaEntryRx()
GPIO.output(led, GPIO.HIGH) # turn the LED on (GPIO.HIGH is the voltage level)
time.sleep(0.5) # wait for a second
GPIO.output(led, GPIO.LOW) # turn the LED on (GPIO.HIGH is the voltage level)
time.sleep(0.5) # wait for a second
i = 0

"""****************************************************************"""
print "start"
while(1):
	#Master
	#i = i + 1
	#sx1276_7_8Data[0] = 'A'
	"""
	GPIO.output(led, GPIO.HIGH) # turn the LED on (GPIO.HIGH is the voltage level)
	sx1276_7_8_LoRaEntryTx()
	sx1276_7_8_LoRaTxPacket("AO",2)
	GPIO.output(led, GPIO.LOW) # turn the LED on (GPIO.HIGH is the voltage level)
	sx1276_7_8_LoRaEntryRx()
	print "send"
	time.sleep(2)
	"""

	temp = sx1276_7_8_LoRaRxPacket(); 
	if(sx1276_7_8_LoRaRxPacket() != 0)
		GPIO.output(led, GPIO.HIGH); # turn the LED on (GPIO.HIGH is the voltage level)
		delay(500);
		GPIO.output(led, GPIO.LOW); # turn the LED on (GPIO.HIGH is the voltage level)
		delay(500);
		sx1276_7_8_LoRaEntryRx()
		print "Data: " + temp
	
	#slaver
	"""	
	if(sx1276_7_8_LoRaRxPacket())
		GPIO.output(led, GPIO.HIGH); # turn the LED on (GPIO.HIGH is the voltage level)
		delay(500); # wait for a second
		GPIO.output(led, GPIO.LOW); # turn the LED on (GPIO.HIGH is the voltage level)
		delay(500); # wait for a second
		sx1276_7_8_LoRaEntryRx();
		GPIO.output(led, GPIO.HIGH); # turn the LED on (GPIO.HIGH is the voltage level)
		sx1276_7_8_LoRaEntryTx();
		sx1276_7_8_LoRaTxPacket();
		GPIO.output(led, GPIO.LOW); # turn the LED on (GPIO.HIGH is the voltage level)*
		sx1276_7_8_LoRaEntryRx();
	"""
