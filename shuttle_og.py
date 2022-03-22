# import all the relevant classes
from kivymd.app import MDApp

from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty, ListProperty, NumericProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.clock import Clock
import random

from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.theming import ThemableBehavior, ThemeManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, MDList


import pandas as pd

from kivy_garden.mapview import MapView, MapSource
from plyer import gps
import plyer


from pathlib import Path 

DECIMAL_PRECISION = 2

"""
df = pd.DataFrame({'Name': ['Raphael', 'Donatello'],
                   'Email': ['red', 'purple'],
                   'Password': ['sai', 'bo staff'],
                   'Token': [1, 2]})

filepath = Path('login.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
df.to_csv(filepath)  

name_dict = {
            'Name': ['a','b','c','d'],
            'Email': [90,80,95,20],
            'Password': ['a', 'b', 'c', 'd'],
            'Token': [1,2,3,4]
          }

df = pd.DataFrame(name_dict)

"""

# class to call the popup function
class PopupWindow(Widget):
    def btn(self):
        popFun()
  
# class to build GUI for a popup window
class P(MDFloatLayout):
    pass
  
# function that displays the content
def popFun():
    show = P()
    window = Popup(title = "popup", content = show,
                   size_hint = (None, None), size = (300, 300))
    window.open()
  
# class to accept user info and validate it
class loginWindow(Screen):
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)
    def validate(self):
        # reading all the data stored
        users=pd.read_csv('login.csv')
  
        # validating if the email already exists 
        if self.email.text not in users['Email'].unique():
            popFun()
        else:
  
            # switching the current screen to display validation result
            sm.current = 'logdata'
  
            # reset TextInput widget
            self.email.text = ""
            self.pwd.text = ""
  
  
# class to accept sign up info  
class signupWindow(Screen):
    name2 = ObjectProperty(None)
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def back(self):
        sm.current = 'login'

    def signupbtn(self):
  
        # creating a DataFrame of the info
        user = pd.DataFrame([[self.name2.text, self.email.text, self.pwd.text, 1]],
                            columns = ['Name', 'Email', 'Password', 'Token'])
        if self.email.text != "":
            if self.email.text not in users['Email'].unique():
  
                # if email does not exist already then append to the csv file
                # change current screen to log in the user now 
                user.to_csv('login.csv', mode = 'a', header = False, index = False)
                sm.current = 'login'
                self.name2.text = ""
                self.email.text = ""
                self.pwd.text = ""
        else:
            # if values are empty or invalid show pop up
            popFun()
      
# class to display validation result
class logDataWindow(Screen):

    latitude = NumericProperty(50) #GET COORDS
    longitude = NumericProperty(3)

    def decimal_precision(self, val, precision):
        # foo process
        return val

    # Getting latitude and longitude (at the moment just random stuff
    def get_gps_latitude(self):
        self.latitude = self.decimal_precision(0.01 * random.random() + 50.6394, DECIMAL_PRECISION)
        return self.latitude # rounding

    def get_gps_longitude(self):
        self.longitude = self.decimal_precision(0.01 * random.random() + 50.6394, DECIMAL_PRECISION)
        return self.longitude

    def update(self, _):
        self.latitude = self.get_gps_latitude()
        self.longitude = self.get_gps_longitude()
        #self.ids.mapview.center_on(self.latitude, self.longitude)

    def on_pre_enter(self):
        print("here")
        Clock.schedule_interval(self.update, 1)
    



class displayWindow(Screen):
    pass
  
# class for managing screens
class windowManager(ScreenManager):
    pass
  
# kv file
kv = Builder.load_file('login.kv')
sm = windowManager()
  
# reading all the data stored
users=pd.read_csv('login.csv')
  
# adding screens

  
# class that builds gui
class loginMain(MDApp):
    def __init__(self, **kwargs):
        self.title = "Shuttle"
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.root = Builder.load_file('login.kv')
        sm.add_widget(loginWindow(name='login'))
        sm.add_widget(signupWindow(name='signup'))
        sm.add_widget(logDataWindow(name='logdata'))
        sm.add_widget(displayWindow(name='display'))
        return sm

  
# driver function
if __name__=="__main__":
    loginMain().run()