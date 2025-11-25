import tkinter as tk

root = tk.Tk()
root.title("Frame Example")
root.geometry("300x200")

# Create a frame
top_frame = tk.Frame(root, bg="lightgray", padx=10, pady=10)
top_frame.pack(pady=20)

# Add widgets INSIDE the frame
label = tk.Label(top_frame, text="Enter your name:")
label.pack()

entry = tk.Entry(top_frame)
entry.pack(pady=5)

button = tk.Button(top_frame, text="Submit")
button.pack()

root.mainloop()
