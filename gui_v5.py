import tkinter as tk
from tkinter import messagebox

# ---------- Logging Function ----------
def log_message(msg):
    log_text.config(state="normal")
    log_text.insert(tk.END, msg + "\n")
    log_text.see(tk.END)
    log_text.config(state="disabled")

# ---------- Dummy Handlers ----------
def project_maps_action():
    log_message("Project Maps menu clicked")
    messagebox.showinfo("Project Maps", "Dummy Project Maps function executed")

def about_app():
    messagebox.showinfo("About", "Sample GUI App\nCreated with Tkinter")

def exit_app():
    root.quit()

def sidebar_action(name):
    log_message("Sidebar button clicked: " + name)
    messagebox.showinfo("Clicked", "You clicked: " + name)

# ---------- Submit Handler ----------
def submit_form():
    project_path = entry_project.get().strip()
    rev_start = entry_rev_start.get().strip()
    rev_end = entry_rev_end.get().strip()

    if not project_path or not rev_start or not rev_end:
        log_message("Error: One or more fields are empty")
        messagebox.showerror("Error", "All fields must be filled out!")
        return

    # Prepare credentials
    credentials = (
        "Project Path: {}\n"
        "Revision Start: {} ({})\n"
        "Revision End: {} ({})"
    ).format(project_path, rev_start, rev_start_option.get(), rev_end, rev_end_option.get())

    # Log it
    log_message("Form submitted with credentials:\n" + credentials)

    # Show in alert
    messagebox.showinfo("Submitted Credentials", credentials)

# ---------- Main Window ----------
root = tk.Tk()
root.title("Integrity Tool")
root.geometry("800x500")
root.configure(bg="#f3f4f6")

# ---------- Menu Bar ----------
menubar = tk.Menu(root)

file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Project Maps", command=project_maps_action)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menubar.add_cascade(label="File", menu=file_menu)

help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=about_app)
menubar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menubar)

# ---------- Sidebar ----------
sidebar = tk.Frame(root, bg="#111827", width=200, height=500)
sidebar.pack(side="left", fill="y")

app_title = tk.Label(sidebar, text="Integrity Tool", bg="#111827", fg="white",
                     font=("Segoe UI", 14, "bold"), pady=20)
app_title.pack()

menu_items = ["Overview", "Services", "Jobs", "Events"]
for item in menu_items:
    btn = tk.Button(sidebar, text=item, bg="#1f2937", fg="white",
                    font=("Segoe UI", 11), anchor="w", padx=20, pady=8,
                    activebackground="#374151", activeforeground="white",
                    relief="flat", command=lambda i=item: sidebar_action(i))
    btn.pack(fill="x", pady=2)

# ---------- Main Form Area ----------
main_area = tk.Frame(root, bg="#f3f4f6", padx=20, pady=20)
main_area.pack(side="left", fill="both", expand=True)

# Project Path
tk.Label(main_area, text="Project Path:", bg="#f3f4f6", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w", pady=5)
entry_project = tk.Entry(main_area, width=40)
entry_project.grid(row=0, column=1, pady=5, sticky="w")

# Revision Start
tk.Label(main_area, text="Revision Start:", bg="#f3f4f6", font=("Segoe UI", 11)).grid(row=1, column=0, sticky="w", pady=5)
entry_rev_start = tk.Entry(main_area, width=25)
entry_rev_start.grid(row=1, column=1, pady=5, sticky="w")

rev_start_option = tk.StringVar()
rev_start_option.set("Development Path")
tk.Radiobutton(main_area, text="Development Path", variable=rev_start_option, value="Development Path",
               bg="#f3f4f6").grid(row=1, column=2, sticky="w")
tk.Radiobutton(main_area, text="Mainline", variable=rev_start_option, value="Mainline", bg="#f3f4f6").grid(row=1, column=3, sticky="w")
tk.Radiobutton(main_area, text="Revision", variable=rev_start_option, value="Revision", bg="#f3f4f6").grid(row=1, column=4, sticky="w")

# Revision End
tk.Label(main_area, text="Revision End:", bg="#f3f4f6", font=("Segoe UI", 11)).grid(row=2, column=0, sticky="w", pady=5)
entry_rev_end = tk.Entry(main_area, width=25)
entry_rev_end.grid(row=2, column=1, pady=5, sticky="w")

rev_end_option = tk.StringVar()
rev_end_option.set("Development Path")
tk.Radiobutton(main_area, text="Development Path", variable=rev_end_option, value="Development Path",
               bg="#f3f4f6").grid(row=2, column=2, sticky="w")
tk.Radiobutton(main_area, text="Mainline", variable=rev_end_option, value="Mainline", bg="#f3f4f6").grid(row=2, column=3, sticky="w")
tk.Radiobutton(main_area, text="Revision", variable=rev_end_option, value="Revision", bg="#f3f4f6").grid(row=2, column=4, sticky="w")

# Submit button
submit_btn = tk.Button(main_area, text="Submit", bg="#2563eb", fg="white",
                       font=("Segoe UI", 11, "bold"), padx=10, pady=5,
                       command=submit_form)
submit_btn.grid(row=3, column=0, columnspan=2, pady=20, sticky="w")

# ---------- Log Area ----------
log_frame = tk.Frame(main_area, bg="#f3f4f6")
log_frame.grid(row=4, column=0, columnspan=5, sticky="nsew", pady=10)

tk.Label(log_frame, text="Logs:", bg="#f3f4f6", font=("Segoe UI", 11, "bold")).pack(anchor="w")

log_text = tk.Text(log_frame, height=10, bg="black", fg="lime", insertbackground="white")
log_text.pack(fill="both", expand=True)
log_text.config(state="disabled")

# allow resizing of log box
main_area.rowconfigure(4, weight=1)
main_area.columnconfigure(1, weight=1)

root.mainloop()
