import tkinter as tk
from tkinter import messagebox


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
        "Project Path: {}\nRevision Start: {} ({})\nRevision End: {} ({})".format(
            project, rev_start, choice2, rev_end, choice3
        )
    )


def about_app():
    messagebox.showinfo("About", "Integrity Tool GUI\nCreated with Tkinter")


def exit_app():
    root.quit()


def open_project_maps():
    """Dummy function triggered from File > Project Maps"""
    project = entry1.get().strip()
    if not project:
        messagebox.showwarning("Warning", "Please enter a Project Path first!")
    else:
        # dummy function behavior
        messagebox.showinfo("Project Maps", "Opening maps for project:\n{}".format(project))


# Main window
root = tk.Tk()
root.title("Integrity Tool GUI")
root.geometry("650x250")

# ----- Menu Bar -----
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

# ----- Widgets -----
# Project Path row
tk.Label(root, text="Project Path:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry1 = tk.Entry(root, width=30)
entry1.grid(row=0, column=1, padx=10, pady=5)

# Revision Start row
tk.Label(root, text="Revision Start:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry2 = tk.Entry(root, width=30)
entry2.grid(row=1, column=1, padx=10, pady=5)

radio_var2 = tk.StringVar()
radio_var2.set("Development Path")

frame_radio2 = tk.Frame(root)
frame_radio2.grid(row=1, column=2, padx=10, pady=5, sticky="w")
tk.Radiobutton(frame_radio2, text="Development Path", variable=radio_var2, value="Development Path").pack(side="left")
tk.Radiobutton(frame_radio2, text="Mainline", variable=radio_var2, value="Mainline").pack(side="left")
tk.Radiobutton(frame_radio2, text="Revision", variable=radio_var2, value="Revision").pack(side="left")

# Revision End row
tk.Label(root, text="Revision End:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry3 = tk.Entry(root, width=30)
entry3.grid(row=2, column=1, padx=10, pady=5)

radio_var3 = tk.StringVar()
radio_var3.set("Development Path")

frame_radio3 = tk.Frame(root)
frame_radio3.grid(row=2, column=2, padx=10, pady=5, sticky="w")
tk.Radiobutton(frame_radio3, text="Development Path", variable=radio_var3, value="Development Path").pack(side="left")
tk.Radiobutton(frame_radio3, text="Mainline", variable=radio_var3, value="Mainline").pack(side="left")
tk.Radiobutton(frame_radio3, text="Revision", variable=radio_var3, value="Revision").pack(side="left")

# Submit button
tk.Button(root, text="Submit", command=on_button_click).grid(row=3, column=1, pady=20)

root.mainloop()
