import subprocess
import os

# Get the current directory of the Python script
current_directory = os.path.dirname(os.path.realpath(__file__))

# Define the file path relative to the current directory
file_path = os.path.join(current_directory, "arabic1.png")

# Define the curl command as a list of arguments
curl_command = [
    "curl",
    "-X", "POST",
    "-F", f"file=@{file_path}",
    "http://192.168.1.46:11200/extract_text"
]

# Execute the curl command using subprocess.run
try:
    result = subprocess.run(curl_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Response from server:")
    print(result.stdout.decode())  # Print the output from the server
except subprocess.CalledProcessError as e:
    print(f"Error occurred: {e}")
    print("Error details:", e.stderr.decode())
