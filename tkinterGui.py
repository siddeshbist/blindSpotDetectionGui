import tkinter as tk
from PIL import Image,ImageTk
from subprocess import call

window = tk.Tk()
window.title("Cycle Safe")
window.geometry("600x600")
window.maxsize(600,600)
prox_colour = "yellow"#default state
prox_state = "Object Approaching"#default state
systext = "System Settings"
LiDAR_data = "5.0 m"
path = 'img/bicycle.png'



#create a top frame and lower frame
top_frame = tk.Frame(window,width=600,height=100, bg="white")#could change frame colour based on proximity
top_frame.pack()
mid_frame = tk.Frame(window, width=600, height=400, bg=prox_colour)#proximity determines colour
mid_frame.pack()
lower_frame = tk.Frame(window,width=600,height=100,bg="white")
lower_frame.pack(fill=tk.BOTH)

#display image on label widget
img = ImageTk.PhotoImage(Image.open(path).resize((100, 100), Image.ANTIALIAS))
lbl = tk.Label(top_frame, image=img)
lbl2 = tk.Label(lower_frame,image=img)
lbl.img = img  # Keep a reference in case this code put is in a function.
lbl2.img = img
lbl.place(x=0,y=0)
lbl2.place(x=400,y=20)

#create text label on frame and add if statment to display different messages by changing labelText var
labelText = prox_state 
text1 = tk.Label(top_frame,text=labelText, background=prox_colour)#can change background colour based on proximity
text1.config(font=("Ariel",16))
text1.config(width=30)
text1.place(x=140,y=30)

#Shutdown function
def shutDown():
   #call("sudo shutdown -h now", shell=True)
   print("function activated")


btn_shutdown = tk.Button(lower_frame,text="shutdown", command = shutDown)#shutdown preocedure for Pi
btn_shutdown.place(x=50,y=30)
text2 = tk.Label(lower_frame,text=LiDAR_data)
text2.place(x=200,y=30)
text3 = tk.Label(lower_frame,text=systext)
text3.place(x=450,y=30)


window.mainloop()

