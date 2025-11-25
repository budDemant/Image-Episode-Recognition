import tkinter as tk

def greet():
    name = entry.get()
    label.config(text=f"Hello, {name}!")

root = tk.Tk()
root.title("Greeting App")

entry = tk.Entry(root)
entry.pack(pady=10)

button = tk.Button(root, text="Greet", command=greet)
button.pack()

label = tk.Label(root, text="")
label.pack(pady=10)

root.mainloop()
