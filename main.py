import os
import rawpy
from PIL import Image
import tkinter as tk
from tkinter import filedialog

def process_cr3(input_path):
    with rawpy.imread(input_path) as raw:
        rgb = raw.postprocess()
    return rgb

def save_as_jpeg(data, output_path):
    image = Image.fromarray(data)
    image.save(output_path, format="JPEG", quality=95)

def process_images_in_directory(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.lower().endswith(".cr3"):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, os.path.splitext(filename)[0] + ".jpg")
            try:
                raw_data = process_cr3(input_path)
                save_as_jpeg(raw_data, output_path)
                print(f"Processed {input_path} and saved as {output_path}")
            except Exception as e:
                print(f"Failed to process {input_path}: {e}")

def select_folder(var):
    folder_path = filedialog.askdirectory()
    var.set(folder_path)

def process_images():
    input_folder = input_folder_var.get()
    output_folder = output_folder_var.get()

    if not os.path.exists(input_folder):
        print(f"Error: The input folder '{input_folder}' does not exist.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    process_images_in_directory(input_folder, output_folder)

# GUI setup
root = tk.Tk()
root.title("CR3 to JPEG Converter")

# Input folder selection
input_frame = tk.Frame(root)
input_frame.pack(pady=10)
input_folder_var = tk.StringVar()
input_folder_label = tk.Label(input_frame, text="Select Input Folder:")
input_folder_label.pack(side=tk.LEFT)
input_folder_entry = tk.Entry(input_frame, textvariable=input_folder_var, width=50)
input_folder_entry.pack(side=tk.LEFT, padx=5)
input_folder_button = tk.Button(input_frame, text="Browse", command=lambda: select_folder(input_folder_var))
input_folder_button.pack(side=tk.LEFT)

# Output folder selection
output_frame = tk.Frame(root)
output_frame.pack(pady=10)
output_folder_var = tk.StringVar()
output_folder_label = tk.Label(output_frame, text="Select Output Folder:")
output_folder_label.pack(side=tk.LEFT)
output_folder_entry = tk.Entry(output_frame, textvariable=output_folder_var, width=50)
output_folder_entry.pack(side=tk.LEFT, padx=5)
output_folder_button = tk.Button(output_frame, text="Browse", command=lambda: select_folder(output_folder_var))
output_folder_button.pack(side=tk.LEFT)

# Convert button
convert_button = tk.Button(root, text="Convert CR3 to JPEG", command=process_images)
convert_button.pack(pady=20)

# Run the GUI event loop
root.mainloop()
