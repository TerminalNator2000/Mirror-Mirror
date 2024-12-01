# Mirror Mirror Application Enhancement with Database Integration and Core Functionality Restoration, Including Shell Type and Payload Generation

import socket
import logging
import tkinter as tk
from tkinter import scrolledtext
import sqlite3
import subprocess

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MirrorMirrorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Mirror Mirror Application")

        # Setting up the User Interface
        self.connection_frame = tk.Frame(master)
        self.connection_frame.pack(pady=10)

        tk.Label(self.connection_frame, text="IP Address to Connect To:").grid(row=0, column=0)
        self.ip_address_entry = tk.Entry(self.connection_frame)
        self.ip_address_entry.grid(row=0, column=1)

        tk.Label(self.connection_frame, text="Port to Connect To:").grid(row=1, column=0)
        self.connect_to_port_entry = tk.Entry(self.connection_frame)
        self.connect_to_port_entry.grid(row=1, column=1)

        tk.Label(self.connection_frame, text="Send From Port:").grid(row=2, column=0)
        self.send_from_port_entry = tk.Entry(self.connection_frame)
        self.send_from_port_entry.grid(row=2, column=1)

        tk.Label(self.connection_frame, text="Listen On Port:").grid(row=3, column=0)
        self.listen_on_port_entry = tk.Entry(self.connection_frame)
        self.listen_on_port_entry.grid(row=3, column=1)

        self.connect_button = tk.Button(master, text="Generate Reverse Shell", command=self.connect_to_server)
        self.connect_button.pack(pady=5)

        # Shell Type Selection Dropdown
        self.shell_type_var = tk.StringVar(master)
        self.shell_type_var.set("bash")  # Set default value
        self.shell_type_label = tk.Label(master, text="Select Shell Type:")
        self.shell_type_label.pack()

        self.shell_type_dropdown = tk.OptionMenu(master, self.shell_type_var, "bash", "powershell")
        self.shell_type_dropdown.pack(pady=5)

        self.logs_text = scrolledtext.ScrolledText(master, width=80, height=10, wrap=tk.WORD)
        self.logs_text.pack(pady=10)

        self.next_best_actions_label = tk.Label(master, text="Next Best Actions:")
        self.next_best_actions_label.pack()
        self.next_best_actions_text = tk.Text(master, height=5, width=80, wrap=tk.WORD)
        self.next_best_actions_text.pack()

        # Shell input and output section
        self.shell_input_label = tk.Label(master, text="Shell Command Input:")
        self.shell_input_label.pack()

        self.shell_input_entry = tk.Entry(master, width=80)
        self.shell_input_entry.pack()

        self.send_shell_command_button = tk.Button(master, text="Send Command", command=self.send_shell_command)
        self.send_shell_command_button.pack()

        self.shell_output_text = scrolledtext.ScrolledText(master, width=80, height=10, wrap=tk.WORD)
        self.shell_output_text.pack(pady=10)

        # Connect to the existing database
        self.connect_to_database()

        # Default Shell Type
        self.shell_type = self.shell_type_var.get()

    def connect_to_database(self):
        # Connect to the SQLite database
        self.conn = sqlite3.connect('mirror_mirror.db')
        self.cursor = self.conn.cursor()

    def send_shell_command(self):
        command = self.shell_input_entry.get()
        if command.lower() in ["exit", "quit"]:
            self.log_message("Exiting shell interaction.")
            return

        try:
            if hasattr(self, 'client_socket') and self.client_socket:
                self.client_socket.send(command.encode())
                response = self.client_socket.recv(4096).decode()
                self.shell_output_text.insert(tk.END, f"{self.shell_type}> {response}\n")
            else:
                self.log_message("No active shell connection.", logging.ERROR)
        except Exception as e:
            self.log_message(f"Error sending command: {e}", logging.ERROR)

    def connect_to_server(self):
        # Retrieve user-provided IP and ports
        ip_address = self.ip_address_entry.get()
        connect_to_port = self.connect_to_port_entry.get()
        send_from_port = self.send_from_port_entry.get()
        listen_on_port = self.listen_on_port_entry.get()

        try:
            # Validate IP address
            socket.inet_aton(ip_address)

            # Validate ports
            connect_to_port = int(connect_to_port)
            send_from_port = int(send_from_port)
            listen_on_port = int(listen_on_port)

            if not (1 <= connect_to_port <= 65535 and 1 <= send_from_port <= 65535 and 1 <= listen_on_port <= 65535):
                raise ValueError("Port numbers must be in the range 1-65535.")

            # Setting up the socket
            self.log_message(f"Attempting to create socket on ports: send from {send_from_port}, listen on {listen_on_port}.")
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.bind(("", send_from_port))
            client_socket.settimeout(5)  # Timeout for testing connections

            server_address = (ip_address, connect_to_port)
            self.log_message(f"Attempting to connect to server at {server_address}.")

            client_socket.connect(server_address)
            self.client_socket = client_socket  # Store socket for shell interaction
            self.log_message("Connection established successfully.", logging.INFO)
            self.suggest_next_best_actions("success")
            self.suggest_rwuc_actions(connect_to_port)

        except socket.error as e:
            if "timed out" in str(e):
                self.log_message(f"Connection failed with error: {e}", logging.ERROR)
                self.suggest_next_best_actions("timeout")
            else:
                self.log_message(f"Connection failed with error: {e}", logging.ERROR)
                self.suggest_next_best_actions("failure")

        except ValueError as e:
            if "Port numbers must be" in str(e):
                self.log_message(str(e), logging.ERROR)
                self.suggest_next_best_actions("port_error")
            else:
                self.log_message("Error: Ports must be integers.", logging.ERROR)
                self.suggest_next_best_actions("failure")

    def log_message(self, message, level=logging.INFO):
        logging.log(level, message)
        self.logs_text.insert(tk.END, message + '\n')
        self.logs_text.yview(tk.END)

    def suggest_next_best_actions(self, status):
        self.next_best_actions_text.delete(1.0, tk.END)

        # Retrieve the appropriate next best action from the database
        self.cursor.execute("SELECT action FROM next_best_actions WHERE status = ?", (status,))
        result = self.cursor.fetchone()
        if result:
            action = result[0]
        else:
            action = "No suggestion available for this status."

        self.next_best_actions_text.insert(tk.END, action)

    def suggest_rwuc_actions(self, port_type):
        # Retrieve RWUC suggestions based on port type
        self.cursor.execute("SELECT command_suggestion FROM rwuc_suggestions WHERE port_type = ?", (port_type,))
        result = self.cursor.fetchone()
        if result:
            rwuc_action = result[0]
            self.next_best_actions_text.insert(tk.END, f"\nRecommended Action for Port {port_type}: {rwuc_action}")
        else:
            self.next_best_actions_text.insert(tk.END, f"\nNo RWUC suggestion available for port {port_type}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MirrorMirrorApp(root)
    root.mainloop()
