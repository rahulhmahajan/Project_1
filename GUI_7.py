import tkinter as tk
from tkinter import messagebox


# ---------------------------
# Logging function
# ---------------------------
def log_message(msg):
    log_box.config(state="normal")
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)
    log_box.config(state="disabled")


# ---------------------------
# Dummy function for Project Maps
# ---------------------------
def open_project_maps():
    log_message("Project Maps opened (dummy function).")


# ---------------------------
# Submit Function
# ---------------------------
def submit_form():
    project_path = entry_project.get().strip()
    rev_start = entry_rev_start.get().strip()
    rev_end = entry_rev_end.get().strip()

    if not project_path or not rev_start or not rev_end:
        messagebox.showerror("Error", "All fields must be filled!")
        return

    credentials = "Project Path: {}\nRevision Start: {}\nRevision End: {}".format(
        project_path, rev_start, rev_end
    )
    messagebox.showinfo("Submitted Credentials", credentials)
    log_message("Form submitted with credentials:\n" + credentials)


# ---------------------------
# Root Window
# ---------------------------
root = tk.Tk()
root.title("Dark Dashboard GUI")
root.geometry("950x600")
root.configure(bg="#1e1e1e")

# ---------------------------
# Sidebar (Left)
# ---------------------------
sidebar = tk.Frame(root, bg="#2d2d2d", width=150)
sidebar.pack(side="left", fill="y")

buttons_sidebar = ["Overview", "Pods", "Deployments", "Jobs", "Events"]
for btn in buttons_sidebar:
    b = tk.Button(sidebar, text=btn, fg="white", bg="#2d2d2d", relief="flat",
                  activebackground="#3a3a3a", command=lambda name=btn: log_message(name + " clicked"))
    b.pack(fill="x", pady=2)

# ---------------------------
# Top Navigation Bar
# ---------------------------
topbar = tk.Frame(root, bg="#2d2d2d", height=40)
topbar.pack(side="top", fill="x")

tabs = ["Overview", "Pods", "Deployments", "DaemonSets", "StatefulSets"]
for tab in tabs:
    t = tk.Button(topbar, text=tab, fg="white", bg="#2d2d2d", relief="flat",
                  activebackground="#3a3a3a", command=lambda name=tab: log_message("Tab " + name + " selected"))
    t.pack(side="left", padx=5, pady=5)

# ---------------------------
# Main Content Area
# ---------------------------
main_frame = tk.Frame(root, bg="#1e1e1e")
main_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

# Form labels and entries
tk.Label(main_frame, text="Project Path:", bg="#1e1e1e", fg="white").grid(row=0, column=0, sticky="w", pady=5)
entry_project = tk.Entry(main_frame, width=40)
entry_project.grid(row=0, column=1, pady=5)

tk.Label(main_frame, text="Revision Start:", bg="#1e1e1e", fg="white").grid(row=1, column=0, sticky="w", pady=5)
entry_rev_start = tk.Entry(main_frame, width=40)
entry_rev_start.grid(row=1, column=1, pady=5)

tk.Label(main_frame, text="Revision End:", bg="#1e1e1e", fg="white").grid(row=2, column=0, sticky="w", pady=5)
entry_rev_end = tk.Entry(main_frame, width=40)
entry_rev_end.grid(row=2, column=1, pady=5)

# Radio Buttons for Rev Start
rev_start_type = tk.StringVar(value="Development Path")
frame_radio1 = tk.Frame(main_frame, bg="#1e1e1e")
frame_radio1.grid(row=1, column=2, padx=10, sticky="w")
tk.Radiobutton(frame_radio1, text="Development Path", variable=rev_start_type, value="Development Path", bg="#1e1e1e",
               fg="white").pack(anchor="w")
tk.Radiobutton(frame_radio1, text="Mainline", variable=rev_start_type, value="Mainline", bg="#1e1e1e", fg="white").pack(
    anchor="w")
tk.Radiobutton(frame_radio1, text="Revision", variable=rev_start_type, value="Revision", bg="#1e1e1e", fg="white").pack(
    anchor="w")

# Radio Buttons for Rev End
rev_end_type = tk.StringVar(value="Development Path")
frame_radio2 = tk.Frame(main_frame, bg="#1e1e1e")
frame_radio2.grid(row=2, column=2, padx=10, sticky="w")
tk.Radiobutton(frame_radio2, text="Development Path", variable=rev_end_type, value="Development Path", bg="#1e1e1e",
               fg="white").pack(anchor="w")
tk.Radiobutton(frame_radio2, text="Mainline", variable=rev_end_type, value="Mainline", bg="#1e1e1e", fg="white").pack(
    anchor="w")
tk.Radiobutton(frame_radio2, text="Revision", variable=rev_end_type, value="Revision", bg="#1e1e1e", fg="white").pack(
    anchor="w")

# Submit Button
submit_btn = tk.Button(main_frame, text="Submit", command=submit_form, bg="#007acc", fg="white")
submit_btn.grid(row=3, column=1, pady=20)

# ---------------------------
# Log/Terminal at bottom
# ---------------------------
log_frame = tk.Frame(root, bg="#000000", height=150)
log_frame.pack(side="bottom", fill="x")

log_box = tk.Text(log_frame, bg="black", fg="white", height=10, state="disabled")
log_box.pack(fill="both", expand=True)

# ---------------------------
# Menu Bar
# ---------------------------
menu_bar = tk.Menu(root)
project_menu = tk.Menu(menu_bar, tearoff=0)
project_menu.add_command(label="Project Maps", command=open_project_maps)
menu_bar.add_cascade(label="File", menu=project_menu)
menu_bar.add_command(label="Help", command=lambda: log_message("Help clicked"))
root.config(menu=menu_bar)

# ---------------------------
# Run App
# ---------------------------
log_message("Application started.")
root.mainloop()
