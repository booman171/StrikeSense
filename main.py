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

#import PyKDL as kdl
#os.environ['KIVY_GL_BACKEND'] = 'gl'
#import sys

kv_path = './kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)

class ActivityButton(Button):
    pass

class SubtractButton(Button):
    pass

class MacInput(BoxLayout):
    pass
    
class State():
    #accelX = StringProperty('0')
    def __init__(self, device):
        self.device = device
        self.samples = 0
        self.callback = FnVoid_VoidP_DataP(self.data_handler)
        self.accelX = StringProperty()
        #print(self.accelX)
    def data_handler(self, ctx, data):
        #print("%s -> %s" % (self.device.address, parse_value(data).x))
        #accelX = 3
#        self.accelX = StringProperty(parse_value(data).x)
#        global val
#        val = self.accelX
        game = Label(text='fff')
        ActivitiesScreen().updateAccel(game)
        #.updateAccel(parse_value(data).x)
        #ActivitiesScreen.val
        #print(val)
        #self.samples+= 1
        
class MainScreen(Screen):
    acceleration = StringProperty("fhfjh")
    b = BoxLayout()
    t = TextInput()
    f = FloatLayout()
    b.add_widget(f)
    b.add_widget(t)
    c = None
    z = None
    message = None
    message = Label(text="StrikeSense", pos=(50, 200 ), font_size='50sp')
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.add_widget(MainScreen.message)
        self.add_widget(MainScreen.button1)
    
    def set_button(self):
        MainScreen.button1 = Button(text='Hello world 1', pos=(0, 100),size_hint = (.4,.2))

    def reposition_button(root, *args):
        b1.pos = root.x, root.height / 2 - b1.height / 2
    
    def enter_mac(self):
        self.display.text = "Scanning"
        MacInput()
        
    def add_device(self):
        value = int(self.display.text)
        self.display.text = str(value+1)
    
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
        if len(ble_devices) > 1:
            for x in range(0, len(ble_devices)):
                print("ggg", ble_devices[x][0])
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
            MainScreen.z = data['value'].z
            #self.ids.display.text = str(MainScreen.z)
            MainScreen.message.text = str(y)
            print("z-axis: ", MainScreen.z)
            
        print("Check accelerometer settings...")
        settings = MainScreen.c.accelerometer.get_current_settings()
        print(settings)
        MainScreen.c.accelerometer.high_frequency_stream = False
        print("Subscribing to accelerometer signal notifications...")
        MainScreen.c.accelerometer.notifications(lambda data: mwc_acc_cb(data))
    

    button1.bind(on_release=register)
        
class ActivitiesScreen(Screen):
    
    def updateAccel(accelX):
        return accelX#self.ids.accel.text = str(accelX)
    
    

    def testAccel(self):
        print("Z: ", MainScreen.z)
    
class AccelScreen(Screen):
    #global val
    #print("rthr", val)
    def updateAccel():
        self.ids.accel.text = str(accelX)
        
sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))
sm.add_widget(ActivitiesScreen(name='activities'))
sm.add_widget(AccelScreen(name='accelView'))
def handle_acc_notification(data):
            # Handle dictionary with [epoch, value] keys.
            #epoch = data["epoch"]
            #xyz = data["value"]
            #print("This: ", str(data))
            #time.sleep(1.0)
            global x
            x = data['value'].x
            #self.ids.accel.text = acceleration
            #y = data['value'].y
            #z = data['value'].z
def getDevice(mac):
    print("Mac: ", mac)
    
def getX():
    print("Accel: ", accelX)
    
class MainApp(App):
    
    def build(self):
        self.title = 'Awesome app!!!'
        return sm
    
if __name__ == "__main__":
    Config.set('graphics', 'fullscreen', '0')
    app = MainApp()
    app.run()