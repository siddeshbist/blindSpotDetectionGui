import time
import threading
import serial

distance=0
ser = serial.Serial("/dev/ttyAMA0", 115200)

def in_thread():
    global distance
    print("in thread")
    while(1):
        count = ser.in_waiting
        if count > 8:
            recv = ser.read(9)  
            ser.reset_input_buffer()  
            # type(recv), 'str' in python2(recv[0] = 'Y'), 'bytes' in python3(recv[0] = 89)
            # type(recv[0]), 'str' in python2, 'int' in python3 
            
            if recv[0] == 0x59 and recv[1] == 0x59:     #python3
                distance = recv[2] + recv[3]*256
                strength = recv[4] + recv[5]*256
                #print('(', distance, ',', strength, ')')
                ser.reset_input_buffer()
    

def main():
    global distance
    x=threading.Thread(target=in_thread)
    x.start()
    while(1):
        print("Sensor Reading")
        print(distance)

if __name__ == "__main__":
    try:
        if ser.is_open == False:
            ser.open()
        main()
    except KeyboardInterrupt:   # Ctrl+C
        if ser != None:
            ser.close()
    #main()
