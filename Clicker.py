import tkinter as tk
import pyautogui
import threading
import time

def main():
    root = tk.Tk()
    root.title("Clicker")
    window_width = 450
    window_height = 150
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    count_var = tk.StringVar(value="9999")
    count_frame = tk.Frame(root)
    count_frame.pack(pady=5)
    tk.Label(count_frame, text="All counts:").pack(side=tk.LEFT)
    count_entry = tk.Entry(count_frame, textvariable=count_var, width=8)
    count_entry.pack(side=tk.LEFT, padx=2)
    count_label = tk.Label(count_frame, text="Current count: 0")
    count_label.pack(side=tk.LEFT, padx=5)
    status_label = tk.Label(count_frame, text="Status: Idle")
    status_label.pack(side=tk.LEFT, padx=20)

    history_list = []
    history_window = [None]
    history_listbox = [None]

    def update_history_position(event=None):
        if history_window[0] and tk.Toplevel.winfo_exists(history_window[0]):
            root_x = root.winfo_x()
            root_y = root.winfo_y()
            root_w = root.winfo_width()
            history_window[0].geometry(f"+{root_x + root_w + 10}+{root_y}")

    def show_history():
        if history_window[0] and tk.Toplevel.winfo_exists(history_window[0]) and history_window[0].state() == "normal":
            history_window[0].withdraw()
        else:
            if history_window[0] is not None and tk.Toplevel.winfo_exists(history_window[0]):
                history_window[0].deiconify()
                history_window[0].lift()
                update_history_position()
                return
            win = tk.Toplevel(root)
            win.title("Action History")
            win.geometry("200x200")
            win.resizable(False, False)
            tk.Label(win, text="Action History:").pack(anchor="w")
            listbox = tk.Listbox(win, height=10)
            listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            for item in history_list:
                listbox.insert(tk.END, item)

            def on_close():
                win.withdraw()

            win.protocol("WM_DELETE_WINDOW", on_close)
            history_window[0] = win
            history_listbox[0] = listbox
            update_history_position()
            win.transient(root)
            win.attributes("-topmost", True)
            root.bind("<Configure>", update_history_position)

        # Change the button creation to:


    def toggle_history(event=None):
        if history_window[0] and tk.Toplevel.winfo_exists(history_window[0]) and history_window[0].state() == "normal":
            history_window[0].withdraw()
        else:
            show_history()

    running = [False]
    count_lock = threading.Lock()
    action_lock = threading.Lock()

    def log_action(action, count):
        timestamp = time.strftime("%H:%M:%S")
        entry = f"[{timestamp}] {action} x{count}"
        history_list.insert(0, entry)
        if len(history_list) > 20:
            history_list.pop()
        if history_listbox[0] and tk.Toplevel.winfo_exists(history_window[0]):
            history_listbox[0].delete(0, tk.END)
            for item in history_list:
                history_listbox[0].insert(tk.END, item)

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
            log_action("Move", count)

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
            log_action("Scroll", count)

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
    tk.Button(button_frame, text="Show History", command=show_history).pack(side=tk.LEFT, pady=5)
    powered_label = tk.Label(root, text="Powered by Chen Shen", font=("Arial", 9), fg="gray")
    powered_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
    root.protocol("WM_DELETE_WINDOW", lambda: (stop_actions(), root.destroy()))
    root.mainloop()

if __name__ == "__main__":
    main()