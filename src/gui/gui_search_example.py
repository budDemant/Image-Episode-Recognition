import tkinter as tk

def search():
    query = entry.get()
    results = fake_search(query)

    # Clear previous results
    listbox.delete(0, tk.END)

    # Add new results
    for item in results:
        listbox.insert(tk.END, item)

def fake_search(q):
    # Simulated search function
    data = ["apple", "banana", "orange", "grape", "pineapple", "peach"]
    return [x for x in data if q.lower() in x.lower()]

def on_select(event):
    selection = listbox.get(listbox.curselection())
    print("Selected:", selection)

root = tk.Tk()
root.title("Search Example")

# Frame for search bar
top = tk.Frame(root)
top.pack(pady=10)

entry = tk.Entry(top, width=30)
entry.pack(side="left")

button = tk.Button(top, text="Search", command=search)
button.pack(side="left", padx=5)

# Listbox for results
listbox = tk.Listbox(root, width=40, height=8)
listbox.pack(pady=10)

listbox.bind("<<ListboxSelect>>", on_select)

root.mainloop()
