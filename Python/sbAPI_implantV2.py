import numpy as np
from ctypes import *
import serial
import time
import math

def startSaving(ser):
    pass
    # ser.write(chr(np.uint8(0)))
    # ser.write(chr(np.uint8(103)))
    # ser.write(chr(np.uint8(23)))

def stopSaving(ser):
    pass
    # ser.write(chr(np.uint8(0)))
    # ser.write(chr(np.uint8(102)))
    # ser.write(chr(np.uint8(35)))
    

def sendData(ser):
  
    ser.write(chr(np.uint8(255)))
    ser.write(chr(np.uint8(0)))
    ser.flush
  
def readCfg(ser,cfgRegister,cfgByte,reqId):
    if (cfgRegister>31) or (cfgRegister <0) or (reqId <0) or (reqId > 31) or (cfgByte <0) or (cfgByte >7):
        print 'cfg_register 0-31, req_id 0-31, cfgByte 0-7'
        return
    
    REG_READ_CFG = np.uint8(64);
    ser.write(chr(REG_READ_CFG | np.uint8(cfgRegister) ))
    ser.write(chr((np.uint8(cfgByte)<<5) | np.uint8(reqId)))
    
    
def readReg(ser, register,reqId):
    if register>15 or register <0 or reqId <0 or reqId > 31:
        print 'register 0 - 15, req_id 0 - 31'
        return
    

    REG_READ_CMD = np.uint8(48);
    ser.write(chr(  REG_READ_CMD | np.uint8(register) ))
    ser.write(chr(np.uint8(reqId)))

    

def writeCfg(ser, cfgRegister,cfgByte,data):
    if cfgRegister>31 or  cfgRegister <0 or  data <0 or  data > 255 or  cfgByte <0 or  cfgByte >7 :
        print 'cfg_register 0-31, data 0-255, cfg_byte 0-7'
        return    
 
    CFG_WRITE_CMD = np.uint8(192);  
    data_h_nibble = (np.uint8(data)>>4)  | (np.uint8(16) )
    data_l_nibble = np.uint8(15) & np.uint8(data)  
    ser.write(chr((CFG_WRITE_CMD  | np.uint8(cfgRegister)) ))
    ser.write(chr((np.uint8(cfgByte)<<5) | data_h_nibble)   )    
    ser.write(chr((CFG_WRITE_CMD  | np.uint8(cfgRegister)) ))
    ser.write (chr(((np.uint8(cfgByte)<<5) | data_l_nibble) )  )
    


def writeReg(ser,register,data):
    if register>15 or register <0 or data <0 or data > 255:
        print 'register 0-15, data 0-255'
        return    
        

    
    REG_WRITE_CMD = np.uint8(176);
    ser.write(chr((REG_WRITE_CMD | np.uint8(register)) ))
    ser.write(chr( np.uint8(data)))
    
    
    
    
    
def enStimCfg(ser,stimCfg):
    if stimCfg >31 | stimCfg<0 :
        print "stim_cfg should be an integer between 0 and 31"
        return
    register =9 + math.floor(stimCfg/8);
    val = np.uint8(1 << (stimCfg % 8)) #check this shifts correctly
    writeReg(ser,register,val);
    
    sendData(ser)
    
def enRec(ser,block,ch_bits,iir,A0,A1,LFP,LP,bits_hp,shift,det_en=0,thresh0=255,thresh1=255,thresh2=255,thresh3=255):
    if ch_bits>15 | ch_bits<0 | iir>15 | iir <0 | A0>15 | A0<0 | \
            A1>15 | A1<0 |LFP>15 | LFP<0 | LP>15 | LP<0 | block>7 \
            | block<0 | bits_hp >31 | bits_hp<0 | shift <0 | shift >9 \
            | spd<0 |spd>15 | det_en<0 | det_en>15:
        print ("Error ch_bits<16, iir<16, A0<16, A1<16, LFP<16,LP<16, block<8, bits_hp<32, shift should be 1 - 9 if using iir")
        return
    
    
    byte0 = int('{:08b}'.format(ch_bits<<4 | det_en)[::-1], 2) #reverses order of bits in a byte
    #byte1 = int('{:08b}'.format( iir | (shift<<4))[::-1], 2)   
    byte1 = int('{:08b}'.format( (iir<<4) | shift)[::-1], 2)   
    byte2 = int('{:08b}'.format((A1<<4)|A0)[::-1], 2) 
    byte3 = int('{:08b}'.format((LFP<<4) |LP)[::-1], 2)
    byte4 = int('{:08b}'.format(thresh0)[::-1], 2)
    byte5 = int('{:08b}'.format(thresh1)[::-1], 2)
    byte6 = int('{:08b}'.format(thresh2)[::-1], 2)
    byte7 = int('{:08b}'.format(thresh3)[::-1], 2)
    byte13 = int('{:08b}'.format(bits_hp<<3)[::-1], 2) #TODO Should i be shifting this by 3 bits??
    #byte13 = (bits_hp<<3) #TODO Should i be shifting this by 3 bits??
    byte8 = block   | 8
    

    
    #print ('A0',A0,'A1',A1,str(byte2))
    writeReg(ser,0,byte0);
    writeReg(ser,1,byte1);
    writeReg(ser,2,byte2);
    writeReg(ser,3,byte3);
    writeReg(ser,4,byte4);
    writeReg(ser,5,byte5);
    writeReg(ser,6,byte6);
    writeReg(ser,7,byte7);
    writeReg(ser,13,byte13);
    writeReg(ser,8,byte8);
    
    sendData(ser)

    
    
    
    
def enStim(ser,stim_cfg,stim_amp,phase_dur, stim_chan_a,stim_chan_b,asymm,interphase,period,ramp,reps):
    if stim_cfg >31 | stim_cfg<0 | \
    stim_amp > 255|  stim_amp <0 | \
    phase_dur > 255|  phase_dur <0 |\
     stim_chan_a > 31|  stim_chan_a <0 |\
    stim_chan_b > 31|  stim_chan_b <0 |\
    asymm > 3|  asymm < 0|\
    interphase > 255|  interphase <0 |\
    period > 255|  period < 0|\
    ramp > 255|  ramp < 0|\
    reps > 255|  reps < 0:
        print "error in vals all are 8 bit except asymm which is 2 bit and chan is 5 bit"
        return



    writeCfg(ser,stim_cfg,0,stim_amp)
    writeCfg(ser,stim_cfg,1,phase_dur)
    writeCfg(ser,stim_cfg,2,stim_chan_a | (asymm<<6))
    writeCfg(ser,stim_cfg,3,stim_chan_b)
    writeCfg(ser,stim_cfg,4,interphase)
    writeCfg(ser,stim_cfg,5,period)
    writeCfg(ser,stim_cfg,6,ramp)
    writeCfg(ser,stim_cfg,7,reps)
    

    sendData(ser)
    
    
def restartRx(ser):

    
    ser.flush
    
    
def flush_buffer(ser):

    
    ser.flush