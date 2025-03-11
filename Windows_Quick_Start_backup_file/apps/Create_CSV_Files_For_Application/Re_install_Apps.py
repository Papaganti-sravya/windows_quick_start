import csv
import subprocess

def generate_install_script(csv_file="installed_apps.csv", output_script="install_apps.ps1", log_file="install_log.txt"):
    microsoft_store_apps = []
    win32_apps = []

    # Read installed apps from CSV
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            app_name = row["Name"]
            source = row["Source"]

            if source == "Microsoft Store":
                microsoft_store_apps.append(app_name)
            else:
                win32_apps.append(app_name)

    # Ask user permission
    user_choice = input("⚡ Do you want to reinstall applications automatically? (yes/no): ").strip().lower()
    if user_choice != "yes":
        print("❌ Installation aborted.")
        return

    print("✅ Creating PowerShell installation script...")

    # Write PowerShell script with logging
    with open(output_script, "w", encoding="utf-8") as ps_file:
        ps_file.write(f"# PowerShell Script to Reinstall Apps\n")
        ps_file.write(f"# Run in Admin Mode\n")
        ps_file.write(f"$LogFile = \"{log_file}\"\n")
        ps_file.write(f"New-Item -Path $LogFile -ItemType File -Force | Out-Null\n\n")

        # Microsoft Store apps
        if microsoft_store_apps:
            ps_file.write("# Microsoft Store App Reinstallation\n")
            for app in microsoft_store_apps:
                ps_file.write(f"Write-Output 'Installing {app}...'\n")
                ps_file.write(f"$app = Get-AppxPackage -Name '{app}' -AllUsers\n")
                ps_file.write("if ($app) {\n")
                ps_file.write("    try {\n")
                ps_file.write("        Add-AppxPackage -Register -DisableDevelopmentMode ($app.InstallLocation + '\\AppxManifest.xml')\n")
                ps_file.write(f"        Add-Content -Path $LogFile -Value '✅ {app} installed successfully.'\n")
                ps_file.write("    } catch {\n")
                ps_file.write(f"        Add-Content -Path $LogFile -Value '❌ Failed to install {app}: $_'\n")
                ps_file.write("    }\n")
                ps_file.write("} else {\n")
                ps_file.write(f"    Add-Content -Path $LogFile -Value '❌ {app} not found in AppxPackage list.'\n")
                ps_file.write("}\n\n")

        # Win32 apps manual notice
        if win32_apps:
            ps_file.write("# Manual Installation Required for Win32 Apps\n")
            for app in win32_apps:
                ps_file.write(f"Add-Content -Path $LogFile -Value 'ℹ️ Please manually install {app}.'\n")

        ps_file.write("\nWrite-Output 'Installation complete. See install_log.txt for details.'\n")

    print(f"✅ Script saved as {output_script}")
    print("💡 Running PowerShell script now...")
    
    # Run the script
    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", output_script], shell=True)

    print("📄 Installation log will be saved in:", log_file)

# Trigger it
generate_install_script()
