import tkinter as tk
from tkinter import messagebox

# ---------- Function to log messages ----------
def log_message(msg):
    log_box.config(state="normal")
    log_box.insert("end", msg + "\n")
    log_box.see("end")
    log_box.config(state="disabled")

# ---------- Dummy function for Project Maps ----------
def open_project_maps():
    log_message("Project Maps opened (dummy function).")
    messagebox.showinfo("Project Maps", "Project Maps function called!")

# ---------- Submit function ----------
def submit_form():
    project_path = entry_project.get().strip()
    rev_start = entry_rev_start.get().strip()
    rev_end = entry_rev_end.get().strip()

    if not project_path or not rev_start or not rev_end:
        log_message("Error: One or more fields are empty")
        messagebox.showerror("Error", "All fields must be filled out!")
        return

    credentials = (
        "Project Path: {}\n"
        "Revision Start: {} ({})\n"
        "Revision End: {} ({})"
    ).format(project_path, rev_start, rev_start_option.get(),
             rev_end, rev_end_option.get())

    log_message("Form submitted with credentials:\n" + credentials)
    messagebox.showinfo("Submitted Credentials", credentials)

# ---------- Main Window ----------
root = tk.Tk()
root.title("Integrity Tool")
root.geometry("800x600")
root.configure(bg="#f3f4f6")

# ---------- Menu Bar ----------
menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Project Maps", command=open_project_maps)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)
root.config(menu=menubar)

# ---------- Sidebar ----------
sidebar = tk.Frame(root, bg="#111827", width=200, height=600)
sidebar.pack(side="left", fill="y")

# Tool Image
try:
    tool_img = tk.PhotoImage(file="tool.gif")  # must be .gif
    tool_label = tk.Label(sidebar, image=tool_img, bg="#111827")
    tool_label.image = tool_img
    tool_label.pack(pady=10)
except Exception as e:
    print("Could not load tool image:", e)

# Sidebar buttons
app_title = tk.Label(sidebar, text="Integrity Tool", bg="#111827", fg="white",
                     font=("Segoe UI", 14, "bold"), pady=10)
app_title.pack()

menu_items = ["Project Maps", "Services", "Jobs", "Events"]
for item in menu_items:
    btn = tk.Button(sidebar, text=item, bg="#1f2937", fg="white",
                    relief="flat", font=("Segoe UI", 11),
                    command=lambda x=item: log_message(x + " clicked"))
    btn.pack(fill="x", padx=10, pady=5)

# ---------- Main Content ----------
content = tk.Frame(root, bg="#f3f4f6", padx=20, pady=20)
content.pack(side="left", fill="both", expand=True)

# Project Path
tk.Label(content, text="Project Path:", bg="#f3f4f6", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w", pady=5)
entry_project = tk.Entry(content, width=40)
entry_project.grid(row=0, column=1, pady=5, sticky="w")

# Revision Start
tk.Label(content, text="Revision Start:", bg="#f3f4f6", font=("Segoe UI", 11)).grid(row=1, column=0, sticky="w", pady=5)
entry_rev_start = tk.Entry(content, width=20)
entry_rev_start.grid(row=1, column=1, pady=5, sticky="w")

rev_start_option = tk.StringVar(value="Development Path")
tk.Radiobutton(content, text="Development Path", variable=rev_start_option, value="Development Path", bg="#f3f4f6").grid(row=1, column=2, sticky="w")
tk.Radiobutton(content, text="Mainline", variable=rev_start_option, value="Mainline", bg="#f3f4f6").grid(row=1, column=3, sticky="w")
tk.Radiobutton(content, text="Revision", variable=rev_start_option, value="Revision", bg="#f3f4f6").grid(row=1, column=4, sticky="w")

# Revision End
tk.Label(content, text="Revision End:", bg="#f3f4f6", font=("Segoe UI", 11)).grid(row=2, column=0, sticky="w", pady=5)
entry_rev_end = tk.Entry(content, width=20)
entry_rev_end.grid(row=2, column=1, pady=5, sticky="w")

rev_end_option = tk.StringVar(value="Development Path")
tk.Radiobutton(content, text="Development Path", variable=rev_end_option, value="Development Path", bg="#f3f4f6").grid(row=2, column=2, sticky="w")
tk.Radiobutton(content, text="Mainline", variable=rev_end_option, value="Mainline", bg="#f3f4f6").grid(row=2, column=3, sticky="w")
tk.Radiobutton(content, text="Revision", variable=rev_end_option, value="Revision", bg="#f3f4f6").grid(row=2, column=4, sticky="w")

# Submit Button
submit_btn = tk.Button(content, text="Submit", bg="#2563eb", fg="white",
                       font=("Segoe UI", 11, "bold"), relief="flat",
                       command=submit_form)
submit_btn.grid(row=3, column=1, pady=20, sticky="w")

# ---------- Log Box (Terminal Style) ----------
log_frame = tk.Frame(content, bg="#e5e7eb")
log_frame.grid(row=4, column=0, columnspan=5, pady=10, sticky="nsew")

log_box = tk.Text(log_frame, height=10, width=80, state="disabled", bg="black", fg="lime", insertbackground="white")
log_box.pack(fill="both", expand=True)

# Allow resizing
content.grid_rowconfigure(4, weight=1)
content.grid_columnconfigure(1, weight=1)

# ---------- Run ----------
root.mainloop()
