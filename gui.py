from tkinter import *
from tkinter import font
import call_mp3 as c
import os
import ctypes

#Hide Console
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

#Variables
errorLabel = ""
errorCalled = False
currentTime = ""
currentTimeLabel = ""
delayTime = 0
delayedOnce = False
selectedAlarm = ""
alarmSet = False
minute = 0
hour = 0

#Window Settings
root = Tk()
root.title("pyAlarm")
root.resizable(False, False)

alarm = c.Alarm() #Call class from call_mp3.py

#Call if current time equals target time
def callAlarm():
    global minute, hour
    if (alarmSet):
        if (alarm.call(minute,hour)):
            minute = ""
            hour = ""
            alarm.mp3(selectedAlarm)

    root.after(1000,callAlarm)

#Update Clock
def updateTimeLabel():
    global delayedOnce, delayTime
    currentTime = alarm.gui_hour()[0]
    currentTimeLabel["text"] = currentTime
    delayTime = 1000
    if delayedOnce != True:
        delayTime = 1000-alarm.gui_hour()[1]
        delayedOnce = True
    currentTimeLabel.after(delayTime,updateTimeLabel)

def callError(err):
    global errorCalled, errorLabel
    if (errorCalled):
        errorLabel.grid_forget() #Forget if called before
    else:
        errorCalled = True #Called before
    #Error Label
    errorLabel = Label(text=err, fg="red", font=customFontLight)
    errorLabel.grid(row=2,column=0,columnspan=2,sticky="W")

def setAlarm():
    global alarmSet, minute, hour
    if (selectedAlarm != ""):
        alarmValue = setSecond.get() #Get the value from Entry
        if len(alarmValue) == 5 or len(alarmValue) == 4:
            if len(alarmValue) == 4:
                alarmValue = "0"+alarmValue
            hour = alarmValue[0]+alarmValue[1]
            minute = alarmValue[3]+alarmValue[4]
            try:
                minute, hour = int(minute), int(hour) #Convert into "Integer" type
                alarm.call(hour,minute)
                #Delete Error Widget
                if (errorCalled): 
                    errorLabel.grid_forget()
                alarmSet = True
            except:
                callError("Wrong hour format! You have to use\n integers as value and a colon for\n specify hour and minute")
        else:
            callError("You have to enter the correct type as hour")
    else:
        callError("You have to select an alarm sound!")

def alarmSound():
    global selectedAlarm
    selectedAlarm = alarmList.get(ACTIVE)

#Font
customFont = font.Font(family="Open Sans",size=12,weight="bold")
customFont2 = font.Font(family="Helvatica",size=8,weight="bold")
customFontLight = font.Font(family="Open Sans",size=8,weight="normal")

#Widgets
currentTimeLabel = Label(text="", font=customFont)
currentTimeLabel.grid(row=0,column=0,columnspan=2,sticky="W") #Clock

setSecond = Entry() #Second Text Entry
setSecond.grid(row=1,column=0,padx=5,ipadx=20)

setAlarmButton = Button(text="Set Alarm", command=setAlarm, font=customFontLight) #Set Alarm Button
setAlarmButton.grid(row=1,column=1,pady=3,padx=2)

updateTimeLabel()

#Alarm Sounds
alarmSoundLabel = Label(text="Alarm Sounds", font=customFont2) #Alarm Sound Label
alarmSoundLabel.grid(row=2,column=0,columnspan=2,sticky="N")

alarms = []
for file in os.listdir(os.getcwd()+"/"+"alarms"):
    alarms.append(file)

alarmList = Listbox(root) #List Alarm Sounds
for file in alarms:
    alarmList.insert('end',file)
alarmList.grid(row=3,column=0,columnspan=2, sticky="W", padx=5, pady=3, ipadx=50)

selectAlarmButton = Button(text="Select Alarm", command=alarmSound) #Select Alarm Button
selectAlarmButton.grid(row=4,column=0,columnspan=2,sticky="W", padx=5, pady=2)

#Check if alarm called every second
root.after(1000,callAlarm)

root.mainloop()