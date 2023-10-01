import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto .sii Decrypt")
        self.root.geometry("300x150")
        self.root.resizable(False, False)
        self.running = False
        self.stopped_by_user = False  # Track if process was stopped by the user

        self.center_window()

        self.found_files = []
        self.current_file_idx = 0
        
        self.title_label = ttk.Label(root, text="Auto .sii Decrypt", font=("Arial", 12, "bold"))
        self.title_label.pack(pady=5)
        
        self.subtitle_label = ttk.Label(root, text="(for ATS and ETS 2)")
        self.subtitle_label.pack(pady=5)
        
        self.label = ttk.Label(root, text="")
        
        self.text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
        
        self.progress = ttk.Progressbar(root, orient="horizontal", mode="determinate")

        self.run_button = ttk.Button(root, text="Run", command=self.run_decrypt)
        self.run_button.pack(side="left", padx=10, pady=10)
        
        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_decrypt, state=tk.DISABLED)
        self.stop_button.pack(side="right", padx=10, pady=10)

        self.info_button = ttk.Button(root, text="Info", command=self.show_info)
        self.info_button.place(x=5, y=125)

    def center_window(self):
        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()
        position_x = int(self.root.winfo_screenwidth()/2 - window_width/2)
        position_y = int(self.root.winfo_screenheight()/2 - window_height/2)
        self.root.geometry("+{}+{}".format(position_x, position_y))

    def show_info(self):
        info_window = tk.Toplevel(self.root)
        info_window.title("Information")
        info_window.resizable(False, False)  # Information window shouldn't be resizable

        info_window_width = 250
        info_window_height = 100
        position_x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (info_window_width // 2)
        position_y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (info_window_height // 2)
        info_window.geometry("+{}+{}".format(position_x, position_y))

        label1 = ttk.Label(info_window, text="Script by CracksVault", cursor="hand2", foreground="blue")
        label1.pack(pady=5)
        label1.bind("<Button-1>", lambda e: self.open_website("http://www.anonimods.com"))
        
        label2 = ttk.Label(info_window, text="SII_Decrypt by TheLazyTomcat", cursor="hand2", foreground="blue")
        label2.pack(pady=5)
        label2.bind("<Button-1>", lambda e: self.open_website("https://github.com/TheLazyTomcat/SII_Decrypt"))
        
        info_window.transient(self.root)
        info_window.grab_set()
        info_window.mainloop()

    def run_decrypt(self):
        if not self.running:
            self.running = True
            self.stopped_by_user = False
            self.info_button.place_forget()  # Hide the Info button
            self.run_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            
            self.title_label.pack_forget()
            self.subtitle_label.pack_forget()
            
            self.label.pack(pady=20)
            
            self.find_sii_files()
            
            self.root.geometry("400x350")
            self.center_window()
            self.text_box.pack(padx=10, pady=10)
            self.progress.pack(padx=10, pady=5, fill="x")
            
            self.decrypt_next_file()

    def stop_decrypt(self):
        self.running = False
        self.stopped_by_user = True
        self.run_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.text_box.insert(tk.END, "Stopped by user.\n")
        messagebox.showinfo("Info", "Stopped by user.")

    def find_sii_files(self):
        for dirpath, dirnames, filenames in os.walk("."):
            for file in filenames:
                if file.endswith(".sii"):
                    self.found_files.append(os.path.join(dirpath, file))

    def decrypt_next_file(self):
        if not self.running or self.current_file_idx >= len(self.found_files):
            self.running = False
            self.run_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            if not self.stopped_by_user:
                self.text_box.insert(tk.END, "Complete.\n")
                messagebox.showinfo("Info", "Complete!")  # Displaying a message box
            return

        current_file = self.found_files[self.current_file_idx]
        self.label.config(text=f"Running on file {self.current_file_idx + 1} of {len(self.found_files)} found")
        
        result = subprocess.run(["sii_core/sii_core.exe", "-i", current_file], capture_output=True, text=True)
        
        self.current_file_idx += 1

        self.text_box.configure(state=tk.NORMAL)
        self.text_box.insert(tk.END, f"Decrypting {current_file}...\n{result.stdout}\n")
        self.text_box.configure(state=tk.DISABLED)
        self.text_box.see(tk.END)

        self.progress["value"] = (self.current_file_idx/len(self.found_files))*100

        self.root.after(100, self.decrypt_next_file)

    def open_website(self, url):
        import webbrowser
        webbrowser.open(url)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
