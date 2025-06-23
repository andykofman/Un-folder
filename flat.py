import os
import shutil
import easygui
import tkinter as tk
from tkinter import filedialog, messagebox

def flatten_folders(folder_paths, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for source_folder in folder_paths:
        for root, dirs, files in os.walk(source_folder):
            # Skip __pycache__ and hidden folders
            dirs[:] = [d for d in dirs if d != "__pycache__" and not d.startswith('.')]
            for file in files:
                source_file = os.path.join(root, file)
                destination_file = os.path.join(destination_folder, file)

                # Rename if there's a collision
                base, ext = os.path.splitext(file)
                counter = 1
                while os.path.exists(destination_file):
                    new_name = f"{base}_{counter}{ext}"
                    destination_file = os.path.join(destination_folder, new_name)
                    counter += 1

                shutil.copy2(source_file, destination_file)
                print(f"Copied {source_file} -> {destination_file}")

def select_folders():
    root = tk.Tk()
    root.withdraw()

    folder_paths = []
    while True:
        prompt = "Select a folder to flatten"
        if folder_paths:
            prompt += f"\n(Already selected: {', '.join(folder_paths)})"
        folder = filedialog.askdirectory(title=prompt)
        if not folder:
            break
        if folder not in folder_paths:
            folder_paths.append(folder)
        # Ask if the user wants to select another folder
        more = messagebox.askyesno("Select More?", "Do you want to select another folder?")
        if not more:
            break

    if not folder_paths:
        messagebox.showinfo("Info", "No folders selected.")
        return

    destination_folder = filedialog.askdirectory(title="Select destination folder")
    if not destination_folder:
        messagebox.showinfo("Info", "No destination folder selected.")
        return

    flatten_folders(folder_paths, destination_folder)
    messagebox.showinfo("Done", "All folders have been flattened!")

if __name__ == "__main__":
    select_folders()

