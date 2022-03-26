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
from kivymd.uix.list import OneLineIconListItem, MDList, ThreeLineIconListItem, OneLineListItem, IconLeftWidget, ImageLeftWidget
from kivymd.uix.selectioncontrol import MDCheckbox

from kivymd.icon_definitions import md_icons


import pandas as pd

from kivy_garden.mapview import MapView, MapSource, MapMarkerPopup

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



class customRide(ThreeLineIconListItem):
    pass

  
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

    data = {
        "Create a ride!": "language-python"
        }

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
        #testyWid = ThreeLineIconListItem(text="Destination Address",secondary_text="Leave Address",tertiary_text="Estimated Time until arrival, including waiting period", on_release=lambda x: print(x.text, x.secondary_text))
        #testyWidy = IconLeftWidget(icon="android")
        #testyWid.add_widget(testyWidy)
        #self.ids.ride_list.add_widget(testyWid)
        Clock.schedule_interval(self.update, 1)
    
    #called when we leave the screen - this removes the current load of rides
    def on_leave(self):
        i = 0
        
        while i < len(self.rideList):
            self.ids.ride_list.remove_widget(self.rideList[i])
            self.ids.mapview.remove_widget(self.mapList[i])
            i = i + 1
            
        self.rideList = []
        self.mapList = []
        

    #called EVERY time we enter the screen - populates current ride list
    def on_enter(self):

        self.manager.transition.direction = "up" #works

        #add coords for mapview
        self.rides = pd.read_excel("ride_data.xlsx")

        list_of_tokens = self.rides['Token']
        list_of_names = self.rides['Name']
        list_of_destinations = self.rides['Destination']
        list_of_departures = self.rides['Depart']
        list_of_eta = self.rides['ETA']

        list_of_x = self.rides['coordx']
        list_of_y = self.rides['coordy']

        i = 0
        self.rideList = []
        self.mapList = []

      
        while i < len(list_of_tokens):

            rideWidget = customRide(text=str(list_of_destinations[i])+" to "+str(list_of_departures[i]), secondary_text="Estimated " + str(list_of_eta[i]) + " minutes", tertiary_text="token: " + str(list_of_tokens[i]),
                                   on_release=lambda x: self.changeDisplay(x.tertiary_text))
            self.ids.ride_list.add_widget(rideWidget)
            self.rideList.append(rideWidget)


            mapWidget = MapMarkerPopup(lat=int(list_of_x[i]),lon=int(list_of_y[i]),source="marker.png")
            self.ids.mapview.add_widget(mapWidget)
            self.mapList.append(mapWidget)


            i = i + 1

        self.children
        self.rideList
        i = 0


    def changeDisplay(self, text):
        #self.ids.destination.text = text
        #self.ids.estimation.text = text
        token = text[7:]
        display_screen = MDApp.get_running_app().root.get_screen('display')
        print(display_screen.ids)

        display_screen.ids.destination.text = token
        display_screen.ids.departure.text = text
        display_screen.ids.estimation.text = text

        print("SUCCESS")
        print(text)
        pass

    
    
        


class displayWindow(Screen):
    pass


class editWindow(Screen):
    pass


class profileWindow(Screen):
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
        sm.add_widget(editWindow(name='edit_window'))
        sm.add_widget(profileWindow(name='profile_window'))
        return sm

  
# driver function
if __name__=="__main__":
    loginMain().run()