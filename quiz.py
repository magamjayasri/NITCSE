import tkinter as tk
import csv

class QuizEntryApp:
    def __init__(self, root):
        self.root = root
        root.title("Quiz Data Entry")
        # create labels and entries for each field
        self.fields = {}
        for i, label in enumerate(["Question", "Option A", "Option B", "Option C", "Correct Answer"]):
            tk.Label(root, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            self.fields[label] = tk.Entry(root, width=50)
            self.fields[label].grid(row=i, column=1, padx=5, pady=5)
        tk.Button(root, text="Submit", command=self.save_data).grid(row=5, column=0, columnspan=2, pady=10)

    def save_data(self):
        row = [self.fields[l].get() for l in ["Question", "Option A", "Option B", "Option C", "Correct Answer"]]
        if all(row):
            with open("quiz_data.csv", "a", newline="") as f:
                csv.writer(f).writerow(row)
            for ent in self.fields.values():
                ent.delete(0, tk.END)
        else:
            tk.messagebox.showerror("Error", "All fields must be filled")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizEntryApp(root)
    root.mainloop()
