import tkinter as tk
from tkinter import messagebox, END

# ---------- Log Function ----------
def log_message(msg):
    log_text.config(state="normal")   # allow editing
    log_text.insert(END, msg + "\n")  # add message
    log_text.see(END)                 # auto scroll
    log_text.config(state="disabled") # lock again

# ---------- Dummy Functions ----------
def dummy_project_maps():
    log_message("Project Maps function called")
    messagebox.showinfo("Project Maps", "Project Maps function called")

def dummy_action(name):
    log_message("Sidebar button clicked: " + name)
    messagebox.showinfo("Clicked", "You clicked " + name)

# ---------- Submit Form ----------
def submit_form():
    project_path = entry_project.get().strip()
    rev_start = entry_rev_start.get().strip()
    rev_end = entry_rev_end.get().strip()

    if not project_path or not rev_start or not rev_end:
        log_message("Error: One or more fields are empty")
        messagebox.showerror("Error", "All fields must be filled out!")
        return

    log_message("Form submitted successfully with values:")
    log_message("Project Path: " + project_path)
    log_message("Revision Start: " + rev_start + " (" + rev_start_option.get() + ")")
    log_message("Revision End: " + rev_end + " (" + rev_end_option.get() + ")")

    messagebox.showinfo("Success", "Form submitted successfully!")

# ---------- Main Window ----------
root = tk.Tk()
root.title("Integrity Tool")
root.geometry("900x600")
root.config(bg="#f3f4f6")

# ---------- Menu Bar ----------
menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Project Maps", command=dummy_project_maps)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)

help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Integrity Tool v1.0"))
menubar.add_cascade(label="Help", menu=help_menu)
root.config(menu=menubar)

# ---------- Sidebar ----------
sidebar = tk.Frame(root, bg="#111827", width=200, height=600)
sidebar.pack(side="left", fill="y")

app_title = tk.Label(sidebar, text="Integrity Tool", bg="#111827", fg="white",
                     font=("Segoe UI", 14, "bold"), pady=20)
app_title.pack()

menu_items = ["Maps", "Sample2", "Sample3", "Sample4"]
for item in menu_items:
    btn = tk.Button(sidebar, text=item, bg="#1f2937", fg="white",
                    font=("Segoe UI", 11), anchor="w", padx=20, pady=8,
                    activebackground="#374151", activeforeground="white",
                    relief="flat", command=lambda i=item: dummy_action(i))
    btn.pack(fill="x", pady=2)

# ---------- Content Area ----------
content = tk.Frame(root, bg="#f3f4f6", padx=20, pady=20)
content.pack(side="top", fill="both", expand=True)

# Labels + Entries + Radios
lbl_project = tk.Label(content, text="Project Path:", bg="#f3f4f6", font=("Segoe UI", 11))
lbl_project.grid(row=0, column=0, sticky="w", pady=5)
entry_project = tk.Entry(content, width=40)
entry_project.grid(row=0, column=1, pady=5, padx=10)

lbl_rev_start = tk.Label(content, text="Revision Start:", bg="#f3f4f6", font=("Segoe UI", 11))
lbl_rev_start.grid(row=1, column=0, sticky="w", pady=5)
entry_rev_start = tk.Entry(content, width=40)
entry_rev_start.grid(row=1, column=1, pady=5, padx=10)

rev_start_option = tk.StringVar()
rev_start_option.set("Development Path")
tk.Radiobutton(content, text="Development Path", variable=rev_start_option, value="Development Path",
               bg="#f3f4f6").grid(row=1, column=2, sticky="w")
tk.Radiobutton(content, text="Mainline", variable=rev_start_option, value="Mainline",
               bg="#f3f4f6").grid(row=1, column=3, sticky="w")
tk.Radiobutton(content, text="Revision", variable=rev_start_option, value="Revision",
               bg="#f3f4f6").grid(row=1, column=4, sticky="w")

lbl_rev_end = tk.Label(content, text="Revision End:", bg="#f3f4f6", font=("Segoe UI", 11))
lbl_rev_end.grid(row=2, column=0, sticky="w", pady=5)
entry_rev_end = tk.Entry(content, width=40)
entry_rev_end.grid(row=2, column=1, pady=5, padx=10)

rev_end_option = tk.StringVar()
rev_end_option.set("Development Path")
tk.Radiobutton(content, text="Development Path", variable=rev_end_option, value="Development Path",
               bg="#f3f4f6").grid(row=2, column=2, sticky="w")
tk.Radiobutton(content, text="Mainline", variable=rev_end_option, value="Mainline",
               bg="#f3f4f6").grid(row=2, column=3, sticky="w")
tk.Radiobutton(content, text="Revision", variable=rev_end_option, value="Revision",
               bg="#f3f4f6").grid(row=2, column=4, sticky="w")

# ---------- Submit Button ----------
submit_btn = tk.Button(content, text="Submit", command=submit_form,
                       bg="#2563eb", fg="white", font=("Segoe UI", 11, "bold"),
                       padx=20, pady=5, relief="flat")
submit_btn.grid(row=3, column=1, pady=20)

# ---------- Log/Terminal ----------
log_frame = tk.Frame(root, bg="black", height=150)
log_frame.pack(side="bottom", fill="x")

log_text = tk.Text(log_frame, bg="black", fg="lime", font=("Consolas", 10), wrap="word")
log_text.pack(fill="both", expand=True)
log_text.config(state="disabled")  # start as read-only

# Start Log
log_message("Application started.")

root.mainloop()
