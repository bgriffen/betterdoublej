import sys,os

try:
    base_path = sys._MEIPASS
except AttributeError:
    base_path = os.path.abspath(".")

import vlc
import time
import datetime as dt 

def is_now_between_time_periods(startTime, endTime, nowTime): 
    if startTime < endTime: 
        return nowTime >= startTime and nowTime <= endTime 
    else: 
        #Over midnight: 
        return nowTime >= startTime or nowTime <= endTime 


class BetterDoubleJ():
    
    def __init__(self):
        #define VLC instance
        self.instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
        
        #Define VLC player
        self.player=self.instance.media_player_new()
        self.playing = ""

    def set_station(self,station):
        if station == self.playing:
            # already playing this station...
            return

        if station == "JJ":
            self.url = 'http://live-radio01.mediahubaustralia.com/4DJW/mp3/'
        elif station == "JJJ":
            self.url = 'http://live-radio01.mediahubaustralia.com/4TJW/mp3/'

        #Define VLC media
        self.media=self.instance.media_new(self.url)
    
        #Set player media
        self.player.set_media(self.media)
        
        #Play the media
        self.player.play()
        
        self.playing = station

    def stop(self):
        self.player.stop()

    def play(self):
        self.player.play()

    def switcher(self):
        current_time = dt.datetime.now()
        current_hour = int(current_time.hour)

        # true if between 59th minute and 3rd minute after the hour
        mhour = is_now_between_time_periods(dt.time(current_hour,59,50), dt.time(current_hour,3,30), current_time.time())
        
        # between 6 and 9am
        if current_hour >= 6 and current_hour <= 9:
            mhalf = is_now_between_time_periods(dt.time(current_hour,30,50), dt.time(current_hour,33,30), current_time.time())
            mwindow = mhalf or mhour
        else:
            # outside of 6 and 9am
            mwindow = mhour

        if mwindow:
            self.set_station("JJJ")
        else:
            self.set_station("JJ")

if __name__ == '__main__':
    j = DouglasJ()
    j.set_station("JJ")
    time.sleep(1)
    while True:
        time.sleep(10)
        j.switcher()

