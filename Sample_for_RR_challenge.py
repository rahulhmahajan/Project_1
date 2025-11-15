#!/usr/bin/env python3
"""
excel_config_gui.py

Tkinter GUI to:
 - Scan a chosen folder for .xls/.xlsx files
 - Let user create parameters (editable names)
 - Assign a file (or multiple files) to each parameter
 - Generate & save a config file (INI or JSON)
 - Show logs in a terminal-like pane
"""

import os
import json
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import configparser

SUPPORTED_EXT = (".xls", ".xlsx")

class ParameterRow:
    """UI element that represents one parameter row: name, selector (combobox or listbox), multi toggle, remove button"""
    def __init__(self, parent, files_getter, on_change_callback):
        """
        files_getter: callable -> list of available filenames
        on_change_callback: called when any assignment changes (for future use)
        """
        self.parent = parent
        self.files_getter = files_getter
        self.on_change = on_change_callback

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="x", pady=2, padx=4)

        # Parameter name
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(self.frame, textvariable=self.name_var, width=22)
        self.name_entry.insert(0, "PARAM")
        self.name_entry.grid(row=0, column=0, padx=(0,6))

        # Single/multi toggle
        self.multi_var = tk.BooleanVar(value=False)
        self.multi_cb = ttk.Checkbutton(self.frame, text="Multi", variable=self.multi_var, command=self._rebuild_selector)
        self.multi_cb.grid(row=0, column=1, padx=(0,6))

        # Placeholder for selector widget
        self.selector_container = ttk.Frame(self.frame)
        self.selector_container.grid(row=0, column=2, sticky="ew")
        self.frame.columnconfigure(2, weight=1)

        # Remove button
        self.remove_btn = ttk.Button(self.frame, text="Remove", command=self.destroy)
        self.remove_btn.grid(row=0, column=3, padx=6)

        # internal vars
        self._combobox = None
        self._listbox = None
        self._build_selector()

    def _build_selector(self):
        # initial build (combobox)
        self._clear_selector()
        files = self.files_getter()
        self.selector_var = tk.StringVar()
        self._combobox = ttk.Combobox(self.selector_container, values=files, textvariable=self.selector_var)
        self._combobox.state(["readonly"])
        self._combobox.bind("<<ComboboxSelected>>", lambda e: self.on_change())
        self._combobox.pack(fill="x")

    def _clear_selector(self):
        for widget in self.selector_container.winfo_children():
            widget.destroy()
        self._combobox = None
        self._listbox = None

    def _rebuild_selector(self):
        self._clear_selector()
        files = self.files_getter()
        if self.multi_var.get():
            # listbox with multiple selection
            lb = tk.Listbox(self.selector_container, selectmode="extended", height=4, exportselection=False)
            for f in files:
                lb.insert(tk.END, f)
            lb.pack(fill="both", expand=True)
            lb.bind("<<ListboxSelect>>", lambda e: self.on_change())
            self._listbox = lb
        else:
            self.selector_var = tk.StringVar()
            cb = ttk.Combobox(self.selector_container, values=files, textvariable=self.selector_var)
            cb.state(["readonly"])
            cb.bind("<<ComboboxSelected>>", lambda e: self.on_change())
            cb.pack(fill="x")
            self._combobox = cb

    def update_files(self):
        """Call when the folder files changed; refresh options but keep selection if possible"""
        files = self.files_getter()
        if self._combobox:
            current = self._combobox.get()
            self._combobox["values"] = files
            if current in files:
                self._combobox.set(current)
            else:
                self._combobox.set("")
        elif self._listbox:
            # rebuild listbox contents keeping selections of items still present
            selected = {self._listbox.get(i) for i in self._listbox.curselection()}
            self._listbox.delete(0, tk.END)
            for f in files:
                self._listbox.insert(tk.END, f)
            # restore selections
            for i, f in enumerate(files):
                if f in selected:
                    self._listbox.selection_set(i)

    def get_assignment(self):
        """Return None if nothing selected, string for single, list for multi"""
        name = self.name_var.get().strip()
        if not name:
            return None, None
        if self._combobox:
            val = self._combobox.get().strip()
            if val == "":
                return name, None
            return name, val
        elif self._listbox:
            sel = [self._listbox.get(i) for i in self._listbox.curselection()]
            return name, sel if sel else None
        return name, None

    def destroy(self):
        self.frame.destroy()
        # caller should remove reference from its list

class ExcelConfigGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel → Config Generator")
        self.root.geometry("880x600")

        self.available_files = []
        self.param_rows = []

        # Top toolbar: folder selection + refresh + save
        toolbar = ttk.Frame(root)
        toolbar.pack(fill="x", padx=6, pady=6)

        ttk.Label(toolbar, text="Folder:").pack(side="left")
        self.folder_var = tk.StringVar()
        self.folder_entry = ttk.Entry(toolbar, textvariable=self.folder_var, width=60)
        self.folder_entry.pack(side="left", padx=6)
        ttk.Button(toolbar, text="Browse", command=self.browse_folder).pack(side="left", padx=4)
        ttk.Button(toolbar, text="Refresh", command=self.scan_folder).pack(side="left", padx=4)
        ttk.Separator(toolbar, orient="vertical").pack(side="left", fill="y", padx=8)

        ttk.Label(toolbar, text="Config Format:").pack(side="left")
        self.format_var = tk.StringVar(value="ini")
        ttk.Radiobutton(toolbar, text="INI", variable=self.format_var, value="ini").pack(side="left", padx=2)
        ttk.Radiobutton(toolbar, text="JSON", variable=self.format_var, value="json").pack(side="left", padx=2)

        ttk.Button(toolbar, text="Generate & Save Config", command=self.generate_and_save).pack(side="right")

        # Middle: left = files list, right = parameters
        middle = ttk.Frame(root)
        middle.pack(fill="both", expand=True, padx=6, pady=4)

        # Left pane: files found
        left = ttk.LabelFrame(middle, text="Excel Files Found")
        left.pack(side="left", fill="both", expand=False, padx=(0,6), pady=2)
        left.config(width=300)
        self.files_listbox = tk.Listbox(left, height=20, width=45)
        self.files_listbox.pack(side="left", fill="both", expand=True, padx=4, pady=4)
        files_scroll = ttk.Scrollbar(left, orient="vertical", command=self.files_listbox.yview)
        files_scroll.pack(side="right", fill="y")
        self.files_listbox.configure(yscrollcommand=files_scroll.set)

        # Right pane: parameters
        right = ttk.LabelFrame(middle, text="Parameters")
        right.pack(side="left", fill="both", expand=True, pady=2)
        self.params_container = ttk.Frame(right)
        self.params_container.pack(fill="both", expand=True, padx=4, pady=4)

        # buttons to add/remove params and load defaults
        params_toolbar = ttk.Frame(right)
        params_toolbar.pack(fill="x", padx=4, pady=(0,6))
        ttk.Button(params_toolbar, text="Add Parameter", command=self.add_parameter).pack(side="left")
        ttk.Button(params_toolbar, text="Add Common Defaults", command=self.add_default_parameters).pack(side="left", padx=6)
        ttk.Button(params_toolbar, text="Clear All Params", command=self.clear_parameters).pack(side="left", padx=6)

        # bottom: logs
        log_frame = ttk.LabelFrame(root, text="Log")
        log_frame.pack(fill="both", expand=False, padx=6, pady=6)
        self.log = tk.Text(log_frame, height=10, wrap="word")
        self.log.pack(fill="both", expand=True, padx=4, pady=4)
        self.log.config(state="disabled")

        # Initialize with a couple of params
        self.add_default_parameters()
        # start with current directory
        self.folder_var.set(os.getcwd())
        self.scan_folder()

    def log_write(self, text):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.log.config(state="normal")
        self.log.insert(tk.END, f"[{timestamp}] {text}\n")
        self.log.see(tk.END)
        self.log.config(state="disabled")

    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.folder_var.get() or os.getcwd())
        if folder:
            self.folder_var.set(folder)
            self.scan_folder()

    def scan_folder(self):
        folder = self.folder_var.get().strip()
        if not folder or not os.path.isdir(folder):
            messagebox.showwarning("Folder missing", "Please choose a valid folder path.")
            return
        files = sorted(f for f in os.listdir(folder) if f.lower().endswith(SUPPORTED_EXT))
        self.available_files = files
        # update files listbox
        self.files_listbox.delete(0, tk.END)
        for f in files:
            self.files_listbox.insert(tk.END, f)
        # notify parameter rows to update their choices
        for pr in list(self.param_rows):
            pr.update_files()
        self.log_write(f"Scanned folder: {folder} — {len(files)} excel file(s) found")

    def add_parameter(self):
        pr = ParameterRow(self.params_container, files_getter=lambda: self.available_files, on_change_callback=lambda: self.log_write("Parameter changed"))
        # set default name unique
        idx = len(self.param_rows) + 1
        pr.name_var.set(f"PARAM_{idx}")
        self.param_rows.append(pr)
        self.log_write(f"Added parameter: {pr.name_var.get()}")

    def add_default_parameters(self):
        defaults = ["Input_File", "Mapping_File", "Lookup_File", "Report_File"]
        # if params already exist, don't add duplicates names; just append numeric suffix
        for d in defaults:
            name = d
            i = 1
            existing_names = {p.name_var.get() for p in self.param_rows}
            while name in existing_names:
                i += 1
                name = f"{d}_{i}"
            self.add_parameter()
            self.param_rows[-1].name_var.set(name)

    def clear_parameters(self):
        for p in list(self.param_rows):
            p.destroy()
        self.param_rows.clear()
        self.log_write("Cleared all parameters")

    def gather_config(self):
        """Return dict mapping param_name -> value (string or list). Validate names unique and non-empty."""
        cfg = {}
        errors = []
        seen = set()
        for pr in self.param_rows:
            name, val = pr.get_assignment()
            if name is None or name == "":
                errors.append("One parameter has an empty name.")
                continue
            if name in seen:
                errors.append(f"Duplicate parameter name: {name}")
                continue
            seen.add(name)
            # val may be None (not assigned)
            cfg[name] = val
        return cfg, errors

    def generate_and_save(self):
        cfg, errors = self.gather_config()
        if errors:
            messagebox.showerror("Validation error", "\n".join(errors))
            return
        if not cfg:
            messagebox.showwarning("No parameters", "No parameters defined.")
            return

        fmt = self.format_var.get().lower()
        # Ask for save location
        ext = ".ini" if fmt == "ini" else ".json"
        savepath = filedialog.asksaveasfilename(defaultextension=ext,
                                                filetypes=[("INI files", "*.ini"), ("JSON files", "*.json"), ("All files", "*.*")])
        if not savepath:
            self.log_write("Save cancelled")
            return

        try:
            if fmt == "ini":
                self._save_ini(savepath, cfg)
            else:
                self._save_json(savepath, cfg)
            self.log_write(f"Config saved to: {savepath}")
            messagebox.showinfo("Saved", f"Config saved to:\n{savepath}")
        except Exception as e:
            self.log_write(f"Error saving config: {e}")
            messagebox.showerror("Error", str(e))

    def _save_ini(self, path, cfg):
        cp = configparser.ConfigParser()
        cp["FILES"] = {}
        for k, v in cfg.items():
            if v is None:
                cp["FILES"][k] = ""
            elif isinstance(v, list):
                # join by comma
                cp["FILES"][k] = ", ".join(v)
            else:
                cp["FILES"][k] = str(v)
        with open(path, "w", encoding="utf-8") as f:
            cp.write(f)

    def _save_json(self, path, cfg):
        # JSON: keep None as null, list as array, string as string
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)

def main():
    root = tk.Tk()
    # Use ttk theme if available
    try:
        style = ttk.Style()
        style.theme_use("clam")
    except Exception:
        pass
    app = ExcelConfigGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
