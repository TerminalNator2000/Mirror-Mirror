import argparse
import subprocess
import sys


def start_cli_shell():
    """Starts a Python CLI shell."""
    print("Entering Python CLI shell (type 'exit' to quit)")
    while True:
        try:
            command = input("cli> ").strip()
            if command.lower() in {"exit", "quit"}:
                print("Exiting CLI shell.")
                break
            if command:
                result = subprocess.run(command, shell=True, text=True, capture_output=True)
                print(result.stdout, end="")
                if result.stderr:
                    print(result.stderr, end="")
        except KeyboardInterrupt:
            print("\nExiting CLI shell.")
            break
        except Exception as e:
            print(f"Error: {e}")


def start_bash_shell():
    """Starts a Bash shell."""
    print("Entering Bash shell (type 'exit' to quit)")
    while True:
        try:
            command = input("bash> ").strip()
            if command.lower() in {"exit", "quit"}:
                print("Exiting Bash shell.")
                break
            if command:
                result = subprocess.run(["bash", "-c", command], text=True, capture_output=True)
                print(result.stdout, end="")
                if result.stderr:
                    print(result.stderr, end="")
        except KeyboardInterrupt:
            print("\nExiting Bash shell.")
            break
        except Exception as e:
            print(f"Error: {e}")


def start_powershell_shell():
    """Starts a PowerShell shell."""
    print("Entering PowerShell shell (type 'exit' to quit)")
    while True:
        try:
            command = input("ps> ").strip()
            if command.lower() in {"exit", "quit"}:
                print("Exiting PowerShell shell.")
                break
            if command:
                result = subprocess.run(["powershell", "-Command", command], text=True, capture_output=True)
                print(result.stdout, end="")
                if result.stderr:
                    print(result.stderr, end="")
        except KeyboardInterrupt:
            print("\nExiting PowerShell shell.")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Reverse Shell CLI")
    parser.add_argument(
        "--shell",
        choices=["cli", "bash", "powershell"],
        required=True,
        help="Choose the type of shell to run (cli, bash, powershell)"
    )
    args = parser.parse_args()

    if args.shell == "cli":
        start_cli_shell()
    elif args.shell == "bash":
        start_bash_shell()
    elif args.shell == "powershell":
        start_powershell_shell()
    else:
        print("Invalid shell type selected.")
        sys.exit(1)


if __name__ == "__main__":
    main()
