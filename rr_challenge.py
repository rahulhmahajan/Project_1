# -*- coding: utf-8 -*-
import os
import json

try:
    # Python 2
    import Tkinter as tk
    import tkFileDialog
    import ttk
except ImportError:
    # Python 3
    import tkinter as tk
    from tkinter import filedialog as tkFileDialog
    from tkinter import ttk

CONFIG_FILE = "config.json"
selected_folder = None
file_list = []
set_frames = []
dropdowns = {}


def log(msg):
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)


def load_existing_config():
    if not os.path.exists(CONFIG_FILE):
        log("No previous config found.")
        return

    try:
        with open(CONFIG_FILE, "r") as f:
            json.load(f)
        log("Existing config found but NOT preloading values.")
    except:
        log("Error reading config.json")


def scan_folder():
    global selected_folder, file_list

    folder = tkFileDialog.askdirectory()
    if not folder:
        log("No folder selected. Scan cancelled.")
        return

    selected_folder = folder
    log("Scanning folder: " + folder)

    file_list = []
    try:
        for f in os.listdir(folder):
            low = f.lower()
            if low.endswith((".xlsx", ".xls", ".csv")):
                file_list.append(f)
    except Exception as e:
        log("Error scanning folder: " + str(e))
        return

    log(f"Found {len(file_list)} file(s).")
    refresh_dropdowns()


def refresh_dropdowns():
    """Update all comboboxes values after scanning."""
    for set_id in dropdowns:
        for key in dropdowns[set_id]:
            dropdowns[set_id][key]["values"] = file_list


def create_sets():
    """Create dynamic dropdown rows based on number entered."""
    global set_frames, dropdowns

    for frame in set_frames:
        frame.destroy()
    set_frames.clear()
    dropdowns.clear()

    try:
        count = int(entry_count.get())
    except:
        log("Enter a valid number of sets!")
        return

    keys = ["Barren", "orphan", "RNI", "SDD_TO_CODE", "SRS_TO_CODE"]

    for i in range(count):
        set_name = f"DataBase{i+1}"

        frame = tk.LabelFrame(scrollable_frame, text=set_name)
        frame.pack(padx=8, pady=4, fill="x")
        set_frames.append(frame)

        dropdowns[set_name] = {}

        for row_index, key in enumerate(keys):
            tk.Label(frame, text=key, anchor="w", width=12).grid(row=row_index, column=0, padx=5, pady=3, sticky="w")

            var = tk.StringVar()
            combo = ttk.Combobox(frame, textvariable=var, width=60)
            combo.grid(row=row_index, column=1, padx=5, pady=3, sticky="w")

            dropdowns[set_name][key] = combo

    refresh_dropdowns()
    log(f"UI updated for {count} sets.")

    root.update()
    canvas.configure(scrollregion=canvas.bbox("all"))


def save_config():
    if not selected_folder:
        log("Scan a folder first!")
        return

    try:
        count = int(entry_count.get())
    except:
        log("Enter valid number of sets!")
        return

    config_data = {"No_of_database": count, "Repo_dir": selected_folder, "sets": {}}

    for set_name in dropdowns:
        config_data["sets"][set_name] = {}

        # regular dropdown values
        for key, widget in dropdowns[set_name].items():
            fname = widget.get()
            full = os.path.join(selected_folder, fname) if fname else ""
            config_data["sets"][set_name][key] = full

        # ---- Add 2 fixed filenames (no path) ----
        set_index = set_name.replace("DataBase", "")
        config_data["sets"][set_name]["TOP_TO_BOTTOM"] = f"database{set_index}_top_to_bottom_out.csv"
        config_data["sets"][set_name]["BOTTOM_TO_TOP"] = f"database{set_index}_bottom_to_top.csv"

    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f, indent=4)
        log("Config saved to " + CONFIG_FILE)
    except Exception as e:
        log("Error writing config: " + str(e))



# ================= GUI =================
root = tk.Tk()
root.title("Config Builder")

# ---- Top Controls ----
top = tk.Frame(root)
top.pack(pady=6)

tk.Label(top, text="Number of Sets:").pack(side="left")
entry_count = tk.Entry(top, width=5)
entry_count.pack(side="left", padx=5)

tk.Button(top, text="Apply", command=create_sets).pack(side="left", padx=5)
tk.Button(root, text="Scan Folder", command=scan_folder).pack(pady=5)
tk.Button(root, text="Save Config", command=save_config).pack(pady=5)

# ---- Log Output ----
log_box = tk.Text(root, height=8, width=95)
log_box.pack(pady=5)

# ---- Scrollable area ----
container = tk.Frame(root)
container.pack(fill="both", expand=True)

canvas = tk.Canvas(container)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

scrollable_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")


def update_scroll_region(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))


scrollable_frame.bind("<Configure>", update_scroll_region)

load_existing_config()
root.mainloop()
