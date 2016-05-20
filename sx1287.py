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

# put your main code here, to run repeatedly:
mode = 0x01 #lora mode
Freq_Sel = 0x00 #433M
Power_Sel = 0x00 #
Lora_Rate_Sel = 0x06 #
BandWide_Sel = 0x07
Fsk_Rate_Sel = 0x00

print "reset"
reset_sx1276()

print "config"
sx1276_7_8_Config()

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
	GPIO.output(led, GPIO.HIGH) # turn the LED on (GPIO.HIGH is the voltage level)
	sx1276_7_8_LoRaEntryTx()
	sx1276_7_8_LoRaTxPacket()
	GPIO.output(led, GPIO.LOW) # turn the LED on (GPIO.HIGH is the voltage level)
	sx1276_7_8_LoRaEntryRx()
	print "send"
	time.sleep(2)

	""" 
	if(sx1276_7_8_LoRaRxPacket())
		GPIO.output(led, GPIO.HIGH); # turn the LED on (GPIO.HIGH is the voltage level)
		delay(500);
		GPIO.output(led, GPIO.LOW); # turn the LED on (GPIO.HIGH is the voltage level)
		delay(500);
	"""
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
