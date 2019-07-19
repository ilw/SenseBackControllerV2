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
        greeting = tk.Label(text="Senseback stim controller", font=BOLD)
        greeting.pack(side='top')
        
        # Create a frame for variable names and entry boxes for their values.
        frame = tk.Frame(master)
        frame.pack(side='top')
        
        #def enRec(ser,block,ch_bits,iir,A0,A1,LFP,LP,bits_hp,shift):
        
        
        
        
        # Create text boxes and entry boxes for the variables.
        # Use grid geometry manager instead of packing the entries in.
        ##############################################################
        row_counter = 0
        self.b_text = tk.Label(frame, text='Channel pairs:') 
        self.b_text.grid(row=row_counter, column=0)
        
        self.b_entry1 = tk.Spinbox(frame,from_=0,to_=31,width=8)
        self.b_entry1.grid(row=row_counter, column=1)
            
        self.b_entry2 = tk.Spinbox(frame,from_=0,to_=31,width=8)
        self.b_entry2.grid(row=row_counter, column=2)
        
        self.b_entry3 = tk.Spinbox(frame,from_=0,to_=31,width=8)
        self.b_entry3.grid(row=row_counter, column=3)
            
        self.b_entry4 = tk.Spinbox(frame,from_=0,to_=31,width=8)
        self.b_entry4.grid(row=row_counter, column=4)

        
        

        
        ##############################################################
        row_counter += 1
        self.amp_text = tk.Label(frame, text='Amp:') 
        self.amp_text.grid(row=row_counter, column=0)
        
        self.per_text = tk.Label(frame, text='Period:') 
        self.per_text.grid(row=row_counter, column=2)
        
        self.reps_text = tk.Label(frame, text='Reps:') 
        self.reps_text.grid(row=row_counter, column=4)
        
        self.amp = tk.IntVar()
        self.period = tk.IntVar()
        self.reps = tk.IntVar()
        
        self.ampIp = tk.Entry(frame)
        self.ampIp.insert(0,'10')
        self.periodIp = tk.Entry(frame)
        self.periodIp.insert(0,'255')
        self.repsIp = tk.Entry(frame)
        self.repsIp.insert(0,'1')
        
        
        self.ampIp.grid(row=row_counter, column=1)
        self.periodIp.grid(row=row_counter, column=3)
        self.repsIp.grid(row=row_counter, column=5)
        
        
        
        
        ##############################################################
        
        row_counter+=1
        self.stim = tk.Button(frame, command=self.stim, text="Stim!")
        self.stim.grid(row=row_counter, column=0)
        
        self.restart = tk.Button(frame,command=self.sbRestart, text="RESTART")
        self.restart.grid(row=row_counter, column=5)
        ##############################################################
        
        
        
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
            val = self.ser.read(100)
            if(val.__len__() > 0):
                self.opFile.write(val)   
                self.opFile.flush()
                print(val)
            
            if self.threadClose:
                break
    
    
    
    def initSerial(self,opFilename='testfile.bin'):
        self.ser = serial.Serial('COM13', baudrate=1000000, bytesize=8, parity='N', stopbits=1,timeout=0.01)
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
    def stim(self,event=None):
    
        self.stim.config(state="disabled")
        # Get these variables from outside the function, and update them.
        print('sending stim')
        
        
        print('channels ' + self.b_entry1.get(), self.b_entry2.get(), self.b_entry3.get(), self.b_entry4.get() )
        print('amplitude', self.ampIp.get())
        print('period', self.periodIp.get())
        print('reps', self.repsIp.get())

        
        sb.startSaving(self.ser)
        sb.enStim(self.ser,0,int(self.ampIp.get()),26, int(self.b_entry1.get()),int(self.b_entry2.get()),0,1,int(self.periodIp.get()),0,int(self.repsIp.get()))
        
        sb.enStim(self.ser,1,int(self.ampIp.get()),26, int(self.b_entry3.get()),int(self.b_entry4.get()),0,1,int(self.periodIp.get()),0,int(self.repsIp.get()))
        
        sb.enStimCfg(self.ser,0)
        # sb.enStimCfg(self.ser,1)
        sb.flush_buffer(self.ser)
        time.sleep(1)
        
        self.stim.config(state="normal")
        
        
    def sbRestart(self,event=None):
        sb.restartRx(self.ser)        
        self.opFile.write("NEW_DATA")
        #self.opFile.seek(0,0)


if __name__ == '__main__':
    root = tk.Tk()
    testGui = sbGUI(root)
    
    
    # Activate the window.
    root.mainloop()
    



