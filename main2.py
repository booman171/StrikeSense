# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 03:04:54 2018

@author: Jenario
"""
import os
os.environ['KIVY_GL_BACKEND'] = 'gl'
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from os import listdir

kv_path = './kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)

class ScanButton(Button):
    pass

class SubtractButton(Button):
    pass


class Container(GridLayout):
    display = ObjectProperty()
    
    def scan_devices(self):
        self.display.text = "Scanning"
        
    def subtract_one(self):
        value = int(self.display.text)
        self.display.text = str(value-1)

class MainApp(App):
    
    def build(self):
        self.title = 'Awesome app!!!'
        return Container()
    
if __name__ == "__main__":
    app = MainApp()
    app.run()