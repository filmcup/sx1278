import RPi.GPIO as GPIO
import time

from sx1278_registers import *
#from sx1278_config import *

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

#sx1276_7_8Data = "Xark1 Lora sx1276_7_8"
#RxData = None

"""*********************************************************
**Name: SPICmd8bit
**Function: SPI Write one byte
**Input: WrPara
**Output: none
**note: use for burst mode
*********************************************************"""
def  SPICmd8bit(WrPara):

	GPIO.output(nsel, GPIO.LOW)#nSEL_L(); 
 	GPIO.output(sck, GPIO.LOW)#SCK_L();

	for bitcnt in range(8):
		 GPIO.output(sck, GPIO.LOW)#SCK_L();

		 if (WrPara&0x80) == 0x80:
		 	GPIO.output(mosi, GPIO.HIGH)#SDI_H();
		 else:
		 	GPIO.output(mosi, GPIO.LOW)#SDI_L();

		 GPIO.output(sck, GPIO.HIGH)#SCK_H();

		 WrPara <<= 1

	GPIO.output(sck, GPIO.LOW)#SCK_L();
	GPIO.output(mosi, GPIO.HIGH)#SDI_H();

	return

"""*********************************************************
**Name: SPIRead8bit
**Function: SPI Read one byte
**Input: None
**Output: result byte
**Note: use for burst mode
*********************************************************"""
def SPIRead8bit():

	RdPara = 0

	GPIO.output(nsel, GPIO.LOW)#nSEL_L();
	GPIO.output(mosi, GPIO.HIGH)#SDI_H(); #Read one byte data from FIFO, MOSI holdto GPIO.HIGH
	for bitcnt in range(8):

		GPIO.output(sck, GPIO.LOW)#SCK_L();
		RdPara <<= 1
		GPIO.output(sck, GPIO.HIGH) #SCK_H();

		if GPIO.input(miso):#if(Get_SDO())
			RdPara |= 0x01
		else:
			RdPara |= 0x00 

	GPIO.output(sck, GPIO.LOW)#SCK_L();

	return RdPara
"""*********************************************************
**Name: SPIRead
**Function: SPI Read CMD
**Input: adr -> address for read
**Output: None
*********************************************************"""
def SPIRead(adr):

	SPICmd8bit(adr) #Send address first
	tmp = SPIRead8bit()
	GPIO.output(nsel, GPIO.HIGH)#nSEL_H();

	return tmp
"""*********************************************************
**Name: SPIWrite
**Function: SPI Write CMD
**Input: u8 address & u8 data
**Output: None
*********************************************************"""
def SPIWrite(adr, WrPara):

	GPIO.output(nsel, GPIO.LOW)#nSEL_L();

	SPICmd8bit(adr|0x80)
	SPICmd8bit(WrPara)

	GPIO.output(sck, GPIO.LOW)#SCK_L();
	GPIO.output(mosi, GPIO.HIGH)#SDI_H();
	GPIO.output(nsel, GPIO.HIGH)#nSEL_H();

	return
"""*********************************************************
**Name: SPIBurstRead
**Function: SPI burst read mode
**Input: adr-----address for read
** ptr-----data buffer point for read
** length--how many bytes for read 
**Output: None
*********************************************************"""
def SPIBurstRead(adr, ptr, leng):

	if leng<=1: #length must more thanone
		return
	else:

		GPIO.output(sck, GPIO.LOW) #SCK_L();
		GPIO.output(nsel, GPIO.LOW)#nSEL_L();

		SPICmd8bit(adr)

		for i in range(leng):
			ptr[i] = SPIRead8bit()

		GPIO.output(nsel, GPIO.HIGH)#nSEL_H();

	return
