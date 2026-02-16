import tkinter as tk
import pyautogui
import pygetwindow as gw
import threading
import time

# pyinstaller - -onefile - -windowed

def main():
    root = tk.Tk()
    root.title("Autoclicker")

    window_width = 500
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    window_titles = [title for title in gw.getAllTitles() if title]
    window_var = tk.StringVar(value=window_titles[0] if window_titles else "")
    window_frame = tk.Frame(root)
    window_frame.pack(pady=5)
    tk.Label(window_frame, text="Select Window").pack(side=tk.LEFT)
    window_menu = tk.OptionMenu(window_frame, window_var, *window_titles)
    window_menu.pack(side=tk.LEFT, padx=5)

    timer_var = tk.StringVar(value="9999")
    timer_frame = tk.Frame(root)
    timer_frame.pack(pady=5)
    tk.Label(timer_frame, text="Countdown Seconds").pack(side=tk.LEFT)
    timer_entry = tk.Entry(timer_frame, textvariable=timer_var)
    timer_entry.pack(side=tk.LEFT, padx=5)
    timer_label = tk.Label(timer_frame, text="Timer: 0")
    timer_label.pack(side=tk.LEFT, padx=5)
    running = [False]

    def activate_window():
        win_title = window_var.get()
        if win_title:
            try:
                win = gw.getWindow(win_title)
                if win:
                    win.activate()
            except Exception:
                pass

    def move_loop():
        activate_window()
        while running[0]:
            x, y = pyautogui.position()
            pyautogui.move(-50, 0)
            pyautogui.move(50, 0)
            time.sleep(5)

    def scroll_loop():
        activate_window()
        while running[0]:
            pyautogui.scroll(50)
            pyautogui.scroll(-50)
            time.sleep(5)

    def timer_countdown(seconds):
        for i in range(seconds, 0, -1):
            if not running[0]:
                break
            timer_label.config(text=f"Timer: {i}")
            time.sleep(1)
        timer_label.config(text="Timer: 0")
        if running[0]:
            running[0] = False
            root.destroy()

    def start_MovingActions():
        if running[0]:
            return
        try:
            seconds = int(timer_var.get())
        except ValueError:
            seconds = 10
        running[0] = True
        threading.Thread(target=move_loop, daemon=True).start()
        threading.Thread(target=timer_countdown, args=(seconds,), daemon=True).start()

    def start_ScrollingActions():
        if running[0]:
            return
        try:
            seconds = int(timer_var.get())
        except ValueError:
            seconds = 10
        running[0] = True
        threading.Thread(target=scroll_loop, daemon=True).start()
        threading.Thread(target=timer_countdown, args=(seconds,), daemon=True).start()

    def stop_actions():
        running[0] = False
        timer_label.config(text="Timer: 0")

    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)
    tk.Button(button_frame, text="Start Moving", command=start_MovingActions).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Start Scrolling", command=start_ScrollingActions).pack(side=tk.LEFT, padx=5)
    tk.Button(root, text="Stop", command=stop_actions).pack(pady=5)

    root.protocol("WM_DELETE_WINDOW", lambda: (stop_actions(), root.destroy()))
    root.mainloop()

if __name__ == "__main__":
    main()