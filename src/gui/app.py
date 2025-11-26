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
        # Frame: video file/folder selection
        video_frame = tk.LabelFrame(self.window, text="Video Selection", padx=10, pady=10)
        video_frame.pack(fill="x", padx=20, pady=10)
        
        # Multi-line textbox for video file/folder path
        self.video_path = tk.Text(video_frame, height=3, width=60, state='disabled')
        self.video_path.pack(side="left", padx=5)
        
        # Select File Button
        select_file_btn = tk.Button(
            video_frame,
            text="Select File",
            command=self._on_submit,
            width=12
        )
        select_file_btn.pack(pady=2)
        
        # Select Folder Button
        select_folder_btn = tk.Button(
            video_frame,
            text="Select Folder",
            command=self._on_submit,
            width=12
        )
        select_folder_btn.pack(pady=2)
        
        # Frame: show selection/search
        search_show_frame = tk.LabelFrame(self.window, text="Search Show", padx=10, pady=10)
        search_show_frame.pack(fill="x", padx=20, pady=10)
        
        show_name_label = tk.Label(search_show_frame, text="Show Name:")
        show_name_label.grid(row=0, column=0, sticky="w", pady=5)
        
        self.show_name_entry = tk.Entry(search_show_frame, width=40)
        self.show_name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        search_show_btn = tk.Button(
            search_show_frame,
            text="Search",
            command=self._on_submit,
            width=12,
        )
        search_show_btn.grid(row=0, column=3, pady=2)
        
        # Frame: search results
        search_results_frame = tk.LabelFrame(self.window, text="Search Results", padx=10, pady=10)
        search_results_frame.pack(fill="x", padx=20, pady=10, expand=True)
        
        search_scrollbar = tk.Scrollbar(search_results_frame)
        search_scrollbar.pack(side="right", fill="y")
        
        listbox = tk.Listbox(search_results_frame, yscrollcommand=search_scrollbar.set,
                             width=80, height=8)
        listbox.pack(side='left', pady=10)
        search_scrollbar.config(command=listbox.yview)

        listbox.bind("<<ListboxSelect>>", self._on_submit)


    
    def _on_submit(self):
        # Get data from input fields
        # Call your existing core functions
        # Display results
        pass
    
    def run(self):
        # Start GUI
        self.window.mainloop()