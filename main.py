import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
import requests
from datetime import datetime

# Replace with your OpenWeatherMap API key
API_KEY = "YpW%2FVjNv55RDuJKf3n3Zz7HcnAz5ZDZuvfNKk3vCfhNw0oEUq%2Fz39qUbIWjvnR4bPZHciViKMSqMMUF2e0Ns6g%3D%3D"
CITY_NAME = "Seoul"

def get_weather():
    try:
        url = f"(문서보고 추가하기)"
        response = requests.get(url)
        weather_data = response.json()

        if weather_data["cod"] != 200:
            messagebox.showerror("Error", "Failed to get weather data")
            return None
        
        temp = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
        return temp, description
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather & Calendar App")
        self.root.geometry("400x600")

        self.weather_frame = ttk.Frame(root)
        self.weather_frame.pack(pady=10)

        self.temp_label = ttk.Label(self.weather_frame, text="Temperature: -- °C")
        self.temp_label.grid(row=0, column=0, padx=5)

        self.desc_label = ttk.Label(self.weather_frame, text="Description: --")
        self.desc_label.grid(row=0, column=1, padx=5)

        self.update_weather()

        self.calendar_frame = ttk.Frame(root)
        self.calendar_frame.pack(pady=10)

        self.calendar = Calendar(self.calendar_frame, selectmode='day')
        self.calendar.pack()

        self.todo_frame = ttk.Frame(root)
        self.todo_frame.pack(pady=10)

        self.todo_list = tk.Listbox(self.todo_frame, height=10, width=50)
        self.todo_list.pack(side=tk.LEFT, padx=10)

        self.scrollbar = ttk.Scrollbar(self.todo_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.todo_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.todo_list.yview)

        self.entry = ttk.Entry(root, width=50)
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.add_todo)

        self.save_button = ttk.Button(root, text="Save To-Do List", command=self.save_todo_list)
        self.save_button.pack(pady=5)

        self.load_button = ttk.Button(root, text="Load To-Do List", command=self.load_todo_list)
        self.load_button.pack(pady=5)

    def update_weather(self):
        weather = get_weather()
        if weather:
            temp, description = weather
            self.temp_label.config(text=f"Temperature: {temp} °C")
            self.desc_label.config(text=f"Description: {description}")

        self.root.after(600000, self.update_weather)  # Update every 10 minutes

    def add_todo(self, event):
        todo = self.entry.get()
        if todo:
            self.todo_list.insert(tk.END, todo)
            self.entry.delete(0, tk.END)

    def save_todo_list(self):
        todos = self.todo_list.get(0, tk.END)
        with open("todo_list.txt", "w") as file:
            for todo in todos:
                file.write(todo + "\n")
        messagebox.showinfo("Info", "To-Do List saved successfully")

    def load_todo_list(self):
        try:
            with open("todo_list.txt", "r") as file:
                todos = file.readlines()
            self.todo_list.delete(0, tk.END)
            for todo in todos:
                self.todo_list.insert(tk.END, todo.strip())
            messagebox.showinfo("Info", "To-Do List loaded successfully")
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No saved To-Do List found")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
