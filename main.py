import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import pyautogui
import time
import threading
import re
import os
import subprocess

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
        self.typing_delay = tk.StringVar(value="0.01")  # Default to a more reliable speed
        typing_delay_spin = ttk.Spinbox(params_frame, from_=0.001, to=1.0, increment=0.001, width=10, 
                                      textvariable=self.typing_delay)
        typing_delay_spin.grid(row=0, column=3, sticky=tk.W)
        
        # Chunk size (new parameter)
        ttk.Label(params_frame, text="Chunk size:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.chunk_size = tk.StringVar(value="40")  # Smaller default chunk for better reliability
        chunk_size_spin = ttk.Spinbox(params_frame, from_=1, to=100, width=10, textvariable=self.chunk_size)
        chunk_size_spin.grid(row=1, column=1, sticky=tk.W, padx=(0, 20), pady=(10, 0))
        
        # Chunk delay (new parameter)
        ttk.Label(params_frame, text="Chunk delay (seconds):").grid(row=1, column=2, sticky=tk.W, pady=(10, 0))
        self.chunk_delay = tk.StringVar(value="0.02")  # Increased for better reliability
        chunk_delay_spin = ttk.Spinbox(params_frame, from_=0.01, to=1.0, increment=0.01, width=10, 
                                     textvariable=self.chunk_delay)
        chunk_delay_spin.grid(row=1, column=3, sticky=tk.W, pady=(10, 0))
        
        # Special character handling options
        ttk.Label(params_frame, text="Punctuation delay:").grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        self.punct_delay_factor = tk.StringVar(value="1")
        punct_delay_spin = ttk.Spinbox(params_frame, from_=1, to=10, width=10, textvariable=self.punct_delay_factor)
        punct_delay_spin.grid(row=2, column=1, sticky=tk.W, padx=(0, 20), pady=(10, 0))
        
        # Hibernate option
        self.hibernate_var = tk.BooleanVar(value=False)
        hibernate_check = ttk.Checkbutton(params_frame, text="Hibernate when finished", 
                                          variable=self.hibernate_var)
        hibernate_check.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
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

    def hibernate_system(self):
        """Put the system into hibernate mode"""
        try:
            if os.name == 'nt':  # Windows
                subprocess.call("shutdown /h /f", shell=True)
            else:  # Linux/Mac
                subprocess.call("systemctl hibernate", shell=True)
        except Exception as e:
            self.status_var.set(f"Failed to hibernate: {e}")
    
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

    def simulate_typing(self, text, typing_delay, chunk_size, chunk_delay, initial_delay, punct_delay_factor):
        # Count down from initial_delay to 0
        for i in range(initial_delay, 0, -1):
            if self.stop_typing:
                self.status_var.set("Typing stopped by user.")
                return
            self.status_var.set(f"Starting in {i} seconds... Switch to your target window!")
            self.root.update()  # Update the GUI
            time.sleep(1)
        
        if self.stop_typing:
            self.status_var.set("Typing stopped by user.")
            return
            
        self.status_var.set("Starting now... Switch to your target window!")
        self.root.update()
        time.sleep(1)
        
        # Disable fail-safe temporarily
        pyautogui.FAILSAFE = False
        
        try:
            # Start timing
            start_time = time.time()
            
            # Get initial cursor position to maintain typing location
            initial_x, initial_y = pyautogui.position()
            
            # Split text into lines to handle newlines separately
            lines = text.split('\n')
            total_lines = len(lines)
            
            # Calculate total character count for progress tracking
            total_chars = sum(len(line) for line in lines) + (total_lines - 1)  # Add newlines
            chars_typed = 0
            
            for line_index, line in enumerate(lines):
                if self.stop_typing:
                    break
                
                # Update status periodically
                if line_index % 10 == 0:
                    # Calculate time metrics
                    elapsed_time = time.time() - start_time
                    typing_speed = chars_typed / elapsed_time if elapsed_time > 0 else 0  # chars per second
                    chars_per_minute = typing_speed * 60  # chars per minute
                    
                    # Estimate remaining time
                    remaining_chars = total_chars - chars_typed
                    estimated_remaining_time = remaining_chars / typing_speed if typing_speed > 0 else 0
                    
                    # Format times for display
                    elapsed_time_str = self.format_time(elapsed_time)
                    remaining_time_str = self.format_time(estimated_remaining_time)
                    
                    progress = (chars_typed / total_chars) * 100 if total_chars > 0 else 100
                    self.status_var.set(f"Progress: {progress:.1f}% | Time: {elapsed_time_str} | Speed: {chars_per_minute:.1f} CPM | Est. remaining: {remaining_time_str}")
                    self.root.update_idletasks()
                
                # Define punctuation that needs special handling
                special_punct = '.,:;/\\\'"`!?@#$%^&*()[]{}|<>'
                problem_punct = '.,:;/\\'  # These characters often cause more problems
                
                # Process the line in chunks for better performance
                for chunk_start in range(0, len(line), chunk_size):
                    if self.stop_typing:
                        break
                        
                    chunk_end = min(chunk_start + chunk_size, len(line))
                    chunk = line[chunk_start:chunk_end]
                    
                    # Check if the chunk contains any special characters that need special handling
                    has_special_chars = any(c in special_punct or c == '\t' for c in chunk)

                    if not has_special_chars:
                        # No special characters, use faster chunk-based typing
                        pyautogui.write(chunk, interval=typing_delay)
                        chars_typed += len(chunk)
                        
                        # Update status occasionally
                        if chunk_start % 50 == 0:
                            # Calculate time metrics
                            elapsed_time = time.time() - start_time
                            typing_speed = chars_typed / elapsed_time if elapsed_time > 0 else 0  # chars per second
                            chars_per_minute = typing_speed * 60  # chars per minute
                            
                            # Estimate remaining time
                            remaining_chars = total_chars - chars_typed
                            estimated_remaining_time = remaining_chars / typing_speed if typing_speed > 0 else 0
                            
                            # Format times for display
                            elapsed_time_str = self.format_time(elapsed_time)
                            remaining_time_str = self.format_time(estimated_remaining_time)
                            
                            progress = (chars_typed / total_chars) * 100 if total_chars > 0 else 100
                            self.status_var.set(f"Progress: {progress:.1f}% | Time: {elapsed_time_str} | Speed: {chars_per_minute:.1f} CPM | Est. remaining: {remaining_time_str}")
                            self.root.update_idletasks()
                    else:
                        # Process each character in the chunk (for chunks with special characters)
                        for i, char in enumerate(chunk):
                            if self.stop_typing:
                                break
                            
                            # Update status occasionally
                            if (chunk_start + i) % 50 == 0:
                                # Calculate time metrics
                                elapsed_time = time.time() - start_time
                                typing_speed = chars_typed / elapsed_time if elapsed_time > 0 else 0  # chars per second
                                chars_per_minute = typing_speed * 60  # chars per minute
                                
                                # Estimate remaining time
                                remaining_chars = total_chars - chars_typed
                                estimated_remaining_time = remaining_chars / typing_speed if typing_speed > 0 else 0
                                
                                # Format times for display
                                elapsed_time_str = self.format_time(elapsed_time)
                                remaining_time_str = self.format_time(estimated_remaining_time)
                                
                                progress = (chars_typed / total_chars) * 100 if total_chars > 0 else 100
                                self.status_var.set(f"Progress: {progress:.1f}% | Time: {elapsed_time_str} | Speed: {chars_per_minute:.1f} CPM | Est. remaining: {remaining_time_str}")
                                self.root.update_idletasks()
                            
                            # Handle special characters
                            if char == '\t':
                                # Tab requires special handling
                                pyautogui.press('tab')
                                time.sleep(typing_delay * punct_delay_factor)  # Keep extra delay for tab
                            elif char in special_punct:
                                # Handle punctuation with extra care
                                # For problematic punctuation, use individual keypress
                                if char in problem_punct:
                                    pyautogui.press(char)
                                    time.sleep(typing_delay * punct_delay_factor)  # Keep extra delay for problem characters
                                else:
                                    pyautogui.write(char)
                                    time.sleep(typing_delay * (punct_delay_factor - 1))  # Keep less delay for other punctuation
                            else:
                                # Normal character, can be typed directly
                                pyautogui.write(char)
                                time.sleep(typing_delay)  # Minimal delay for normal characters
                            
                            chars_typed += 1  # Increment character count
                            # Check for stop flag more frequently
                            if self.stop_typing:
                                break
                    
                    # Add a delay between chunks (only if not at the end of the line)
                    if chunk_end < len(line) and not self.stop_typing:
                        time.sleep(chunk_delay)
                
                # Handle newline at the end of each line (except the last line)
                if line_index < total_lines - 1 and not self.stop_typing:
                    pyautogui.press('enter')
                    time.sleep(typing_delay * 2)  # Slightly longer delay for enter key
                    chars_typed += 1  # Increment character count for newline
           
            if not self.stop_typing:
                # Final time metrics
                elapsed_time = time.time() - start_time
                typing_speed = chars_typed / elapsed_time if elapsed_time > 0 else 0  # chars per second
                chars_per_minute = typing_speed * 60  # chars per minute
                elapsed_time_str = self.format_time(elapsed_time)
                
                self.status_var.set(f"Typing completed! | Total time: {elapsed_time_str} | Average speed: {chars_per_minute:.1f} CPM")
                
                # Hibernate if enabled
                if self.hibernate_var.get():
                    # Give user a few seconds to see the completion message
                    self.status_var.set(f"Typing completed! Hibernating in 5 seconds...")
                    self.root.update_idletasks()
                    time.sleep(5)
                    self.hibernate_system()
            else:
                self.status_var.set("Typing stopped by user.")
                
        except Exception as e:
            self.status_var.set(f"An error occurred: {e}")
        finally:
            # Re-enable fail-safe
            pyautogui.FAILSAFE = True
            # Reset button state regardless of how we exit
            self.start_button.configure(text="Start Typing", command=self.start_typing)
    
    def format_time(self, seconds):
        """Format seconds into a human-readable time string."""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            remaining_seconds = seconds % 60
            return f"{minutes}m {remaining_seconds:.0f}s"
        else:
            hours = int(seconds // 3600)
            remaining_minutes = int((seconds % 3600) // 60)
            return f"{hours}h {remaining_minutes}m"
    
    def start_typing(self):
        text = self.text_area.get('1.0', tk.END)
        if not text.strip():
            messagebox.showwarning("Warning", "Please enter some text to type.")
            return
            
        try:
            typing_delay = float(self.typing_delay.get())
            chunk_size = int(self.chunk_size.get())
            chunk_delay = float(self.chunk_delay.get())
            initial_delay = int(self.initial_delay.get())
            punct_delay_factor = int(self.punct_delay_factor.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for parameters.")
            return
            
        # Normalize line endings to '\n'
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        self.stop_typing = False
        self.start_button.configure(text="Stop Typing", command=self.stop_typing_command)
        
        # Start typing in a separate thread
        self.typing_thread = threading.Thread(
            target=self.simulate_typing,
            args=(text, typing_delay, chunk_size, chunk_delay, initial_delay, punct_delay_factor)
        )
        self.typing_thread.daemon = True
        self.typing_thread.start()
        
    def stop_typing_command(self):
        self.stop_typing = True
        self.status_var.set("Stopping typing... Please wait.")
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSimulatorGUI(root)
    root.mainloop()