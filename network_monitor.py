import subprocess

def ping_device(ip):
    try:
        result = subprocess.run(
            ["ping", "-n", "1", ip],
            capture_output=True,
            text=True
        )

        return "Online" if result.returncode == 0 else "Offline"

    except:
        return "Offline"