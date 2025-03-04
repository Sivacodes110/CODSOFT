import tkinter as tk
from tkinter import messagebox

def calculate():
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        operation = operation_var.get()
        
        if operation == "+":
            result.set(num1 + num2)
        elif operation == "-":
            result.set(num1 - num2)
        elif operation == "*":
            result.set(num1 * num2)
        elif operation == "/":
            result.set(num1 / num2 if num2 != 0 else "Error")
        else:
            result.set("Invalid")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers")

root = tk.Tk()
root.title("Colorful Calculator")
root.geometry("300x400")
root.configure(bg="#222831")

title_label = tk.Label(root, text="Simple Calculator", font=("Arial", 16, "bold"), fg="#EEEEEE", bg="#222831")
title_label.pack(pady=10)

entry1 = tk.Entry(root, font=("Arial", 14), bg="#393E46", fg="#00ADB5", insertbackground="#00ADB5")
entry1.pack(pady=5)

entry2 = tk.Entry(root, font=("Arial", 14), bg="#393E46", fg="#00ADB5", insertbackground="#00ADB5")
entry2.pack(pady=5)

operation_var = tk.StringVar()
operation_var.set("+")

operations_frame = tk.Frame(root, bg="#222831")
operations_frame.pack(pady=10)

for op in ["+", "-", "*", "/"]:
    tk.Radiobutton(operations_frame, text=op, variable=operation_var, value=op, font=("Arial", 14), fg="#EEEEEE", bg="#222831", selectcolor="#393E46").pack(side=tk.LEFT, padx=10)

calculate_button = tk.Button(root, text="Calculate", font=("Arial", 14, "bold"), bg="#00ADB5", fg="#222831", command=calculate)
calculate_button.pack(pady=10)

result = tk.StringVar()
result_label = tk.Label(root, textvariable=result, font=("Arial", 16, "bold"), fg="#00ADB5", bg="#222831")
result_label.pack(pady=10)

root.mainloop()
