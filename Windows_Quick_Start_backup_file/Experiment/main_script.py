from Data_collection import collect_data
from Generate_qr_method import generate_qr_code

def main():
    # Step 1: Collect data and create a ZIP file
    zip_file = collect_data(output_path="collected_data.zip")
    print(f"Collected ZIP file is saved at: {zip_file}")

    # Step 2: Generate a QR code for the ZIP file
    qr_image = "collected_data_qr.png"  # Name for the QR code image file
    generate_qr_code(zip_file, output_image=qr_image)

    print(f"QR code generation complete. File saved at: {qr_image}")

# Run the main script
if __name__ == "__main__":
    main()
