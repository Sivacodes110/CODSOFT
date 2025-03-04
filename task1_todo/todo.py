import tkinter as tk
from tkinter import ttk, font
import json

class NeonTodo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Neon Vortex Task Manager")
        self.geometry("1000x600")
        self.configure(bg="#0A0F24")
        self.tasks = []
        self.custom_font = ("Roboto", 10)
        self.colors = {
            "bg": "#0A0F24",
            "accent1": "#FF6B6B",
            "accent2": "#4ECDC4",
            "text": "#FFFFFF",
            "entry_bg": "#1A1F34",
            "progress": "#FF9F43",
            "priority": {
                "High": "#FF4757",
                "Medium": "#FFA502",
                "Low": "#2ED573"
            }
        }
        self.categories = ["Work", "Personal", "Creative", "Fitness"]
        self.setup_ui()
        self.load_tasks()
        self.bind_animations()

    def setup_ui(self):
        self.header = tk.Frame(self, bg=self.colors["bg"])
        self.header.pack(pady=20)
        
        self.task_entry = tk.Entry(self.header, width=40, bg=self.colors["entry_bg"], 
                                 fg=self.colors["text"], insertbackground=self.colors["text"],
                                 font=self.custom_font, relief="flat")
        self.task_entry.pack(side=tk.LEFT, padx=10)
        self.task_entry.insert(0, "Enter your task...")
        self.task_entry.bind("<FocusIn>", self.clear_placeholder)
        
        self.priority_var = tk.StringVar()
        self.priority_menu = ttk.Combobox(self.header, textvariable=self.priority_var, 
                                        values=list(self.colors["priority"].keys()),
                                        state="readonly", width=8)
        self.priority_menu.current(0)
        self.priority_menu.pack(side=tk.LEFT, padx=10)
        
        self.category_var = tk.StringVar()
        self.category_menu = ttk.Combobox(self.header, textvariable=self.category_var,
                                        values=self.categories, state="readonly", width=10)
        self.category_menu.current(0)
        self.category_menu.pack(side=tk.LEFT, padx=10)
        
        self.add_btn = tk.Button(self.header, text="+", command=self.add_task,
                               bg=self.colors["accent1"], fg=self.colors["text"],
                               activebackground="#FF5252", activeforeground="#FFFFFF",
                               relief="flat", font=("Roboto", 12, "bold"), width=3)
        self.add_btn.pack(side=tk.LEFT, padx=10)
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self, textvariable=self.search_var, bg=self.colors["entry_bg"],
                                   fg=self.colors["text"], insertbackground=self.colors["text"],
                                   font=self.custom_font, relief="flat")
        self.search_entry.pack(pady=10)
        self.search_entry.insert(0, "Search tasks...")
        self.search_entry.bind("<FocusIn>", self.clear_search_placeholder)
        self.search_entry.bind("<KeyRelease>", self.search_tasks)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=self.colors["entry_bg"], fieldbackground=self.colors["entry_bg"],
                      foreground=self.colors["text"], rowheight=25, borderwidth=0)
        style.configure("Treeview.Heading", background=self.colors["bg"], foreground=self.colors["accent2"],
                      font=("Roboto", 10, "bold"))
        style.map("Treeview", background=[("selected", self.colors["accent2"] + "30")])
        
        self.tree = ttk.Treeview(self, columns=("ID", "Task", "Priority", "Category", "Status"),
                               show="headings", selectmode="browse")
        self.tree.heading("ID", text="ID", anchor=tk.W)
        self.tree.heading("Task", text="Task", anchor=tk.W)
        self.tree.heading("Priority", text="Priority", anchor=tk.W)
        self.tree.heading("Category", text="Category", anchor=tk.W)
        self.tree.heading("Status", text="Status", anchor=tk.W)
        
        for col in ("ID", "Task", "Priority", "Category", "Status"):
            self.tree.column(col, width=100 if col == "ID" else 200, anchor=tk.W)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20)
        self.tree.bind("<Double-1>", self.toggle_status)
        
        self.progress = ttk.Progressbar(self, orient="horizontal", length=200,
                                      mode="determinate", style="custom.Horizontal.TProgressbar")
        style.configure("custom.Horizontal.TProgressbar", thickness=20, troughcolor=self.colors["entry_bg"],
                      background=self.colors["progress"], bordercolor=self.colors["bg"])
        self.progress.pack(pady=15)
        
        self.control_frame = tk.Frame(self, bg=self.colors["bg"])
        self.control_frame.pack(pady=10)
        
        self.delete_btn = tk.Button(self.control_frame, text="🗑️ Delete", command=self.delete_task,
                                  bg=self.colors["accent1"], fg=self.colors["text"],
                                  activebackground="#FF5252", activeforeground="#FFFFFF",
                                  relief="flat", font=self.custom_font)
        self.delete_btn.pack(side=tk.LEFT, padx=10)
        
        self.stats_label = tk.Label(self.control_frame, text="", bg=self.colors["bg"],
                                  fg=self.colors["accent2"], font=self.custom_font)
        self.stats_label.pack(side=tk.LEFT, padx=20)

    def bind_animations(self):
        widgets = [self.add_btn, self.delete_btn]
        for widget in widgets:
            widget.bind("<Enter>", lambda e: e.widget.config(bg=e.widget.cget("activebackground")))
            widget.bind("<Leave>", lambda e: e.widget.config(bg=e.widget.cget("bg")))

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text and task_text != "Enter your task...":
            new_task = {
                "id": len(self.tasks) + 1,
                "content": task_text,
                "priority": self.priority_var.get(),
                "category": self.category_var.get(),
                "completed": False
            }
            self.tasks.append(new_task)
            self.task_entry.delete(0, tk.END)
            self.update_display()
            self.save_tasks()

    def delete_task(self):
        selected = self.tree.selection()
        if selected:
            task_id = int(self.tree.item(selected[0], "values")[0])
            self.tasks = [task for task in self.tasks if task["id"] != task_id]
            self.update_display()
            self.save_tasks()

    def toggle_status(self, event):
        selected = self.tree.selection()
        if selected:
            task_id = int(self.tree.item(selected[0], "values")[0])
            for task in self.tasks:
                if task["id"] == task_id:
                    task["completed"] = not task["completed"]
            self.update_display()
            self.save_tasks()

    def update_display(self):
        self.tree.delete(*self.tree.get_children())
        for task in self.tasks:
            status = "✓" if task["completed"] else "✗"
            tags = ("completed", task["priority"].lower())
            self.tree.insert("", "end", values=(
                task["id"],
                task["content"],
                task["priority"],
                task["category"],
                status
            ), tags=tags)
        
        self.tree.tag_configure("completed", foreground="#666666")
        for priority, color in self.colors["priority"].items():
            self.tree.tag_configure(priority.lower(), foreground=color)
        
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t["completed"])
        self.progress["value"] = (completed / total * 100) if total > 0 else 0
        self.stats_label.config(text=f"Tasks: {total} | Completed: {completed} ({self.progress['value']:.1f}%)")

    def search_tasks(self, event=None):
        query = self.search_var.get().lower()
        for child in self.tree.get_children():
            values = self.tree.item(child, "values")
            if query in values[1].lower():
                self.tree.selection_set(child)
                self.tree.see(child)
            else:
                self.tree.selection_remove(child)

    def clear_placeholder(self, event):
        if self.task_entry.get() == "Enter your task...":
            self.task_entry.delete(0, tk.END)
            self.task_entry.config(fg=self.colors["text"])

    def clear_search_placeholder(self, event):
        if self.search_entry.get() == "Search tasks...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg=self.colors["text"])

    def save_tasks(self):
        with open("neon_tasks.json", "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        try:
            with open("neon_tasks.json", "r") as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            self.tasks = []
        self.update_display()

if __name__ == "__main__":
    app = NeonTodo()
    app.mainloop()