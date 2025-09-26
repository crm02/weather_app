import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,QVBoxLayout)

from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):   
        super().__init__()
        self.city_label = QLabel("Enter city name: " , self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel("70°",self)
        self.emoji_label = ("☀︎",self)
        self.description_label = QLabel("Sunny", self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("WeatherApp")

if __name__ =="__main__":
    app = QApplication(sys.argv)

    weather_app = WeatherApp()
    weather_app.show() # Shows app window
    sys.exit(app.exec_())  #Keeps app window open until told otherwise