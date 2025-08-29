import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import csv
import os
from tkinter import ttk

csv_data = []
csv_headers = []
csv_file = None

def load_csv():
    """Open and load a CSV file"""
    global csv_data, csv_headers, csv_file
    file_path = filedialog.askopenfilename(
        title="Open CSV File",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if not file_path:
        return

    try:
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            rows = list(reader)
            if not rows:
                messagebox.showwarning("Empty", "CSV file is empty")
                return

            csv_headers[:] = rows[0]
            csv_data[:] = rows[1:]
            csv_file = file_path
            refresh_table()
            messagebox.showinfo("Loaded", "CSV file loaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", "Failed to read CSV:\n" + str(e))


def refresh_table():
    """Clear and repopulate the table"""
    for col in tree.get_children():
        tree.delete(col)

    tree["columns"] = csv_headers
    tree["show"] = "headings"

    # set headings
    for h in csv_headers:
        tree.heading(h, text=h)
        tree.column(h, width=100, anchor="center")

    # insert rows
    for row in csv_data:
        tree.insert("", tk.END, values=row)


def delete_record():
    """Delete selected row"""
    global csv_data
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("No Selection", "Please select a record to delete.")
        return

    for item in sel:
        values = tree.item(item, "values")
        if values in csv_data:
            csv_data.remove(list(values))
        tree.delete(item)

    messagebox.showinfo("Deleted", "Selected record(s) deleted.")


def save_csv():
    """Save current data back to file (overwrite)"""
    global csv_file
    if not csv_file:
        messagebox.showwarning("No File", "Load a CSV file first.")
        return

    try:
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(csv_headers)
            writer.writerows(csv_data)
        messagebox.showinfo("Saved", "CSV file saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", "Failed to save CSV:\n" + str(e))


# --- GUI ---
root = tk.Tk()
root.title("CSV Reader & Delete Records")
root.geometry("800x500")

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

btn_load = tk.Button(frame_top, text="Load CSV", width=12, command=load_csv)
btn_load.grid(row=0, column=0, padx=5)

btn_delete = tk.Button(frame_top, text="Delete Record", width=15, command=delete_record)
btn_delete.grid(row=0, column=1, padx=5)

btn_save = tk.Button(frame_top, text="Save CSV", width=12, command=save_csv)
btn_save.grid(row=0, column=2, padx=5)

# Table
frame_table = tk.Frame(root)
frame_table.pack(fill="both", expand=True)

tree = ttk.Treeview(frame_table)
tree.pack(side="left", fill="both", expand=True)

scroll_y = tk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
scroll_y.pack(side="right", fill="y")
tree.configure(yscrollcommand=scroll_y.set)

scroll_x = tk.Scrollbar(root, orient="horizontal", command=tree.xview)
scroll_x.pack(fill="x")
tree.configure(xscrollcommand=scroll_x.set)

root.mainloop()
