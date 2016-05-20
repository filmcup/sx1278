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

from sx1278_registers import *
from sx1278_function import *

led = 13;
nsel = 8;
sck = 11;
mosi = 10;
miso = 9;
dio0 = 24;
reset = 23;

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(led, GPIO.OUT)
GPIO.setup(nsel, GPIO.OUT)
GPIO.setup(sck, GPIO.OUT)
GPIO.setup(mosi, GPIO.OUT)
GPIO.setup(miso, GPIO.IN)
GPIO.setup(dio0, GPIO.IN)
GPIO.setup(reset, GPIO.OUT)

"""***********************************************
# RF module: sx1276_7_8
# FSK:
# Carry Frequency: 434MHz
# Bit Rate: 1.2Kbps/2.4Kbps/4.8Kbps/9.6Kbps
# Tx Power Output: 20dbm/17dbm/14dbm/11dbm
# Frequency Deviation: +/-35KHz
# Receive Bandwidth: 83KHz
# Coding: NRZ
# Packet Format: 0x5555555555+0xAA2DD4+"Mark1 Lora sx1276_7_8" (total: 29bytes)
# LoRa:
# Carry Frequency: 434MHz
# Spreading Factor: 6/7/8/9/10/11/12
# Tx Power Output: 20dbm/17dbm/14dbm/11dbm
# Receive Bandwidth:7.8KHz/10.4KHz/15.6KHz/20.8KHz/31.2KHz/41.7KHz/62.5KHz/125KHz/250KHz/500KHz
# Coding: NRZ
# Packet Format: "HR_WT Lora sx1276_7_8" (total: 21 bytes)
# Tx Current: about 120mA (RFOP=+20dBm,typ.)
# Rx Current: about 11.5mA (typ.)
*********************************************************"""
########################/ LoRa mode
#########################
#Error Coding rate (CR)setting
CR_4_5 = 0
CR_4_6 = 1
CR_4_7 = 1
CR_4_8 = 1

if CR_4_5 == 0:
	CR = 0x01
elif CR_4_6 == 0:
	CR = 0x02
elif CR_4_7 == 0:
	CR = 0x03
elif CR_4_8 == 0:
	CR = 0x04


#CRC Enable
CRC_EN = 1
if CRC_EN == 1:
	CRC = 0x01 #CRC Enable
else:
	CRC = 0x00

"""*********************************************************
**Parameter table define
*********************************************************"""
sx1276_7_8FreqTbl = [[0x6C, 0x80, 0x00]] #433MHz
sx1276_7_8PowerTbl = [0xFF,0xFC,0xF9,0xF6]  #20 17 14 11 dbm
sx1276_7_8SpreadFactorTbl = [6,7,8,9,10,11,12]
sx1276_7_8LoRaBwTbl = [0,1,2,3,4,5,6,7,8,9] 
#7.8KHz,10.4KHz,15.6KHz,20.8KHz,31.2KHz,41.7KHz,62.5KHz,125KHz,250KHz,500KHz

sx1276_7_8Data = "Xark1 Lora sx1276_7_8"
RxData = None


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
