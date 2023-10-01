import os
import tkinter as tk
from tkinter import filedialog

# Function to find and copy data from files with specific extensions
def copy_bank_paths(folder_path, output_file):
    supported_extensions = ['.sii', '.sui', '.soundref']
    bank_paths = set()  # Use a set to store unique bank paths

    # Iterate through files in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_name, file_extension = os.path.splitext(file)
            if file_extension in supported_extensions:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            if ".bank" in line:
                                # Extract the bank path and add it to the set
                                line = line.strip()
                                start_index = line.find("/sound/")
                                end_index = line.find(".bank")
                                if start_index != -1 and end_index != -1:
                                    bank_path = line[start_index:end_index + 5]
                                    bank_paths.add(bank_path)
                                    # Add the corresponding .bank.guids path
                                    bank_guids_path = bank_path + ".guids"
                                    bank_paths.add(bank_guids_path)
                except Exception as e:
                    print(f"Error reading {file_path}: {str(e)}")

    # Get the directory of the script
    script_directory = os.path.dirname(__file__)

    # Combine the script directory with the output file name
    output_file_path = os.path.join(script_directory, output_file)

    # Write the collected bank paths to List.txt
    with open(output_file_path, 'w', encoding='utf-8') as output:
        for bank_path in bank_paths:
            output.write(bank_path + "\n")

    print(f"{len(bank_paths)} bank paths copied to {output_file_path}")

def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(0, folder_path)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Bank Path Copy Program")

    folder_label = tk.Label(root, text="Select a folder:")
    folder_label.pack()

    folder_path_entry = tk.Entry(root)
    folder_path_entry.pack()

    browse_button = tk.Button(root, text="Browse", command=browse_folder)
    browse_button.pack()

    copy_button = tk.Button(root, text="Copy Bank Paths", command=lambda: copy_bank_paths(folder_path_entry.get(), "List.txt"))
    copy_button.pack()

    root.mainloop()
