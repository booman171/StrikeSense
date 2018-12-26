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
from kivy.properties import ObjectProperty
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen

#from mbientlab.metawear import MetaWear, libmetawear
#from mbientlab.metawear.cbindings import *

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


class MainScreen(Screen):
    textinput = TextInput(text='Hello world')
    b = BoxLayout()
    t = TextInput()
    f = FloatLayout()
    b.add_widget(f)
    b.add_widget(t)
    def enter_mac(self):
        self.display.text = "Scanning"
        MacInput()
        
    def subtract_one(self):
        value = int(self.display.text)
        self.display.text = str(value-1)
    
    def register(self):
        mac = self.ids.mac_input.text
        print('User pressed enter in', mac)
#        device = MetaWear(mac)
#        device.connect()
#        print("Connected")
#        pattern= LedPattern(repeat_count= Const.LED_REPEAT_INDEFINITELY)
#        libmetawear.mbl_mw_led_load_preset_pattern(byref(pattern), LedPreset.SOLID)
#        libmetawear.mbl_mw_led_write_pattern(device.board, byref(pattern), LedColor.GREEN)
#        libmetawear.mbl_mw_led_play(device.board)

class ActivitiesScreen(Screen):
    pass
# Create the screen manager
sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))
sm.add_widget(ActivitiesScreen(name='activities'))
    
    
    
    
class MainApp(App):
    
    def build(self):
        self.title = 'Awesome app!!!'
        return sm
    
if __name__ == "__main__":
    Config.set('graphics', 'fullscreen', '0')
    app = MainApp()
    app.run()