# Mirror Mirror Application Enhancement with Database Integration, Connection Persistence,
# and Core Functionality Restoration, Including Shell Type and Payload Generation

import socket
import logging
import tkinter as tk
from tkinter import scrolledtext
import sqlite3
import threading
import time

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MirrorMirrorApp:
    def __init__(self, master):
        """
        Initialize the Mirror Mirror GUI application with core functionality,
        including connection setup, shell command interaction, and persistence handling.
        """
        self.master = master
        self.master.title("Mirror Mirror Application")

        # Initialize connection status
        self.connection_active = False
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5  # Max retries for reconnection

        # Set up GUI elements for connection
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

        # Button to establish a connection
        self.connect_button = tk.Button(master, text="Generate Reverse Shell", command=self.connect_to_server)
        self.connect_button.pack(pady=5)

        # Dropdown menu to select shell type
        self.shell_type_var = tk.StringVar(master)
        self.shell_type_var.set("bash")  # Set default shell type
        self.shell_type_label = tk.Label(master, text="Select Shell Type:")
        self.shell_type_label.pack()

        self.shell_type_dropdown = tk.OptionMenu(master, self.shell_type_var, "bash", "powershell")
        self.shell_type_dropdown.pack(pady=5)

        # Log output window
        self.logs_text = scrolledtext.ScrolledText(master, width=80, height=10, wrap=tk.WORD)
        self.logs_text.pack(pady=10)

        # Next Best Actions display
        self.next_best_actions_label = tk.Label(master, text="Next Best Actions:")
        self.next_best_actions_label.pack()
        self.next_best_actions_text = tk.Text(master, height=5, width=80, wrap=tk.WORD)
        self.next_best_actions_text.pack()

        # Shell command input/output section
        self.shell_input_label = tk.Label(master, text="Shell Command Input:")
        self.shell_input_label.pack()

        self.shell_input_entry = tk.Entry(master, width=80)
        self.shell_input_entry.pack()

        self.send_shell_command_button = tk.Button(master, text="Send Command", command=self.send_shell_command)
        self.send_shell_command_button.pack()

        self.shell_output_text = scrolledtext.ScrolledText(master, width=80, height=10, wrap=tk.WORD)
        self.shell_output_text.pack(pady=10)

        # Connect to the SQLite database
        self.connect_to_database()

        # Start a thread to monitor the connection
        self.monitor_thread = threading.Thread(target=self.monitor_connection, daemon=True)
        self.monitor_thread.start()

    def connect_to_database(self):
        """Connect to the SQLite database for storing and retrieving Next Best Actions."""
        self.conn = sqlite3.connect('mirror_mirror.db')
        self.cursor = self.conn.cursor()

    def monitor_connection(self):
        """Continuously checks the status of the connection and attempts to reconnect if needed."""
        while True:
            if hasattr(self, 'client_socket') and self.client_socket:
                try:
                    # Send a heartbeat signal to check connection
                    self.client_socket.send(b'heartbeat')
                    self.client_socket.recv(4096)
                    self.connection_active = True  # Connection is active
                    self.reconnect_attempts = 0  # Reset attempts
                except socket.error:
                    self.connection_active = False
                    self.log_message("Connection lost. Attempting to reconnect...", logging.WARNING)
                    self.reconnect_to_server()
            time.sleep(5)  # Check connection every 5 seconds

    def reconnect_to_server(self):
        """Attempts to reconnect to the server when the connection is lost."""
        if self.reconnect_attempts >= self.max_reconnect_attempts:
            self.log_message("Maximum reconnection attempts reached. Giving up.", logging.ERROR)
            return

        self.reconnect_attempts += 1
        try:
            self.connect_to_server()
            self.log_message(f"Reconnection attempt {self.reconnect_attempts} successful.", logging.INFO)
        except Exception as e:
            self.log_message(f"Reconnection attempt {self.reconnect_attempts} failed: {e}", logging.ERROR)

    def connect_to_server(self):
        """Establish a connection to the server."""
        ip_address = self.ip_address_entry.get()
        connect_to_port = self.connect_to_port_entry.get()
        send_from_port = self.send_from_port_entry.get()
        listen_on_port = self.listen_on_port_entry.get()

        try:
            # Validate IP address and ports
            socket.inet_aton(ip_address)
            connect_to_port = int(connect_to_port)
            send_from_port = int(send_from_port)
            listen_on_port = int(listen_on_port)

            if not (1 <= connect_to_port <= 65535 and 1 <= send_from_port <= 65535 and 1 <= listen_on_port <= 65535):
                raise ValueError("Port numbers must be in the range 1-65535.")

            # Create and configure the socket
            self.log_message(f"Creating socket on ports: send from {send_from_port}, listen on {listen_on_port}.")
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.bind(("", send_from_port))
            client_socket.settimeout(5)  # Set timeout for connection

            server_address = (ip_address, connect_to_port)
            self.log_message(f"Connecting to server at {server_address}.")
            client_socket.connect(server_address)

            self.client_socket = client_socket
            self.connection_active = True  # Mark connection as active
            self.log_message("Connection established successfully.", logging.INFO)
        except socket.error as e:
            self.connection_active = False
            self.log_message(f"Connection failed: {e}", logging.ERROR)

    def send_shell_command(self):
        """Send a shell command to the connected server."""
        if not self.connection_active:
            self.log_message("No active connection. Command not sent.", logging.ERROR)
            return

        command = self.shell_input_entry.get()
        if command.lower() in ["exit", "quit"]:
            self.log_message("Exiting shell interaction.")
            return

        try:
            self.client_socket.send(command.encode())
            response = self.client_socket.recv(4096).decode()
            self.shell_output_text.insert(tk.END, f"{self.shell_type_var.get()}> {response}\n")
        except Exception as e:
            self.log_message(f"Error sending command: {e}", logging.ERROR)

    def log_message(self, message, level=logging.INFO):
        """Log messages to the GUI and console."""
        logging.log(level, message)
        self.logs_text.insert(tk.END, message + '\n')
        self.logs_text.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = MirrorMirrorApp(root)
    root.mainloop()
