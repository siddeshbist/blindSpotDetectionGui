import tkinter as tk
from PIL import ImageTk, Image

window = tk.Tk()
window.title("Cycle Safe")

#create a top frame and lower frame
frame = tk.Frame(window,width=300,height=300,bg="tomato")
frame.pack()
lower_frame = tk.Frame(window,width=300,height=100,bg="black")
lower_frame.pack()

#create text label on frame and add if statment to display different messages by changing labelText var
labelText = "All Clear!" #white background is an issue !!!
text1 = tk.Label(frame,text=labelText)
text1.place(x=0,y=0)
text1.pack()

#import photos from direcotry and add if statment to upload different images 
#render = ImageTk.PhotoImage(Image.open("foo.png"))
#render = ImageTk.PhotoImage(Image.open("foo1.png"))
render = ImageTk.PhotoImage(Image.open("foo2.png"))
img = tk.Label(frame,image=render)
img.image = render
img.place(x=0,y=0)
img.pack()

#create widgets for lower frame
btn_shutdown = tk.Button(lower_frame,text="shutdown")
text2 = tk.Label(lower_frame,text="lidarSensor")
text3 = tk.Label(lower_frame,text="SystemSettings")

#arrange widgets inside lower frame
btn_shutdown.grid(row=0,column=0)
text2.grid(row=0,column=1)
text3.grid(row=0,column=2)


window.mainloop()

