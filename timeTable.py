from Tkinter import *
import mvg_api
import threading
import time

#Get Departures
idStation = mvg_api.get_id_for_station("Ostbahnhof")

#Set Types to show
typesToShow=['u', 'b', 's']

#Start TKinter dialog
top = Tk()

#Define Threading class
class myThread (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      while not stopEvent.is_set():
         updateTimes()
         stopEvent.wait(30)
     
   
def exitButton():
   print "Exit"
   stopEvent.set()
   top.destroy()

def busButton():
   print "BusButton"
    
   if 'b' in typesToShow:
      typesToShow.remove('b')
   else:
      typesToShow.append('b')
      
   print typesToShow
   updateTimes()

def subwayButton():
   print "Test"
   
   if 'u' in typesToShow:
      typesToShow.remove('u')
   else:
      typesToShow.append('u')
   
   updateTimes()
      
def sbahnButton():
   print "Test"
   
   if 's' in typesToShow:
      typesToShow.remove('s')
   else:
      typesToShow.append('s')

   updateTimes()

def updateTimes():

   departures = mvg_api.get_departures(idStation)
   departures = departures[:8]

   #Fill dialog with departures   
   print "Update Times..."   

   depNumber=0
   for departure in departures:
      
      #Get information from mvg_api
      strDestination = departure['destination'][:17]
      strProduct = departure['product']
      strLabel = departure['label']
      strLineBackgroundColor = departure['lineBackgroundColor']
      strDepartureMin = departure['departureTimeMinutes']

      strText = strProduct, strLabel, strDestination, strDepartureMin
      
      #check, if current Product should be shown
      if strProduct in typesToShow:
         
         timeEntryDict = timeTableEntries[depNumber]
         varLine = timeEntryDict['Line']
         varLine.set(strProduct + strLabel)
         labelLine = timeEntryDict['labelLine']
         labelLine.config(bg=strLineBackgroundColor)
         
         varDestination = timeEntryDict['Destination']
         varDestination.set(strDestination)
         
         varTimeLeft = timeEntryDict['TimeLeft']
         varTimeLeft.set(strDepartureMin)          
         
         depNumber += 1

#Make it resizeable, when window is expanded
#top.grid_rowconfigure(0, weight=1)
top.grid_columnconfigure(0, weight=1)

#Define Frames
#typeFrame = Frame(top)
#typeFrame.grid_columnconfigure(0, weight=1)
#typeFrame.grid_rowconfigure(0, weight=1)
#typeFrame.grid(row=0, column=0, sticky="nsew")

#subwayButton = Button(typeFrame, text="U-Bahn")
#subwayButton.pack(fill = X, expand=1)

#busButton = Button(typeFrame, text="Bus")
#busButton.pack(fill = X, expand=1)

#Frame
#listFrame = Frame(top)
#listFrame.grid_columnconfigure(0, weight=1)
#listFrame.grid_rowconfigure(0, weight=1)
#listFrame.grid(row=0, column=0, sticky="nsew")

#Define Buttons
b = Button(top, text="Exit", command=exitButton)
b.grid(row=0, column=0, columnspan=3, sticky='we')

buttonBus = Button(top, text="Bus", command=busButton)
buttonBus.grid(row=1, column=0, sticky='we')

buttonSubway = Button(top, text="U-Bahn", command=subwayButton)
buttonSubway.grid(row=1, column=1, sticky='we')

buttonSBahn = Button(top, text="S-Bahn", command=sbahnButton)
buttonSBahn.grid(row=1, column=2, sticky='we')

#Define Frame to hold Labels for lines to whow
labelFrame = Frame(top)
labelFrame.grid(row=2, column=0, columnspan=3, sticky='we')

timeTableEntries = []
labelContent = []
labels = []
for i in range(30):
   varLine = StringVar()
   varLine.set('')
   labelLine = Label(labelFrame, textvariable=varLine, fg='white', font=("Arial", 12))
   labelLine.grid(row=i, column=0, sticky='we')
   
   varDestination = StringVar()
   varDestination.set('')
   labelDestination = Label(labelFrame, textvariable=varDestination, font=("Arial", 12))
   labelDestination.grid(row=i, column=1, sticky='w')
   
   varTimeLeft = StringVar()
   varTimeLeft.set('')
   labelTimeLeft = Label(labelFrame, textvariable=varTimeLeft, font=("Arial", 12))
   labelTimeLeft.grid(row=i, column=2, sticky='we')
   
   timeEntryDict = {'Line' : varLine, 'labelLine' : labelLine, 'Destination' : varDestination, 'labelDestination' : labelDestination,
                    'TimeLeft' : varTimeLeft, 'labelTimeLeft' : labelTimeLeft}
   
   timeTableEntries.append(timeEntryDict)

#Start UpdateThread
stopEvent = threading.Event()
thread = myThread()
thread.start()

top.attributes('-fullscreen', True)
top.mainloop()
