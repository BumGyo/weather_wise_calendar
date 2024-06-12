# main.py
import sys
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import QDate
from calender_ui import Ui_MainWindow

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.api_key = '68548aa7522943958ef20615241206'  # Replace with your WeatherAPI key
        self.calendarWidget.selectionChanged.connect(self.show_weather)

    def show_weather(self):
        selected_date = self.calendarWidget.selectedDate()
        date_str = selected_date.toString('yyyy-MM-dd')
        try:
            weather_info = self.get_weather(date_str)
            self.weatherLabel.setText(f"Weather on {date_str}: {weather_info}")
        except Exception as e:
            self.show_error_message(str(e))

    def get_weather(self, date_str):
        city = 'Seoul'  # You can change this to any city
        selected_date = QDate.fromString(date_str, 'yyyy-MM-dd')
        current_date = QDate.currentDate()
        max_forecast_days = 15
        
        try:
            if selected_date <= current_date:
                url = f'http://api.weatherapi.com/v1/history.json?key={self.api_key}&q={city}&dt={date_str}'
            elif selected_date <= current_date.addDays(max_forecast_days):
                url = f'http://api.weatherapi.com/v1/forecast.json?key={self.api_key}&q={city}&dt={date_str}'
            else:
                return "Weather data is not available beyond 2 weeks in the future"
            
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            
            data = response.json()
            if selected_date <= current_date:
                weather = data['forecast']['forecastday'][0]['day']['condition']['text']
                temperature = data['forecast']['forecastday'][0]['day']['avgtemp_c']
            else:
                weather = data['forecast']['forecastday'][0]['day']['condition']['text']
                temperature = data['forecast']['forecastday'][0]['day']['avgtemp_c']
            return f"{weather}, {temperature}°C"
        except requests.RequestException as e:
            raise Exception("Network error: " + str(e))
        except (KeyError, IndexError) as e:
            raise Exception("Data parsing error: " + str(e))
        except Exception as e:
            raise Exception("An unexpected error occurred: " + str(e))

    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText("Error")
        msg.setInformativeText(message)
        msg.setWindowTitle("Error")
        msg.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
