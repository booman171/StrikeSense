# -*- coding: utf-8 -*
from __future__ import print_function
from kivy.config import Config
from kivy.app import App
from kivy.lang import Builder
import time
from kivy.clock import Clock
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
from datetime import datetime, timedelta
from mbientlab.metawear import MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *
from pymetawear.exceptions import PyMetaWearException
from mbientlab.warble import BleScanner
from discover import discover_devices
from client import MetaWearClient
#Config.set('graphics', 'width', '460')
#Config.set('graphics', 'height', '300')
#Config.set('graphics', 'resizable', False)
Builder.load_file("mainscreen.kv")


class MainScreen(App):
    stop_watch_start = False
    start = False
    seconds = 1800
    current = None
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
    activity = ""
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.title = 'Rarmen Timer'
        now = datetime.now()
        self.wait_time = datetime(now.year, now.month, now.day, hour=0, minute=0, second=0)
        self.wait_time = self.wait_time + timedelta(seconds=self.seconds)
        
    def build(self):
        self.root.ids.time.text = '{}'.format(
            self.wait_time.time().strftime("%M:%S"))

    def update_time(self, seconds):
        if self.stop_watch_start:
            self.wait_time -= timedelta(seconds=1)

        self.root.ids.time.text = '{}'.format(self.wait_time.time().strftime("%M:%S"))
        #MainScreen.current = '{}'.format(self.wait_time.time().strftime("%M:%S"))
        
    def start_stop(self):
        if self.stop_watch_start:
            self.stop_watch_start = False
            MainScreen.start = False
            self.root.ids.bt_start_stop.text = 'Start'
            Clock.unschedule(self.update_time)
        else:
            self.stop_watch_start = True
            MainScreen.start = True
            self.root.ids.bt_start_stop.text = 'Stop'
            Clock.schedule_interval(self.update_time, 1)

    def reset(self):

        if self.stop_watch_start:
            self.root.ids.bt_start_stop.text = 'Start'
            self.stop_watch_start = False

        now = datetime.now()
        self.wait_time = datetime(now.year, now.month, now.day, hour=0, minute=0, second=0)
        self.wait_time = self.wait_time + timedelta(seconds=180)

        self.root.ids.time.text = '{}'.format(
            self.wait_time.time().strftime("%M:%S"))

    def register(self):
            global mac
            """Run `discover_devices` and display a list to select from.

            :param int timeout: Duration of scanning.
            :return: The selected device's address.
            :rtype: str

            """
            timeout = 3
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
                if MainScreen.start:
                    MainScreen.dataList.append(x)
                    
                    if len(MainScreen.dataList) >= 2:
                        for i in MainScreen.dataList:
                            current = self.root.ids.time.text
                            currentActivity = MainScreen.activity
                            
                            if current == "29:58":
                                MainScreen.activity = "Jogging"
                            elif current == "28:00":
                                MainScreen.activity = "Sprint"
                            elif current == "27:00":
                                MainScreen.activity = "Hammer Curls"
                            elif current == "25:00":
                                activity = "Squats"
                            elif current == "22:00":
                                MainScreen.activity = "Foot Fires"
                            elif current == "21:00":
                                MainScreen.activity = "Bent-over Rows"
                            elif current == "18:00":
                                MainScreen.activity = "Squat Hold"
                            elif current == "16:00":
                                MainScreen.activity = "Jogging"
                            elif current == "13;00":
                                MainScreen.activity = "Shoulder Press"
                            elif current == "12:00":
                                MainScreen.activity = "Sprint"
                            elif current == "09:00":
                                MainScreen.activity = "Jab, Duck, Hook"
                            elif current == "08:00":
                                MainScreen.activity = "Foot Fires"
                            elif current == "05:00":
                                MainScreen.activity = "Elbow, Cross"
                            elif current == "04:00":
                                MainScreen.activity = "Jogging"
                            elif current == "03:00":
                                MainScreen.activity = "Hooks"
                        
                            f.write(str(current) + "," + str(i))
                            f.write("\n")
                            #print("Elapsed: " + self.root.ids.time.text)
                            self.root.ids.activity.text = MainScreen.activity
                else:
                    pass
                    
            print("Check accelerometer settings...")
            settings = MainScreen.c.accelerometer.get_current_settings()
            print(settings)
            MainScreen.c.accelerometer.high_frequency_stream = False
            print("Subscribing to accelerometer signal notifications...")
            self.root.ids.bt_connect.pos = (5000, 5000)
            self.root.ids.bt_start_stop.pos = (0, 0)
            self.root.ids.bt_start_stop.x = self.root.width
            print(self.root.width)
            MainScreen.button1.y = 5000
            MainScreen.button2.y = MainScreen.sizeY
            self.root.ids.bt_start_stop.text = "Start"
            #self.root.ids.bt_start_stop.bind(on_press=self.start_stop)
            
            start = time.time()
            elapsed = 0
            f = open('csvfile.csv','w')
            MainScreen.c.switch.notifications(lambda data: print(data))
            MainScreen.c.accelerometer.notifications(lambda data: mwc_acc_cb(data))
if __name__ == '__main__':
    MainScreen().run()

