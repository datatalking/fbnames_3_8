import os
import subprocess

# Create required folders if they don't exist
folders = ["data", "tests", "model", "source", "output"]
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Check for and create required files
files = [".env", ".gitignore", "README.md", "requirements.txt"]
for file in files:
    if not os.path.isfile(file):
        open(file, "w").close()
        print(f"{file} file created")
    else:
        print(f"{file} file exists")

# Check if black[d] linter is loaded
try:
    import black

    print("black[d] linter is loaded")
except ImportError:
    print("black[d] linter is not loaded")

# Run test coverage and unit tests
if os.path.exists("tests.py") and os.path.exists("coverage.txt"):
    subprocess.call(["coverage", "run", "--source=.", "tests.py"])
    subprocess.call(["coverage", "report", "-m", "--fail-under=80"])
else:
    print("Either tests.py or coverage.txt file does not exist")
