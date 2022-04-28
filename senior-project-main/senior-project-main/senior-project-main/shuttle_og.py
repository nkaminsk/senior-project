# import all the relevant classes
from os import scandir
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
import secrets

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
        now = secrets.token_hex(16)
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
    markerList = []
    displayList = []
    schedule = None
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

        test1 = "https://revgeocode.search.hereapi.com/v1/revgeocode?at=%s,%s&lang=en-US&apiKey=%s"%(str(36),str(-115), api_key)
        test2 = UrlRequest(test1, on_success=self.parse_test, on_failure=self.failure, on_error=self.error)
        #print(test2)

        try:
            test = UrlRequest(url, on_success=self.success, on_failure=self.failure, on_error=self.error)
            print (test)
        except Exception as e:
            print(e)

    def parse_test(self, urlrequest, result):
        print(result)

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
    longitude = NumericProperty(50)

    def decimal_precision(self, val, precision):
        # foo process
        return val

    # Getting latitude and longitude (at the moment just random stuff
    def get_gps_latitude(self):
        self.latitude = self.decimal_precision(0.01 * random.random() + 55.6394, DECIMAL_PRECISION)
        return self.latitude # rounding

    def get_gps_longitude(self):
        self.longitude = self.decimal_precision(0.01 * random.random() + 55.6394, DECIMAL_PRECISION)
        return self.longitude

    def update(self, _):
        
        print("calling update")
        self.latitude = self.get_gps_latitude()
        self.longitude = self.get_gps_longitude()

        display = MDApp.get_running_app().root.get_screen('display')
        #self.ids.mapview.center_on(self.latitude, self.longitude)
        #self.i = self.i + 1
        #print(i)
        #if self.i > 3:
        j = 0
            
        while j < len(self.markerList):
            self.ids.mapview.remove_widget(self.markerList[j])
            display.ids.displayview.remove_widget(self.displayList[j])
            j = j + 1

        
        mapWidget = MapMarkerPopup(lat=self.latitude,lon=self.longitude,source="marker.png")
        displayWidget = MapMarkerPopup(lat=self.latitude,lon=self.longitude,source="marker.png")
        self.ids.mapview.add_widget(mapWidget)
        display.ids.displayview.add_widget(displayWidget)
        self.markerList.append(mapWidget)
        self.displayList.append(displayWidget)
        self.ids.mapview.do_update(1)
        self.i = 0

    def on_pre_enter(self):
        #testyWid = ThreeLineIconListItem(text="Destination Address",secondary_text="Leave Address",tertiary_text="Estimated Time until arrival, including waiting period", on_release=lambda x: print(x.text, x.secondary_text))
        #testyWidy = IconLeftWidget(icon="android")
        #testyWid.add_widget(testyWidy)
        #self.ids.ride_list.add_widget(testyWid)
        
        if self.schedule != None:
            Clock.unschedule(self.schedule)
        self.schedule = Clock.schedule_interval(self.update, 2)
       
    
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


        self.ids.mapview.center_on(self.latitude, self.longitude)
        
        self.manager.transition.direction = "up" #works

        #add coords for mapview
        self.rides = pd.read_csv("ride_data.csv")

        list_of_tokens = self.rides['Token']
        list_of_names = self.rides['Name']
        list_of_destinations = self.rides['Destination']
        list_of_departures = self.rides['Depart']
        list_of_eta = self.rides['ETA']

        list_of_x = self.rides['coordxd']
        list_of_y = self.rides['coordyd']

        #list_of_destx = self.rides['coordxd']
        #list_of_desty = self.rides['coordyd']

        

        self.i = 0
        i = 0
        self.rideList = []
        self.mapList = []
        #self.markerList = []
        #self.displayList = []
      
        while i < len(list_of_tokens):
            rideWidget = customRide(text=str(list_of_destinations[i])+" to "+str(list_of_departures[i]), secondary_text="Estimated " + str(list_of_eta[i]) + " minutes", tertiary_text="token: " + str(list_of_tokens[i]),
                                   on_release=lambda x: self.changeDisplay(x.tertiary_text))
            self.ids.ride_list.add_widget(rideWidget)
            self.rideList.append(rideWidget)


            mapWidget = MapMarkerPopup(lat=int(list_of_x[i]),lon=int(list_of_y[i]),source="markerb.png")
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
        ride_data = self.rides.loc[(self.rides.Token == str(token))]
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
    markerList = []
    def sign_up(self):
        print("signing up")

        #current users token
        #current rides token

        ride_data = self.rides.loc[(self.rides.Token == str(self.token))]
        print(ride_data)
        #test = ride_data.at['Token', 0]
        #self.rides.loc[(self.rides.Token == str(self.token)), ['p1']] = 'test_token'
        #print(self.rides.loc[(self.rides.Token == str(self.token)), ['p1']])
        #print("printed data")
        ride_token = self.ids.token.text
        print(ride_token)

        profile_storage = MDApp.get_running_app().root.get_screen('profile_window')
        my_token = profile_storage.ids.token.text
        print(my_token)

        driver_token = ride_data.values[0][14]
        print(driver_token)
        try:

        #if they equal, alert they cant sign up for their own ride
            if (driver_token == my_token):
                Snackbar(text="Cannot sign up for your own ride", snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()
            else:
                #12,11,10,9
                if(my_token == ride_data.values[0][12] or my_token == ride_data.values[0][11] or my_token == ride_data.values[0][10] or my_token == ride_data.values[0][9]):
                    Snackbar(text="You've already signed up for this!", snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()
                else:
                    i = 9
                    while i < 13:
                        j = 1
                        #check for empty passengers '0.0'
                        if(str(ride_data.values[0][i]) == '0.0'):
                            self.rides.loc[(self.rides.Token == str(self.token)), ['p'+str(j)]] = my_token
                            self.rides.to_csv('ride_data.csv', index=False)
                            self.rides = pd.read_csv('ride_data.csv')
                            Snackbar(text="You have successfully signed up for this ride!", snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()

                            break
                        j = j + 1
                        i = i + 1
                    Snackbar(text="Ride is full, sorry!", snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()


        except Exception as e:
            Snackbar(text="Failed to sign up for ride, please try again", snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()

            print(e)

        #if they're not
        #check p1 p2 p3 p4
        #if equal to any
        #alert they're already signed up

        #else find any empty one
        #put it in the empty one
        #no empties?
        #snackbar ride is full, find another one


        pass

    def on_enter(self):
        #do stuff
        self.token = self.ids.token.text

        self.rides = pd.read_csv("ride_data.csv")

        ride_data = self.rides.loc[(self.rides.Token == str(self.token))]

        print(ride_data)
        print(ride_data.values[0][0])
        print(ride_data.values[0][1])
        print(ride_data.values[0][2])
        print(ride_data.values[0][3])
        print(ride_data.values[0][4])
        print(ride_data.values[0][5])#
        print(ride_data.values[0][6])#
        print(ride_data.values[0][7])#
        print(ride_data.values[0][8])#

        cur_lat = ride_data.values[0][5]
        cur_lon = ride_data.values[0][6]
        dest_lat = ride_data.values[0][7]
        dest_lon = ride_data.values[0][8]
        
        

        self.ids.displayview.center_on(dest_lat, dest_lon)
        self.ids.displayview.zoom = 12

        destWidget = MapMarkerPopup(lat=dest_lat,lon=dest_lon,source="markerb.png")
        curWidget = MapMarkerPopup(lat=cur_lat,lon=cur_lon,source="markery.png")

        self.ids.displayview.add_widget(destWidget)
        self.ids.displayview.add_widget(curWidget)

        self.markerList.append(destWidget)
        self.markerList.append(curWidget)

        self.ids.displayview.do_update(1)

        self.ids.token.text = ride_data.values[0][0]
        self.ids.name.text = ride_data.values[0][1] + " is leaving " + ride_data.values[0][3]
        self.ids.departure.text = "Arriving at : " + ride_data.values[0][2]
        self.ids.price.text = "This ride is going to cost : " + str(ride_data.values[0][15])

        print(self.token)
        pass

    def on_leave(self):
        j = 0
        while j < len(self.markerList):
            self.ids.displayview.remove_widget(self.markerList[j])
            j = j + 1
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

    def bad_time(self):
        Snackbar(text="Please select a time", snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()

    def callback(self, address):
        api_key = apikey_
        address = parse.quote(address)

        self.current_lat = self.get_gps_latitude()
        self.current_lon = self.get_gps_longitude()

        url = "https://geocoder.ls.hereapi.com/6.2/geocode.json?searchtext=%s&apiKey=%s"%(address, api_key)
        cur_loc_url = "https://revgeocode.search.hereapi.com/v1/revgeocode?at=%s,%s&lang=en-US&apiKey=%s"%(self.current_lat,self.current_lon, api_key)
        try:
            search_search = UrlRequest(url, on_success=self.success, on_failure=self.failure, on_error=self.error)
            location_search = UrlRequest(cur_loc_url, on_success=self.cur_success, on_failure=self.failure, on_error=self.error)
            #print (test)
        except Exception as e:
            Snackbar(text="Could not connect", snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()
            print(e)

    def cur_success(self, urlrequest, result):
        self.location_name = result['items'][0]['address']['label']
        print(self.location_name)

    def error(self, urlrequest, result):
        Snackbar(text="Could not search that address", snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()
        print("Error")
        print(result)
 
    def failure(self, urlrequest, result):
        Snackbar(text="Could not search that address", snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()
        print("Failure")
        print(result)

    def success(self, urlrequest, result):
        print("Success")
        print(result)
        
        try:
            self.destination_name = result['Response']['View'][0]['Result'][0]['Location']['Address']['Label']
            self.search_latitude = result['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Latitude']
            self.search_longitude = result['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Longitude']
            print(self.search_latitude, self.search_longitude)
            app = MDApp.get_running_app().root.get_screen('display')
            mapview = app.ids.displayview
            mapview.center_on(self.search_latitude, self.search_longitude)
            mapview.zoom = 14


            #search latitutde
            #saerch longitude

            #need our lat/long

            #need to grab input time
            self.selected_time = self.ids.timepick.text
            if self.selected_time == 'Open time picker':
                self.bad_time()
                raise Exception("bad time")
            #print(self.selected_time)
            self.ride_price = self.ids.rideprice.text
            if (self.ride_price == ''):
                Snackbar(text="Please select a price you'd like your ride to be", snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()
                raise Exception("ride blank")
            #print(self.ride_price)
            #grab input price
            #4 passengers
            #owners token

            #create ride
            #create token
            #self.ride_token = '' #randomly generate this
            #send token to display.text
            
            profile_storage = MDApp.get_running_app().root.get_screen('profile_window')
            self.my_token = profile_storage.ids.token.text 
            self.prof_name = profile_storage.ids.name.text
            #make display grab token and populate the rest of the fields on_enter
            #self.name = "HARD_CODE_NAME"
            #make pandas dataframe with all these fields
            self.ride_token = secrets.token_hex(16)
            
            user = pd.DataFrame([[self.ride_token, self.prof_name, self.destination_name, self.location_name, "Estimations Coming Soon...", self.current_lat, self.current_lon, self.search_latitude, self.search_longitude, '0.0', '0.0', '0.0', '0.0', self.selected_time, self.my_token, self.ride_price]],
                            columns = ['Token', 'Name', 'Destination', 'Depart', 'ETA', 'coordx', 'coordy', 'coordxd', 'coordyd', 'p1', 'p2', 'p3', 'p4', 'Time', 'Owner', 'Price'])
            user.to_csv('ride_data.csv', mode = 'a', header = False, index = False)
            app.ids.token.text = self.ride_token
            Snackbar(text="Ride has been created successfully", snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()
            sm.current = 'display'
        except Exception as e:
            Snackbar(text="Address not found, please try other addresses.", snackbar_x="10dp", snackbar_y="10dp", size_hint_x=(Window.width - (dp(10) * 2)) / Window.width).open()
            print(e)
            pass

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
    
    def create_ride(self):
        address = self.ids.destination.text
        self.callback(address)
        pass



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
        self.theme_cls.primary_palette = 'BlueGray'
        self.theme_cls.primary_hue = "500"

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
    #global CREATE_RIDE_LIST
    loginMain().run()