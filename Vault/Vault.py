import os
import shutil
import zlib

def create_vault():
    """Create a fixed Vault folder at C:/Boot/zFRXk92wgpN6jLsQ"""
    vault_path = "C:\\Boot\\zFRXk92wgpN6jLsQ"
    if not os.path.exists(vault_path):
        os.makedirs(vault_path)
        print("Vault created at C:/Boot/zFRXk92wgpN6jLsQ.")
    return vault_path

def send_to_vault(file_path, vault_path):
    """Compress and send the file to the Vault"""
    if not os.path.exists(file_path):
        print("File does not exist. Please check the path!")
        return
    
    # Read the file and compress its contents
    with open(file_path, 'rb') as file:
        data = file.read()
        compressed_data = zlib.compress(data)
    
    # Save the compressed file in the Vault with a ".vault" extension
    file_name = os.path.basename(file_path)
    encrypted_file_path = os.path.join(vault_path, file_name + ".vault")
    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(compressed_data)
    
    print("Your file has been sent to the vault. Use VaultOpen.py when you want to retrieve the file back.")
    
    # Delete the original file
    os.remove(file_path)

def main():
    # Step 1: Create the Vault if it doesn't already exist
    vault_path = create_vault()
    
    # Step 2: Prompt the user for the file path
    file_path = input('Path to the file you want to send to the vault (Include ""): ').strip('"')
    send_to_vault(file_path, vault_path)

if __name__ == "__main__":
    main()