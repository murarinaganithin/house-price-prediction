import os
import sys
import subprocess

# Fix paths: ensure we are running from the backend directory
backend_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(backend_dir)
sys.path.insert(0, backend_dir)

PORT = 8000

def kill_port():
    """Kill any process currently using the target port."""
    print(f"Checking for existing processes on port {PORT}...")
    try:
        output = subprocess.check_output(["netstat", "-ano"], text=True)
        pids_killed = set()

        for line in output.strip().splitlines():
            parts = line.split()
            if len(parts) >= 5:
                local_addr = parts[1]
                pid = parts[-1]
                if f":{PORT}" in local_addr and pid.isdigit() and int(pid) > 0 and pid not in pids_killed:
                    print(f"  -> Killing process {pid} on port {PORT}...")
                    subprocess.run(["taskkill", "/F", "/PID", pid],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    pids_killed.add(pid)

        if pids_killed:
            print(f"Cleared {len(pids_killed)} process(es) from port {PORT}.")
        else:
            print(f"Port {PORT} is free.")
    except Exception as e:
        print(f"Warning: Could not check port {PORT}: {e}")


if __name__ == "__main__":
    kill_port()
    print(f"\n===================================================")
    print(f"Frontend Web Application: http://localhost:5173")
    print(f"Backend API Server:        http://127.0.0.1:{PORT}")
    print(f"Swagger UI Docs:          http://127.0.0.1:{PORT}/docs")
    print(f"===================================================\n")

    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=PORT, reload=True)
