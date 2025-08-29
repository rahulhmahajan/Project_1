import tkinter as tk
import tkinter.messagebox as messagebox
import json
import os

CONFIG_FILE = "config.json"

def load_config():
    """Load config with items, defaults, selection, and ignore."""
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {"items": [], "defaults": [], "selection": [], "ignore": []}

def save_config():
    """Save updated selection/ignore into config file."""
    config["selection"] = list(lb_include.get(0, tk.END))
    config["ignore"] = list(lb_ignore.get(0, tk.END))
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
    messagebox.showinfo("Saved", "Config updated successfully!")

def move_selected(source, target):
    """Move selected items from one listbox to another."""
    selected = source.curselection()
    for i in selected[::-1]:  # reverse to prevent shifting indexes
        item = source.get(i)
        target.insert(tk.END, item)
        source.delete(i)

def clear_selection():
    """Move everything to ignore list."""
    lb_include.delete(0, tk.END)
    lb_ignore.delete(0, tk.END)
    for item in config["items"]:
        lb_ignore.insert(tk.END, item)
    save_config()

# --- GUI ---
root = tk.Tk()
root.title("Include / Ignore Manager with Defaults")
root.geometry("650x450")

config = load_config()

# Initialize selection/ignore if empty (first run → use defaults)
if not config["selection"] and not config["ignore"]:
    defaults = set(config.get("defaults", []))
    all_items = set(config.get("items", []))
    config["selection"] = sorted(list(defaults & all_items))
    config["ignore"] = sorted(list(all_items - defaults))
    # ❌ don't call save_config() here, listboxes aren't ready yet

# Frames
frame = tk.Frame(root)
frame.pack(pady=20)

# Include listbox
frame_include = tk.Frame(frame)
frame_include.grid(row=0, column=0, padx=20)
tk.Label(frame_include, text="Include (Selection)", font=("Arial", 12, "bold")).pack()
lb_include = tk.Listbox(frame_include, selectmode=tk.MULTIPLE, width=25, height=15)
lb_include.pack()

# Buttons to move items
frame_buttons = tk.Frame(frame)
frame_buttons.grid(row=0, column=1, padx=10)
btn_to_ignore = tk.Button(frame_buttons, text="→", width=5,
                          command=lambda: move_selected(lb_include, lb_ignore))
btn_to_ignore.pack(pady=5)
btn_to_include = tk.Button(frame_buttons, text="←", width=5,
                           command=lambda: move_selected(lb_ignore, lb_include))
btn_to_include.pack(pady=5)

# Ignore listbox
frame_ignore = tk.Frame(frame)
frame_ignore.grid(row=0, column=2, padx=20)
tk.Label(frame_ignore, text="Ignore", font=("Arial", 12, "bold")).pack()
lb_ignore = tk.Listbox(frame_ignore, selectmode=tk.MULTIPLE, width=25, height=15)
lb_ignore.pack()

# Bottom buttons
frame_bottom = tk.Frame(root)
frame_bottom.pack(pady=10)

btn_submit = tk.Button(frame_bottom, text="Submit", width=12, bg="lightgreen", command=save_config)
btn_submit.grid(row=0, column=0, padx=10)

btn_clear = tk.Button(frame_bottom, text="Clear", width=12, bg="lightcoral", command=clear_selection)
btn_clear.grid(row=0, column=1, padx=10)

# Populate listboxes
for item in config["selection"]:
    lb_include.insert(tk.END, item)
for item in config["ignore"]:
    lb_ignore.insert(tk.END, item)

# ✅ Now safe to save the config after populating UI
save_config()

root.mainloop()
