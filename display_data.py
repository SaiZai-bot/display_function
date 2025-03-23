"""
categories
food
transportation
utilities
rent
entertainment
other
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from expenses_database import saving_to_database, fetch_database

updated_database = fetch_database()

#functions

current_day = 0
duration_day = 0

budget_list = []

#for next day and update of database
def delete_items():
    global current_inputs

    date = datein.get()
    category = categoryin.get()
    item = itemin.get()
    amount = amountin.get()

    saving_to_database(date, category, item, amount)

    current_inputs.append((date, category, item, amount))

    categoryin.delete(0, tk.END)
    itemin.delete(0, tk.END)
    amountin.delete(0, tk.END)

#for next day
def next_day():
    global current_day, current_inputs, duration_day, chart_frame

    current_day += 1

    if current_day < duration_day:
        messagebox.showinfo("Next Day", f"Moving to Day {current_day + 1}")
        datein.delete(0, tk.END)

    else:
        messagebox.showinfo("Data Entry Complete", "You have entered data for all days.")
        
        print(f"current inputs: {current_inputs}")
        display_table_Chart(current_inputs, budget_list)

# mawala ang mga widgets
def clear_widgets():
    for widget in window.winfo_children():
            widget.destroy()


#show yung entries
def show_fields():
    global current_day, duration_day, current_inputs, budget_list

    try:
        duration_day = int(durationin.get())
        budget_value = float(budgetin.get())
        if duration_day <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input")

    budget_list.clear()
    budget_list.append(budget_value)
    current_day = 0

    current_inputs = []
  
    date.grid(row=3, column=0)
    datein.grid(row=3, column=1)

    category.grid(row=4, column=0)        
    categoryin.grid(row=4, column=1)

    item.grid(row=5, column=0)
    itemin.grid(row=5, column=1)

    amount.grid(row=6, column=0)
    amountin.grid(row=6, column=1)

    insert.grid(row=7, column=0)
    next_btn.grid(row=7, column=1)


#displaying of table from database
def display_table_Chart(data, budget):  
    global chart_frame

    window.geometry("")

    for widget in window.winfo_children():
        widget.destroy()

    header = tk.Label(window, text="Duration Complete", font=("Arial", 14, "bold"))
    header.pack(side="top", fill="x")

    content_frame = tk.Frame(window)
    content_frame.pack(side="top", fill="both", expand=True, padx=20, pady=10)


    table_frame = tk.Frame(content_frame)
    table_frame.pack(side="top", fill="both", expand=True, pady=(0, 10))

    height_database = min(len(data), 50)
    table = ttk.Treeview(table_frame, columns=("Date", "Category", "Item", "Amount"), show="headings", height= height_database)

    table.heading("Date", text="Date", anchor="center")
    table.heading("Category", text="Category", anchor="center")
    table.heading("Item", text="Item", anchor="center")
    table.heading("Amount", text="Amount", anchor="center")

    table.column("Date", width=120, anchor="center")
    table.column("Category", width=120, anchor="center")
    table.column("Item", width=120, anchor="center")
    table.column("Amount", width=120, anchor="center")

    total_expenses = 0

    for row in data:
        table.insert("","end", values=row)
        total_expenses += float(row[3])

    table.pack(side="top", fill="both", expand=True, padx=10, pady=5)
    table.tag_configure("summary", font=("Arial", 10, "bold"))

    budget_left = budget[0] - total_expenses

    budget_row = ("Budget Left", f"{budget_left:.2f}", "TOTAL", f"{total_expenses:.2f}")

    table.insert("", "end", values=budget_row, tags=("summary",))

    if 'chart_frame' in globals() and chart_frame.winfo_exists():
        chart_frame.destroy()

    chart_frame = tk.Frame(content_frame)
    chart_frame.pack(side="top", fill="both", expand=True, pady=(10, 20))

    for_pie_chart(data)

    button_frame = tk.Frame(content_frame)
    button_frame.pack(side="top", fill="x", pady=(10, 20))

    save_button = tk.Button(button_frame, text="SAVE", command=show_data)
    save_button.pack(side="left", padx=20, pady=5)

    delete_button = tk.Button(button_frame, text="DELETE")
    delete_button.pack(side="right", padx=20, pady=5)

    messagebox.showinfo("Information", f"Congrats you have completed the duration. You have saved {budget_left:.2f}")
    messagebox.showwarning("Attention", "Press save if you want to visit your history. Delete if you want to remove all")

#kay Wang
def show_data():
    pass

#display pie chart
def for_pie_chart(data):
    global chart_frame

    category_totals = {}

    for row in data:
        category = row[1]
        amount = float(row[3])

        if category in  category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount

    labels = list(category_totals.keys())
    values = list(category_totals.values())

    fig = Figure(figsize=(4, 4), dpi=100)
    plot = fig.add_subplot(111)

    if sum(values) > 0:
        plot.pie(values, labels=labels, autopct="%1.1f%%")
        plot.set_title("Price of Categories based on Budget")
    else:
        plot.text(0.5, 0.5, "No data available", ha='center', va='center')

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    canvas.draw()

    



#inserting data
window = tk.Tk()
window.title("Insert data")
window.geometry("900x300+300+100")

duration = tk.Label(window, text ="duration (days)")
duration.grid(row=0, column=0)
durationin = tk.Entry(window, width=20)
durationin.grid(row=0, column=1)

budget = tk.Label(window, text="budget")
budget.grid(row=1, column=0)
budgetin = tk.Entry(window, width=20)
budgetin.grid(row=1, column=1)


confirm = tk.Button(window, text="Confirm", command=show_fields)
confirm.grid(row=2, columnspan=2)


date = tk.Label(window, text="date")
datein = tk.Entry(window, width=20)


category = tk.Label(window, text="category")
categoryin = tk.Entry(window, width=20)


item  = tk.Label(window, text="item")
itemin = tk.Entry(window, width=20)


amount = tk.Label(window, text="amount")
amountin = tk.Entry(window, width=20)


insert = tk.Button(window, text="insert", command=delete_items)

#main kong function
next_btn = tk.Button(window, text="Next Day", command=next_day)


window.mainloop()