# -----------------------------------------------------------------------------
# sbGUI.py
# ----------------------------------------------------------------------------- 
"""
Author:     Ian 
Created:    2016 Apr 15
Modified:   2016 Apr 15

Description
-----------
Build a GUI to control recording settings.
"""

try:
    # This will work in Python 2.7
    import Tkinter as tk
except ImportError:
    # This will work in Python 3.5
    import tkinter as tk
        
        
import serial
import threading
import time
import datetime
import math
import array
import os


import numpy as np
from ctypes import *
from dwfconstants import *
import sys
import sbAPI_implantV2 as sb

class sbGUI:
    
    
    def sbStart(self,event=None):
        sb.startSaving(self.ser)
            
    def sbStop(self,event=None):
        for i in range(7):
            sb.enRec(self.ser,i,0,0,0,0,0,0,0,0)
            time.sleep(0.5)
        sb.stopSaving(self.ser)
    
    def sbRestartRx(self,event=None):
        sb.restartRx(self.ser)        
        self.opFile.write("NEW_DATA")
        #self.opFile.seek(0,0)
    
    
    def __init__(self,master,opFilename='testfile.bin'):
        
       
        self.master = master
        
        currentDateTime = datetime.datetime.now()
        currentDate= currentDateTime.strftime("%Y-%m-%d")
        currentTime = currentDateTime.strftime("%H%M")
        if not os.path.exists(currentDate) : 
            os.mkdir(currentDate)
    
        opFilename = currentDate+"/data_op"+currentTime+".bin"
        self.initSerial(opFilename)
        
        self.master.protocol("WM_DELETE_WINDOW", self.exitGUI)
        # Define a bold font:
        BOLD = ('Courier', '24', 'bold')
              
        
        # Create a text box explaining the application.
        greeting = tk.Label(text="Senseback controller", font=BOLD)
        greeting.pack(side='top')
        
        # Create a frame for variable names and entry boxes for their values.
        frame = tk.Frame(master)
        frame.pack(side='top')
        
        #def enRec(ser,block,ch_bits,iir,A0,A1,LFP,LP,bits_hp,shift):
        
        # Variables for the calculation, and default values.
        self.block = tk.StringVar()
        self.block.set('0')
        
        
        
        # Create text boxes and entry boxes for the variables.
        # Use grid geometry manager instead of packing the entries in.
        ##############################################################
        row_counter = 0
        self.b_text = tk.Label(frame, text='Block:') 
        self.b_text.grid(row=row_counter, column=0)
        
        self.b_entry = tk.Spinbox(frame,from_=0,to_=7,width=8)
        self.b_entry.grid(row=row_counter, column=1)
        ##############################################################
        row_counter += 1
        self.c_text = tk.Label(frame, text='Channel:') 
        self.c_text.grid(row=row_counter, column=0)
        
        self.c1 = tk.IntVar()
        self.c2 = tk.IntVar()
        self.c3 = tk.IntVar()
        self.c4 = tk.IntVar()
        
        self.cCheck1 = tk.Checkbutton(frame,variable=self.c1)
        self.cCheck2 = tk.Checkbutton(frame,variable=self.c2)
        self.cCheck3 = tk.Checkbutton(frame,variable=self.c3)
        self.cCheck4 = tk.Checkbutton(frame,variable=self.c4)
        
        
        
        
        self.cCheck1.grid(row=row_counter, column=1)
        self.cCheck2.grid(row=row_counter, column=2)
        self.cCheck3.grid(row=row_counter, column=3)
        self.cCheck4.grid(row=row_counter, column=4)
        
        ##############################################################
        row_counter += 1
        self.d_text = tk.Label(frame, text='Detect_en:') 
        self.d_text.grid(row=row_counter, column=0)
        
        self.d1 = tk.IntVar()
        self.d2 = tk.IntVar()
        self.d3 = tk.IntVar()
        self.d4 = tk.IntVar()
        
        self.dCheck1 = tk.Checkbutton(frame,variable=self.d1)
        self.dCheck2 = tk.Checkbutton(frame,variable=self.d2)
        self.dCheck3 = tk.Checkbutton(frame,variable=self.d3)
        self.dCheck4 = tk.Checkbutton(frame,variable=self.d4)
        
        
        
        
        self.dCheck1.grid(row=row_counter, column=1)
        self.dCheck2.grid(row=row_counter, column=2)
        self.dCheck3.grid(row=row_counter, column=3)
        self.dCheck4.grid(row=row_counter, column=4)
        

        ##############################################################
        row_counter += 1
        self.th_text = tk.Label(frame, text='Thresh:') 
        self.th_text.grid(row=row_counter, column=0)
        
        self.th1 = tk.IntVar()
        self.th2 = tk.IntVar()
        self.th3 = tk.IntVar()
        self.th4 = tk.IntVar()
        
        self.cCheck1Thresh = tk.Entry(frame,text=self.th1)
        self.cCheck2Thresh = tk.Entry(frame,text=self.th2)
        self.cCheck3Thresh = tk.Entry(frame,text=self.th3)
        self.cCheck4Thresh = tk.Entry(frame,text=self.th4)
        
        self.th1.set(255)
        self.th2.set(255)
        self.th3.set(255)
        self.th4.set(255)

        
        
        self.cCheck1Thresh.grid(row=row_counter, column=1)
        self.cCheck2Thresh.grid(row=row_counter, column=2)
        self.cCheck3Thresh.grid(row=row_counter, column=3)
        self.cCheck4Thresh.grid(row=row_counter, column=4)


        
        ##############################################################
        row_counter += 1
        self.g_text = tk.Label(frame, text='Gain:') 
        self.g_text.grid(row=row_counter, column=0)
        
        self.gOptionList = ('4725','270','2138','225')

        
        self.gVal1 = tk.StringVar()
        self.gVal2 = tk.StringVar()
        self.gVal3 = tk.StringVar()
        self.gVal4 = tk.StringVar()
        
        self.g1= tk.OptionMenu(frame,self.gVal1,*self.gOptionList)
        self.g2= tk.OptionMenu(frame,self.gVal2,*self.gOptionList)
        self.g3= tk.OptionMenu(frame,self.gVal3,*self.gOptionList)
        self.g4= tk.OptionMenu(frame,self.gVal4,*self.gOptionList)
        
        self.gVal1.set(self.gOptionList[0])
        self.gVal2.set(self.gOptionList[0])
        self.gVal3.set(self.gOptionList[0])
        self.gVal4.set(self.gOptionList[0])
        
        self.g1.grid(row=row_counter, column=1)
        self.g2.grid(row=row_counter, column=2)
        self.g3.grid(row=row_counter, column=3)
        self.g4.grid(row=row_counter, column=4)
        
        
        ##############################################################
        row_counter += 1
        self.lfp_text = tk.Label(frame, text='LFP enable:') 
        self.lfp_text.grid(row=row_counter, column=0)
        
        self.lfp1 = tk.IntVar()
        self.lfp2 = tk.IntVar()
        self.lfp3 = tk.IntVar()
        self.lfp4 = tk.IntVar()
        
        self.lfpCheck1 = tk.Checkbutton(frame,variable=self.lfp1)
        self.lfpCheck2 = tk.Checkbutton(frame,variable=self.lfp2)
        self.lfpCheck3 = tk.Checkbutton(frame,variable=self.lfp3)
        self.lfpCheck4 = tk.Checkbutton(frame,variable=self.lfp4)
        
        self.lfpCheck1.grid(row=row_counter, column=1)
        self.lfpCheck2.grid(row=row_counter, column=2)
        self.lfpCheck3.grid(row=row_counter, column=3)
        self.lfpCheck4.grid(row=row_counter, column=4)
        
        ##############################################################
        row_counter += 1
        self.lp_text = tk.Label(frame, text='Low Pass filter:') 
        self.lp_text.grid(row=row_counter, column=0)
        
        self.lp1 = tk.IntVar()
        self.lp2 = tk.IntVar()
        self.lp3 = tk.IntVar()
        self.lp4 = tk.IntVar()
        
        self.lpCheck1 = tk.Checkbutton(frame,variable=self.lp1)
        self.lpCheck2 = tk.Checkbutton(frame,variable=self.lp2)
        self.lpCheck3 = tk.Checkbutton(frame,variable=self.lp3)
        self.lpCheck4 = tk.Checkbutton(frame,variable=self.lp4)
        
        self.lpCheck1.grid(row=row_counter, column=1)
        self.lpCheck2.grid(row=row_counter, column=2)
        self.lpCheck3.grid(row=row_counter, column=3)
        self.lpCheck4.grid(row=row_counter, column=4)
        
        ##############################################################
        row_counter += 1
        self.hp_text = tk.Label(frame, text='High Pass filter:') 
        self.hp_text.grid(row=row_counter, column=0)
        
        
        self.hpOptionList = np.linspace(560,15,31).astype(int)
        self.hpVal = tk.StringVar()
        self.hpOpt= tk.OptionMenu(frame,self.hpVal,*self.hpOptionList)
        self.hpVal.set(self.hpOptionList[0])
        self.hpOpt.grid(row=row_counter, column=1)
        
        
        #self.hp_entry = tk.Spinbox(frame,from_=0,to_=31,width=8)
        #self.hp_entry.grid(row=row_counter, column=1)
        
        ##############################################################
        row_counter += 1
        self.iir_text = tk.Label(frame, text='iir enable:') 
        self.iir_text.grid(row=row_counter, column=0)
        
        self.iir1 = tk.IntVar()
        self.iir2 = tk.IntVar()
        self.iir3 = tk.IntVar()
        self.iir4 = tk.IntVar()
        
        self.iirCheck1 = tk.Checkbutton(frame,variable=self.iir1)
        self.iirCheck2 = tk.Checkbutton(frame,variable=self.iir2)
        self.iirCheck3 = tk.Checkbutton(frame,variable=self.iir3)
        self.iirCheck4 = tk.Checkbutton(frame,variable=self.iir4)
        
        self.iirCheck1.grid(row=row_counter, column=1)
        self.iirCheck2.grid(row=row_counter, column=2)
        self.iirCheck3.grid(row=row_counter, column=3)
        self.iirCheck4.grid(row=row_counter, column=4)
        
        ##############################################################
        row_counter += 1
        self.iir_text = tk.Label(frame, text='High Pass IIR:') 
        self.iir_text.grid(row=row_counter, column=0)
        
        #self.iirOptionList = ('1764.8', '732.64', '340', '164.32', '80.848', '40.096', '19.968', '9.9664', '4.9792')
        self.iirOptionList = ( '732.64', '340', '164.32', '80.848', '40.096', '19.968', '9.9664', '4.9792')
        self.iirVal = tk.StringVar()
        self.iirOpt= tk.OptionMenu(frame,self.iirVal,*self.iirOptionList)
        self.iirVal.set(self.iirOptionList[0])
        self.iirOpt.grid(row=row_counter, column=1)
        
        ##############################################################
        
        row_counter+=1
        self.startSave = tk.Button(frame, command=self.sbStart, text="Start")
        self.startSave.grid(row=row_counter, column=0)
        
        self.stopSave = tk.Button(frame, command=self.sbStop, text="Stop")
        self.stopSave.grid(row=row_counter, column=1)

        self.restartRX = tk.Button(frame,command=self.sbRestartRx, text="RESTART")
        self.restartRX.grid(row=row_counter, column=4)
        ##############################################################
        
        # Add a button to create the plot.
        uploadConfig = tk.Button(master, command=self.sendConfig, text="Send Configuration")
        uploadConfig.pack(side='bottom', fill='both')
        
        
        # Allow pressing <Esc> to close the window.
        master.bind('<Escape>', self.closeGUI)
        
    
    
    def closeGUI(self,event):
        self.exitGUI()
    
    def exitGUI(self):
        self.threadClose=True
        self.ser.close()
        self.opFile.close()
        self.master.destroy()
    
    def serMonitor(self):
        #valArray= bytearray(500)
        while True:
            bytesToRead = self.ser.inWaiting()
            val = self.ser.read(bytesToRead)
            if(val.__len__() > 0):
                self.opFile.write(val)   
                self.opFile.flush()
            
            if self.threadClose:
                break
    
    
    
    def initSerial(self,opFilename='testfile.bin'):
        self.ser = serial.Serial('COM13', baudrate=1000000, bytesize=8, parity='N', stopbits=1,timeout=None)
        self.ser.set_buffer_size(rx_size = 32768, tx_size = 32768)
        #self.ser = serial.Serial('COM21', baudrate=3750000, bytesize=8, parity='N', stopbits=1,timeout=0.01)
        #output dump file
        self.opFile = open(opFilename,'wb') 
        #flag to close thread
        self.threadClose=False
        #thread to monitor the serial port and dump to a file
        t = threading.Thread(name='serMonitor', target=self.serMonitor)
        t.daemon = True
        t.start()


    # Define a function to create the desired plot.
    def sendConfig(self,event=None):
        # Get these variables from outside the function, and update them.
        print('in sendConfig')
        gain1 = self.gOptionList.index(self.gVal1.get())
        gain2 = self.gOptionList.index(self.gVal2.get())
        gain3 = self.gOptionList.index(self.gVal3.get())
        gain4 = self.gOptionList.index(self.gVal4.get())
        
        th1 = int(self.cCheck1Thresh.get())
        th2 = int(self.cCheck2Thresh.get())
        th3 = int(self.cCheck3Thresh.get())
        th4 = int(self.cCheck4Thresh.get() )       
        
        print('block ', self.b_entry.get())
        print('channel bits ', self.c1.get()+2*self.c2.get()+4*self.c3.get() + 8*self.c4.get())
        print('Detect enable bits ', self.d1.get()+2*self.d2.get()+4*self.d3.get() + 8*self.d4.get())
        print('Thresholds: ' + str(th1) + ', '+ str(th2) + ', '+ str(th3) + ', ' + str(th4))
        print('gain ', gain1,gain2,gain3,gain4)
        print('lfp ',  self.lfp1.get()+2*self.lfp2.get()+4*self.lfp3.get()+8*self.lfp4.get())
        print('lp ', self.lp1.get()+2*self.lp2.get()+4*self.lp3.get()+8*self.lp4.get())
        print('hp ',self.hpOptionList.tolist().index(int(self.hpVal.get())))
        print('iir ', self.iir1.get()+2*self.iir2.get()+4*self.iir3.get()+8*self.iir4.get())
        print('iir freq shift' , self.iirOptionList.index(self.iirVal.get())+1)
        print('A0' ,(gain1 & 1)+ 2*(gain2 & 1) +4*(gain3 & 1)+8*(gain4 & 1))
        print( 'A1' ,((gain1 & 2)+ 2*(gain2 & 2) +4*(gain3 & 2)+8*(gain4 & 2))/2)

        
        
        block = int(self.b_entry.get())
        ch_bits = self.c1.get()+2*self.c2.get()+4*self.c3.get() + 8*self.c4.get()
        det_en = self.d1.get()+2*self.d2.get()+4*self.d3.get() + 8*self.d4.get()
        iir = self.iir1.get()+2*self.iir2.get()+4*self.iir3.get()+8*self.iir4.get()
        A0 = (gain1 & 1)+ 2*(gain2 & 1) +4*(gain3 & 1)+8*(gain4 & 1)
        A1 = ((gain1 & 2)+ 2*(gain2 & 2) +4*(gain3 & 2)+8*(gain4 & 2))/2
        LFP = self.lfp1.get()+2*self.lfp2.get()+4*self.lfp3.get()+8*self.lfp4.get()
        LP = self.lp1.get()+2*self.lp2.get()+4*self.lp3.get()+8*self.lp4.get()
        bits_hp = self.hpOptionList.tolist().index(int(self.hpVal.get()))
        shift =  self.iirOptionList.index(self.iirVal.get())+1
        
        sb.enRec(self.ser,block,ch_bits,iir,A0,A1,LFP,LP,bits_hp,shift,det_en,th1,th2,th3,th4)
        
        


if __name__ == '__main__':
    root = tk.Tk()
    testGui = sbGUI(root)
    
    
    # Activate the window.
    root.mainloop()
    



