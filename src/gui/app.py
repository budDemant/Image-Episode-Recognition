import tkinter as tk
from tkinter import filedialog

from src.query_show import QueryShow
from src.episode_image_fetcher import EpisodeImageFetcher
from src.video_processor import process_videos
from src.rename_file import rename_file

import os

class EpisodeRecognizerGUI:
    def __init__(self):
        # 1. Create main window
        self.window = tk.Tk()
        self.window.title("Image-Episode Recognition")
        self.window.geometry("700x600")
        self.window.resizable(True, True)
        
        # Variables to store user input
        self.video_paths = []
        self.show_id = None
        self.season_number_entry = None
        self.search_results = []  # Store full search results
        
        # 2. Create widgets (buttons, text fields, etc.)
        self._create_widgets()
    
    def _create_widgets(self):
        # Frame: video file/folder selection
        video_frame = tk.LabelFrame(self.window, text="Video Selection", padx=10, pady=10)
        video_frame.pack(fill="x", padx=20, pady=10)
        
        # Multi-line textbox for video file/folder path
        self.video_path_text = tk.Text(video_frame, height=3, width=60, state='disabled')
        self.video_path_text.pack(side="left", padx=5)
        
        # Select File Button
        select_file_btn = tk.Button(
            video_frame,
            text="Select File",
            command=self._select_file,
            width=12
        )
        select_file_btn.pack(pady=2)
        
        # Select Folder Button
        select_folder_btn = tk.Button(
            video_frame,
            text="Select Folder",
            command=self._select_folder,
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
        
        
        
        # Frame: search results
        search_results_frame = tk.LabelFrame(self.window, text="Search Results", padx=10, pady=10)
        search_results_frame.pack(fill="x", padx=20, pady=10, expand=True)
        
        search_scrollbar = tk.Scrollbar(search_results_frame)
        search_scrollbar.pack(side="right", fill="y")
        
        listbox = tk.Listbox(search_results_frame, yscrollcommand=search_scrollbar.set,
                             width=80, height=8)
        listbox.pack(side='left', pady=10)
        search_scrollbar.config(command=listbox.yview)

        listbox.bind("<<ListboxSelect>>", self._select_list)
        
        search_show_btn = tk.Button(
            search_show_frame,
            text="Search",
            command=lambda: self._search_show(self.show_name_entry, listbox),
            width=12,
        )
        search_show_btn.grid(row=0, column=3, pady=2)
        
        # Season number
        season_number_label = tk.Label(search_results_frame, text="Season Number:")
        season_number_label.pack(pady=5)
        # TODO: Error handling for invalid input
        self.season_number_entry = tk.Entry(search_results_frame, width=40)
        self.season_number_entry.pack(padx=10, pady=5)
        
        # Process button
        process_btn = tk.Button(
            self.window,
            text="Process Video(s)",
            command=self._process,
            bg="green",
            fg="white",
            font=("Arial", 12, "bold"),
            height=2,
            width=20
        )
        process_btn.pack(pady=10)
        
        # Frame: Recognition Results
        recognition_results_frame = tk.LabelFrame(self.window, text="Recognition Results", 
                                                  padx=10, pady=10)
        recognition_results_frame.pack(fill="x", padx=20, pady=10, expand=True)
        
        recognition_scrollbar = tk.Scrollbar(recognition_results_frame)
        recognition_scrollbar.pack(side="right", fill="y")
        
        self.recognition_listbox = tk.Listbox(recognition_results_frame, 
                                              yscrollcommand=recognition_scrollbar.set,
                             width=80, height=8, state='disabled', exportselection=False)
        self.recognition_listbox.pack(side='left', pady=10)
        recognition_scrollbar.config(command=self.recognition_listbox.yview)
        
    def _select_list(self, event):
        listbox = event.widget
        if listbox.curselection():
            index = listbox.curselection()[0]
            if index < len(self.search_results):
                selected_show = self.search_results[index]
                self.show_id = selected_show.get("id")
                # print(f"Selected: {self.show_id}")
    
    def _search_show(self, entry, listbox):
        query = entry.get()
        #TODO: refactor numbered_list function in query_show to remove print statements
        self.search_results = QueryShow().search_show_by_name(query)
        listbox.delete(0, tk.END)
        self.show_id = None  # Reset selection
        
        for show in self.search_results:
            name = show.get("name")
            first_air_date = show.get("first_air_date", "")
            year = first_air_date[:4] if first_air_date else "N/A"
            show_entry = f"{name} ({year})"
            listbox.insert(tk.END, show_entry)
    
    def _select_file(self):
        """Open file dialog to select a single video file"""
        filetypes = (
            ('Video files', '*.mkv *.mp4 *.avi *.mov'),
            ('All files', '*.*')
        )
        filepath = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=filetypes
        )
        if filepath:
            self.video_paths = [os.path.normpath(filepath)]
            self._update_video_display()
            
    def _select_folder(self):
        """Open dialog to select a folder containing video files"""
        folder = filedialog.askdirectory(title="Select Folder with Videos")
        if folder:
            # Get all video files from folder
            folder = os.path.normpath(folder)
            video_extensions = ('.mkv', '.mp4', '.avi', '.mov')
            self.video_paths = [
                os.path.join(folder, f)
                for f in os.listdir(folder)
                if f.lower().endswith(video_extensions)
            ]
            
            self._update_video_display()

    def _update_video_display(self):
        """Update the text widget to show selected videos"""
        self.video_path_text.config(state='normal') # enable editing temporarily
        self.video_path_text.delete(1.0, tk.END)
        if len(self.video_paths) == 1:
            self.video_path_text.insert(1.0, self.video_paths[0])
        else:
            self.video_path_text.insert(1.0, f"{len(self.video_paths)} videos selected:\n")
            for path in self.video_paths[:5]:  # Show first 5
                self.video_path_text.insert(tk.END, f"  • {os.path.basename(path)}\n")
            if len(self.video_paths) > 5:
                self.video_path_text.insert(tk.END, f"  ... and {len(self.video_paths) - 5} more")
        self.video_path_text.config(state='disabled')
        
    def _process(self):
        fetcher = EpisodeImageFetcher()
        season_number = int(self.season_number_entry.get())
        episode_images, images_temp_dir = fetcher.fetch_season_images(self.show_id, 
                                                                      season_number)
        results = process_videos(self.video_paths, self.show_id, 
                                 season_number, episode_images)
        self.recognition_listbox.config(state='normal')
        self.recognition_listbox.delete(0, tk.END)
        for video_path, result in results:  # unpack tuple
            old_filename = os.path.basename(video_path)
            name, ext = os.path.splitext(old_filename)
            new_filename = f"S{season_number}E{result['episode_number']}{ext}"  
            rename_file(
                video_path,  
                season_number,
                result['episode_number'],
                result['episode_name'],
                style='db'
            )
            self.recognition_listbox.insert(tk.END, f"Renamed {old_filename} to {new_filename}")
        fetcher.cleanup_temp_files(images_temp_dir)
        

    def run(self):
        # Start GUI
        self.window.mainloop()