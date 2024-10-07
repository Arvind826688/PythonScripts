import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox

def select_video_file():
    """
    Opens a file dialog to select a video file.
    """
    video_file_path = filedialog.askopenfilename(
        title="Select Video File",
        filetypes=[
            ("All Video Files", "*.mp4;*.avi;*.mkv;*.mov;*.wmv;*.flv;*.webm;*.mpeg;*.mpg;*.m4v;*.3gp;*.3g2;*.f4v"),
            ("MP4 files", "*.mp4"),
            ("AVI files", "*.avi"),
            ("MKV files", "*.mkv"),
            ("MOV files", "*.mov"),
            ("WMV files", "*.wmv"),
            ("FLV files", "*.flv"),
            ("WEBM files", "*.webm"),
            ("MPEG files", "*.mpeg;*.mpg"),
            ("M4V files", "*.m4v"),
            ("3GP files", "*.3gp;*.3g2"),
            ("F4V files", "*.f4v")
        ]
    )
    video_path_entry.delete(0, tk.END)
    video_path_entry.insert(0, video_file_path)

def select_output_directory():
    """
    Opens a file dialog to select the output directory where frames will be saved.
    """
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    output_dir_entry.delete(0, tk.END)
    output_dir_entry.insert(0, output_dir)

def extract_frames(video_path, output_dir):
    """
    Extracts frames from a video file and saves them to a specified output directory.

    Args:
    - video_path (str): The path to the video file.
    - output_dir (str): The path to the directory where frames will be saved.
    """
    try:
        if not os.path.isfile(video_path):
            raise FileNotFoundError("The selected video file does not exist.")

        if not os.path.isdir(output_dir):
            raise NotADirectoryError("The selected output directory does not exist.")

        # Extract the video name (without extension) to create a folder for frames
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        frames_dir = os.path.join(output_dir, f"{video_name}_frames")

        # Create the frames directory if it does not exist
        os.makedirs(frames_dir, exist_ok=True)

        # Open the video file using OpenCV
        cap = cv2.VideoCapture(video_path)

        # Check if video opened successfully
        if not cap.isOpened():
            raise IOError("Error opening video file. The file may be corrupted or in an unsupported format.")

        frame_count = 0
        success = True

        while success:
            # Read the next frame from the video
            success, frame = cap.read()
            if success:
                # Save the frame as an image file
                frame_filename = os.path.join(frames_dir, f"frame_{frame_count:05d}.jpg")
                cv2.imwrite(frame_filename, frame)
                frame_count += 1
                print(f"Extracted frame {frame_count}: {frame_filename}")
            else:
                if frame_count == 0:
                    raise ValueError("No frames could be extracted. The video may be empty or corrupted.")

        # Release the video capture object
        cap.release()

        messagebox.showinfo("Success", f"Frames extracted and saved to {frames_dir}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def start_extraction():
    """
    Starts the frame extraction process after user input is validated.
    """
    video_path = video_path_entry.get()
    output_dir = output_dir_entry.get()

    if not video_path or not output_dir:
        messagebox.showerror("Error", "Please select both the video file and the output directory.")
        return

    extract_frames(video_path, output_dir)

# Create the main application window
root = tk.Tk()
root.title("Video Frame Extractor")

# Create and place GUI elements
tk.Label(root, text="Select Video File:").grid(row=0, column=0, padx=10, pady=10)
video_path_entry = tk.Entry(root, width=50)
video_path_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_video_file).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Select Output Directory:").grid(row=1, column=0, padx=10, pady=10)
output_dir_entry = tk.Entry(root, width=50)
output_dir_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_output_directory).grid(row=1, column=2, padx=10, pady=10)

tk.Button(root, text="Start Extraction", command=start_extraction).grid(row=2, column=1, padx=10, pady=20)

# Run the application
root.mainloop()
