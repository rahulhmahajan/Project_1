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
        f = open(CONFIG_FILE, "r")
        data = json.load(f)
        f.close()
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
            if low.endswith(".xlsx") or low.endswith(".xls") or low.endswith(".csv"):
                file_list.append(f)
    except Exception as e:
        log("Error scanning folder: " + str(e))
        return

    log("Found " + str(len(file_list)) + " file(s).")

    refresh_dropdowns()


def refresh_dropdowns():
    """Update all comboboxes values after scanning."""
    for set_id in dropdowns:
        for key in dropdowns[set_id]:
            combo = dropdowns[set_id][key]
            combo["values"] = file_list


def create_sets():
    """Create dynamic dropdown rows based on number entered."""
    global set_frames, dropdowns

    for frame in set_frames:
        frame.destroy()
    set_frames = []
    dropdowns = {}

    try:
        count = int(entry_count.get())
    except:
        log("Enter a valid number of sets!")
        return

    for i in range(count):
        set_name = "DataBase" + str(i + 1)

        frame = tk.LabelFrame(root, text=set_name)
        frame.pack(padx=5, pady=3, fill="x")
        set_frames.append(frame)

        dropdowns[set_name] = {}

        for key in ["Barren", "orphan", "RNI",'SDD_TO_CODE','SRS_TO_CODE']:
            row = tk.Frame(frame)
            row.pack(fill="x")
            tk.Label(row, text=key, width=6, anchor="w").pack(side="left")

            var = tk.StringVar()
            combo = ttk.Combobox(row, textvariable=var, width=60)
            combo.pack(side="left", padx=3)
            dropdowns[set_name][key] = combo

    refresh_dropdowns()
    log("UI updated for " + str(count) + " sets.")


def save_config():
    if not selected_folder:
        log("Scan a folder first!")
        return

    try:
        count = int(entry_count.get())
    except:
        log("Enter valid number of sets!")
        return

    config_data = {
        "count": count,
        "scan_path": selected_folder,
        "sets": {}
    }

    for set_name in dropdowns:
        config_data["sets"][set_name] = {}
        for key in dropdowns[set_name]:
            fname = dropdowns[set_name][key].get()
            full = os.path.join(selected_folder, fname) if fname else ""
            config_data["sets"][set_name][key] = full

    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f, indent=4)
        log("Config saved to " + CONFIG_FILE)
    except Exception as e:
        log("Error writing config: " + str(e))


# ---------------- GUI ----------------
root = tk.Tk()
root.title("Config Builder")

top = tk.Frame(root)
top.pack(pady=5)

tk.Label(top, text="Number of Sets:").pack(side="left")
entry_count = tk.Entry(top, width=5)
entry_count.pack(side="left", padx=5)

btn_apply = tk.Button(top, text="Apply", command=create_sets)
btn_apply.pack(side="left", padx=5)

btn_scan = tk.Button(root, text="Scan Folder", command=scan_folder)
btn_scan.pack(pady=5)

btn_save = tk.Button(root, text="Save Config", command=save_config)
btn_save.pack(pady=5)

log_box = tk.Text(root, height=10, width=80)
log_box.pack(pady=5)

# Load old config AFTER log_box exists
load_existing_config()


root.mainloop()