"""*********************************************************
**Name: SPIBurstWrite
**Function: SPI burst write mode
**Input: adr-----address for write
** ptr-----data buffer point for write
** length--how many bytes for write
**Output: none
*********************************************************"""
def BurstWrite(adr, ptr, leng):

	if leng<=1: #length must more thanone
		return
	else:

		GPIO.output(sck, GPIO.LOW)#SCK_L();
		GPIO.output(nsel, GPIO.LOW)#nSEL_L();

		SPICmd8bit(adr|0x80)

		for i in range(leng):
			SPICmd8bit(ptr[i])

		GPIO.output(nsel, GPIO.HIGH)#nSEL_H();

	return


def BurstWrite2(adr, ptr, leng):

        if leng<=1: #length must more thanone
                return
        else:

                GPIO.output(sck, GPIO.LOW)#SCK_L();
                GPIO.output(nsel, GPIO.LOW)#nSEL_L();

                SPICmd8bit(adr|0x80)

                for i in range(leng):
                        SPICmd8bit(ord(ptr[i]))

                GPIO.output(nsel, GPIO.HIGH)#nSEL_H();

        return

"""*********************************************************
**Name: sx1276_7_8_Standby
**Function: Entry standby mode
**Input: None
**Output: None
*********************************************************""" 
def sx1276_7_8_Standby():

	SPIWrite(LR_RegOpMode,0x09)
	#Standby#GPIO.LOW Frequency Mode
	#SPIWrite(LR_RegOpMode,0x01);
	#Standby#GPIO.HIGH Frequency Mode

	return
"""*********************************************************
**Name: sx1276_7_8_Sleep
**Function: Entry sleep mode
**Input: None
**Output: None
*********************************************************"""
def sx1276_7_8_Sleep():

	SPIWrite(LR_RegOpMode,0x08) #Sleep#GPIO.LOWFrequency Mode
 	#SPIWrite(LR_RegOpMode,0x00)#Sleep#GPIO.HIGH Frequency Mode

	return
"""*******************************************************"""
#LoRa mode
"""*******************************************************"""
"""*********************************************************
**Name: sx1276_7_8_EntryLoRa
**Function: Set RFM69 entry LoRa(LongRange) mode
**Input: None
**Output: None
*********************************************************"""
def sx1276_7_8_EntryLoRa():

	SPIWrite(LR_RegOpMode,0x88)#GPIO.LOW Frequency Mode
	#SPIWrite(LR_RegOpMode,0x80)#GPIO.HIGH Frequency Mode

	return
"""*********************************************************
**Name: sx1276_7_8_LoRaClearIrq
**Function: Clear all irq
**Input: None
**Output: None
*********************************************************"""
def sx1276_7_8_LoRaClearIrq(): 

	SPIWrite(LR_RegIrqFlags,0xFF)

	return
"""*********************************************************
**Name: sx1276_7_8_LoRaEntryRx
**Function: Entry Rx mode
**Input: None
**Output: None
*********************************************************"""
def sx1276_7_8_LoRaEntryRx():

	addr = 0x00

	#sx1276_7_8_Config() #setting baseparameter

	SPIWrite(REG_LR_PADAC,0x84) #Normal and Rx
	SPIWrite(LR_RegHopPeriod,0xFF) #RegHopPeriod NO FHSS
	SPIWrite(REG_LR_DIOMAPPING1,0x01) #DIO0=00, DIO1=00,DIO2=00, DIO3=01

	SPIWrite(LR_RegIrqFlagsMask,0x3F) #Open RxDone interrupt & Timeout
	sx1276_7_8_LoRaClearIrq()

	SPIWrite(LR_RegPayloadLength,21) #RegPayloadLength21byte(this register must difine when the data long of one byte in SF is 6)

	addr = SPIRead(LR_RegFifoRxBaseAddr) #ReadRxBaseAddr
	SPIWrite(LR_RegFifoAddrPtr,addr) #RxBaseAddr ->FiFoAddrPtr
	SPIWrite(LR_RegOpMode,0x8d) #Continuous RxMode#GPIO.LOW Frequency Mode
	#SPIWrite(LR_RegOpMode,0x05); #Continuous RxMode#GPIO.HIGH Frequency Mode
	#SysTime = 0;
	while(1):
		if(SPIRead(LR_RegModemStat)&0x04)==0x04: #Rx-on going RegModemStat
			break
	#if(SysTime>=3)return 0; #over time for error

 	return
 
