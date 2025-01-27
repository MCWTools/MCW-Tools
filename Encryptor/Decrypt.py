from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

# Fixed 32-byte (256-bit) encryption key
key = b'MCWEncryptor1831830900()4--1[14124144]141241-0)()'[:32]  # Use only the first 32 bytes

# Function to encrypt a file
def encrypt_file(file_path):
    try:
        # Read the original file data
        with open(file_path, 'rb') as f:
            file_data = f.read()

        # Generate a random IV (Initialization Vector) for the encryption
        iv = os.urandom(16)

        # Initialize the AES cipher in CBC mode with the provided key and IV
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Pad the file data to ensure its length is a multiple of the block size
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(file_data) + padder.finalize()

        # Encrypt the padded data
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        # Modify the file extension by adding 'enc' to the original file's extension
        base, ext = os.path.splitext(file_path)
        encrypted_file_path = base + ext + 'enc'  # Add 'enc' as a suffix to the original extension

        # Save the encrypted data along with the IV to the new file
        with open(encrypted_file_path, 'wb') as f:
            f.write(iv + encrypted_data)

        # Delete the original file
        os.remove(file_path)

        # Provide feedback to the user
        print(f"File has been encrypted and saved at: {encrypted_file_path}")
        print(f"The original file has been deleted.")
        print(f"Decrypt key is: {key.decode()}")  # Display the encryption key in the console

    except Exception as e:
        print(f"Error: {e}")

# Example usage
file_path = input("Enter the full path of the file to encrypt (include quotes if necessary): ").strip('"')
encrypt_file(file_path)
