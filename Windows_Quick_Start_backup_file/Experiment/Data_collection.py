import os
import shutil
import zipfile

def collect_data(output_path="collected_data.zip"):
    # Directories to collect data from
    folders_to_collect = [
        "C:\\Users\\SRAVYA\\Documents",
        "C:\\Users\\SRAVYA\\Pictures",
        #"C:\\Users\\SRAVYA\\Videos",
        #"C:\\Users\\SRAVYA\\OneDrive\\Desktop",
        #"C:\\Users\\SRAVYA\\python_blockchain_app"
    ]

    # Create a temporary folder to store collected data
    temp_folder = "temp_data"
    print(f"Creating temporary folder: {temp_folder}")
    os.makedirs(temp_folder, exist_ok=True)

    # Copy files into the temp folder
    for folder in folders_to_collect:
        print(f"Checking folder: {folder}")
        if os.path.exists(folder):
            for root, dirs, files in os.walk(folder):
                # Skip system-related files like "desktop.ini"
                files = [f for f in files if not f.lower().endswith(".ini")]
                
                for file in files:
                    try:
                        src_file = os.path.join(root, file)
                        dest_file = os.path.join(temp_folder, os.path.relpath(src_file, folder))
                        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                        #print(f"Copying {src_file} to {dest_file}")
                        shutil.copy2(src_file, dest_file)
                    except PermissionError as e:
                        print(f"Permission denied for {src_file}: {e}")
                    except Exception as e:
                        print(f"Error copying {src_file}: {e}")
        else:
            print(f"Folder does not exist: {folder}")

    # Compress the collected data into a ZIP file
    print(f"Creating ZIP file: {output_path}")
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_folder):
            for file in files:
                file_path = os.path.join(root, file)
                #print(f"Adding file to ZIP: {file_path}")
                zipf.write(file_path, os.path.relpath(file_path, temp_folder))

    # Clean up the temporary folder
    print("Cleaning up temporary folder.")
    shutil.rmtree(temp_folder)
    print(f"Data collected and compressed into {output_path}")
    return output_path


# Call the function
#output_zip = collect_data()

