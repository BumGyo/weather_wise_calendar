import sys
from PyQt6 import QtWidgets, QtCore
from calender_ui import Ui_MainWindow
from datetime import datetime

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Simulated weather data for demonstration purposes
        self.weather_data = {
            "2023-06-01": "Sunny, 25°C",
            "2023-06-02": "Cloudy, 22°C",
            "2023-06-03": "Rainy, 19°C",
        }
        self.calendarWidget.selectionChanged.connect(self.show_weather)
        self.todo_lists = {}
        self.completed_todo_lists = {}
        self.todoListWidget.itemChanged.connect(self.handleItemChanged)

    def show_weather(self):
        selected_date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        weather_info = self.weather_data.get(selected_date, "No data available")
        self.weatherLabel.setText(f"Weather on {selected_date}: {weather_info}")

    def addItem(self):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Add To-Do Item")
        dialog.resize(300, 200)

        layout = QtWidgets.QVBoxLayout()

        text_label = QtWidgets.QLabel("Enter a new to-do item:")
        layout.addWidget(text_label)
        text_input = QtWidgets.QLineEdit()
        layout.addWidget(text_input)

        time_label = QtWidgets.QLabel("Enter the time:")
        layout.addWidget(time_label)
        time_input = QtWidgets.QTimeEdit()
        time_input.setDisplayFormat("HH:mm")
        layout.addWidget(time_input)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(button_box)

        dialog.setLayout(layout)

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            item_text = text_input.text()
            item_time = time_input.time().toString("HH:mm")
            if item_text:
                item = QtWidgets.QListWidgetItem(f"{item_text} ({item_time})")
                item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(QtCore.Qt.CheckState.Unchecked)
                selected_date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
                if selected_date not in self.todo_lists:
                    self.todo_lists[selected_date] = []
                self.todo_lists[selected_date].append((item_text, item_time, QtCore.Qt.CheckState.Unchecked))
                self.loadTodoListForSelectedDate()  # Update the displayed list

    def removeItem(self):
        selected_items = self.todoListWidget.selectedItems()
        if not selected_items: return
        selected_date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        if selected_date in self.todo_lists:
            for item in selected_items:
                self.todoListWidget.takeItem(self.todoListWidget.row(item))
                for todo in self.todo_lists[selected_date]:
                    if f"{todo[0]} ({todo[1]})" == item.text():
                        self.todo_lists[selected_date].remove(todo)
                        break
        self.updateUncheckedTodoList()

    def handleItemChanged(self, item):
        font = item.font()
        selected_date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        if item.checkState() == QtCore.Qt.CheckState.Checked:
            font.setStrikeOut(True)
            # Save the completed item only if it's not already in the completed list
            if selected_date not in self.completed_todo_lists:
                self.completed_todo_lists[selected_date] = []
            if item.text() not in self.completed_todo_lists[selected_date]:
                self.completed_todo_lists[selected_date].append(item.text())
        else:
            font.setStrikeOut(False)
            # Remove item from the completed list if it is unchecked
            if selected_date in self.completed_todo_lists and item.text() in self.completed_todo_lists[selected_date]:
                self.completed_todo_lists[selected_date].remove(item.text())
        item.setFont(font)
        if selected_date in self.todo_lists:
            for i, todo in enumerate(self.todo_lists[selected_date]):
                if f"{todo[0]} ({todo[1]})" == item.text():
                    self.todo_lists[selected_date][i] = (todo[0], todo[1], item.checkState())
        self.updateUncheckedTodoList()

    def loadTodoListForSelectedDate(self):
        selected_date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        self.todoListWidget.clear()
        if selected_date in self.todo_lists:
            for todo in self.todo_lists[selected_date]:
                item = QtWidgets.QListWidgetItem(f"{todo[0]} ({todo[1]})")
                item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(todo[2])
                self.todoListWidget.addItem(item)
        self.updateUncheckedTodoList()

    def updateUncheckedTodoList(self):
        self.uncheckedTodoListWidget.clear()
        current_month = self.calendarWidget.selectedDate().toString("yyyy-MM")
        for date, todos in self.todo_lists.items():
            if date.startswith(current_month):
                for todo in todos:
                    if todo[2] == QtCore.Qt.CheckState.Unchecked:
                        item = QtWidgets.QListWidgetItem(f"{todo[0]} ({todo[1]}) - {date}")
                        self.uncheckedTodoListWidget.addItem(item)

    def openTodoListDialog(self):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("To-Do List")
        dialog.resize(400, 300)

        layout = QtWidgets.QVBoxLayout()

        buttons_layout = QtWidgets.QHBoxLayout()
        self.completedTasksButton = QtWidgets.QPushButton("Completed Tasks")
        self.pendingTasksButton = QtWidgets.QPushButton("Pending Tasks")
        buttons_layout.addWidget(self.completedTasksButton)
        buttons_layout.addWidget(self.pendingTasksButton)
        layout.addLayout(buttons_layout)

        self.yearComboBox = QtWidgets.QComboBox()
        self.yearComboBox.addItems([str(year) for year in range(2020, 2031)])
        self.monthComboBox = QtWidgets.QComboBox()
        self.monthComboBox.addItems([str(month).zfill(2) for month in range(1, 13)])

        # Set current year and month as default
        current_date = datetime.now()
        self.yearComboBox.setCurrentText(str(current_date.year))
        self.monthComboBox.setCurrentText(str(current_date.month).zfill(2))

        layout.addWidget(self.yearComboBox)
        layout.addWidget(self.monthComboBox)

        self.todoListTextEdit = QtWidgets.QTextEdit()
        layout.addWidget(self.todoListTextEdit)

        self.completedTasksButton.clicked.connect(self.showCompletedTasks)
        self.pendingTasksButton.clicked.connect(self.showPendingTasks)

        dialog.setLayout(layout)
        dialog.exec()

    def showCompletedTasks(self):
        selected_year = self.yearComboBox.currentText()
        selected_month = self.monthComboBox.currentText()
        self.todoListTextEdit.clear()
        for date, todos in self.completed_todo_lists.items():
            if date.startswith(f"{selected_year}-{selected_month}"):
                for todo in todos:
                    self.todoListTextEdit.append(f"{todo} - {date}")

    def showPendingTasks(self):
        selected_year = self.yearComboBox.currentText()
        selected_month = self.monthComboBox.currentText()
        self.todoListTextEdit.clear()
        for date, todos in self.todo_lists.items():
            if date.startswith(f"{selected_year}-{selected_month}"):
                for todo in todos:
                    if todo[2] == QtCore.Qt.CheckState.Unchecked:
                        self.todoListTextEdit.append(f"{todo[0]} ({todo[1]}) - {date}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
