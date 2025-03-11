import subprocess
import winreg
import os
import csv

def get_installed_apps_from_registry():
    print("📌 Fetching installed Win32 apps from Windows Registry...")

    reg_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    installed_apps = []

    for reg_path in reg_paths:
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
            for i in range(winreg.QueryInfoKey(reg_key)[0]):
                subkey_name = winreg.EnumKey(reg_key, i)
                subkey = winreg.OpenKey(reg_key, subkey_name)
                try:
                    app_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                    app_version, _ = winreg.QueryValueEx(subkey, "DisplayVersion") if winreg.QueryValueEx(subkey, "DisplayVersion") else ("Unknown", None)
                    installed_apps.append({"Name": app_name, "Version": app_version, "Source": "Registry"})
                except FileNotFoundError:
                    pass  # Some registry entries do not have DisplayName or DisplayVersion
                winreg.CloseKey(subkey)
            winreg.CloseKey(reg_key)
        except Exception as e:
            print(f"❌ Error reading registry path: {reg_path} - {e}")

    return installed_apps

def get_installed_apps_using_powershell():
    print("📌 Fetching Microsoft Store apps using PowerShell...")

    command = 'powershell -ExecutionPolicy Bypass -Command "Get-AppxPackage | Select-Object Name, Version"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding="utf-8")

    installed_apps = []

    if result.stdout.strip():
        lines = result.stdout.split("\n")
        for line in lines:
            parts = line.strip().split()
            if len(parts) > 1:
                app_name = parts[0]
                app_version = parts[-1]
                installed_apps.append({"Name": app_name, "Version": app_version, "Source": "Microsoft Store"})
    else:
        print("❌ PowerShell returned no Microsoft Store apps.")

    return installed_apps

def scan_program_files():
    print("📌 Scanning Program Files for additional installed applications...")

    program_files_dirs = [
        "C:\\Program Files",
        "C:\\Program Files (x86)",
        os.path.expanduser("~\\AppData\\Local\\Programs")
    ]

    installed_apps = set()

    for directory in program_files_dirs:
        if os.path.exists(directory):
            for folder in os.listdir(directory):
                installed_apps.add(folder)

    return [{"Name": app, "Version": "Unknown", "Source": "File System"} for app in installed_apps]

def save_as_csv(data):
    filename = "installed_apps.csv"  # Always overwrite this file

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Name", "Version", "Source"])
        writer.writeheader()
        writer.writerows(data)

    print(f"✅ Installed applications saved to {filename} (Overwriting previous file)")

# Run all methods and combine results
apps_registry = get_installed_apps_from_registry()
apps_powershell = get_installed_apps_using_powershell()
apps_filesystem = scan_program_files()

all_apps = apps_registry + apps_powershell + apps_filesystem

# Save as CSV (Overwrites previous file)
save_as_csv(all_apps)

print("\n🚀 All installed applications (with versions) have been collected and saved to `installed_apps.csv`!")
