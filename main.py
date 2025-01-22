import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import pyautogui
import time
import threading

class TypingSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Simulator")
        self.root.geometry("800x600")
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Text area
        self.text_label = ttk.Label(main_frame, text="Enter text to type:")
        self.text_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.text_area = scrolledtext.ScrolledText(main_frame, height=20, width=80, wrap=tk.WORD)
        self.text_area.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Parameters frame
        params_frame = ttk.LabelFrame(main_frame, text="Parameters", padding="10")
        params_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Initial delay
        ttk.Label(params_frame, text="Initial delay (seconds):").grid(row=0, column=0, sticky=tk.W)
        self.initial_delay = tk.StringVar(value="5")
        initial_delay_spin = ttk.Spinbox(params_frame, from_=1, to=30, width=10, textvariable=self.initial_delay)
        initial_delay_spin.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # Typing delay
        ttk.Label(params_frame, text="Typing delay (seconds):").grid(row=0, column=2, sticky=tk.W)
        self.typing_delay = tk.StringVar(value="0.1")
        typing_delay_spin = ttk.Spinbox(params_frame, from_=0.01, to=1.0, increment=0.01, width=10, 
                                      textvariable=self.typing_delay)
        typing_delay_spin.grid(row=0, column=3, sticky=tk.W)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Load file button
        self.load_button = ttk.Button(button_frame, text="Load File", command=self.load_file)
        self.load_button.pack(side=tk.LEFT, padx=5)
        
        # Start button
        self.start_button = ttk.Button(button_frame, text="Start Typing", command=self.start_typing)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

    def load_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # Normalize line endings to '\n'
                    content = content.replace('\r\n', '\n').replace('\r', '\n')
                    self.text_area.delete('1.0', tk.END)
                    self.text_area.insert('1.0', content)
            except Exception as e:
                messagebox.showerror("Error", f"Error reading file: {e}")

    def simulate_typing(self, text, delay, initial_delay):
        self.status_var.set(f"Starting in {initial_delay} seconds... Switch to your target window!")
        self.start_button.configure(text="Start Typing", command=self.start_typing)
        self.stop_typing = False
        time.sleep(initial_delay)
        
        # Disable fail-safe temporarily
        pyautogui.FAILSAFE = False
        
        try:
            for char in text:
                if self.stop_typing:
                    break
                if char == '\n':
                    pyautogui.write('\r')  # Simulate carriage return
                    time.sleep(float(delay))
                    pyautogui.write('\n')  # Simulate line feed
                    time.sleep(float(delay))                
                elif char == '\t':
                    pyautogui.press('tab')
                else:
                    pyautogui.write(char)
                time.sleep(float(delay))
            
            if not self.stop_typing:
                self.status_var.set("Typing completed!")
            else:
                self.status_var.set("Typing stopped by user.")
                
        except Exception as e:
            self.status_var.set(f"An error occurred: {e}")
        finally:
            # Re-enable fail-safe
            pyautogui.FAILSAFE = True
           
                       
                
    
    def start_typing(self):
        text = self.text_area.get('1.0', tk.END)
        print("Text to be typed:", repr(text))  # Debugging statement
        if not text.strip():
            messagebox.showwarning("Warning", "Please enter some text to type.")
            return
            
        try:
            delay = float(self.typing_delay.get())
            initial_delay = int(self.initial_delay.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for delays.")
            return
            
        # Normalize line endings to '\n'
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        self.stop_typing = False
        self.start_button.configure(text="Stop Typing", command=self.stop_typing_command)
        
        # Start typing in a separate thread
        self.typing_thread = threading.Thread(
            target=self.simulate_typing,
            args=(text, delay, initial_delay)
        )
        self.typing_thread.daemon = True
        self.typing_thread.start()
        
    def stop_typing_command(self):
        self.stop_typing = True

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSimulatorGUI(root)
    root.mainloop()