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



from threading import Event
from time import sleep
import time
from threading import Event
from os import listdir
import signal
import subprocess
import platform
import os
import operator
import csv
from datetime import datetime, timedelta

#import PyKDL as kdl
#os.environ['KIVY_GL_BACKEND'] = 'gl'
#import sys


        
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
        MainScreen.button1.y = 5000
        MainScreen.button2.y = MainScreen.sizeY
        #MainScreen.button1.bind(on_release=MainScreen.onPause)
        
        start = time.time()
        elapsed = 0

        
    
    
    
        
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