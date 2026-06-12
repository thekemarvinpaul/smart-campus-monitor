import subprocess
import platform

def ping_device(ip):
    try:
        param = "-n" if platform.system().lower() == "windows" else "-c"

        result = subprocess.run(
            ["ping", param, "1", ip],
            capture_output=True,
            text=True
        )

        return "Online" if result.returncode == 0 else "Offline"

    except Exception:
        return "Offline"