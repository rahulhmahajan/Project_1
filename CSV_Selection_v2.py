import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import csv
import os
from tkinter import ttk

csv_data = []
csv_headers = []
csv_file = None

def set_status(msg):
    """Update status bar"""
    status_var.set(msg)

def load_csv():
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
            set_status("Loaded {} records from {}".format(len(csv_data), os.path.basename(file_path)))
    except Exception as e:
        messagebox.showerror("Error", "Failed to read CSV:\n" + str(e))

def refresh_table(filtered=None):
    """Clear and repopulate the table"""
    for col in tree.get_children():
        tree.delete(col)

    tree["columns"] = csv_headers
    tree["show"] = "headings"

    for h in csv_headers:
        tree.heading(h, text=h)
        tree.column(h, width=120, anchor="center")

    data_to_show = filtered if filtered is not None else csv_data
    for i, row in enumerate(data_to_show):
        tag = "evenrow" if i % 2 == 0 else "oddrow"
        tree.insert("", tk.END, values=row, tags=(tag,))

    tree.tag_configure("evenrow", background="#f0f0f0")
    tree.tag_configure("oddrow", background="#ffffff")

def delete_record():
    global csv_data
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("No Selection", "Please select a record to delete.")
        return

    deleted_count = 0
    for item in sel:
        values = tree.item(item, "values")
        if values in csv_data:
            csv_data.remove(list(values))
            deleted_count += 1
        tree.delete(item)

    set_status("Deleted {} record(s)".format(deleted_count))

def save_csv():
    global csv_file
    if not csv_file:
        messagebox.showwarning("No File", "Load a CSV file first.")
        return

    try:
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(csv_headers)
            writer.writerows(csv_data)
        set_status("Saved {} records to {}".format(len(csv_data), os.path.basename(csv_file)))
    except Exception as e:
        messagebox.showerror("Error", "Failed to save CSV:\n" + str(e))

def search_records():
    query = search_var.get().strip().lower()
    if not query:
        refresh_table()
        set_status("Showing all records")
        return

    filtered = [row for row in csv_data if any(query in str(cell).lower() for cell in row)]
    refresh_table(filtered)
    set_status("Found {} matching records".format(len(filtered)))

def on_right_click(event):
    try:
        menu.tk_popup(event.x_root, event.y_root)
    finally:
        menu.grab_release()

# --- GUI ---
root = tk.Tk()
root.title("Interactive CSV Manager")
root.geometry("900x550")

# Top controls
frame_top = tk.Frame(root)
frame_top.pack(pady=5, fill="x")

btn_load = tk.Button(frame_top, text="📂 Load CSV", width=12, command=load_csv)
btn_load.pack(side="left", padx=5)

btn_delete = tk.Button(frame_top, text="🗑 Delete", width=12, command=delete_record)
btn_delete.pack(side="left", padx=5)

btn_save = tk.Button(frame_top, text="💾 Save", width=12, command=save_csv)
btn_save.pack(side="left", padx=5)

tk.Label(frame_top, text="🔍 Search:").pack(side="left", padx=5)
search_var = tk.StringVar()
entry_search = tk.Entry(frame_top, textvariable=search_var, width=30)
entry_search.pack(side="left")
btn_search = tk.Button(frame_top, text="Go", command=search_records)
btn_search.pack(side="left", padx=3)

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

# Status bar
status_var = tk.StringVar(value="Ready")
status_bar = tk.Label(root, textvariable=status_var, relief="sunken", anchor="w")
status_bar.pack(fill="x", side="bottom")

# Right-click menu
menu = tk.Menu(root, tearoff=0)
menu.add_command(label="Delete Row", command=delete_record)
menu.add_command(label="Save CSV", command=save_csv)

tree.bind("<Button-3>", on_right_click)   # right click
root.bind("<Delete>", lambda e: delete_record())   # delete key
root.bind("<Control-s>", lambda e: save_csv())     # ctrl+s save

root.mainloop()
