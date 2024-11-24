import tkinter as tk
from tkinter import messagebox
from pynput.keyboard import Controller as KeyboardController, KeyCode, Listener as KeyboardListener
from pynput.mouse import Button, Controller as MouseController, Listener as MouseListener
import threading
import time
import sys

class AutoClicker:
    def __init__(self):
        self.running = False
        self.recorded_input = None  # 用於紀錄按鍵或滑鼠按鍵
        self.interval = 1.0
        self.keyboard = KeyboardController()
        self.mouse = MouseController()

        # 建立視窗
        self.window = tk.Tk()
        self.window.title("自動連點器")
        self.window.protocol("WM_DELETE_WINDOW", self.force_stop)

        # 設置監聽器
        self.kb_listener = KeyboardListener(on_press=self.on_key_press)
        self.mouse_listener = MouseListener(on_click=self.on_mouse_click)
        self.kb_listener.start()
        self.mouse_listener.start()

        # UI 初始化
        self.create_widgets()
        self.window.mainloop()

    def create_widgets(self):
        # 顯示錄製的按鍵或滑鼠按鍵
        tk.Label(self.window, text="錄製的按鍵或滑鼠按鍵：").grid(row=0, column=0, padx=10, pady=5)
        self.recorded_label = tk.Label(self.window, text="尚未錄製")
        self.recorded_label.grid(row=0, column=1, padx=10, pady=5)

        # 間隔時間輸入
        tk.Label(self.window, text="間隔時間 (秒)：").grid(row=1, column=0, padx=10, pady=5)
        self.interval_entry = tk.Entry(self.window)
        self.interval_entry.grid(row=1, column=1, padx=10, pady=5)

        # 按鍵錄製按鈕
        self.record_button = tk.Button(self.window, text="開始錄製", command=self.start_recording)
        self.record_button.grid(row=2, column=0, padx=10, pady=10)

        # 開始與停止按鈕
        self.start_button = tk.Button(self.window, text="開始", command=self.start_clicking)
        self.start_button.grid(row=3, column=0, padx=10, pady=10)

        self.stop_button = tk.Button(self.window, text="停止", command=self.stop_clicking)
        self.stop_button.grid(row=3, column=1, padx=10, pady=10)

    def start_recording(self):
        self.recorded_input = None
        self.recorded_label.config(text="請按下鍵盤或點擊滑鼠按鍵...")

    def on_key_press(self, key):
        if self.recorded_input is None:
            try:
                if isinstance(key, KeyCode):
                    self.recorded_input = key
                    self.recorded_label.config(text=f"錄製的鍵盤按鍵：{key.char}")
                else:
                    self.recorded_input = key
                    self.recorded_label.config(text=f"錄製的鍵盤按鍵：{str(key)}")
            except Exception as e:
                messagebox.showerror("錯誤", f"錄製鍵盤按鍵時發生錯誤：{e}")

    def on_mouse_click(self, x, y, button, pressed):
        if self.recorded_input is None and pressed:
            self.recorded_input = button
            self.recorded_label.config(text=f"錄製的滑鼠按鍵：{str(button)}")

    def start_clicking(self):
        if not self.running and self.recorded_input:
            try:
                self.interval = float(self.interval_entry.get())
                self.running = True
                threading.Thread(target=self.clicking).start()
            except ValueError:
                messagebox.showerror("錯誤", "請輸入有效的間隔時間（數字）。")
        else:
            messagebox.showwarning("警告", "請先錄製按鍵或滑鼠按鍵並設置間隔時間。")

    def clicking(self):
        while self.running:
            if isinstance(self.recorded_input, KeyCode):
                self.keyboard.press(self.recorded_input)
                self.keyboard.release(self.recorded_input)
            elif isinstance(self.recorded_input, Button):
                self.mouse.click(self.recorded_input)
            time.sleep(self.interval)

    def stop_clicking(self):
        self.running = False

    def force_stop(self):
        self.running = False
        self.kb_listener.stop()
        self.mouse_listener.stop()
        self.window.destroy()
        sys.exit(0)  # 強制結束程式

if __name__ == "__main__":
    try:
        AutoClicker()
    except KeyboardInterrupt:
        print("已使用 Ctrl+C 強制停止。")
        sys.exit(0)
