import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TIME_SLOTS = ["08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00",
              "12:00-13:00", "13:00-14:00", "14:00-15:00", "15:00-16:00"]

DATA_FILE = "timetable_data.json"

class TimetableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weekly Timetable Scheduler")

        self.schedule = {}  # {(day, time): course_name}

        self.create_widgets()
        self.load_schedule()

    def create_widgets(self):
        # Buttons
        tk.Button(self.root, text="Add/Edit Course", command=self.add_edit_course).grid(row=0, column=0, columnspan=len(DAYS)+1, pady=10)

        # Timetable grid labels
        tk.Label(self.root, text="Time / Day").grid(row=1, column=0, padx=5, pady=5)
        for col, day in enumerate(DAYS, start=1):
            tk.Label(self.root, text=day, borderwidth=1, relief="solid", width=15).grid(row=1, column=col)

        # Create grid of labels for timetable slots
        self.cells = {}
        for row, timeslot in enumerate(TIME_SLOTS, start=2):
            tk.Label(self.root, text=timeslot, borderwidth=1, relief="solid", width=15).grid(row=row, column=0)
            for col, day in enumerate(DAYS, start=1):
                label = tk.Label(self.root, text="", borderwidth=1, relief="solid", width=15, height=2, bg="white")
                label.grid(row=row, column=col, padx=1, pady=1)
                label.bind("<Button-1>", lambda e, d=day, t=timeslot: self.edit_slot(d, t))
                self.cells[(day, timeslot)] = label

        # Save button
        tk.Button(self.root, text="Save Schedule", command=self.save_schedule).grid(row=len(TIME_SLOTS)+2, column=0, columnspan=len(DAYS)+1, pady=10)

    def add_edit_course(self):
        # Input course info
        day = simpledialog.askstring("Day", f"Enter day ({', '.join(DAYS)}):")
        if day not in DAYS:
            messagebox.showerror("Error", "Invalid day entered.")
            return

        timeslot = simpledialog.askstring("Time Slot", f"Enter time slot ({', '.join(TIME_SLOTS)}):")
        if timeslot not in TIME_SLOTS:
            messagebox.showerror("Error", "Invalid time slot entered.")
            return

        course = simpledialog.askstring("Course", "Enter course name:")
        if not course:
            messagebox.showerror("Error", "Course name cannot be empty.")
            return

        self.schedule[(day, timeslot)] = course
        self.update_cell(day, timeslot)

    def edit_slot(self, day, timeslot):
        current_course = self.schedule.get((day, timeslot), "")
        new_course = simpledialog.askstring("Edit Course", f"Current course: {current_course}\nEnter new course name (or leave empty to delete):")
        if new_course == "":
            # Delete entry
            if (day, timeslot) in self.schedule:
                del self.schedule[(day, timeslot)]
        elif new_course:
            self.schedule[(day, timeslot)] = new_course
        self.update_cell(day, timeslot)

    def update_cell(self, day, timeslot):
        label = self.cells[(day, timeslot)]
        course = self.schedule.get((day, timeslot), "")
        label.config(text=course, bg="lightgreen" if course else "white")

    def save_schedule(self):
        # Convert keys to string for JSON
        json_data = {f"{day}|{time}": course for (day, time), course in self.schedule.items()}
        with open(DATA_FILE, "w") as f:
            json.dump(json_data, f)
        messagebox.showinfo("Saved", "Schedule saved successfully.")

    def load_schedule(self):
        if not os.path.exists(DATA_FILE):
            return
        with open(DATA_FILE, "r") as f:
            json_data = json.load(f)
        for key, course in json_data.items():
            day, time = key.split("|")
            self.schedule[(day, time)] = course
            self.update_cell(day, time)


if __name__ == "__main__":
    root = tk.Tk()
    app = TimetableApp(root)
    root.mainloop()
