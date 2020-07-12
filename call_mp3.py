import datetime
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #Hide Welcome Message of pygame
from pygame import mixer

class Alarm:
    def __init__(self):
        #Date
        self.dates()

    def dates(self):
        self.currentDate = datetime.datetime.now()
        self.hour = self.currentDate.hour
        self.minute = self.currentDate.minute
        self.second = self.currentDate.second

    def gui_hour(self):
        self.dates()

        if len(str(self.hour)) == 1:
            self.hour = "0"+str(self.hour)
        if len(str(self.minute)) == 1:
            self.minute = "0"+str(self.minute)
        if len(str(self.second)) == 1:
            self.second = "0"+str(self.second)

        return [str(self.hour)+":"+str(self.minute)+":"+str(self.second),int(self.second)] #FULLDATE, SECOND

    def call(self,minute,hour):
        self.dates()
        
        #Data
        self.alarmMin = minute
        self.alarmHour = hour

        if (self.alarmHour == int(self.hour) and self.alarmMin == int(self.minute)):
            return True
        else:
            return False

    def mp3(self, alarm):
        #Run mp3 file from background
        mixer.init()
        mixer.music.load("alarms/{}".format(alarm))
        mixer.music.play()