import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,QVBoxLayout)
from PyQt5 import QtGui

from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):   
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('favicon-32x32.png'))  # Set the window icon
        self.city_label = QLabel("Enter city name: " , self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("WeatherApp")

        vbox = QVBoxLayout() # Vertical layout manager
        # Add widgets for everything we want to show, then self.setLayout(layout manager)
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        self.setLayout(vbox)

        # Center our widgets // get_weather_button takes up all horizontal space so no need to center it
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        # To stylize
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        
        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: Sans-serif;
                           }
            QPushButton {
                background-color: lightblue;
                           }
            QLabel#city_label{
                           font-size: 40px;
                           font-style: italic;
                           }
                           QLineEdit#city_input{
                           font-size: 40px;
                           }
                           QPushButton#get_weather_button{
                           font-size:30px;
                           font-weight: bold;
                           }
                           QLabel#temperature_label{
                           font-size:75px;
                           }
                           QLabel#emoji_label{
                           font-size: 100px;
                           font-family: Segoe UI emoji;
                           }
                           QLabel#description_label{
                           font-size: 50px;

                           }


                           """)
        self.get_weather_button.clicked.connect(self.get_weather) 
        #When get_weather_button is clicked, call self.get_weather function


    def get_weather(self):
        api_key = "50aab3917d489a513f2d5fb62a6101d1"
        city = self.city_input.text() # Get input from user 
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}" #api url

        try:
            response = requests.get(url) # creates response object of api request
            response.raise_for_status() # raises exception for HTTP errors
            data = response.json() # converts response object from json format to python dictionary
            

            if data["cod"] ==200: # 200 is a HTTP response code meaning request was successful.
                self.display_weather(data) 
        except requests.exceptions.HTTPError as http_error: # HTTPError is an expection raised by the request module when an HTTP code > 400
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\n Please check the city name.")
                case 401:
                    self.display_error("Unauthorized:\n Please check your API key.")
                case 403:
                    self.display_error("Forbidden:\n You don't have permission to access this resource.")
                case 404:
                    self.display_error("City not found:\n Please check the city name.")
                case 500:
                    self.display_error("Internal server error:\n Please try again later.")
                case 502:
                    self.display_error("Bad gateway:\n Invalid server response.")
                case 503:
                    self.display_error("Service unavailable:\n Server is down or being upgraded.")
                case 504:
                    self.display_error("Gateway timeout:\n Server is not responding.")
                case _:
                    self.display_error(f"HTTP error occurred:\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Check your internet connection and try again.")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\n The request timed out.")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects:\n Check the URL.")
        except requests.exceptions.RequestException as req_error: # RequestException is a base class for all exceptions raised by the requests module (invalid urls etc.)
            self.display_error(f"Request Error:\n{req_error}")


    def display_error(self,msg):
        self.temperature_label.setStyleSheet("font-size: 30px; color: red;")
        self.city_label.setText("Retry:")
        self.temperature_label.setText(msg)
        self.emoji_label.setText("Error")
        self.description_label.setText("")
        
    
    def display_weather(self,weather):
        temperature_kelvin = weather["main"]["temp"]
        temperature_fahrenheit = int((temperature_kelvin * 9/5) -459.67) # Convert Kelvin to Fahrenheit
        print(temperature_fahrenheit)
        self.temperature_label.setText(f"{temperature_fahrenheit}°F")

        
        condition = weather["weather"][0]["main"]
        print(weather)
        
         # Set emoji and description based on weather condition
        if condition == "Clear":
            self.description_label.setText('Clear Skies')
            self.emoji_label.setText("☀︎")
        elif condition == "Clouds":
            self.description_label.setText('Cloudy')
            self.emoji_label.setText("☁︎")
        elif condition == "Rain":
            self.description_label.setText('Rainy')
            self.emoji_label.setText("☂︎")
        else:
            self.description_label.setText("")
            


if __name__ =="__main__":
    app = QApplication(sys.argv)

    weather_app = WeatherApp()
    weather_app.show() # Shows app window
    sys.exit(app.exec_())  #Keeps app window open until told otherwise