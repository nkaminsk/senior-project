# import all the relevant classes
from kivymd.app import App

from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
import pandas as pd

from kivy_garden.mapview import MapView
from plyer import gps
import plyer

"""
from pathlib import Path 

df = pd.DataFrame({'Name': ['Raphael', 'Donatello'],
                   'Email': ['red', 'purple'],
                   'Password': ['sai', 'bo staff']})

filepath = Path('login.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
df.to_csv(filepath)  

name_dict = {
            'Name': ['a','b','c','d'],
            'Email': [90,80,95,20],
            'Password': ['a', 'b', 'c', 'd']
          }

df = pd.DataFrame(name_dict)
"""


# class to call the popup function
class PopupWindow(Widget):
    def btn(self):
        popFun()
  
# class to build GUI for a popup window
class P(FloatLayout):
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
    def signupbtn(self):
  
        # creating a DataFrame of the info
        user = pd.DataFrame([[self.name2.text, self.email.text, self.pwd.text]],
                            columns = ['Name', 'Email', 'Password'])
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
sm.add_widget(loginWindow(name='login'))
sm.add_widget(signupWindow(name='signup'))
sm.add_widget(logDataWindow(name='logdata'))
  
# class that builds gui
class loginMain(App):
    def build(self):
        mapview = MapView(zoom=10, lat=36, lon=-115)
        return sm

  
# driver function
if __name__=="__main__":
    loginMain().run()