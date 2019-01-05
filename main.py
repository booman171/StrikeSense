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
#import PyKDL as kdl
#os.environ['KIVY_GL_BACKEND'] = 'gl'
#import sys

kv_path = './kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)
        
class MainScreen(Screen):
        
    def register(self):
        global mac
        """Run `discover_devices` and display a list to select from.

        :param int timeout: Duration of scanning.
        :return: The selected device's address.
        :rtype: str

        """
        timeout = 3
        MainScreen.acceleration = StringProperty("fghffffffffffffffffffffffffffffffhtf")
        time.sleep(1.0)
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
            
            MainScreen.dataList.append(x)
            
            activity = ""
            #print(MainScreen.dataList)
            if len(MainScreen.dataList) >= 2:
                for i in MainScreen.dataList:
                    MainScreen.count += 1
                    elapsed = time.time() - start
                    if elapsed >= 0 and elapsed < 300:
                        activity = "Jogging"
                    elif elapsed >= 300 and elapsed <= 420:
                        activity = "Knee Kicks"
                    else:
                        activity = "Free"
                        
                    f.write(activity + "," + str(elapsed) + "," + str(i))
                    f.write("\n")
                    
                    print(elapsed)
                    MainScreen.message.text = activity
                    
                    
                    #f.write("\n")#Give your csv text here.
            ## Python will convert \n to os.linesep
            #f.close()
                
            #MainScreen.message2.text = str("Accel: ") + str(y)
            #file.close()
        print("Check accelerometer settings...")
        settings = MainScreen.c.accelerometer.get_current_settings()
        print(settings)
        MainScreen.c.accelerometer.high_frequency_stream = False
        print("Subscribing to accelerometer signal notifications...")
        MainScreen.button1.text = str("Start")
        start = time.time()
        f = open('csvfile.csv','w')

        MainScreen.c.accelerometer.notifications(lambda data: mwc_acc_cb(data))
        
        print("dghdf")
        
    acceleration = StringProperty("fhfjh")
    b = BoxLayout()
    t = TextInput()
    f = FloatLayout()
    b.add_widget(f)
    b.add_widget(t)
    c = None
    message = Label(text="StrikeSense")#, pos=(50, 200 ), font_size='50sp')
    message2 = Label(text="message2")#, pos=(50, 200 ), font_size='50sp')
    button1 = Button(text='Hello world 1')
    file = open('csvfile.csv','w')
    #file.write('hi there\n') #Give your csv text here.
    ## Python will convert \n to os.linesep
    #f.close()
    dataList = []
    count = 0
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        MainScreen.button1 = Button(text='Connect', pos=(self.x, self.y),size_hint = (1,.2))
        MainScreen.message = Label(text="StrikeSense", pos=(self.x, self.height * .75), font_size='50sp')
        MainScreen.message2 = Label(text="message2", pos=(self.x, self.y), font_size='50sp')
        MainScreen.button1.bind(on_release=MainScreen.register)
        self.add_widget(MainScreen.message)
        self.add_widget(MainScreen.message2)
        self.add_widget(MainScreen.button1)

    
    
    
    
        
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