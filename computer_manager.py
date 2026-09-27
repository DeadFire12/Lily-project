import platform
import psutil
import socket
import getpass
import datetime
import subprocess


def get_system_info():

    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }


def get_cpu_info():

    return {
        "cpu_percent": psutil.cpu_percent(
            interval=1
        ),

        "cpu_count": psutil.cpu_count()
    }


def get_memory_info():

    memory = psutil.virtual_memory()

    return {
        "total_gb": round(
            memory.total / (1024 ** 3),
            2
        ),

        "used_gb": round(
            memory.used / (1024 ** 3),
            2
        ),

        "available_gb": round(
            memory.available / (1024 ** 3),
            2
        ),

        "percent": memory.percent
    }


def get_disk_info():

    disk = psutil.disk_usage(
        "C:\\"
    )

    return {
        "total_gb": round(
            disk.total / (1024 ** 3),
            2
        ),

        "used_gb": round(
            disk.used / (1024 ** 3),
            2
        ),

        "free_gb": round(
            disk.free / (1024 ** 3),
            2
        ),

        "percent": disk.percent
    }


def get_computer_status():

    return {
        "system": get_system_info(),
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "disk": get_disk_info()
    }
    

# =========================================================
# BATTERY INFO
# =========================================================

def get_battery_info():

    battery = psutil.sensors_battery()

    if battery is None:

        return {
            "available": False,
            "percent": None,
            "plugged": None,
            "seconds_left": None
        }

    return {
        "available": True,
        "percent": battery.percent,
        "plugged": battery.power_plugged,
        "seconds_left": battery.secsleft
    }


# =========================================================
# NETWORK INFO
# =========================================================

def get_network_info():

    interfaces = psutil.net_if_addrs()

    result = []

    for interface_name, addresses in interfaces.items():

        ipv4_addresses = []

        for address in addresses:

            if address.family == socket.AF_INET:

                ipv4_addresses.append(
                    address.address
                )

        if ipv4_addresses:

            result.append({
                "name": interface_name,
                "ipv4": ipv4_addresses
            })

    return result


# =========================================================
# USER INFO
# =========================================================

def get_user_info():

    return {
        "username": getpass.getuser(),
        "computer_name": socket.gethostname()
    }


# =========================================================
# DATE AND TIME INFO
# =========================================================

def get_datetime_info():

    now = datetime.datetime.now()

    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day": now.strftime("%A"),
        "full": now.strftime(
            "%A, %Y-%m-%d %H:%M:%S"
        )
    }


# =========================================================
# LAUNCH PROGRAM
# =========================================================

# =========================================================
# LAUNCH PROGRAM
# =========================================================

def launch_program(program):

    try:

        # =====================================================
        # CHROME
        # =====================================================

        if program.lower() == "chrome":

            chrome_path = (
                r"C:\Users\sedaghat\AppData\Local"
                r"\Google\Chrome\Application\chrome.exe"
            )

            subprocess.Popen(
                [chrome_path]
            )

            return {
                "success": True,
                "program": "Chrome"
            }


        # =====================================================
        # NORMAL PROGRAMS
        # =====================================================

        subprocess.Popen(
            program,
            shell=True
        )

        return {
            "success": True,
            "program": program
        }


    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# SCREENSHOT
# =========================================================

def take_screenshot(filename):

    try:

        import pyautogui

        screenshot = pyautogui.screenshot()

        screenshot.save(
            filename
        )

        return {
            "success": True,
            "filename": filename
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }