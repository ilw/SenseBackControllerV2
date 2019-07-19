import sys
import numpy as np
from vispy import scene, visuals, app
import vispy.util
from vispy.visuals.transforms import (STTransform, LogTransform, MatrixTransform, PolarTransform)
import time
import array
import os
import glob
import datetime

N = 10000 # number of points
pos = np.zeros((N, 2), dtype=np.float32) # create zeroed array of 2D vertex positions of data to draw
xScale = 0.1
yScale = 0.5
x_lim = [0., xScale*N]
#y_lim = [0, 1024]
pos[:, 0] = np.linspace(x_lim[0], x_lim[1], N)
#pos[:, 1] = np.random.normal(size=N, scale=100, loc=400) # y coordinates are generated randomly



# color array
color = np.ones((N, 4), dtype=np.float32) # create a N * 4 array of ones with colour values
#color[:, 0] = np.linspace(0, 1, N) #column 0 is linearly between 0 and 1???
#color[:, 1] = color[::-1, 0]  # column 1 is filled with the contents of dimension 0 backwards

xsize = N * xScale
ysize=1024 #* yScale #10 bit data so 1024
canvas = scene.SceneCanvas(keys='interactive', size=(xsize, ysize), show=True) # create canvas object and show it
#path = '2019-06-28/'
currentDateTime = datetime.datetime.now()
path = currentDateTime.strftime("%Y-%m-%d") + '/'
print path
list_of_files = glob.glob(path+'*.bin') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print latest_file
filename = latest_file
writePos = 0
readPos = 0

fLength = 0
channel =0


def readInitialData():
    global filename,pos,N,fLength,readPos, channel
    with open(filename, 'rb') as f:
        fLength = os.stat(filename).st_size
        fdata = f.read()
        readPos = f.tell()
        f.close()

    if fLength %2 ==1:
        fdata = fdata[1:]
    #print(readPos)
    farray = array.array('H',fdata)    
    #print(farray[:10])
    farray.byteswap()
    #print(farray[:10])
    raw = [i for i in farray if ((i>32767+channel*1024) and (i<33792+channel*1024))]
    #raw = farray;
    if len(raw) >= N:
        rawslice = raw[-N:]
    else:
        rawslice = raw

    data = np.zeros((N,1))
    for i in range(0,len(rawslice)):
        data[(i+N-len(rawslice))] = ysize-rawslice[i]+32768+channel*1024
    
    writePos =0
    pos[:,1] = np.squeeze(data);


def readNewData():
    global N,writePos,readPos,filename,pos,channel
    with open(filename,'rb') as f:
        f.seek (0,2)
        endPos = f.tell()
        f.seek(readPos)
        if ((endPos-readPos)%2) == 1:
            # print("Odd Size")
            endPos=endPos-1
        readSize = endPos-readPos
        fdata = f.read(readSize)
        readPos = f.tell()
        f.close()
    farray = array.array('H',fdata)    
    farray.byteswap()
    raw = [i for i in farray if ((i>32767+channel*1024) and (i<33792+channel*1024))]
    if len(raw) >= N:
        rawslice = raw[-N:]  #shouldn't happen - consumer should be faster than producer
        print ('too much data')
    else:
        rawslice = raw
    writeLength = len(rawslice)    
    for i in range(0,writeLength):
        rawslice[i] = ysize-rawslice[i]+32768+channel*1024
    if writePos + writeLength > N :
        pos[writePos:,1] =  rawslice[:N-writePos]
        pos[:writeLength-N+writePos,1] =  rawslice[N-writePos:]
    else: 
        pos[writePos:writePos+writeLength,1] = rawslice 
    writePos +=writeLength
    writePos = writePos % N

        
readInitialData()
line = scene.Line(pos, color, parent=canvas.scene) # create a line with the positions and colours chosen
# line.transform = STTransform(scale=(xScale, yScale),translate=[0,0])
prevfLength = fLength


def update(ev):
    global pos, color, line, writePos, writeLength,filename,readPos,data,prevReadPos,prevfLength #access the global variables
    
    # if file has shrunk reset 
    fLength = os.stat(filename).st_size
    if     fLength < prevfLength:
        readInitialData()
    elif fLength > prevfLength:
        readNewData()
    prevfLength = fLength
    line.set_data(pos=pos, color=color)
    # line.transform = STTransform(scale=(xScale, yScale),translate=[0,0])
    #time.sleep(0.1)

timer = app.Timer(connect=update)#,interval=0.1) #interval gets ignored...
#timer.connect(update)
timer.start(0)

if __name__ == '__main__' and sys.flags.interactive == 0:
    app.run()