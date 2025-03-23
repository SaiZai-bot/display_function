import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from expenses_database import saving_to_database, fetch_database
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

day_count = 1  # Initialize the day counter
all_data = []  # List to store past days' data
total_amount = 0  # Initialize total amount

#PART NI ZAI displaying fields
def display_table_Chart(data, budget):  
    global chart_frame

    root.geometry("")

    for widget in root.winfo_children():
        widget.destroy()

    header = tk.Label(root, text="Duration Complete", font=("Arial", 14, "bold"))
    header.pack(side="top", fill="x")

    content_frame = tk.Frame(root)
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

    total_expenses = 1500 #for sample to HAA

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


#pra sa pie Chart
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

# kay WANG NA FUNCTION
def show_data():
    pass

#DATABASE

duration_days = 3 #sample plng pra sa inputs ko

def insert_data():
    """Inserts data into the table and updates the total amount."""
    global total_amount, current_inputs

    current_inputs = [] #pra sa display mastore current inputs

    date = date_entry.get()
    category = category_combo.get()
    item = item_entry.get()
    amount = amount_entry.get()
    
    if date and category and item and amount:
        try:
            amount = float(amount)  # Convert amount to float for summation
            tree.insert("", "end", values=(date, category, item, f"{amount:.2f}"))
            total_amount += amount  # Update total
            update_total_label()  # Refresh the total amount display

            current_inputs.append((date, category, item, amount)) #LAGAY SA DAY_DATA pra sa display ko (ZAI)
            saving_to_database(date, category, item, amount) #lagay sa database

            reset_inputs()  # Reset input fields after inserting data
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a number.")
    else:
        messagebox.showerror("Missing Data", "Please complete all fields before inserting.")

def reset_inputs():
    """Clears input fields for new entry."""
    date_entry.set_date(None)  # Reset date field correctly
    category_combo.set("")  # Reset category selection
    item_entry.delete(0, tk.END)  # Clear item field
    amount_entry.delete(0, tk.END)  # Clear amount field

def next_day():
    """Progresses the day count, saves current data, resets table, and keeps total."""
    global day_count, all_data, total_amount, day_data, current_inputs
    
    # Check if there is at least one entry before proceeding
    if not tree.get_children():
        messagebox.showwarning("No Data Entered", "Please insert at least one expense before moving to the next day.")
        return

    # Save the current day's data
    day_data = []
    for item in tree.get_children():
        day_data.append(tree.item(item)["values"])  # Store row data
    
    if day_data:
        all_data.append((f"Day {day_count}", day_data))  # Store with day label
    


    if day_count == duration_days: # pra mag display si table at pie chart pag si days nag reach sa duration
        all_expenses = [item for day, data in all_data for item in data]
        budget = [total_amount] # pra sa calculations
        display_table_Chart(all_expenses, budget) #function pang display
        return


    # Increment the day count
    day_count += 1
    day_label.config(text=f"Day {day_count}")
    
    # Clear the table for the new day
    tree.delete(*tree.get_children())

    # Reset input fields
    reset_inputs()

def update_total_label():
    """Updates the total amount label."""
    total_label.config(text=f"Total: {total_amount:.2f}")  # Format to 2 decimal places

def create_gui():
    global date_entry, category_combo, item_entry, amount_entry, tree, day_label, total_label, root
    
    root = tk.Tk()
    root.title("Expense Tracker")
    root.configure(bg="purple")
    
    # Style Configuration
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))  # Bold headers

    
    # Day Label
    day_label = tk.Label(root, text=f"Day {day_count}", font=("Arial", 16, "bold"), fg="white", bg="purple")
    day_label.place(x=100, y=15)
    
    # Input Form
    form_frame = tk.Frame(root, bg="purple")
    form_frame.place(x=10, y=50)
    
    tk.Label(form_frame, text="Date", font=("Arial", 12, "bold"), fg="white", bg="purple").grid(row=0, column=0, sticky="w")
    date_entry = DateEntry(form_frame, font=("Arial", 12), width=18, background='darkblue', foreground='white', borderwidth=2)
    date_entry.grid(row=1, column=0, pady=5)
    
    tk.Label(form_frame, text="Category", font=("Arial", 12, "bold"), fg="white", bg="purple").grid(row=2, column=0, sticky="w")
    category_combo = ttk.Combobox(form_frame, font=("Arial", 12), width=18, values=["Food", "Transport", "Entertainment", "Rent", "Utilities", "Others"])
    category_combo.grid(row=3, column=0, pady=5)
    
    tk.Label(form_frame, text="Item", font=("Arial", 12, "bold"), fg="white", bg="purple").grid(row=4, column=0, sticky="w")
    item_entry = tk.Entry(form_frame, font=("Arial", 12), width=20, bg="lightyellow")
    item_entry.grid(row=5, column=0, pady=5)
    
    tk.Label(form_frame, text="Amount", font=("Arial", 12, "bold"), fg="white", bg="purple").grid(row=6, column=0, sticky="w")
    amount_entry = tk.Entry(form_frame, font=("Arial", 12), width=20, bg="lightyellow")
    amount_entry.grid(row=7, column=0, pady=5)
    
    # Button Frame (Insert & Next Side by Side)
    button_frame = tk.Frame(form_frame, bg="purple")
    button_frame.grid(row=8, column=0, pady=10, columnspan=2)
    
    tk.Button(button_frame, text="Insert", font=("Arial", 12, "bold"), bg="lightyellow", command=insert_data).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Next", font=("Arial", 12, "bold"), bg="lightyellow", command=next_day).pack(side=tk.LEFT, padx=5)
    
    # Table Frame
    table_frame = tk.Frame(root, bg="lightgray", bd=2)
    table_frame.place(x=250, y=50, width=600, height=300)
    
    # Table Header and Treeview
    columns = ("Date", "Category", "Item", "Amount")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col)  # Bold headers
        tree.column(col, width=140, anchor="center")  # Center align data
    
    tree.pack(expand=True, fill="both")
    
    # Remaining & Total Section
    footer_frame = tk.Frame(root, bg="lightyellow", padx=10, pady=5)
    footer_frame.place(x=250, y=360, width=600)
    
    tk.Label(footer_frame, text="Remaining:\t\t", font=("Arial", 12, "bold"), bg="lightyellow").grid(row=0, column=0, sticky="w")
    
    # Total Amount Label (Updated Dynamically)
    total_label = tk.Label(footer_frame, text="Total: 0.00", font=("Arial", 12, "bold"), bg="lightyellow")
    total_label.grid(row=0, column=1, sticky="e")

    root.geometry("880x450")
    root.mainloop()

create_gui()