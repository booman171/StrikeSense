# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 03:04:54 2018

@author: Jenario
"""
from __future__ import print_function

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.clock import Clock

from mbientlab.metawear import MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *
from pymetawear.exceptions import PyMetaWearException
from mbientlab.warble import BleScanner
from discover import discover_devices
from client import MetaWearClient

from threading import Event
from time import sleep
import time
from threading import Event
from os import listdir
import signal
import subprocess
import platform
import os
import main2
import operator
import csv
from datetime import datetime, timedelta

#import PyKDL as kdl
#os.environ['KIVY_GL_BACKEND'] = 'gl'
#import sys

kv_path = './kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)
        
class MainScreen(Screen):
    stop_watch_start = False
    seconds = 3600
    wait_time = None
    
        
    acceleration = StringProperty("fhfjh")
    b = BoxLayout()
    t = TextInput()
    f = FloatLayout()
    b.add_widget(f)
    b.add_widget(t)
    c = None
    message = Label(text="StrikeSense")#, pos=(50, 200 ), font_size='50sp')
    message2 = Label(text="message2")#, pos=(50, 200 ), font_size='50sp')\
    timeLabel = Label(text='[b]00:00[/b]', font_name='./fonts/DSEG7Classic-Regular.ttf', font_size=100, markup=True)
    button1 = Button(text='Hello world 1')
    button2 = Button(text='Hello world 1')
    
    sizeY = 0
    sizex = 0
    file = open('csvfile.csv','w')
    dataList = []
    count = 0
    paused = True
    restTime = 0
    pausedTime = 0
    now = 0
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.title = 'StrikeSense'
        now = datetime.now()
        MainScreen.wait_time = datetime(now.year, now.month, now.day, hour=0, minute=0, second=0)
        MainScreen.wait_time = MainScreen.wait_time + timedelta(seconds=self.seconds)
        
        MainScreen.sizeY = self.y
        MainScreen.sizeX = self.x
        MainScreen.button1 = Button(text='Connect', pos=(self.x, self.y),size_hint = (1,.2))
        MainScreen.button2 = Button(text='Start', pos=(self.x, 5000),size_hint = (1,.2))
        MainScreen.message = Label(text="StrikeSense", pos=(self.x, self.height * .75), font_size='50sp')
        MainScreen.message2 = Label(text="message2", pos=(self.x, self.y), font_size='50sp')
        MainScreen.button1.bind(on_release=MainScreen.register)
        MainScreen.button2.bind(on_release=MainScreen.start_stop)
        self.add_widget(MainScreen.message)
        self.add_widget(MainScreen.message2)
        self.add_widget(MainScreen.button1)
        self.add_widget(MainScreen.button2)
        self.add_widget(MainScreen.timeLabel)

    def build(self):
        self.root.ids.time.text = '{}'.format(MainScreen.wait_time.time().strftime("%M:%S"))
        print("ffdgbvfd")
        
    def update_time(self):
        if MainScreen.stop_watch_start:
            MainScreen.wait_time -= timedelta(seconds=1)

        MainScreen.timeLabel.text = '{}'.format(MainScreen.wait_time.time().strftime("%M:%S"))
        print(MainScreen.wait_time.time().strftime("%M:%S"))
        
    def start_stop(self):
        if MainScreen.stop_watch_start:
            MainScreen.stop_watch_start = False
            MainScreen.button2.text = 'Start'
            Clock.unschedule(MainScreen.update_time)
        else:
            MainScreen.stop_watch_start = True
            MainScreen.button2.text = 'Stop'
            Clock.schedule_interval(MainScreen.update_time, 1)

    def reset(self):

        if MainScreen.stop_watch_start:
            MainScreen.button2.text = 'Start'
            MainScreen.stop_watch_start = False

        now = datetime.now()
        MainScreen.wait_time = datetime(now.year, now.month, now.day, hour=0, minute=0, second=0)
        MainScreen.wait_time = MainScreen.wait_time + timedelta(seconds=180)

        self.root.ids.time.text = '{}'.format(
            MainScreen.wait_time.time().strftime("%M:%S"))
        
            
    def register(self):
        global mac
        """Run `discover_devices` and display a list to select from.

        :param int timeout: Duration of scanning.
        :return: The selected device's address.
        :rtype: str

        """
        timeout = 3
        MainScreen.acceleration = StringProperty("fghffffffffffffffffffffffffffffffhtf")
        print("ghgghDiscovering nearby Bluetooth Low Energy devices...")
        ble_devices = discover_devices(timeout=timeout)
        oneConnected = False
        if len(ble_devices) > 1 & oneConnected == False:
            for x in range(0, len(ble_devices)):
                print("ggg", ble_devices[x][1])
                if ble_devices[x][1] == "MetaWear":
                    address = ble_devices[x][0]
                    print("connecting to: ", ble_devices[x][0])
                    oneConnected = True
#            for i, d in enumerate(ble_devices):
#                print("[{0}] - {1}: {2}".format(i + 1, *d))
#            s = input("Which device do you want to connect to? ")
#            if int(s) <= (i + 1):
#                address = ble_devices[int(s) - 1][0]
#            else:
#                raise ValueError("Incorrect selection. Aborting...")
        elif len(ble_devices) == 1:
            address = ble_devices[0][0]
            print("Found only one device: {0}: {1}.".format(*ble_devices[0][::-1]))
        else:
            #raise ValueError("Did not detect any BLE devices.")
            print("Did not detect any BLE devices.")

        #D7:88:89:11:EC:DC
        MainScreen.c = MetaWearClient(str(address), debug=True)
        print("Connected")
        pattern = MainScreen.c.led.load_preset_pattern('pulse')
        MainScreen.c.led.write_pattern(pattern, 'b')
        MainScreen.c.led.play()
        
    
        def mwc_acc_cb(data):
            x = data['value'].x
            y = data['value'].y
            z = data['value'].z
            
            row = "this," + str(x)
            now = time.time()
#            if MainScreen.stop_watch_start:
#                MainScreen.dataList.append(x)
#                
#                activity = ""
#                #print(MainScreen.dataList)
#                if len(MainScreen.dataList) >= 2:
#                    for i in MainScreen.dataList:
#                        MainScreen.count += 1
#                        elapsed = (time.time() - start) - MainScreen.restTime
#                        MainScreen.pausedTime = (time.time() - start) - MainScreen.restTime
#
#                        if elapsed >= 0 and elapsed < 300:
#                            activity = "Jogging"
#                        elif elapsed >= 300 and elapsed <= 420:
#                            activity = "Sprint"
#                        elif elapsed >= 420 and elapsed <= 720:
#                            activity = "Hammer Curls"
#                        elif elapsed >= 720 and elapsed <= 1020:
#                            activity = "Squats"
#                        elif elapsed >= 1020 and elapsed <= 1140:
#                            activity = "Foot Fires"
#                        elif elapsed >= 1140 and elapsed <= 1440:
#                            activity = "Bentover Rows"
#                        elif elapsed >= 1440 and elapsed <= 1740:
#                            activity = "Squat Hold"
#                        elif elapsed >= 1740 and elapsed <= 1860:
#                            activity = "Jogging"
#                        elif elapsed >= 1860 and elapsed <= 2160:
#                            activity = "Shoulder Press"
#                        elif elapsed >= 2160 and elapsed <= 2280:
#                            activity = "Sprint"
#                        elif elapsed >= 2280 and elapsed <= 2580:
#                            activity = "Jab, Duck, Hook"
#                        elif elapsed >= 2580 and elapsed <= 2880:
#                            activity = "Foot Fires"
#                        elif elapsed >= 2880 and elapsed <= 3180:
#                            activity = "Elbow, Cross"
#                        elif elapsed >= 3180 and elapsed <= 3300:
#                            activity = "Jogging"
#                        elif elapsed >= 3300 and elapsed <= 3600:
#                            activity = "Hooks"
#                        else:
#                            activity = "Rest"
#                            
#                        f.write(activity + "," + str(elapsed) + "," + str(i))
#                        f.write("\n")
#                        #print("Elapsed: " + str(elapsed))
#                        MainScreen.message.text = activity
#            else:
#                pass
                
        print("Check accelerometer settings...")
        settings = MainScreen.c.accelerometer.get_current_settings()
        print(settings)
        MainScreen.c.accelerometer.high_frequency_stream = False
        print("Subscribing to accelerometer signal notifications...")
        MainScreen.button1.y = 5000
        MainScreen.button2.y = MainScreen.sizeY
        #MainScreen.button1.bind(on_release=MainScreen.onPause)
        
        start = time.time()
        elapsed = 0
        f = open('csvfile.csv','w')
        
        MainScreen.c.accelerometer.notifications(lambda data: mwc_acc_cb(data))
        
    
    
    
        
sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))
    
class MainApp(App):
    
    def build(self):
        self.title = 'Awesome app!!!'
        return sm
    
if __name__ == "__main__":
    Config.set('graphics', 'fullscreen', '0')
    app = MainApp()
    app.run()