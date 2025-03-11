import os
import csv
from datetime import datetime
import string

# Detect all available drives
def get_available_drives():
    return [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]

# List of system directories to exclude
excluded_dirs = [
    "C:\\Windows",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "C:\\$Recycle.Bin",
    "C:\\System Volume Information"
]

output_file = "collected_all_drives.csv"
error_log_file = "scan_errors.log"

def collect_all_drive_files():
    file_data = []
    error_logs = []
    drives = get_available_drives()
    
    print(f"📌 Detected Drives: {drives}")

    for drive in drives:
        print(f"🔍 Scanning Drive: {drive}")
        
        for root, _, files in os.walk(drive):
            if any(root.startswith(excluded) for excluded in excluded_dirs):
                continue

            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    last_modified = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                    file_data.append([file_path, file_size, last_modified])
                except Exception as e:
                    error_logs.append(f"{file_path} - {e}")

    # Save collected file data
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["File Path", "Size (Bytes)", "Last Modified"])
        writer.writerows(file_data)

    # Save errors to log file
    if error_logs:
        with open(error_log_file, "w", encoding="utf-8") as log_file:
            log_file.write("⚠️ The following files could not be processed:\n\n")
            for error in error_logs:
                log_file.write(f"{error}\n")
        print(f"❌ Some files couldn't be processed. See {error_log_file} for details.")

    print(f"✅ Collected files saved to: {output_file}")

# Run the function
collect_all_drive_files()
