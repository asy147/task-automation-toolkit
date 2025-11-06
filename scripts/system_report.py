#!/usr/bin/env python3
import argparse
import datetime
import importlib
import shutil
import platform
import socket
import subprocess
import psutil
import importlib.metadata


def mac_specific():
    # gather macOS-only metrics
    cpu_model = (
        subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"])
        .decode()
        .strip()
    )
    return {"cpu_model": cpu_model, "os_version": "macOS " + platform.mac_ver()[0]}


def linux_specific():
    # gather Linux-only metrics
    return {"cpu_model": "...", "distro": "..."}


def windows_specific():
    # gather Windows-only metrics
    return {"cpu_model": "...", "os_version": "..."}


def main():
    # 1. Create parser
    parser = argparse.ArgumentParser(description="Overall system report")
    # 2. Add arguments #fix parser and args!
    parser.add_argument(
        "--json",  # format argument
        nargs="?",  # make it optional
        default="text",
        help="Default formatting is plain text",
    )
    parser.add_argument(
        "--save",
        # nargs="?",  # optional
        default=".",  # current direcgt
        help="Saves output to current directory by default",
    )

    current_os = platform.system()
    os_info = {}

    if current_os == "Darwin":
        os_info = mac_specific()
        mac_ver = os_info["os_version"]
        cpu_model = os_info["cpu_model"]

    elif current_os == "Linux":
        os_info = linux_specific()
    elif current_os == "Windows":
        os_info = windows_specific()

    # Implement for Windows later!

    # --- Cross-platform info ---
    cpu_cores = psutil.cpu_count(logical=True)
    cpu_usage = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = shutil.disk_usage("/")
    python_ver = platform.python_version()
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    packages = [p.metadata["Name"] for p in importlib.metadata.distributions()]
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    top_procs = [
        (p.info["name"], p.info["cpu_percent"])
        for p in psutil.process_iter(["name", "cpu_percent"])
    ]

    print("System Report\n=============\n")
    print(f"OS: macOS {mac_ver}")
    print(f"CPU: {cpu_model} ({cpu_cores} cores)")
    print(f"CPU usage: {cpu_usage}%")
    print(
        f"Memory: {mem.total/(1024**3):.1f} GB total / {mem.used/(1024**3):.1f} GB used"
    )
    print(
        f"Disk: {disk.total/(1024**3):.1f} GB total / {disk.free/(1024**3):.1f} GB free"
    )
    print(f"Python: {python_ver}")
    print(f"Hostname: {hostname}")
    print(f"IP Address: {ip}")
    print(f"Boot Time: {boot_time}")
    print(f"Installed Packages: {packages[:5]} ...")
    print(f"Top Processes: {top_procs[:5]}")


if __name__ == "__main__":
    main()

"""
System Report
=============
OS: macOS 14.5 (Sonoma)
CPU: Apple M2 (8 cores)
Memory: 8.0 GB total / 3.2 GB used
Disk: 256 GB total / 180 GB free
Python: 3.11.6 (venv)
Top Processes: [python, code, chrome]

"""
