#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import re

def generate_shellcode():
    ip = ip_entry.get()
    port = port_entry.get()
    language = language_combo.get().lower()
    variable = variable_entry.get()
    shell_type = shell_type_combo.get().lower()
    save = save_var.get()
    output_file = output_file_entry.get()

    # Validate the IP and Port
    ip_pattern = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')
    if not ip_pattern.match(ip):
        messagebox.showerror("Input Error", "Invalid IP Address format.")
        return
    if not port.isdigit() or not (1 <= int(port) <= 65535):
        messagebox.showerror("Input Error", "Port must be a number between 1 and 65535.")
        return

    # Construct the command
    command = ["python3", "mirrormirror.py", "--ip", ip, "--port", port, "--language", language,
               "--variable", variable, "--type", shell_type, "--save", str(save), "--output", output_file]
    
    # Execute the command and show result
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        messagebox.showinfo("Success", f"Shellcode generated successfully!\n\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred:\n\n{e.stderr}")

# Create the main application window
root = tk.Tk()
root.title("Mirror Mirror - Reverse Shell Generator")
root.geometry("600x450")

# IP Address Entry
ip_label = tk.Label(root, text="IP Address:")
ip_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
ip_entry = tk.Entry(root)
ip_entry.grid(row=0, column=1, padx=10, pady=10, sticky='e')

# Port Entry
port_label = tk.Label(root, text="Port:")
port_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
port_entry = tk.Entry(root)
port_entry.grid(row=1, column=1, padx=10, pady=10, sticky='e')

# Language Dropdown
language_label = tk.Label(root, text="Language:")
language_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')
language_combo = ttk.Combobox(root, values=["Python", "C", "CSharp", "PowerShell"])
language_combo.grid(row=2, column=1, padx=10, pady=10, sticky='e')
language_combo.current(0)

# Variable Name Entry
variable_label = tk.Label(root, text="Variable Name:")
variable_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')
variable_entry = tk.Entry(root)
variable_entry.grid(row=3, column=1, padx=10, pady=10, sticky='e')
variable_entry.insert(0, "buf")

# Shell Type Dropdown
shell_type_label = tk.Label(root, text="Shell Type:")
shell_type_label.grid(row=4, column=0, padx=10, pady=10, sticky='w')
shell_type_combo = ttk.Combobox(root, values=["cmd", "PowerShell"])
shell_type_combo.grid(row=4, column=1, padx=10, pady=10, sticky='e')
shell_type_combo.current(0)

# Save Option Checkbox
save_var = tk.StringVar(value="False")
save_checkbox = tk.Checkbutton(root, text="Save to File", variable=save_var, onvalue="True", offvalue="False")
save_checkbox.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Output File Entry with Browse Button
output_file_label = tk.Label(root, text="Output File:")
output_file_label.grid(row=6, column=0, padx=10, pady=10, sticky='w')
output_file_entry = tk.Entry(root)
output_file_entry.grid(row=6, column=1, padx=10, pady=10, sticky='e')

# Browse Button
def browse_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".bin", filetypes=[("Binary files", "*.bin"), ("All files", "*.*")])
    if file_path:
        output_file_entry.delete(0, tk.END)
        output_file_entry.insert(0, file_path)

browse_button = tk.Button(root, text="Browse", command=browse_output_file)
browse_button.grid(row=6, column=2, padx=5, pady=10)

# Generate Button
generate_button = tk.Button(root, text="Generate Shellcode", command=generate_shellcode)
generate_button.grid(row=7, column=0, columnspan=3, pady=20)

# Run the Tkinter main loop
root.mainloop()
