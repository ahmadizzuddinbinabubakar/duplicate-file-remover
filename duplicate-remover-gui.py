import tkinter as tk
from tkinter import filedialog
import os
import tkinter.ttk as ttk
import hashlib

#todo; complete find_duplicate_files
#todo: put duplicates into tree view
#todo: complete remove_duplicate_files
#todo: set default window size
   
# select directory
def select_directory():
	folder_path = filedialog.askdirectory()
	if folder_path:
		current_dir.set(folder_path)
# 		list_files(folder_path)
        
def list_files(folder_path):
    for item in tree_view.get_children():
        tree_view.delete(item)
    
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            tree_view.insert("", "end", values=(filename,))
            
def calculate_file_hash(file_path):
    """Calculates the hash value of a file's content."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicate_files(root_folder):
    """Traverses through the root folder and identifies duplicate files."""
    duplicates = {}
    for folder_path, _, file_names in os.walk(root_folder):
        for file_name in file_names:
            file_path = os.path.join(folder_path, file_name)
            file_hash = calculate_file_hash(file_path)
            if file_hash in duplicates:
                duplicates[file_hash].append(file_path)
            else:
                duplicates[file_hash] = [file_path]
    return duplicates

def remove_duplicate_files(duplicates):
    """Removes duplicate files from the file system."""
    count = 0
    for file_paths in duplicates.values():
        if len(file_paths) > 1:
            print(f"Duplicate files found:\n{file_paths}\n")
            for file_path in file_paths[1:]:
                os.remove(file_path)
                count += 1
                print(f"{file_path} has been deleted.\n")
    current_status.set(f"{count} files deleted")
                
def find_remove_duplicate_files(root_folder):
	duplicates = find_duplicate_files(root_folder)
	remove_duplicate_files(duplicates)
	
# new window with a title
window = tk.Tk()
window.title("Duplicate Remover")

current_dir = tk.StringVar()
current_status = tk.StringVar()

browse_button = tk.Button(window, text="Browse Directory", command=select_directory)
browse_button.pack(pady=10)

folder_label = tk.Label(window, textvariable=current_dir)
folder_label.pack()

find_duplicates_button = tk.Button(window, text="Find and remove duplicates", command=lambda: find_remove_duplicate_files(current_dir.get()))
find_duplicates_button.pack(pady=10)

folder_label = tk.Label(window, textvariable=current_status)
folder_label.pack()

# tree_view = ttk.Treeview(window, columns=("Files",), show="headings", selectmode="browse")
# tree_view.heading("Files", text="Files in Directory")
# tree_view.pack(padx=20, pady=20, fill="both", expand=True)

# start the app
window.mainloop()