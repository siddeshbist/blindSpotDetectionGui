import tkinter as tk
import tk_tools
from PIL import ImageTk, Image
from subprocess import call

window = tk.Tk()
window.title("Cycle Safe")
window.geometry("600x600")
prox_colour = "red"#default state
prox_state = "All Clear!"#default state
systext = "System Settings"
LiDAR_data = "Insert LiDAR readings"

#create a top frame and lower frame
top_frame = tk.Frame(window,width=600,height=600,bg="green")#could change frame colour based on proximity
top_frame.pack()
mid_frame = tk_tools.Gauge(window, height = 600, width = 600,min_value=4, max_value=0,label=LiDAR_data,unit="m",bg='grey')
mid_frame.pack()
lower_frame = tk.Frame(window,width=600,height=100,bg="black")
lower_frame.pack()

#create text label on frame and add if statment to display different messages by changing labelText var
labelText = prox_state 
text1 = tk.Label(top_frame,text=labelText, background=prox_colour)#can change background colour based on proximity
text1.place(x=0,y=0)
text1.pack()

#import photos from direcotry and add if statment to upload different images 
#render = ImageTk.PhotoImage(Image.open("foo.png"))
#render = ImageTk.PhotoImage(Image.open("foo1.png"))
##render = ImageTk.PhotoImage(Image.open("foo2.png"))
##img = tk.Label(frame,image=render)
##img.image = render
##img.place(x=0,y=0)
##img.pack()

#create widgets for lower frame
btn_shutdown = tk.Button(lower_frame,text="shutdown", background="teal")
##btn_shutdown = tk.Button(lower_frame,text="shutdown", command = shutDown)#shutdown preocedure for Pi
text2 = tk.Label(lower_frame,text=LiDAR_data)
text3 = tk.Label(lower_frame,text=systext)

#arrange widgets inside lower frame
btn_shutdown.grid(row=0,column=0)
text2.grid(row=0,column=1)
text3.grid(row=0,column=2)

#Shutdown function
##def shutDown():
##    call("sudo shutdown -h now", shell=True)
testdata=[1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,3,4]
x=0
def sensorinfo():
    global testdata
    global x
    print("into function")
    mid_frame.set_value(testdata[x])
    x=x+1

    window.after(1000,sensorinfo)
    
window.after(500, sensorinfo)    
window.mainloop()

