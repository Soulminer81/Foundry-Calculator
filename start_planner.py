import subprocess
import os
import sys
import time

# Paths (adjust if workspace location changes)
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

# Activate virtual environment for backend if exists
VENV_PYTHON = os.path.join(ROOT_DIR, ".venv", "Scripts", "python.exe")
if not os.path.isfile(VENV_PYTHON):
    VENV_PYTHON = "python"  # fallback to system python

def start_backend():
    """Start the FastAPI backend in a subprocess."""
    cmd = [VENV_PYTHON, "main.py"]
    print("Starting backend:", " ".join(cmd))
    return subprocess.Popen(cmd, cwd=BACKEND_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def start_frontend():
    """Start a simple HTTP server for the frontend files."""
    cmd = ["python", "-m", "http.server", "8080"]
    print("Starting frontend server on http://localhost:8080")
    return subprocess.Popen(cmd, cwd=FRONTEND_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

if __name__ == "__main__":
    backend_proc = start_backend()
    frontend_proc = start_frontend()
    try:
        # Keep the script alive while both processes run
        while True:
            # Forward any output (optional)
            out = backend_proc.stdout.readline()
            if out:
                sys.stdout.buffer.write(out)
                sys.stdout.flush()
            # Sleep briefly to avoid busy loop
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nShutting down servers…")
        backend_proc.terminate()
        frontend_proc.terminate()
        backend_proc.wait()
        frontend_proc.wait()
        print("All stopped.")
