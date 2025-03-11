import os
import shutil
import subprocess

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = os.path.join(BASE_DIR, "windows_quick_start_backup")
ZIP_OUTPUT = os.path.join(BASE_DIR, "windows_quick_start_backup_protected.zip")
SEVEN_ZIP_PATH = r'"C:\Program Files\7-Zip\7z.exe"'
PASSWORD = "YourSecurePassword123"

# Subfolder paths
folders_to_include = {
    "apps": os.path.join(BACKUP_DIR, "apps"),
    "browser": os.path.join(BACKUP_DIR, "browser"),
    "drivers": os.path.join(BACKUP_DIR, "drivers")
}

source_data = {
    "apps": [
        "apps/Create_CSV_Files_For_Application/App_Data.py",
        "apps/Create_CSV_Files_For_Application/installed_apps.csv",
        "apps/Create_CSV_Files_For_Application/Re_install_Apps.py"
    ],
    "browser": [
        "Browser_backup/Browser_data.py",
        "Browser_backup/browser_backup/Chrome_bookmarks.json",
        "Browser_backup/browser_backup/Edge_bookmarks.json"
    ],
    "drivers": [
        "Driver/Collect_actual_files.py",
        "Driver/d_drive_backup.zip"
    ]
}

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"✅ Created: {path}")
    else:
        print(f"📁 Folder already exists: {path}")

def copy_files():
    print("\n📄 Copying files into backup folder...")
    for category, files in source_data.items():
        dest_folder = folders_to_include[category]
        ensure_dir(dest_folder)
        for file_rel in files:
            src = os.path.join(BASE_DIR, file_rel)
            if os.path.exists(src):
                shutil.copy2(src, dest_folder)
                print(f"📎 Copied: {src}")
            else:
                print(f"⚠️ Missing: {src}")

def create_password_protected_zip():
    print("\n🔐 Creating password-protected zip...")

    if os.path.exists(ZIP_OUTPUT):
        os.remove(ZIP_OUTPUT)

    zip_command = (
        f'{SEVEN_ZIP_PATH} a -tzip "{ZIP_OUTPUT}" "{BACKUP_DIR}\\*" -p{PASSWORD} -mem=AES256 -r'
    )

    result = subprocess.run(zip_command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"\n✅ Password-protected zip created successfully:\n{ZIP_OUTPUT}")
    else:
        print("❌ Failed to create ZIP:")
        print(result.stderr)

def main():
    print("\n📁 Creating folder structure...")
    for path in folders_to_include.values():
        ensure_dir(path)

    copy_files()
    create_password_protected_zip()

if __name__ == "__main__":
    main()
