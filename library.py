import tkinter as tk
from tkinter import ttk, messagebox
import csv

CSV_FILE = "library.csv"

def append_record(fields):
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(fields)

def load_table():
    for row in tree.get_children():
        tree.delete(row)
    try:
        with open(CSV_FILE, newline="") as f:
            reader = csv.reader(f)
            for r in reader:
                tree.insert("", "end", values=r)
    except FileNotFoundError:
        open(CSV_FILE, "w", newline="").close()

def submit():
    bid = entry_id.get().strip()
    title = entry_title.get().strip()
    author = entry_author.get().strip()
    avail = status_var.get()
    if not (bid and title and author):
        messagebox.showwarning("Input error", "ID, Title, and Author are required.")
        return
    append_record([bid, title, author, avail])
    entry_id.delete(0, tk.END)
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    load_table()
    messagebox.showinfo("Saved", "Record added")

root = tk.Tk()
root.title("Library Management")

tk.Label(root, text="Book ID").grid(row=0, column=0)
entry_id = tk.Entry(root); entry_id.grid(row=0, column=1)
tk.Label(root, text="Title").grid(row=1, column=0)
entry_title = tk.Entry(root); entry_title.grid(row=1, column=1)
tk.Label(root, text="Author").grid(row=2, column=0)
entry_author = tk.Entry(root); entry_author.grid(row=2, column=1)
status_var = tk.StringVar(value="Available")
tk.OptionMenu(root, status_var, "Available", "Borrowed").grid(row=3, column=1)

tk.Button(root, text="Submit", command=submit).grid(row=4, column=0, columnspan=2)

cols = ("ID", "Title", "Author", "Avail")
tree = ttk.Treeview(root, columns=cols, show="headings")
for c in cols:
    tree.heading(c, text=c)
tree.grid(row=5, column=0, columnspan=2)

load_table()
root.mainloop()
