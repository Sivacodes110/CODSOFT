import tkinter as tk
from tkinter import font

class GlowCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NeonCalc")
        self.configure(bg="#1a1a1a")
        self.result = ""
        self.history = []
        self.create_widgets()
        self.bind_keys()

    def create_widgets(self):
        custom_font = font.Font(family="Digital-7", size=24)
        self.display = tk.Entry(self, font=custom_font, justify="right", 
                               bg="#2d2d2d", fg="#00ff9d", insertbackground="#00ff9d",
                               borderwidth=0, readonlybackground="#2d2d2d")
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=20, ipady=15, sticky="ew")
        self.display.config(state="readonly")

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('÷', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('×', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('⌫', 5, 0), ('C', 5, 1), ('√', 5, 2), ('%', 5, 3)
        ]

        for (text, row, col) in buttons:
            btn = tk.Button(self, text=text, font=("Arial", 14, "bold"),
                           bg="#333333", fg="white", activebackground="#404040",
                           activeforeground="white", borderwidth=0,
                           command=lambda t=text: self.on_button_click(t))
            btn.grid(row=row, column=col, padx=5, pady=5, ipadx=15, ipady=10, sticky="nsew")
            self.grid_columnconfigure(col, weight=1)
            self.grid_rowconfigure(row, weight=1)

            if text in ['÷', '×', '-', '+', '=']:
                btn.config(bg="#004a45", activebackground="#006b5f")
            elif text in ['⌫', 'C']:
                btn.config(bg="#4a0000", activebackground="#6b0000")

    def bind_keys(self):
        self.bind("<Key>", self.key_pressed)
        for num in ['0','1','2','3','4','5','6','7','8','9']:
            self.bind(num, self.key_pressed)
        self.bind("<Return>", lambda e: self.calculate_result())
        self.bind("<BackSpace>", lambda e: self.backspace())

    def on_button_click(self, char):
        if char == '=':
            self.calculate_result()
        elif char == 'C':
            self.clear_display()
        elif char == '⌫':
            self.backspace()
        elif char == '√':
            self.square_root()
        elif char == '%':
            self.percentage()
        else:
            self.add_to_expression(char)

    def add_to_expression(self, value):
        self.display.config(state="normal")
        self.display.insert(tk.END, value.replace('÷', '/').replace('×', '*'))
        self.display.config(state="readonly")

    def clear_display(self):
        self.display.config(state="normal")
        self.display.delete(0, tk.END)
        self.display.config(state="readonly")

    def backspace(self):
        self.display.config(state="normal")
        current = self.display.get()
        self.display.delete(0, tk.END)
        self.display.insert(0, current[:-1])
        self.display.config(state="readonly")

    def square_root(self):
        try:
            value = float(self.display.get())
            result = value ** 0.5
            self.display.config(state="normal")
            self.display.delete(0, tk.END)
            self.display.insert(0, f"√{value} = {round(result, 5)}")
            self.display.config(state="readonly")
        except:
            self.show_error("Invalid Input")

    def percentage(self):
        try:
            value = float(self.display.get())
            result = value / 100
            self.display.config(state="normal")
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
            self.display.config(state="readonly")
        except:
            self.show_error("Invalid Input")

    def calculate_result(self):
        try:
            expression = self.display.get().replace('÷', '/').replace('×', '*')
            result = eval(expression)
            self.history.append(f"{expression} = {result}")
            self.display.config(state="normal")
            self.display.delete(0, tk.END)
            self.display.insert(0, str(round(result, 5)))
            self.display.config(state="readonly")
        except Exception as e:
            self.show_error("Math Error")

    def key_pressed(self, event):
        key = event.char
        if key in ['+', '-', '*', '/']:
            self.add_to_expression(key)
        elif key == '.':
            self.add_to_expression('.')
        elif key in ['\r', '=']:
            self.calculate_result()

    def show_error(self, message):
        self.display.config(state="normal")
        self.display.delete(0, tk.END)
        self.display.insert(0, message)
        self.display.config(state="readonly")
        self.after(1500, self.clear_display)

if __name__ == "__main__":
    calculator = GlowCalculator()
    calculator.mainloop()