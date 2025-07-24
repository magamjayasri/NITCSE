import tkinter as tk
from tkinter import messagebox

class GradeCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grade Calculator")

        self.subjects = ["Math", "Science", "English", "History", "Art"]

        self.entries = {}
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Enter marks for each subject (0-100):").grid(row=0, column=0, columnspan=2, pady=10)

        for i, subject in enumerate(self.subjects, start=1):
            tk.Label(self.root, text=subject + ":").grid(row=i, column=0, sticky='e', padx=5, pady=2)
            entry = tk.Entry(self.root, width=10)
            entry.grid(row=i, column=1, pady=2)
            self.entries[subject] = entry

        tk.Button(self.root, text="Calculate", command=self.calculate_grades).grid(row=len(self.subjects)+1, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(self.root, text="", justify="left", font=("Arial", 12))
        self.result_label.grid(row=len(self.subjects)+2, column=0, columnspan=2)

    def calculate_grades(self):
        marks = []
        for subject in self.subjects:
            try:
                mark = float(self.entries[subject].get())
                if not (0 <= mark <= 100):
                    raise ValueError
                marks.append(mark)
            except ValueError:
                messagebox.showerror("Invalid input", f"Please enter a valid number (0-100) for {subject}.")
                return

        total = sum(marks)
        average = total / len(marks)
        grade = self.get_letter_grade(average)

        result_text = f"Total Marks: {total:.2f}\nAverage Marks: {average:.2f}\nGrade: {grade}"
        self.result_label.config(text=result_text)

    def get_letter_grade(self, avg):
        if avg >= 90:
            return "A"
        elif avg >= 80:
            return "B"
        elif avg >= 70:
            return "C"
        elif avg >= 60:
            return "D"
        else:
            return "F"

if __name__ == "__main__":
    root = tk.Tk()
    app = GradeCalculatorApp(root)
    root.mainloop()
