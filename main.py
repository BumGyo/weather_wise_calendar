import sys
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import QDate, QTimer, QTime
from calender_ui import Ui_MainWindow

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.api_key = '41c136f4da01d88aca640b5fc695dd9f'  # Replace with your OpenWeatherMap API key
        self.calendarWidget.selectionChanged.connect(self.show_weather)

        # 현재 시간을 표시할 레이블 추가
        self.currentTimeLabel = QLabel(self)
        self.currentTimeLabel.setGeometry(920, 20, 350, 100)  # 시간 표시 위치 및 크기 조정
        self.currentTimeLabel.setStyleSheet("font-size: 36px; font-weight: bold; color: blue;")  # 스타일 조정

        # 타이머를 사용하여 현재 시간 업데이트
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_current_time)
        self.timer.start(1000)  # 1초마다 업데이트

    def show_weather(self):
        selected_date = self.calendarWidget.selectedDate()
        date_str = selected_date.toString('yyyy-MM-dd')
        weather_info = self.get_weather(date_str)
        self.weatherLabel.setText(f"Weather on {date_str}: {weather_info}")

    def get_weather(self, date_str):
        city = 'Seoul'  # You can change this to any city
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]['description']
            temperature = data['main']['temp']
            return f"{weather}, {temperature}°C"
        else:
            return "Error fetching weather data"

    def update_current_time(self):
        current_time = QTime.currentTime().toString('hh:mm:ss')
        self.currentTimeLabel.setText(current_time)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())