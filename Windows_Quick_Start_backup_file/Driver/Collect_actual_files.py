import os
import csv
import shutil
import zipfile
from datetime import datetime

# === Config ===
DRIVE_TO_SCAN = "D:\\"
BACKUP_FOLDER = "files_backup_d"
CSV_FILE = "file_metadata_d.csv"
ZIP_FILE = "d_drive_backup.zip"
ERROR_LOG = "scan_errors_d.log"

# === Excluded folders (for safety, tweak if needed) ===
excluded_dirs = [
    "$Recycle.Bin",
    "System Volume Information"
]

def is_excluded_path(path):
    return any(excluded.lower() in path.lower() for excluded in excluded_dirs)

def safe_copy_file(src_path, backup_root, error_logs):
    try:
        rel_path = os.path.relpath(src_path, start=DRIVE_TO_SCAN)
        dest_path = os.path.join(backup_root, rel_path)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy2(src_path, dest_path)
        #print(f"✅ Copied: {rel_path}")
        return rel_path, os.path.getsize(src_path), datetime.fromtimestamp(os.path.getmtime(src_path)).strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f"❌ Skipped {src_path} — {e}")
        error_logs.append(f"{src_path} - {e}")
        return None

def collect_and_backup_d_drive():
    print(f"\n🚀 Starting backup for drive: {DRIVE_TO_SCAN}")
    file_metadata = []
    error_logs = []

    # Ensure backup folder exists
    os.makedirs(BACKUP_FOLDER, exist_ok=True)

    for root, _, files in os.walk(DRIVE_TO_SCAN):
        if is_excluded_path(root):
            print(f"🔒 Skipping excluded system directory: {root}")
            continue

        for file in files:
            full_path = os.path.join(root, file)
            result = safe_copy_file(full_path, BACKUP_FOLDER, error_logs)
            if result:
                rel_path, size, modified = result
                file_metadata.append([rel_path, size, modified])

    # Save metadata CSV
    print(f"\n📝 Saving metadata to: {CSV_FILE}")
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Relative Path", "Size (Bytes)", "Last Modified"])
        writer.writerows(file_metadata)
    print("✅ Metadata saved.")

    # Save error log if needed
    if error_logs:
        print(f"🧾 Writing error log to: {ERROR_LOG}")
        with open(ERROR_LOG, "w", encoding="utf-8") as logfile:
            logfile.write("⚠️ These files could not be copied:\n\n")
            for error in error_logs:
                logfile.write(f"{error}\n")
        print("⚠️ Some files were skipped. See log for details.")

    # Create final ZIP
    print(f"\n📦 Creating ZIP archive: {ZIP_FILE}")
    with zipfile.ZipFile(ZIP_FILE, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(CSV_FILE)
        for foldername, _, filenames in os.walk(BACKUP_FOLDER):
            for filename in filenames:
                abs_path = os.path.join(foldername, filename)
                arc_path = os.path.relpath(abs_path, start=".")
                zipf.write(abs_path, arc_path)
                #print(f"➕ Zipped: {arc_path}")
    print(f"\n✅ Backup completed successfully! Final ZIP: {ZIP_FILE}")

if __name__ == "__main__":
    collect_and_backup_d_drive()
