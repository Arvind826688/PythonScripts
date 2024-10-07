import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import logging
from datetime import datetime

# Configure logging
log_filename = f"image_mover_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Define the image formats to search for
image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.ico', '.heic', '.heif')

def select_directory():
    """
    Opens a file dialog to select a directory.
    """
    directory_path = filedialog.askdirectory(title="Select Directory")
    return directory_path

def move_images_to_photo_directory(root_directory, destination_directory):
    """
    Searches for images in the specified directory and moves them to 'PHOTO DIRECTORY'.

    Args:
    - root_directory (str): The path to the directory to search for images.
    - destination_directory (str): The directory where "PHOTO DIRECTORY" will be created.
    """
    try:
        # Create a "PHOTO DIRECTORY" in the destination directory
        photo_directory = os.path.join(destination_directory, "PHOTO DIRECTORY")
        os.makedirs(photo_directory, exist_ok=True)

        # Walk through all the directories and subdirectories
        for subdir, _, files in os.walk(root_directory):
            for file in files:
                file_path = os.path.join(subdir, file)

                # Check if the file is an image
                if file.lower().endswith(image_extensions):
                    try:
                        # Create a unique filename if a file with the same name already exists
                        destination_path = os.path.join(photo_directory, file)
                        if os.path.exists(destination_path):
                            base, extension = os.path.splitext(file)
                            counter = 1
                            while os.path.exists(destination_path):
                                destination_path = os.path.join(photo_directory, f"{base}_{counter}{extension}")
                                counter += 1

                        # Move the image file to the "PHOTO DIRECTORY"
                        shutil.move(file_path, destination_path)
                        logging.info(f"Moved: {file_path} -> {destination_path}")
                        print(f"Moved: {file_path} -> {destination_path}")

                    except Exception as e:
                        logging.error(f"Failed to move {file_path}: {e}")
                        print(f"Failed to move {file_path}: {e}")

        messagebox.showinfo("Success", "All images have been moved to PHOTO DIRECTORY.")
        logging.info("All images have been successfully moved to PHOTO DIRECTORY.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        logging.error(f"An error occurred during processing: {e}")

def start_moving():
    """
    Starts the image moving process after validating user input.
    """
    root_directory = source_directory_entry.get()
    destination_directory = destination_directory_entry.get()

    if not root_directory or not destination_directory:
        messagebox.showerror("Error", "Please select both the source directory and the destination directory.")
        logging.error("Source or destination directory not selected.")
        return

    logging.info(f"Starting to move images from {root_directory} to {destination_directory}")
    move_images_to_photo_directory(root_directory, destination_directory)

# Create the main application window
root = tk.Tk()
root.title("Image Mover to PHOTO DIRECTORY")

# Create and place GUI elements
tk.Label(root, text="Select Source Directory:").grid(row=0, column=0, padx=10, pady=10)
source_directory_entry = tk.Entry(root, width=50)
source_directory_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=lambda: source_directory_entry.insert(0, select_directory())).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Select Destination Directory:").grid(row=1, column=0, padx=10, pady=10)
destination_directory_entry = tk.Entry(root, width=50)
destination_directory_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=lambda: destination_directory_entry.insert(0, select_directory())).grid(row=1, column=2, padx=10, pady=10)

tk.Button(root, text="Start Moving", command=start_moving).grid(row=2, column=1, padx=10, pady=20)

# Run the application
root.mainloop()
