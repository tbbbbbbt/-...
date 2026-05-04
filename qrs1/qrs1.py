import serial
import matplotlib.pyplot as plt

ser = serial.Serial("COM6", 115200)
plt.ion()

while True:
    line = ser.readline().decode('utf-8', 'ignore').strip() 
    
    if line and len(line) > 5: 
        data = [float(x) for x in line.split(',')]
        plt.clf()
        plt.plot(data, 'r-o', linewidth=2)
        plt.pause(0.01)
        