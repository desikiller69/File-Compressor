import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import zipfile
import os
from tkinter import filedialog, messagebox

def compress_folders(folder_paths, zip_name):
    try:
        with zipfile.ZipFile(zip_name, 'w') as zip_file:
            for folder_path in folder_paths:
                for folder_root, _, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(folder_root, file)
                        arcname = os.path.relpath(file_path, folder_path)
                        zip_file.write(file_path, arcname=arcname)
        result_label.config(text=f"Compression completed. ZIP file saved as {zip_name}")
    except Exception as e:
        result_label.config(text=f"Error during compression: {str(e)}")

def choose_folders():
    folder_paths = []
    while True:
        folder_path = filedialog.askdirectory()
        if not folder_path:
            break
        folder_paths.append(folder_path)

    if folder_paths:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, ", ".join(folder_paths))

def choose_output_file():
    output_file = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP files", "*.zip")])
    if output_file:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_file)

def on_drop(event):
    folder_paths = event.data
    if all(os.path.isdir(path) for path in folder_paths):
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, ", ".join(folder_paths))
    else:
        result_label.config(text="Error: Please drop valid folders.")

def compress():
    folder_paths = [os.path.abspath(path) for path in folder_entry.get().split(", ")]
    output_zip_file = os.path.abspath(output_entry.get())

    if not folder_paths:
        result_label.config(text="Error: Please select at least one folder.")
        return

    if os.path.exists(output_zip_file):
        overwrite = messagebox.askyesno("File Exists", "The output ZIP file already exists. Do you want to overwrite it?")
        if not overwrite:
            result_label.config(text="Operation canceled. Choose a different output file name.")
            return

    compress_folders(folder_paths, output_zip_file)

# GUI setup
root = TkinterDnD.Tk()
root.title("Folder Compressor")

folder_label = tk.Label(root, text="Select Folders:")
folder_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

folder_entry = tk.Entry(root, width=60)
folder_entry.grid(row=0, column=1, padx=10, pady=5, columnspan=2)

folder_button = tk.Button(root, text="Browse", command=choose_folders)
folder_button.grid(row=0, column=3, pady=5)

output_label = tk.Label(root, text="Output ZIP File:")
output_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

output_entry = tk.Entry(root, width=60)
output_entry.grid(row=1, column=1, padx=10, pady=5, columnspan=2)

output_button = tk.Button(root, text="Browse", command=choose_output_file)
output_button.grid(row=1, column=3, pady=5)

drag_label = tk.Label(root, text="Drag and drop folders here:")
drag_label.grid(row=4, column=0, columnspan=3, pady=5)
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

result_label = tk.Label(root, text="")
result_label.grid(row=3, column=0, columnspan=3)

compress_button = tk.Button(root, text="Compress", command=compress)
compress_button.grid(row=2, column=0, pady=10, columnspan=3)

root.mainloop()
