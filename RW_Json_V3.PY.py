import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class ConfigGUI:
    def __init__(self, root):
        self.root = root
        root.title("CSV Config Editor (Python 3.5+)")

        # Initialize variables
        self.scan_path = ""
        self.csv_files = []
        self.original_json = {}
        self.modified_json = {}

        # ---------------- TOP BUTTONS ----------------
        top = tk.Frame(root)
        top.pack(fill="x", padx=10, pady=10)

        tk.Button(top, text="Select CSV Folder", command=self.select_folder).pack(side="left")
        self.scan_label = tk.Label(top, text="No folder selected", fg="red")
        self.scan_label.pack(side="left", padx=10)

        tk.Button(top, text="Load Existing Config", command=self.load_config).pack(side="right", padx=5)
        tk.Button(top, text="Generate Config File", command=self.generate_config).pack(side="right", padx=5)

        # ---------------- DB COUNT INPUT ----------------
        db_frame = tk.Frame(root)
        db_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(db_frame, text="Number of AS databases:").pack(side="left")
        self.db_count_entry = tk.Entry(db_frame, width=5)
        self.db_count_entry.insert(0, "3")
        self.db_count_entry.pack(side="left", padx=5)

        tk.Button(db_frame, text="Generate DB Blocks", command=self.generate_db_blocks).pack(side="left", padx=5)

        # ---------------- SCROLLABLE AREA ----------------
        self.canvas = tk.Canvas(root)
        self.frame = tk.Frame(self.canvas)
        self.scroll = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll.set)

        self.scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Dictionary to hold all DB blocks
        self.db_blocks = {}

        # Categories for AS/OS DBs
        self.categories = ["ORPHAN", "RNI", "Barren", "SRS_TO_SDD", "SDD_TO_CODE"]
        # Categories for Test block
        self.test_categories = ["AS_SDD_2_CHILD", "AS_SRS_2_CHILD", "OS_SDD_2_CHILD", "OS_SRS_2_CHILD"]

    # ----------------- Select folder + scan CSVs -----------------
    def select_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return

        self.scan_path = folder
        self.scan_label.config(text="Scan Path: " + folder, fg="green")
        self.workaround_path = os.path.join(folder, "WorkAround")

        # Scan CSV files
        self.csv_files = [f for f in os.listdir(folder) if f.lower().endswith(".csv")]

        # Update dropdowns in all DB blocks
        for db in self.db_blocks:
            self.update_dropdowns(self.db_blocks[db])

        messagebox.showinfo("Folder Loaded", f"Found {len(self.csv_files)} CSV files.")

    # ----------------- Generate DB blocks (AS/OS/Test) -----------------
    def generate_db_blocks(self):
        try:
            count = int(self.db_count_entry.get())
        except:
            messagebox.showerror("Error", "Enter valid number.")
            return

        # Clear old blocks
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.db_blocks = {}

        # Create AS1..ASn + OS + Test
        db_list = ["AS" + str(i) for i in range(1, count + 1)]
        db_list.append("OS")
        db_list.append("Test")  # Include Test block

        for db in db_list:
            if db == "Test":
                self.db_blocks[db] = self.create_test_block(db)
            else:
                self.db_blocks[db] = self.create_db_block(db)

    # ----------------- Create AS/OS DB block -----------------
    def create_db_block(self, db_name):
        frame = tk.LabelFrame(self.frame, text=db_name, padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=10)

        dropdowns = {}

        for cat in self.categories:
            row = tk.Frame(frame)
            row.pack(fill="x", pady=5)

            tk.Label(row, text=cat + ": ", width=15, anchor="w").pack(side="left")

            cb = ttk.Combobox(row, values=self.csv_files, state="readonly", width=40)
            cb.pack(side="left", padx=5)

            old_label = tk.Label(row, text="Old: <none>", fg="blue", anchor="w")
            old_label.pack(side="left", padx=5)

            dropdowns[cat] = {"combo": cb, "old": old_label}

        return dropdowns

    # ----------------- Create Test block -----------------
    def create_test_block(self, db_name):
        frame = tk.LabelFrame(self.frame, text=db_name, padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=10)

        dropdowns = {}

        for cat in self.test_categories:
            row = tk.Frame(frame)
            row.pack(fill="x", pady=5)

            tk.Label(row, text=cat + ": ", width=25, anchor="w").pack(side="left")

            cb = ttk.Combobox(row, values=self.csv_files, state="readonly", width=40)
            cb.pack(side="left", padx=5)

            old_label = tk.Label(row, text="Old: <none>", fg="blue", anchor="w")
            old_label.pack(side="left", padx=5)

            dropdowns[cat] = {"combo": cb, "old": old_label}

        return dropdowns

    # ----------------- Update dropdowns -----------------
    def update_dropdowns(self, dropdowns):
        for cat in dropdowns:
            dropdowns[cat]["combo"]["values"] = self.csv_files

    # ----------------- Load existing JSON config -----------------
    def load_config(self):
        file = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file:
            return

        with open(file, "r") as f:
            self.original_json = json.load(f)
            self.modified_json = json.loads(json.dumps(self.original_json))

        # Load scan path
        if "scan_path" in self.original_json:
            self.scan_path = self.original_json["scan_path"]
            self.scan_label.config(text="Scan Path: " + self.scan_path, fg="green")

            if os.path.isdir(self.scan_path):
                self.csv_files = [f for f in os.listdir(self.scan_path) if f.endswith(".csv")]

        # Load sets data
        sets_data = self.original_json.get("sets", {})
        count = len([k for k in sets_data if k.startswith("AS")])

        self.db_count_entry.delete(0, tk.END)
        self.db_count_entry.insert(0, str(count))

        # Regenerate DB blocks including Test
        self.generate_db_blocks()

        # Populate dropdowns and old labels
        for db, mapping in sets_data.items():
            if db not in self.db_blocks:
                continue

            for cat, filepath in mapping.items():
                if cat not in self.db_blocks[db]:
                    continue  # ignore extra keys

                filename = os.path.basename(filepath)
                if filename in self.csv_files:
                    self.db_blocks[db][cat]["combo"].set(filename)

                self.db_blocks[db][cat]["old"].config(text="Old: " + filepath)

        messagebox.showinfo("Config Loaded", "Config loaded successfully!")

    # ----------------- Save updated JSON config -----------------
    def generate_config(self):
        if not self.scan_path:
            messagebox.showerror("Error", "Please select CSV folder first.")
            return

        self.modified_json["scan_path"] = self.scan_path
        self.modified_json["WorkAroundParentFolder"] = os.path.join(self.scan_path, "WorkAround")

        if "sets" not in self.modified_json:
            self.modified_json["sets"] = {}

        for db, block in self.db_blocks.items():
            if db not in self.modified_json["sets"]:
                self.modified_json["sets"][db] = {}

            for cat in block:
                val = block[cat]["combo"].get()
                if val:
                    self.modified_json["sets"][db][cat] = os.path.join(self.scan_path, val)

        save_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile="Database_Configuration.json"
        )

        if not save_path:
            return

        with open(save_path, "w") as f:
            json.dump(self.modified_json, f, indent=4)

        messagebox.showinfo("Saved", "Config updated (only changed values modified).")

# ----------------- Start application -----------------
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1050x700")
    ConfigGUI(root)
    root.mainloop()