"""*********************************************************
**Name: sx1276_7_8_LoRaReadRSSI
**Function: Read the RSSI value
**Input: none
**Output: temp, RSSI value
*********************************************************"""
def sx1276_7_8_LoRaReadRSSI():

	temp = 10
	temp = SPIRead(LR_RegRssiValue) #Read RegRssiValu, Rssi value
	temp = temp + 127 - 137 #127:Max RSSI,137:RSSI offset

	return temp

"""*********************************************************
**Name: sx1276_7_8_LoRaRxPacket
**Function: Receive data in LoRa mode
**Input: None
**Output: 1- Success
 0- Fail
*********************************************************"""
def sx1276_7_8_LoRaRxPacket(Lora_Rate_Sel):

	i = None
	addr = None
	packet_size = None
	RxData = None

	if GPIO.input(dio0): #if(Get_NIRQ())

		addr = SPIRead(LR_RegFifoRxCurrentaddr) #last packet addr
		SPIWrite(LR_RegFifoAddrPtr,addr) #RxBaseAddr ->FiFoAddrPtr

		if sx1276_7_8SpreadFactorTbl[Lora_Rate_Sel] == 6: #WhenSpreadFactor is six,will used Implicit Header mode(Excluding internal packet length)
			packet_size=21
		else:
			packet_size = SPIRead(LR_RegRxNbBytes) #Number for received bytes 
		
		RxData = SPIBurstRead(0x00, packet_size)
		sx1276_7_8_LoRaClearIrq()
		
		if(i>=16): #Rx success
			return(RxData)
		else:
			return(0)
	else:
		return(0)


"""*********************************************************
**Name: sx1276_7_8_LoRaEntryTx
**Function: Entry Tx mode
**Input: None
**Output: None
*********************************************************"""
def sx1276_7_8_LoRaEntryTx():

	addr = None
	temp = None

	#sx1276_7_8_Config() #setting baseparameter

	SPIWrite(REG_LR_PADAC,0x87) #Tx for 20dBm
	SPIWrite(LR_RegHopPeriod,0x00) #RegHopPeriodNO FHSS
	SPIWrite(REG_LR_DIOMAPPING1,0x41) #DIO0=01, DIO1=00,DIO2=00, DIO3=01

	sx1276_7_8_LoRaClearIrq()
	SPIWrite(LR_RegIrqFlagsMask,0xF7) #Open TxDoneinterrupt
	SPIWrite(LR_RegPayloadLength,21) #RegPayloadLength21byte

	addr = SPIRead(LR_RegFifoTxBaseAddr) #RegFiFoTxBaseAddr
	SPIWrite(LR_RegFifoAddrPtr,addr) #RegFifoAddrPtr 
	#SysTime = 0;
	while(1):
		temp = SPIRead(LR_RegPayloadLength)
		if temp == 21:
			break
	#if(SysTime>=3)return 0;

	return
"""*********************************************************
**Name: sx1276_7_8_LoRaTxPacket
**Function: Send data in LoRa mode
**Input: None
**Output: 1- Send over
*********************************************************"""
def sx1276_7_8_LoRaTxPacket(DataTemp,leng):

	TxFlag = 0
	addr = None

	#BurstWrite2(0x00, sx1276_7_8Data, 2)
	BurstWrite2(0x00, DataTemp, leng)
	SPIWrite(LR_RegOpMode,0x8b) #Tx Mode

	while(1):
		if GPIO.input(dio0): #if(Get_NIRQ()) #Packet send over
			SPIRead(LR_RegIrqFlags)
			sx1276_7_8_LoRaClearIrq() #Clear irq
			sx1276_7_8_Standby() #Entry Standbymode
			break

	return

