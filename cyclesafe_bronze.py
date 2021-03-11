import tkinter
from tkinter import Label, Button, Frame, StringVar
#from PIL import Image,ImageTk
from subprocess import call
import time
import threading
import random
import queue
import serial
import RPi.GPIO as GPIO


echoPIN = 24
triggerPIN = 18
     
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(echoPIN,GPIO.IN)
GPIO.setup(triggerPIN,GPIO.OUT)
GPIO.setwarnings(True)

ser = serial.Serial("/dev/ttyAMA0", 115200)
#ser.open()

class GuiPart:
    def __init__(self, window, queue, endCommand):
        self.queue = queue
        self.window = window
        # Set up the GUI
        # console = Tkinter.Button(master, text='Done', command=endCommand)
        # console.pack()
        # Add more GUI stuff here
        window.title("Cycle Safe")
        window.geometry("600x600")
        window.maxsize(600,600)



        self.prox_colour = "green"#default state
        self.prox_state = "All Clear!"#default state

        self.systext = "System Settings"
        self.LiDAR_data = "Initializing..."
        self.path = 'img/bicycle.png'

        #create a top frame and lower frame
        self.top_frame = Frame(window,width=600,height=100, bg="white")#could change frame colour based on proximity
        self.top_frame.pack()
        self.mid_frame = Frame(window, width=600, height=400, bg= self.prox_colour)#proximity determines colour
        self.mid_frame.pack()
        self.lower_frame = Frame(window,width=600,height=100,bg="white")
        #both parameter missing 
        self.lower_frame.pack()

        #display image on label widget
        # self.img = ImageTk.PhotoImage(Image.open(self.path).resize((100, 100), Image.ANTIALIAS))
        # self.lbl = Label(self.top_frame, image=self.img)
        # self.lbl2 = Label(self.lower_frame,image=self.img)
        # self.lbl.img = self.img  # Keep a reference in case this code put is in a function.
        # self.lbl2.img = self.img
        # self.lbl.place(x=0,y=0)
        # self.lbl2.place(x=400,y=20)

        #create text label on frame and add if statment to display different messages by changing labelText var
        self.labelText = self.prox_state 
        self.text1 = Label(self.top_frame,text=self.labelText, background=self.prox_colour)#can change background colour based on proximity
        self.text1.config(font=("Ariel",16))
        self.text1.config(width=30)
        self.text1.place(x=140,y=30)

        self.v = StringVar()
        self.v.set('old')

        self.btn_shutdown = Button(self.lower_frame,text="shutdown", command = self.shutDown)#shutdown preocedure for Pi
        self.btn_shutdown.place(x=50,y=30)
        self.text2 = Label(self.lower_frame,text="Text")
        self.text2.place(x=200,y=30)
        self.text3 = Label(self.lower_frame,text=self.systext)
        self.text3.place(x=450,y=30)

        #Shutdown function
    def shutDown(self):
        print("inside")
        call("sudo shutdown -h now", shell=True)

    # def setLidar(self,newText):
    #     print("INSIDE")
    #     self.v.set(newText)

    # def setLidar(self,newText):
    #     #self.v.set("Hello")
    #     #print(self.v.get())
    #     self.text2['text'] = newText


    def processIncoming(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        while self.queue.qsize():
            try:
                distance = self.queue.get_nowait()
                # Check contents of message and do what it says
                # As a test, we simply print it
                self.text2['text'] = distance
            except Queue.Empty:
                pass

    def changeColor(self,level):
        if level == 1:
            #print("inside level 1")
            self.mid_frame['bg'] = "red"
            self.text1['text'] ="DANGER"
            self.text1['bg'] = "red"
        elif level == 2:
            #print("inside level 2")
            self.mid_frame['bg'] = "yellow"
            self.text1['text'] ="car approaching"
            self.text1['bg'] = "yellow"
        else:
            #print("inside level 3")
            self.mid_frame['bg'] = "green"
            self.text1['text'] ="All Clear"
            self.text1['bg'] = "green"
    def errormessage(self):
        messagebox.showinfo("Error","please check ultrasonic sensors")

class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI. We spawn a new thread for the worker.
        """
        self.master = master

        # Create the queue of inifinite maxsize
        self.queue = queue.Queue(maxsize = 0)

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More can be made if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()

        # self.thread2 = threading.Thread(target=self.workerThread2)
        # self.thread2.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(100, self.periodicCall)

    def ultrasonic(self):
        #global distance 
     
            distance = 0
            duration = 0
            counter=0
            new_reading =False
            #send trigger
            GPIO.output(triggerPIN, 0)
            time.sleep(0.000002)
            GPIO.output(triggerPIN, 1)
            time.sleep(0.000010)
            GPIO.output(triggerPIN, 0)
            time.sleep(0.000002)
            
            # wait for echo reading
            while GPIO.input(echoPIN) == 0:
                pass
                counter +=1
                if counter==5000:
                    new_reading= True
                    break
            startT = time.time()

            if new_reading:
                return False
            
            while GPIO.input(echoPIN) == 1: pass
            feedbackT = time.time()

            # calculating distance
            if feedbackT == startT:
                distance = "N/A"
            else:
                duration = feedbackT - startT
            soundSpeed = 34300 # cm/s
            distance = duration * soundSpeed / 2
            distance = round(distance, 1)
            print('ultra(', distance)
            time.sleep(0.2)
            return distance
        

    def lidar(self):
        x=0
        distance = 0
        while x==0:
            #time.sleep(0.1)
            count = ser.in_waiting
            if count > 8:
                recv = ser.read(9)  
                ser.reset_input_buffer()  
                if recv[0] == 0x59 and recv[1] == 0x59:     
                    distance = recv[2] + recv[3]*256
                    strength = recv[4] + recv[5]*256
                    #print('Lidar (', distance, ',', strength, ')') #comment out if distance not needed
                    ser.reset_input_buffer()

            x=1
            return distance
    
    def algo(self,ultrasonicDistance,lidarDistance):
        #print("inside algorithm")
        if ultrasonicDistance < 100:
            return 1
        elif lidarDistance < 200:
            return 2
        else:
            return 3




    def workerThread1(self):
        while self.running:
            try:
                ultson_state=1
                lidar_state=0
                while True:
                    if ultson_state==1:
                        
                        ultrasonicDistance = self.ultrasonic()
                        #print (" ultra Distance : " + str(ultrasonicDistance())+ "   ")
                        self.queue.put(ultrasonicDistance)
                        ultson_state=0
                        lidar_state=1
                    if lidar_state==1:
                        if ser.is_open == False:
                            ser.open()
                        lidarDistance = self.lidar()
                        
                        ultson_state=1
                        lidar_state=0
                    state = self.algo(ultrasonicDistance,lidarDistance)
                    self.gui.changeColor(state)
            
            except KeyboardInterrupt:   # Ctrl+C
                if ser != None:
                    ser.close()
                    GPIO.cleanup()




  
    def endApplication(self):
        self.running = 0


rand = random.Random()
root = tkinter.Tk()
client = ThreadedClient(root)
root.mainloop()
