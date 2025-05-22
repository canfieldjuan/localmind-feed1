
import os
import subprocess

# Restrict command execution to the LocalMind folder
LOCALMIND_FOLDER = os.path.dirname(os.path.abspath(__file__))

# Execute command within LocalMind folder
def execute_command(cmd):
    # Ensure the command runs only within the LOCALMIND_FOLDER
    if os.path.commonpath([os.getcwd(), LOCALMIND_FOLDER]) == LOCALMIND_FOLDER:
        try:
            result = subprocess.run(cmd, shell=True, cwd=LOCALMIND_FOLDER, text=True, capture_output=True)
            output = result.stdout.strip() if result.stdout else result.stderr.strip()
            return output
        except Exception as e:
            return f"Error executing command: {str(e)}"
    else:
        return "Access denied: Commands can only be executed within LocalMind folder."

# Example usage
if __name__ == "__main__":
    command = input("Enter your command: ")  # Take command from user
    print(execute_command(command))  # Execute the command
