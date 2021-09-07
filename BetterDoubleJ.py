"""BetterDoublej

This program creates a streaming instance (JJ) and every hour switches 
to Triple J for the news. It also switches to the news between 6am and 9am 
when it occurs in 30 minute intervals.

"""

__name__ = "BetterDoubleJ"
__author__ = "Brendan Griffen"
__version__ = "Version 0.1.0"
__license__ = "MIT"


import sys,os

try:
    base_path = sys._MEIPASS
except AttributeError:
    base_path = os.path.abspath(".")

import vlc
import time
import datetime as dt 

def is_now_between_time_periods(startTime, endTime, nowTime):
    """Check if time is between two times.
    
    Args:
        startTime (datetime): start of time to check
        endTime (datetime): end time to check
        nowTime (datetime): current time
    
    Returns:
        bool: True/False
    """
    if startTime < endTime: 
        return nowTime >= startTime and nowTime <= endTime 
    else: 
        # Over midnight 
        return nowTime >= startTime or nowTime <= endTime 


class BetterDoubleJ():

    def __init__(self):
        #define VLC instance
        self.instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
        
        #Define VLC player
        self.player=self.instance.media_player_new()
        self.playing = ""

    def set_station(self,station):

        # Return if already playing selected station
        if station == self.playing:
            return

        if station == "JJ":
            self.url = 'http://live-radio01.mediahubaustralia.com/4DJW/mp3/'
        elif station == "JJJ":
            self.url = 'http://live-radio01.mediahubaustralia.com/4TJW/mp3/'

        # Define VLC media
        self.media=self.instance.media_new(self.url)
        #self.media.add_option("sout=file/ts:sample.mp3")

        # Set player media
        self.player.set_media(self.media)
        
        # Play the media
        self.player.play()
        
        # Set playing station
        self.playing = station

    def switcher(self):

        # Current time and hour
        current_time = dt.datetime.now()
        current_hour = int(current_time.hour)

        # Check if time is between 59th minute and 3rd minute after the hour
        mhour = is_now_between_time_periods(dt.time(current_hour,59,50), 
                                            dt.time(current_hour,3,30), 
                                            current_time.time())
        
        # Is between 6 and 9am create a half hour window
        if current_hour >= 6 and current_hour <= 9:
            mhalf = is_now_between_time_periods(dt.time(current_hour,30,50), 
                                                dt.time(current_hour,33,50), 
                                                current_time.time())
            mwindow = mhalf or mhour
        else:

            mwindow = mhour

        # If satisfied then switch to Triple J (JJJ) 
        if mwindow:
            self.set_station("JJJ")
        else:
            self.set_station("JJ")


if __name__ == 'BetterDoubleJ':
    j = BetterDoubleJ()
    j.set_station("JJ")
    time.sleep(1)
    while True:
        time.sleep(10)
        j.switcher()