"""*********************************************************
**Name: sx1276_7_8_ReadRSSI
**Function: Read the RSSI value
**Input: none
**Output: temp, RSSI value
*********************************************************""" 
def sx1276_7_8_ReadRSSI():

	temp = 0xff

	temp = SPIRead(0x11)
	temp >>= 1
	temp = 127 - temp #127:Max RSSI
	return temp
"""*********************************************************
**Name: sx1276_7_8_Config
**Function: sx1276_7_8 base config
**Input: mode
**Output: None
*********************************************************"""
def sx1276_7_8_Config(mode, Freq_Sel, Power_Sel, Lora_Rate_Sel, BandWide_Sel, Fsk_Rate_Sel):

	sx1276_7_8_Sleep() #Change modem modeMust in Sleep mode
	time.sleep(0.1)

	#lora mode
	sx1276_7_8_EntryLoRa()
	#SPIWrite(0x5904); #?? Change digital regulator form 1.6V to 1.47V: see erratanote

	BurstWrite(LR_RegFrMsb,sx1276_7_8FreqTbl[Freq_Sel],3) #setting frequencyparameter
	#setting base parameter
	SPIWrite(LR_RegPaConfig,sx1276_7_8PowerTbl[Power_Sel]) #Settingoutput power parameter

	SPIWrite(LR_RegOcp,0x0B) #RegOcp,Close Ocp
	SPIWrite(LR_RegLna,0x23) #RegLNA,GPIO.HIGH & LNAEnable

	if sx1276_7_8SpreadFactorTbl[Lora_Rate_Sel]==6 :#SFactor=6
		
		SPIWrite(LR_RegModemConfig1,((sx1276_7_8LoRaBwTbl[BandWide_Sel]<<4)+(CR<<1)+0x01))
		#Implicit Enable CRC Enable(0x02) & Error Coding rate 4/5(0x01), 4/6(0x02),4/7(0x03), 4/8(0x04)
		SPIWrite(LR_RegModemConfig2,((sx1276_7_8SpreadFactorTbl[Lora_Rate_Sel]<<4)+(CRC<<2)+0x03))

		tmp = SPIRead(0x31)
		tmp &= 0xF8
		tmp |= 0x05
		SPIWrite(0x31,tmp)
		SPIWrite(0x37,0x0C)
		
	else:
		SPIWrite(LR_RegModemConfig1,((sx1276_7_8LoRaBwTbl[BandWide_Sel]<<4)+(CR<<1)+0x00)) 
		#Explicit Enable CRC Enable(0x02) & Error Coding rate 4/5(0x01), 4/6(0x02),4/7(0x03), 4/8(0x04)
		SPIWrite(LR_RegModemConfig2,((sx1276_7_8SpreadFactorTbl[Lora_Rate_Sel]<<4)+(CRC<<2)+0x03)) 
		#SFactor & LNA gain set by the internal AGC loop

	SPIWrite(LR_RegSymbTimeoutLsb,0xFF) #RegSymbTimeoutLsbTimeout = 0x3FF(Max)
	SPIWrite(LR_RegPreambleMsb,0x00) #RegPreambleMsb
	SPIWrite(LR_RegPreambleLsb,12) #RegPreambleLsb8+4=12byte Preamble
	SPIWrite(REG_LR_DIOMAPPING2,0x01) #RegDioMapping2DIO5=00, DIO4=01
	sx1276_7_8_Standby() #Entry standbymode

	return


def reset_sx1276():

    GPIO.output(reset, GPIO.LOW);
    time.sleep(0.01)
    GPIO.output(reset, GPIO.HIGH);
    time.sleep(0.02)

    return

"""****************************************************************"""
