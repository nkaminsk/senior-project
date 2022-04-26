# import all the relevant classes
import pkg_resources
from subprocess import call

#packages = [dist.project_name for dist in pkg_resources.working_set]
#call("pip install --upgrade " + ' '.join(packages), shell=True)




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

from kivy_garden.mapview import MapView, MapSource, MapMarkerPopup, MapMarker

#from plyer import gps
#import plyer

from datetime import datetime

from pathlib import Path 

from urllib import parse
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.dialog import MDDialog, BaseDialog
from kivymd.uix.dialog import *
from kivymd.uix.snackbar import Snackbar
from kivy.animation import Animation
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.textfield import MDTextField

from kivymd.uix.picker import MDTimePicker

DECIMAL_PRECISION = 2

apikey_ = "OYXBuL4wN3X2SUAMHtGQt4Gs0BAmuccDI6N5WecJXdI"

class SearchPopupMenu(MDDialog):
    def __init__(self): 
        super().__init__() # super() inherits all the methods in MDInputDialog, within the __init__() function
        self.size_hint = [.9, .3]
        self.events_callback = self.callback #call the callback function below
 
    def on_open(self):
        #super().on_open() # super() inherits all the methods in MDInputDialog, within the open() function
        address = "123 east main st kent oh"
        self.geocode_get_lat_lon(address)
        #Clock.schedule_once(self.set_field_focus, 0.5)
        #self.callback()
 
    def callback(self, *args):
        address = self.text_field.text
        self.geocode_get_lat_lon(address)
 
    def geocode_get_lat_lon(self, address):
        
        api_key = apikey_
        address = parse.quote(address)
        url = "https://geocoder.ls.hereapi.com/6.2/geocode.json?searchtext=%s&apiKey=%s"%(address, api_key)
        UrlRequest(url, on_success=self.success, on_failure=self.failure, on_error=self.error)
        #certifi directs our apps to ssl certificate
 
    def success(self, urlrequest, result):
        print("Success")
        print(result)
        try:
            latitude = result['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Latitude']
            longitude = result['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Longitude']
            print(latitude, longitude)
            app = MDApp.get_running_app().root.get_screen('logdata')
            mapview = app.ids.mapview
            mapview.center_on(latitude, longitude)
        except Exception as e:
            Snackbar(text="Address not found, please try other addresses.", snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()
            print(e)
            pass

        #this all works, the result is a completed full result - we get lat and lon, so have user search of destination and see if it matches ride list, plus or minus coords maybe?
        #return if theres a ride there or not
        #sort list with closest items on top
        #create a ride uses this to grab lat and lon 
        #
 
 
    def error(self, urlrequest, result):
        print("Error")
        print(result)
 
    def failure(self, urlrequest, result):
        print("Failure")
        print(result)


class GpsBlinker(MapMarker):
    def blink(self):
        # Animation that changes the blink size and opacity
        anim = Animation(outer_opacity=0, blink_size=50)
         
        # When the animation completes, reset the animation, then repeat
        anim.bind(on_complete = self.reset)
        anim.start(self)
 
    def reset(self, *args):
        self.outer_opacity = 1
        self.blink_size = self.default_blink_size
        self.blink()
 
    # blink --> outer_opacity = 0, blink_size = 50
    # reset --> outer_opacity = 1, blink_size = default = 25

class Content(MDBoxLayout):
    pass


'''
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

'''

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

    #search_menu = None

    
 
        # Instantiate SearchPopupMenu
    #self.search_menu = SearchPopupMenu(self.dialog)

    def validate(self):
        # reading all the data stored
        users=pd.read_csv('login.csv')
        df = pd.DataFrame(users)

        user = self.email.text
        pasw = self.pwd.text
  
        # validating if the email already exists 
        if self.email.text not in users['Email'].unique():
            popFun()
        else:
            matching_creds = (len(df[(df.Email == user) & (df.Password == pasw)]) > 0)
            # switching the current screen to display validation result
            if matching_creds:
                #store the user data in the viewprofile window
                profile_storage = MDApp.get_running_app().root.get_screen('profile_window')
                
                login_info = df.loc[(df.Email == user) & (df.Password == pasw)]

                print(login_info)
             
                login_email = login_info['Email'].to_string(index=False)
                
                login_token = login_info['Token'].to_string(index=False)
                login_name = login_info['Name'].to_string(index=False)

                profile_storage.ids.email.text = str(login_email)
                profile_storage.ids.name.text = str(login_name)
                profile_storage.ids.token.text = str(login_token)


                sm.current = 'logdata'
  
                # reset TextInput widget
                self.email.text = ""
                self.pwd.text = ""
            else:
                popFun()
  
  
# class to accept sign up info  
class signupWindow(Screen):
    name2 = ObjectProperty(None)
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def back(self):
        sm.current = 'login'

    def signupbtn(self):
        now = datetime.now()
        # creating a DataFrame of the info
        user = pd.DataFrame([[self.name2.text, self.email.text, self.pwd.text, now]],
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
        "Create a ride!": "language-python",
        "Search!": "language-ruby"
        }

    def speed_click(self, instance):
        if (instance.icon == 'language-ruby'):
            self.dialog.open()
        if (instance.icon == 'language-python'):
            sm.current = 'cride_window'

    def speed_dial_click():
        print("speed_dial_click")

    def callback(self, address):
        api_key = apikey_
        address = parse.quote(address)
        url = "https://geocoder.ls.hereapi.com/6.2/geocode.json?searchtext=%s&apiKey=%s"%(address, api_key)
        try:
            test = UrlRequest(url, on_success=self.success, on_failure=self.failure, on_error=self.error)
            print (test)
        except Exception as e:
            print(e)

    def error(self, urlrequest, result):
        print("Error")
        print(result)
 
    def failure(self, urlrequest, result):
        print("Failure")
        print(result)

    def success(self, urlrequest, result):
        print("Success")
        print(result)
        try:
            self.search_latitude = result['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Latitude']
            self.search_longitude = result['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Longitude']
            print(self.search_latitude, self.search_longitude)
            app = MDApp.get_running_app().root.get_screen('logdata')
            mapview = app.ids.mapview
            mapview.center_on(self.search_latitude, self.search_longitude)
            mapview.zoom = 14
            self.dialog.dismiss()
            Snackbar(text="Ride list has been updated to near your desired destination", snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()
        except Exception as e:
            Snackbar(text="Address not found, please try other addresses.", snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()
            print(e)
            pass


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

        

        self.dialog = MDDialog(
        title="Search by Address: ",
        type="custom",
        content_cls=Content(),
        buttons=[
            MDFlatButton(
                text="CANCEL", on_press=lambda x: self.dialog.dismiss()
            ),
            MDFlatButton(
                text="ACCEPT", on_press=lambda x: self.callback(self.dialog.content_cls.ids.searchdestination.text)
            ),
        ],
    )
        #self.dialog.dismiss()
        #self.dialog.open()

        #open this dialog, and have the accept button interact with a global request function that returns the coordinates or adds the snackbar



        
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
        ride_data = self.rides.loc[(self.rides.Token == int(token))]
        # :: token | name | destination | depart | ETA | coordx | coordy
        #print(token)
        #print(ride_data)
       
        try:
            #print(ride_data.values[0][1])
            display_screen.ids.token.text = str(ride_data.values[0][0])
            display_screen.ids.departure.text = str(ride_data.values[0][3])
            display_screen.ids.estimation.text = str(ride_data.values[0][4])
        except Exception as e:
            print(e)

        print("SUCCESS")
        print(text)
        pass

    
    
        


class displayWindow(Screen):
    pass


class editWindow(Screen):
    pass


class profileWindow(Screen):
    pass
  
class crideWindow(Screen):
    def get_time(self, instance, time):
        '''
    The method returns the set time.

    :type instance: <kivymd.uix.picker.MDTimePicker object>
    :type time: <class 'datetime.time'>
        '''
        self.ids.timepick.text = str(time)
        return time

    def show_time_picker(self):
        '''Open time picker dialog.'''

        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time)
        time_dialog.open()

# class for managing screens
class windowManager(ScreenManager):
    pass
  
# kv file
#kv = Builder.load_file('login.kv')
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
        sm.add_widget(crideWindow(name='cride_window'))
        return sm

  
# driver function
if __name__=="__main__":
    loginMain().run()