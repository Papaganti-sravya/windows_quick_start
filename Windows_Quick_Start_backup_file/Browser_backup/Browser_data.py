import os
import json
import subprocess
import shutil

# Output JSON file
backup_file = "backup_data.json"
browser_backup_folder = "browser_backup"

# Ensure browser backup folder exists
os.makedirs(browser_backup_folder, exist_ok=True)


# 📌 Step 1: Collect Installed Applications
def collect_installed_apps():
    print("📥 Collecting installed applications...")
    app_data = {"installed_apps": []}

    try:
        # Get traditional installed apps (Registry-based)
        result = subprocess.run(
            'powershell "Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*"',
            shell=True, capture_output=True, text=True)
        lines = result.stdout.split("\n")

        for line in lines:
            if "DisplayName" in line:
                app_name = line.split(":")[-1].strip()
                app_data["installed_apps"].append({
                    "name": app_name,
                    "source": "Traditional",
                    "version": "N/A",
                    "exe_path": None  # Placeholder for .exe paths
                })

        # Get Microsoft Store apps
        result = subprocess.run(
            'powershell "Get-AppxPackage | Select-Object Name, PackageFullName"',
            shell=True, capture_output=True, text=True)
        lines = result.stdout.split("\n")

        for line in lines:
            if line.strip():
                parts = line.split()
                if len(parts) > 1:
                    app_name = parts[0].strip()
                    app_data["installed_apps"].append({
                        "name": app_name,
                        "source": "Microsoft Store",
                        "version": "N/A",
                        "exe_path": None
                    })

        # Scan for Portable Applications (Standalone `.exe` files)
        search_paths = ["C:\\Users", "D:\\"]
        for search_path in search_paths:
            for root, _, files in os.walk(search_path):
                for file in files:
                    if file.endswith(".exe"):
                        app_data["installed_apps"].append({
                            "name": file,
                            "source": "Portable App",
                            "version": "N/A",
                            "exe_path": os.path.join(root, file)
                        })

    except Exception as e:
        print(f"❌ Error collecting installed apps: {e}")

    return app_data


# 📌 Step 2: Backup Browser Bookmarks
def backup_browser_data():
    print("📥 Backing up browser data...")

    browser_paths = {
        "Chrome": os.path.expanduser("~") + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks",
        "Edge": os.path.expanduser("~") + "\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Bookmarks",
        "Firefox": os.path.expanduser("~") + "\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles"
    }

    browser_data = {"browser_bookmarks": {}}

    for browser, path in browser_paths.items():
        if os.path.exists(path):
            backup_path = os.path.join(browser_backup_folder, f"{browser}_bookmarks.json")
            shutil.copy(path, backup_path)
            print(f"✅ {browser} bookmarks backed up.")

            # Load bookmark file into JSON
            with open(backup_path, "r", encoding="utf-8") as f:
                browser_data["browser_bookmarks"][browser] = json.load(f)

    print("✅ Browser backup completed.")
    return browser_data


# 📌 Step 3: Save Backup Data to JSON
def save_to_json(data):
    print("📥 Saving backup data to JSON...")

    with open(backup_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"✅ Backup saved to {backup_file}")


# 📌 Run Full Backup Process
def full_backup():
    print("\n🔹 Starting Full Application & Browser Backup...\n")

    backup_data = collect_installed_apps()
    browser_data = backup_browser_data()

    # Merge all data
    backup_data.update(browser_data)

    save_to_json(backup_data)

    print("\n✅ Full Backup Completed Successfully! 🚀\n")


# **Trigger the backup**
if __name__ == "__main__":
    full_backup()
