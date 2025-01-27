from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

# Fixed 32-byte (256-bit) encryption key for comparison
correct_key = b'MCWEncryptor1831830900()4--1[14124144]141241-0)()'[:32]  # Use only the first 32 bytes

# Function to decrypt an encrypted file
def decrypt_file(encrypted_file_path, key):
    try:
        # Ensure the file has the correct 'enc' suffix
        if not encrypted_file_path.endswith('enc'):
            print("Error: The file does not have the expected '.enc' extension.")
            return

        # Read the encrypted file
        with open(encrypted_file_path, 'rb') as f:
            iv_and_encrypted_data = f.read()

        # Extract the IV and encrypted data
        iv = iv_and_encrypted_data[:16]  # The first 16 bytes are the IV
        encrypted_data = iv_and_encrypted_data[16:]  # The rest is the encrypted data

        # Initialize the AES cipher in CBC mode with the provided key and IV
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt the data
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # Remove padding from the decrypted data
        unpadder = padding.PKCS7(128).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

        # Determine the original file extension by removing the 'enc' suffix
        decrypted_file_path = encrypted_file_path[:-3]  # Remove the last 3 characters (enc)

        # Save the decrypted data to a new file
        with open(decrypted_file_path, 'wb') as f:
            f.write(unpadded_data)

        # Delete the encrypted file after successful decryption
        os.remove(encrypted_file_path)

        # Provide feedback to the user
        print("File decrypted successfully!")
        print(f"The decrypted file has been saved at: {decrypted_file_path}")
        print("The encrypted file has been deleted.")

    except Exception as e:
        print(f"Error during decryption: {e}")

# Example usage
encrypted_file_path = input("Enter the full path of the encrypted file (include quotes if necessary): ").strip('"')

# Ask the user to input the secret key
key_input = input("Enter the secret key: ").encode()  # Convert input to bytes

# Validate the key
if key_input != correct_key:
    print("Your secret key is not correct! Decryption aborted.")
else:
    print("Your secret key is correct!")
    decrypt_file(encrypted_file_path, key_input)
