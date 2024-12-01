![image](https://github.com/user-attachments/assets/26517dbb-22ac-412c-a171-35e71a322651)



# Mirror Mirror Application

## Overview
The **Mirror Mirror Application** is an enhanced reverse shell utility, integrating database-driven suggestions and advanced functionality such as shell type selection, logging, and automated payload generation. The application provides a graphical user interface (GUI) to facilitate interactions, configure network parameters, and execute commands for penetration testing or remote management tasks.

## Key Features
1. **Database-Driven Next Best Actions**: The application is integrated with a SQLite database (`mirror_mirror.db`) that provides actionable suggestions based on the connection status, port type, and services running behind specific ports. This feature makes it easy for users to determine the next steps during remote interactions.

2. **Reverse Shell Generation**: Generate a reverse shell with customizable options, including:
   - Target IP Address
   - Port to Connect To
   - Port to Send From
   - Port to Listen On

3. **Shell Type Selection**: Users can choose the type of shell they want to use, either **Bash** or **PowerShell**, based on the environment they are connecting to.

4. **Logs and Shell Interaction**:
   - Logs display connection attempts, errors, and detailed information for troubleshooting.
   - Users can interact directly with the shell by sending commands via the GUI.

5. **Automated Payload Suggestions**: The application dynamically generates payloads and provides **Recommended Way to Use Commands (RWUC)** based on common port usages and services.

## Installation
To install the application, make sure you have the following requirements:

1. **Python 3.x**
2. **Tkinter**: GUI toolkit for Python, which is usually included with Python distributions.
3. **SQLite3**: To interact with the integrated database (`mirror_mirror.db`).
4. **Clone the Repository**:
   ```bash
   git clone https://github.com/TerminalNator2000/mirror-mirror-app.git
   cd mirror-mirror-app
   ```
5. **Install Dependencies**:
   If any dependencies are missing, you can use `pip` to install them:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. **Running the Application**:
   To run the application, execute the following command:
   ```bash
   python mirror_mirror_gui.py
   ```

2. **Database Setup**:
   Ensure that the SQLite database (`mirror_mirror.db`) is correctly populated with the necessary tables and data. If you need to recreate the database, use the provided SQL script (`create_mirror_mirror_db.sql`) to create the following tables:
   - `next_best_actions`: Contains suggestions for successful or failed connection attempts.
   - `rwuc_suggestions`: Stores command suggestions for common ports and services.

3. **Graphical Interface**:
   The application will launch with a graphical interface that includes fields to input the IP address, ports, and options to select the shell type. Logs and command suggestions are displayed in the interface to assist in decision-making.

## Example Commands
- **Generate Reverse Shell**: Input the target IP address and port details, then click **Generate Reverse Shell** to initiate the connection.
- **Shell Type Selection**: Choose between **Bash** or **PowerShell** depending on the environment you are working with.
- **Send Commands**: After establishing a connection, use the command input box to send instructions to the remote server.

## Database Structure
### Tables in `mirror_mirror.db`
1. **`next_best_actions`**:
   - **Columns**: `status`, `action`
   - Provides suggestions based on connection status, such as success, failure, or invalid IP format.

2. **`rwuc_suggestions`**:
   - **Columns**: `port_type`, `service_name`, `command_suggestion`
   - Contains command suggestions for specific ports like SSH (`22`), HTTP (`80`), DNS (`53`), etc., to assist with further exploitation or diagnostics.

## Example Entries in the Database
- **`rwuc_suggestions`** for Port `53` (DNS):
  - Command Suggestion: `Use: dig @target_ip or nslookup target_ip to check DNS service. You may also run nmap -sU -p 53 for UDP scan or nmap -sT -p 53 for TCP scan.`

## Troubleshooting
- **WinError 10053**: If you encounter `[WinError 10053] An established connection was aborted by the software in your host machine`, it may be due to a firewall or an antivirus software blocking the connection. Make sure to allow the application through your firewall and verify that the target ports are open.

- **No Active Shell Connection**: Ensure that the IP address and ports are correctly configured before attempting to send shell commands. If the connection fails, check the logs for error details and refer to the suggested **Next Best Actions**.

## Contribution
Feel free to contribute to this project by opening issues or submitting pull requests. Any enhancements or bug fixes are welcome.

### To Contribute:
1. **Fork the Repository**.
2. **Create a Branch** for your feature (`git checkout -b feature/AmazingFeature`).
3. **Commit your Changes** (`git commit -m 'Add some AmazingFeature'`).
4. **Push to the Branch** (`git push origin feature/AmazingFeature`).
5. **Open a Pull Request**.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Thanks to all contributors and users for feedback and improvements.
- Inspired by various penetration testing utilities that provide GUI-based interactions.

Feel free to contact us at [mnations058@gmail.com](mailto:mnations058@gmail.com) for any questions or support regarding this project.

