import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from calender_ui import Ui_MainWindow  

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 여기에 추가 기능 및 슬롯 연결을 작성합니다
        # self.someButton.clicked.connect(s
    # def someFunction(self):
    #     print("Button clicked")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())