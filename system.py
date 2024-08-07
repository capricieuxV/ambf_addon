import sys
import subprocess

# Get the current Python executable path
python_executable = sys.executable

# Use the Python executable to run pip and get the list of installed packages
result = subprocess.run([python_executable, "-m", "pip", "list"], capture_output=True, text=True)

# Print the output of pip list
print(result.stdout)
