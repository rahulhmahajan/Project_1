import tkinter as tk
from tkinter import ttk, messagebox


def on_button_click():
    project = entry1.get().strip()
    rev_start = entry2.get().strip()
    rev_end = entry3.get().strip()

    if not project or not rev_start or not rev_end:
        messagebox.showwarning("Warning", "All fields must be filled before submitting!")
        return

    choice2 = radio_var2.get()
    choice3 = radio_var3.get()

    messagebox.showinfo(
        "Result",
        f"Project Path: {project}\nRevision Start: {rev_start} ({choice2})\nRevision End: {rev_end} ({choice3})"
    )


def about_app():
    messagebox.showinfo("About", "Integrity Tool GUI\nCreated with Tkinter")


def exit_app():
    root.quit()


def open_project_maps():
    project = entry1.get().strip()
    if not project:
        messagebox.showwarning("Warning", "Please enter a Project Path first!")
    else:
        messagebox.showinfo("Project Maps", f"Opening maps for project:\n{project}")


root = tk.Tk()
root.title("Integrity Tool GUI")
root.geometry("850x400")
root.configure(bg="#f8f9fa")  # light background

# ---------- Sidebar ----------
sidebar = tk.Frame(root, bg="#111827", width=200, height=400)
sidebar.pack(side="left", fill="y")

app_title = tk.Label(sidebar, text="Integrity Tool", bg="#111827", fg="white",
                     font=("Segoe UI", 14, "bold"), pady=20)
app_title.pack()

menu_items = ["Overview", "Services", "Jobs", "Events"]
for item in menu_items:
    lbl = tk.Label(sidebar, text=item, bg="#111827", fg="#d1d5db",
                   font=("Segoe UI", 11), anchor="w", padx=20, pady=8)
    lbl.pack(fill="x")

# ---------- Main Content ----------
main_frame = tk.Frame(root, bg="#f8f9fa", padx=30, pady=20)
main_frame.pack(side="right", expand=True, fill="both")

# Section: Form
section = tk.LabelFrame(main_frame, text="Project Configuration",
                        bg="white", font=("Segoe UI", 12, "bold"),
                        labelanchor="n", padx=20, pady=20, relief="groove")
section.pack(fill="x", pady=10)

# Project Path
ttk.Label(section, text="Project Path:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry1 = ttk.Entry(section, width=40)
entry1.grid(row=0, column=1, padx=10, pady=10)

# Revision Start
ttk.Label(section, text="Revision Start:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry2 = ttk.Entry(section, width=40)
entry2.grid(row=1, column=1, padx=10, pady=10)

radio_var2 = tk.StringVar(value="Development Path")
frame_radio2 = ttk.Frame(section)
frame_radio2.grid(row=1, column=2, padx=10, pady=10, sticky="w")
ttk.Radiobutton(frame_radio2, text="Development Path", variable=radio_var2, value="Development Path").pack(side="left")
ttk.Radiobutton(frame_radio2, text="Mainline", variable=radio_var2, value="Mainline").pack(side="left")
ttk.Radiobutton(frame_radio2, text="Revision", variable=radio_var2, value="Revision").pack(side="left")

# Revision End
ttk.Label(section, text="Revision End:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
entry3 = ttk.Entry(section, width=40)
entry3.grid(row=2, column=1, padx=10, pady=10)

radio_var3 = tk.StringVar(value="Development Path")
frame_radio3 = ttk.Frame(section)
frame_radio3.grid(row=2, column=2, padx=10, pady=10, sticky="w")
ttk.Radiobutton(frame_radio3, text="Development Path", variable=radio_var3, value="Development Path").pack(side="left")
ttk.Radiobutton(frame_radio3, text="Mainline", variable=radio_var3, value="Mainline").pack(side="left")
ttk.Radiobutton(frame_radio3, text="Revision", variable=radio_var3, value="Revision").pack(side="left")

# Submit button
submit_btn = ttk.Button(main_frame, text="Submit", command=on_button_click)
submit_btn.pack(pady=20)

# Menu Bar (still kept like original)
menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Project Maps", command=open_project_maps)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menubar.add_cascade(label="File", menu=file_menu)

help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=about_app)
menubar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menubar)

root.mainloop()
