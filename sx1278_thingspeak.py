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

"""****************************************************************"""
print "start"
while(1):

	#Master
	sx1276_7_8_LoRaEntryTx()
	sx1276_7_8_LoRaTxPacket("Xark1 Lora sx1276_7_8",21)
	sx1276_7_8_LoRaEntryRx()
	print "send"
	
	print "wait"
	temp = sx1276_7_8_LoRaRxPacket(Lora_Rate_Sel) 
	while temp == 0:
	  temp = sx1276_7_8_LoRaRxPacket(Lora_Rate_Sel) 
	  
	sx1276_7_8_LoRaEntryRx()
	print "Data: " + str(temp)
		
	time.sleep(5)
