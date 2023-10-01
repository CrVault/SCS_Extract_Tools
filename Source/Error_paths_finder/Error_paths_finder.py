import os
import tkinter as tk
from tkinter import filedialog

# Function to find and copy file paths from game.log.txt
def copy_error_paths(log_file_path, output_file):
    error_paths = set()  # Use a set to store unique error paths

    # Check if the log file exists
    if not os.path.exists(log_file_path):
        print(f"Log file '{log_file_path}' does not exist.")
        return

    try:
        with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as log_file:
            for line in log_file:
                if "Failed to open file" in line:
                    # Extract the file path between single quotes and add it to the set
                    start_index = line.find("'")
                    end_index = line.rfind("'")
                    if start_index != -1 and end_index != -1:
                        error_path = line[start_index + 1:end_index]
                        error_paths.add(error_path)
    except Exception as e:
        print(f"Error reading {log_file_path}: {str(e)}")

    # Get the directory of the script
    script_directory = os.path.dirname(__file__)

    # Combine the script directory with the output file name
    output_file_path = os.path.join(script_directory, output_file)

    # Write the collected error paths to List.txt
    with open(output_file_path, 'w', encoding='utf-8') as output:
        for error_path in error_paths:
            output.write(error_path + "\n")

    print(f"{len(error_paths)} error paths copied to {output_file_path}")

def browse_log_file():
    log_file_path = filedialog.askopenfilename(filetypes=[("Log files", "*.log.txt")])
    log_file_path_entry.delete(0, tk.END)
    log_file_path_entry.insert(0, log_file_path)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Error Path Copy Program")

    log_file_label = tk.Label(root, text="Select the game.log file:")
    log_file_label.pack()

    log_file_path_entry = tk.Entry(root)
    log_file_path_entry.pack()

    browse_button = tk.Button(root, text="Browse", command=browse_log_file)
    browse_button.pack()

    copy_button = tk.Button(root, text="Copy Error Paths", command=lambda: copy_error_paths(log_file_path_entry.get(), "List.txt"))
    copy_button.pack()

    root.mainloop()
