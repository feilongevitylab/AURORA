#!/usr/bin/env python3
"""
AURORA Project Runner
Starts FastAPI backend and React frontend in parallel, then opens browser.
"""

import subprocess
import sys
import os
import time
import signal
import webbrowser
from pathlib import Path

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.absolute()
BACKEND_DIR = PROJECT_ROOT / "aurora-backend"
FRONTEND_DIR = PROJECT_ROOT / "aurora-frontend"

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_status(message, color=Colors.BLUE):
    """Print colored status message"""
    print(f"{color}{Colors.BOLD}[AURORA]{Colors.END} {color}{message}{Colors.END}")

def check_requirements():
    """Check if all requirements are met"""
    print_status("Checking requirements...", Colors.YELLOW)
    
    # Check if backend venv exists
    venv_path = BACKEND_DIR / "venv"
    if not venv_path.exists():
        print_status("Backend virtual environment not found!", Colors.RED)
        print_status("Please run setup first: cd aurora-backend && python3 -m venv venv", Colors.YELLOW)
        return False
    
    # Check if frontend node_modules exists
    node_modules = FRONTEND_DIR / "node_modules"
    if not node_modules.exists():
        print_status("Frontend dependencies not installed!", Colors.RED)
        print_status("Please run: cd aurora-frontend && npm install", Colors.YELLOW)
        return False
    
    print_status("All requirements met!", Colors.GREEN)
    return True

def start_backend():
    """Start FastAPI backend server"""
    print_status("Starting FastAPI backend on http://localhost:8000...", Colors.BLUE)
    
    # Activate venv and run backend
    if sys.platform == "win32":
        activate_script = BACKEND_DIR / "venv" / "Scripts" / "activate.bat"
        python_cmd = BACKEND_DIR / "venv" / "Scripts" / "python.exe"
    else:
        activate_script = BACKEND_DIR / "venv" / "bin" / "activate"
        python_cmd = BACKEND_DIR / "venv" / "bin" / "python"
    
    # Change to backend directory
    os.chdir(BACKEND_DIR)
    
    # Start backend using Python directly (since we're already in venv context)
    backend_process = subprocess.Popen(
        [str(python_cmd), "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    return backend_process

def start_frontend():
    """Start React frontend server"""
    print_status("Starting React frontend on http://localhost:3000...", Colors.BLUE)
    
    # Change to frontend directory
    os.chdir(FRONTEND_DIR)
    
    # Start frontend
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    return frontend_process

def wait_for_server(url, max_wait=30):
    """Wait for server to be ready"""
    import urllib.request
    import urllib.error
    
    print_status(f"Waiting for server at {url}...", Colors.YELLOW)
    
    for i in range(max_wait):
        try:
            urllib.request.urlopen(url, timeout=2)
            print_status(f"Server at {url} is ready!", Colors.GREEN)
            return True
        except (urllib.error.URLError, OSError):
            time.sleep(1)
            if i % 5 == 0:
                print_status(f"Still waiting... ({i}/{max_wait} seconds)", Colors.YELLOW)
    
    print_status(f"Server at {url} did not start in time!", Colors.RED)
    return False

def open_browser(url):
    """Open browser to specified URL"""
    print_status(f"Opening browser at {url}...", Colors.GREEN)
    time.sleep(2)  # Give servers a moment to fully start
    webbrowser.open(url)

def main():
    """Main function to orchestrate everything"""
    print_status("=" * 60, Colors.BLUE)
    print_status("AURORA Project Runner", Colors.BOLD)
    print_status("=" * 60, Colors.BLUE)
    print()
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    print()
    
    processes = []
    
    try:
        # Start backend
        backend_process = start_backend()
        processes.append(("Backend", backend_process))
        time.sleep(2)  # Give backend time to start
        
        # Start frontend
        frontend_process = start_frontend()
        processes.append(("Frontend", frontend_process))
        time.sleep(3)  # Give frontend time to start
        
        # Wait for frontend to be ready
        if wait_for_server("http://localhost:3000", max_wait=30):
            # Open browser
            open_browser("http://localhost:3000")
        
        print()
        print_status("=" * 60, Colors.GREEN)
        print_status("Services are running!", Colors.GREEN)
        print_status("  Backend:  http://localhost:8000", Colors.BLUE)
        print_status("  Frontend: http://localhost:3000", Colors.BLUE)
        print_status("=" * 60, Colors.GREEN)
        print()
        print_status("Press Ctrl+C to stop all services", Colors.YELLOW)
        print()
        
        # Monitor processes and print output
        while True:
            time.sleep(1)
            
            # Check if processes are still alive
            for name, process in processes:
                if process.poll() is not None:
                    print_status(f"{name} process exited with code {process.returncode}", Colors.RED)
                    if process.returncode != 0:
                        # Print any error output
                        output = process.stdout.read()
                        if output:
                            print(output)
                        return
    
    except KeyboardInterrupt:
        print()
        print_status("Stopping all services...", Colors.YELLOW)
        
        # Terminate all processes
        for name, process in processes:
            try:
                print_status(f"Stopping {name}...", Colors.YELLOW)
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print_status(f"Force killing {name}...", Colors.RED)
                process.kill()
        
        print_status("All services stopped. Goodbye!", Colors.GREEN)
    
    except Exception as e:
        print_status(f"Error: {str(e)}", Colors.RED)
        
        # Clean up processes
        for name, process in processes:
            try:
                process.terminate()
            except:
                pass
        
        sys.exit(1)

if __name__ == "__main__":
    main()

