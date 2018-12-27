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
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.clock import Clock

from mbientlab.metawear import MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *

from threading import Event
from time import sleep
from threading import Event
from os import listdir
import os
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
    
class State:
    #accelX = StringProperty('0')
    def __init__(self, device):
        self.device = device
        self.samples = 0
        self.callback = FnVoid_VoidP_DataP(self.data_handler)
        self.accelX = 0.0
        #print(self.accelX)
    def data_handler(self, ctx, data):
        #print("%s -> %s" % (self.device.address, parse_value(data).x))
        #accelX = 3
        self.accelX = parse_value(data).x
        global val
        val = self.accelX
        #ActivitiesScreen.val
        #print(App.get_running_app().root.ids.activities)
        #self.samples+= 1
        
class MainScreen(Screen):
    display = ObjectProperty()
    sensors = ObjectProperty()
    textinput = TextInput(text='Hello world')
    b = BoxLayout()
    t = TextInput()
    f = FloatLayout()
    b.add_widget(f)
    b.add_widget(t)
    #b.add_widget(display)
    #b.add_widget(sensors)
    def enter_mac(self):
        self.display.text = "Scanning"
        MacInput()
        
    def add_device(self):
        value = int(self.display.text)
        self.display.text = str(value+1)
    
    def register(self):
        global mac
        mac = self.ids.mac_input.text
        # D7:88:89:11:EC:DC
        print('User pressed enter in', mac)
        global device
        device = MetaWear(mac)
        device.connect()
        connected = True
        print("Connected")
        #val = str(self.sensors.text)
        #self.sensors.text = str(0)
        if connected:
            self.ids.sensors.text = str("Connected")
        pattern= LedPattern(repeat_count= Const.LED_REPEAT_INDEFINITELY)
        libmetawear.mbl_mw_led_load_preset_pattern(byref(pattern), LedPreset.SOLID)
        libmetawear.mbl_mw_led_write_pattern(device.board, byref(pattern), LedColor.GREEN)
        libmetawear.mbl_mw_led_play(device.board)
        global s
        s = State(device)

    
        
class ActivitiesScreen(Screen):
    def updateAccel():
        self.ids.accel.text = str(accelX)
        
    def testAccel(self):
        print("Configuring device")
        print(mac)
        print("rthr", s.accelX)
        global val
        val = s.accel
#        Clock.schedule_interval(self.timer, 0.1)
#        self.val = s.accelX# = str(s.accelX)
        #print("afsdfg", accelX)
        libmetawear.mbl_mw_settings_set_connection_parameters(s.device.board, 7.5, 7.5, 0, 6000)
        sleep(1.5)

        libmetawear.mbl_mw_acc_set_odr(s.device.board, 50.0)
        libmetawear.mbl_mw_acc_set_range(s.device.board, 16.0)
        libmetawear.mbl_mw_acc_write_acceleration_config(s.device.board)

        signal = libmetawear.mbl_mw_acc_get_acceleration_data_signal(s.device.board)
        libmetawear.mbl_mw_datasignal_subscribe(signal, None, s.callback)
        
        libmetawear.mbl_mw_acc_enable_acceleration_sampling(s.device.board)
        libmetawear.mbl_mw_acc_start(s.device.board)
        sm.current = 'accelView'
        
class AccelScreen(Screen):
    global val
    print("rthr", val)
    def updateAccel():
        self.ids.accel.text = str(accelX)
        
sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))
sm.add_widget(ActivitiesScreen(name='activities'))
sm.add_widget(AccelScreen(name='accelView'))

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