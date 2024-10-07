import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def move_videos(source_dir, target_dir):
    """
    Moves all video files from the source directory and its subdirectories to a target directory.

    Args:
    - source_dir (str): The root directory to search for video files.
    - target_dir (str): The target directory where the 'VIDEOS_DIRECTORY' will be created to store the video files.
    """
    # Define the directory where all videos will be moved
    videos_dir = os.path.join(target_dir, 'VIDEOS_DIRECTORY')

    # Define a set of common video file extensions
    video_extensions = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.mpeg', '.mpg', '.m4v', '.3gp', '.3g2', '.f4v'}

    # Create the target directory if it does not exist
    os.makedirs(videos_dir, exist_ok=True)

    # Walk through the source directory and its subdirectories
    for subdir, _, files in os.walk(source_dir):
        for file in files:
            try:
                # Check if the file is a video by its extension
                if os.path.splitext(file)[1].lower() in video_extensions:
                    # Construct the full file path
                    source_path = os.path.join(subdir, file)
                    # Construct the target path
                    target_path = os.path.join(videos_dir, file)

                    # Check if a file with the same name already exists in the target directory
                    if os.path.exists(target_path):
                        # If a duplicate is found, rename the file
                        base, extension = os.path.splitext(file)
                        count = 1
                        while os.path.exists(target_path):
                            new_file_name = f"{base}_{count}{extension}"
                            target_path = os.path.join(videos_dir, new_file_name)
                            count += 1
                        print(f"Duplicate found. Renaming and moving file to: {target_path}")

                    # Move the file to the target directory
                    shutil.move(source_path, target_path)
                    print(f"Moved: {source_path} -> {target_path}")

            except Exception as e:
                print(f"Error moving file {file}: {e}")

    print("All videos have been moved to the VIDEOS DIRECTORY.")
    messagebox.showinfo("Success", "All videos have been moved to the VIDEOS DIRECTORY.")

def select_source_directory():
    """
    Opens a dialog for selecting the source directory to search for videos.
    """
    source_dir = filedialog.askdirectory(title="Select Directory to Search for Videos")
    source_dir_entry.delete(0, tk.END)
    source_dir_entry.insert(0, source_dir)

def select_target_directory():
    """
    Opens a dialog for selecting the target directory where the 'VIDEOS_DIRECTORY' will be created.
    """
    target_dir = filedialog.askdirectory(title="Select Target Directory for VIDEOS_DIRECTORY")
    target_dir_entry.delete(0, tk.END)
    target_dir_entry.insert(0, target_dir)

def start_moving_videos():
    """
    Starts the process of moving videos after user has selected both source and target directories.
    """
    source_dir = source_dir_entry.get()
    target_dir = target_dir_entry.get()

    if not source_dir or not target_dir:
        messagebox.showerror("Error", "Please select both the source and target directories.")
        return

    if not os.path.isdir(source_dir):
        messagebox.showerror("Error", "The selected source directory does not exist.")
        return

    if not os.path.isdir(target_dir):
        messagebox.showerror("Error", "The selected target directory does not exist.")
        return

    move_videos(source_dir, target_dir)

# Create the main application window
root = tk.Tk()
root.title("Video Mover Application")

# Create and place GUI elements
tk.Label(root, text="Select Directory to Search for Videos:").grid(row=0, column=0, padx=10, pady=10)
source_dir_entry = tk.Entry(root, width=50)
source_dir_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_source_directory).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Select Target Directory for VIDEOS_DIRECTORY:").grid(row=1, column=0, padx=10, pady=10)
target_dir_entry = tk.Entry(root, width=50)
target_dir_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_target_directory).grid(row=1, column=2, padx=10, pady=10)

tk.Button(root, text="Start Moving Videos", command=start_moving_videos).grid(row=2, column=1, padx=10, pady=20)

# Run the application
root.mainloop()
