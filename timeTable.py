from Tkinter import *
import mvg_api
import threading
import time

#Get Departures
idStation = mvg_api.get_id_for_station("Ostbahnhof")

#Set Types to show
typesToShow=['u', 'b']

#Start TKinter dialog
top = Tk()

#Define Threading class
class myThread (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      while not stopEvent.is_set():
         updateTimes()
         stopEvent.wait(10)
     
   
def exitButton():
   stopEvent.set()
   top.destroy()

def subwayButton():
   print "Test"

def updateTimes():

   departures = mvg_api.get_departures(idStation)

   #Fill dialog with departures   
   print "Update Times..."   

   depNumber=0
   for departure in departures:
      strDestination = departure['destination']
      strProduct = departure['product']
      strLabel = departure['label']
      strLineBackgroundColor = departure['lineBackgroundColor']
      strDepartureMin = departure['departureTimeMinutes']

      strText = strProduct, strLabel, strDestination, strDepartureMin
      
      if strProduct in typesToShow:
         var = labelContent[depNumber]
         label = labels[depNumber]
         var.set(strText)
         label.config(bg=strLineBackgroundColor)
         depNumber += 1

#Make it resizeable, when window is expanded
top.grid_rowconfigure(0, weight=1)
top.grid_columnconfigure(0, weight=1)

#Define Frames
typeFrame = Frame(top)
typeFrame.grid_columnconfigure(0, weight=1)
typeFrame.grid_rowconfigure(0, weight=1)
typeFrame.grid(row=0, column=0, sticky="nsew")

subwayButton = Button(typeFrame, text="U-Bahn")
subwayButton.pack(fill = X, expand=1)

busButton = Button(typeFrame, text="Bus")
busButton.pack(fill = X, expand=1)

#Frame
listFrame = Frame(top)
listFrame.grid_columnconfigure(0, weight=1)
listFrame.grid_rowconfigure(0, weight=1)
listFrame.grid(row=0, column=0, sticky="nsew")

#Define Buttons
b = Button(listFrame, text="Exit", command=exitButton)
b.pack( fill=X, expand=0 )

#Define Frame to hold Labels for lines to whow
labelFrame = Frame(listFrame)
labelFrame.pack(fill=BOTH, expand=1)

labelContent = []
labels = []
for i in range(30):
   var = StringVar()
   var.set(i)
   labelContent.append(var)
   label=Label(labelFrame, textvariable=var)
   label.grid_columnconfigure(0, weight=1, pad=1000)
   label.grid(row=i, column=0, sticky='w')
   labels.append(label)

#Start UpdateThread
stopEvent = threading.Event()
thread = myThread()
thread.start()

top.attributes('-fullscreen', True)
top.mainloop()
