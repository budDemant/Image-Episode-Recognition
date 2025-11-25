import tkinter as tk
from tkinter import filedialog

class EpisodeRecognizerGUI:
    def __init__(self):
        # 1. Create main window
        self.window = tk.Tk()
        self.window.title("Image-Episode Recognition")
        self.window.geometry("700x600")
        self.window.resizable(True, True)
        
        # 2. Create widgets (buttons, text fields, etc.)
        self._create_widgets()
    
    def _create_widgets(self):
        # Frame for video file/folder selection
        video_frame = tk.LabelFrame(self.window, text="Video Selection", padx=10, pady=10)
        video_frame.pack(fill="x", padx=20, pady=10)
        
        # Multi-line textbox for video file/folder path
        self.video_path = tk.Text(video_frame, height=3, width=60, state='disabled')
        self.video_path.pack(side="left", padx=5)
        
        # Align buttons for file/folder selection
        video_btn_frame = tk.Frame(video_frame)
        video_btn_frame.pack(side="right", padx=5)
        
        # Select File Button
        select_file_btn = tk.Button(
            video_btn_frame,
            text="Select File",
            command=self._on_submit,
            width=12
        )
        select_file_btn.pack(pady=2)
        
        # Select Folder Button
        select_folder_btn = tk.Button(
            video_btn_frame,
            text="Select Folder",
            command=self._on_submit,
            width=12
        )
        select_folder_btn.pack(pady=2)



    
    def _on_submit(self):
        # Get data from input fields
        # Call your existing core functions
        # Display results
        pass
    
    def run(self):
        # Start GUI
        self.window.mainloop()