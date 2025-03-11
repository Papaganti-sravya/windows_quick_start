import csv

def generate_install_script(csv_file="installed_apps.csv", output_script="install_apps.ps1"):
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

    # Write PowerShell script
    with open(output_script, "w", encoding="utf-8") as ps_file:
        ps_file.write("# PowerShell Script to Reinstall Applications\n")
        ps_file.write("# Run this script in PowerShell (Admin Mode)\n\n")

        # Install Microsoft Store apps
        if microsoft_store_apps:
            ps_file.write("# Installing Microsoft Store Apps\n")
            for app in microsoft_store_apps:
                ps_file.write(f"Write-Output 'Installing {app}...'\n")
                ps_file.write(f"Get-AppxPackage -Name '{app}' -AllUsers | Foreach-Object {{ Add-AppxPackage -Register -DisableDevelopmentMode ($_.InstallLocation + '\\AppxManifest.xml') }}\n")

        # List Win32 applications
        if win32_apps:
            ps_file.write("\n# The following Win32 applications need to be installed manually:\n")
            for app in win32_apps:
                ps_file.write(f"Write-Output 'Please install {app} manually.'\n")

        ps_file.write("\nWrite-Output 'Installation script completed.'\n")

    print(f"✅ Installation script saved as {output_script}")
    print("💡 Run the script using PowerShell (Admin Mode) to install Microsoft Store apps.")

# Generate the installation script
generate_install_script()
