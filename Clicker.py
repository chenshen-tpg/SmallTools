import tkinter as tk
import pyautogui
import threading
import time

def main():
    root = tk.Tk()
    root.title("Clicker")
    window_width = 580
    window_height = 120
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    count_var = tk.StringVar(value="9999")
    count_frame = tk.Frame(root)
    count_frame.pack(pady=5)
    tk.Label(count_frame, text="All count").pack(side=tk.LEFT)
    count_entry = tk.Entry(count_frame, textvariable=count_var, width=8)
    count_entry.pack(side=tk.LEFT, padx=2)
    count_label = tk.Label(count_frame, text="Current count: 0")
    count_label.pack(side=tk.LEFT, padx=5)
    status_label = tk.Label(count_frame, text="Status: Idle")
    status_label.pack(side=tk.LEFT, padx=20)

    running = [False]
    count_lock = threading.Lock()
    action_lock = threading.Lock()

    def move_loop(count):
        with action_lock:
            for i in range(count):
                if not running[0]:
                    break
                pyautogui.moveRel(-50, 0)
                pyautogui.moveRel(50, 0)
                with count_lock:
                    count_label.config(text=f"Count: {i + 1}")
                time.sleep(5)
            running[0] = False
            status_label.config(text="Status: Idle")

    def scroll_loop(count):
        with action_lock:
            for i in range(count):
                if not running[0]:
                    break
                pyautogui.scroll(50)
                pyautogui.scroll(-50)
                with count_lock:
                    count_label.config(text=f"Count: {i + 1}")
                time.sleep(5)
            running[0] = False
            status_label.config(text="Status: Idle")

    def start_MovingActions():
        if action_lock.locked():
            status_label.config(text="Status: Busy, stop first")
            return
        stop_actions()
        time.sleep(0.1)
        status_label.config(text="Status: Moving")
        try:
            count = int(count_var.get())
        except ValueError:
            count = 10
        running[0] = True
        threading.Thread(target=move_loop, args=(count,), daemon=True).start()

    def start_ScrollingActions():
        if action_lock.locked():
            status_label.config(text="Status: Busy, stop first")
            return
        stop_actions()
        time.sleep(0.1)
        status_label.config(text="Status: Scrolling")
        try:
            count = int(count_var.get())
        except ValueError:
            count = 10
        running[0] = True
        threading.Thread(target=scroll_loop, args=(count,), daemon=True).start()

    def stop_actions():
        running[0] = False
        count_label.config(text="Count: 0")
        status_label.config(text="Status: Idle")

    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)
    tk.Button(button_frame, text="Start Moving", command=start_MovingActions).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Start Scrolling", command=start_ScrollingActions).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Stop", command=stop_actions).pack(side=tk.LEFT, pady=5)
    powered_label = tk.Label(root, text="Powered by Chen Shen", font=("Arial", 9), fg="gray")
    powered_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
    root.protocol("WM_DELETE_WINDOW", lambda: (stop_actions(), root.destroy()))
    root.mainloop()
if __name__ == "__main__":
    main()