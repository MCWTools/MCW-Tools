import os
import zlib

def get_vault_path():
    """Return the fixed Vault folder path"""
    vault_path = "C:\\Boot\\zFRXk92wgpN6jLsQ"
    if os.path.exists(vault_path):
        return vault_path
    print("Vault does not exist! Please ensure you've used FileVault.py to create it.")
    return None

def list_files_in_vault(vault_path):
    """List all the files in the Vault"""
    files = os.listdir(vault_path)
    return [f for f in files if f.endswith('.vault')]

def extract_file(file_name, vault_path):
    """Decompress and restore a file"""
    file_path = os.path.join(vault_path, file_name)
    original_file_name = file_name.replace('.vault', '')

    with open(file_path, 'rb') as encrypted_file:
        compressed_data = encrypted_file.read()
        data = zlib.decompress(compressed_data)
    
    # Restore the file to the current directory
    with open(original_file_name, 'wb') as original_file:
        original_file.write(data)
    
    # Delete the encrypted file from the Vault
    os.remove(file_path)
    print(f"Restored: {original_file_name}")

def main():
    # Step 1: Locate the Vault
    vault_path = get_vault_path()
    if not vault_path:
        return

    # Step 2: List files in the Vault
    files = list_files_in_vault(vault_path)
    if not files:
        print("The vault is empty. No files to restore.")
        return

    print("Here's all the files in your vault:")
    for i, file_name in enumerate(files, 1):
        print(f"{i}: {file_name}")
    
    # Step 3: Prompt user to select files to restore
    selected_files = input("\nEnter the numbers of the files you want to restore (comma-separated): ").strip()
    if not selected_files:
        print("No files selected. Exiting...")
        return
    
    try:
        selected_indices = [int(x.strip()) - 1 for x in selected_files.split(",")]
    except ValueError:
        print("Invalid input. Please enter numbers separated by commas.")
        return
    
    # Step 4: Restore the selected files
    for index in selected_indices:
        if 0 <= index < len(files):
            extract_file(files[index], vault_path)
        else:
            print(f"Invalid number: {index + 1}. Skipping...")

if __name__ == "__main__":
    main()