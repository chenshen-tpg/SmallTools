import tkinter as tk
import pyautogui
import threading
import time

def main():

    #Main method
    root = tk.Tk()
    root.title("Clicker")


    #Main Window
    window_width = 600
    window_height = 110
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



    #Main lock
    count_lock = threading.Lock()
    action_lock = threading.Lock()

    #Main objects
    history_list = []
    history_window = [None]
    history_listbox = [None]
    moving_window = [None]
    scrolling_window = [None]
    clicking_window = [None]
    running = [False]


############### The saperate window
    def show_clicking_window():
        if clicking_window[0] and tk.Toplevel.winfo_exists(clicking_window[0]):
            clicking_window[0].deiconify()
            clicking_window[0].lift()
            update_clicking_position()
            return
        win = tk.Toplevel(root)
        win.title("Clicking Window")
        win.geometry("200x100")
        win.resizable(False, False)
        tk.Label(win, text="Clicking in progress...").pack(pady=5)
        tk.Button(win, text="Click", command=start_ClickingActions).pack(pady=10)

        def on_close():
            win.after(2000, win.withdraw)

        win.protocol("WM_DELETE_WINDOW", on_close)
        clicking_window[0] = win
        win.transient(root)
        win.attributes("-topmost", True)
        update_clicking_position()
        root.bind("<Configure>", update_clicking_position)

    def show_moving_window():
        if moving_window[0] and tk.Toplevel.winfo_exists(moving_window[0]):
            moving_window[0].deiconify()
            moving_window[0].lift()
            update_moving_position()
            return
        win = tk.Toplevel(root)
        win.title("Moving Window")
        win.geometry("200x100")
        win.resizable(False, False)
        tk.Label(win, text="Moving in progress...").pack(pady=5)
        tk.Button(win, text="Move", command=start_MovingActions).pack(pady=10)

        def on_close():
            win.after(2000, win.withdraw)

        win.protocol("WM_DELETE_WINDOW", on_close)
        moving_window[0] = win
        win.transient(root)
        win.attributes("-topmost", True)
        update_moving_position()
        root.bind("<Configure>", update_moving_position)

    def show_scrolling_window():
        if scrolling_window[0] and tk.Toplevel.winfo_exists(scrolling_window[0]):
            scrolling_window[0].deiconify()
            scrolling_window[0].lift()
            update_scrolling_position()
            return
        win = tk.Toplevel(root)
        win.title("Scrolling Window")
        win.geometry("200x100")
        win.resizable(False, False)
        tk.Label(win, text="Moving in progress...").pack(pady=5)
        tk.Button(win, text="Scroll", command=start_ScrollingActions).pack(pady=10)

        def on_close():
            win.after(2000, win.withdraw)

        win.protocol("WM_DELETE_WINDOW", on_close)
        scrolling_window[0] = win
        win.transient(root)
        win.attributes("-topmost", True)
        update_scrolling_position()
        root.bind("<Configure>", update_scrolling_position)
#############

    def update_clicking_position(event=None):
        if clicking_window[0] and tk.Toplevel.winfo_exists(clicking_window[0]):
            btn = click_btn
            btn_x = btn.winfo_rootx()
            btn_y = btn.winfo_rooty()
            btn_h = btn.winfo_height()
            clicking_window[0].geometry(f"+{btn_x}+{btn_y + btn_h + 50}")

    def update_scrolling_position(event=None):
        if scrolling_window[0] and tk.Toplevel.winfo_exists(scrolling_window[0]):
            root_x = root.winfo_x()
            root_y = root.winfo_y()
            root_w = root.winfo_width()
            # Attach to the right of the main window
            scrolling_window[0].geometry(f"+{root_x}+{root_y - 150}")

    def update_moving_position(event=None):
        if moving_window[0] and tk.Toplevel.winfo_exists(moving_window[0]):
            root_x = root.winfo_x()
            root_y = root.winfo_y()
            root_w = root.winfo_width()
            # Attach to the bottom of the main window
            moving_window[0].geometry(f"+{root_x - 210}+{root_y}")

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
                win.after(2000, win.withdraw)

            win.protocol("WM_DELETE_WINDOW", on_close)
            history_window[0] = win
            history_listbox[0] = listbox
            update_history_position()
            win.transient(root)
            win.attributes("-topmost", True)
            root.bind("<Configure>", update_history_position)

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

    def click_loop(count):
        with action_lock:
            for i in range(count):
                if not running[0]:
                    break
                pyautogui.click()
                with count_lock:
                    count_label.config(text=f"Count: {i + 1}")
                time.sleep(5)
            running[0] = False
            status_label.config(text="Status: Idle")
            log_action("Click", count)

    def open_MovingActions():
        if moving_window[0] and tk.Toplevel.winfo_exists(moving_window[0]) and moving_window[0].state() == "normal":
            moving_window[0].withdraw()
        else:
            show_moving_window()

    def open_ScrollingActions():
        if scrolling_window[0] and tk.Toplevel.winfo_exists(scrolling_window[0]) and scrolling_window[
            0].state() == "normal":
            scrolling_window[0].withdraw()
        else:
            show_scrolling_window()

    def stop_actions():
        running[0] = False
        count_label.config(text="Count: 0")
        status_label.config(text="Status: Idle")
        for win in [history_window[0], moving_window[0], scrolling_window[0], clicking_window[0]]:
            if win and tk.Toplevel.winfo_exists(win):
                win.withdraw()

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

    def start_ClickingActions():
        if action_lock.locked():
            status_label.config(text="Status: Busy, stop first")
            return
        stop_actions()
        time.sleep(1)
        status_label.config(text="Status: Clicking")
        try:
            count = int(count_var.get())
        except ValueError:
            count = 10
        running[0] = True
        threading.Thread(target=click_loop, args=(count,), daemon=True).start()

    global click_btn
    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)
    tk.Button(button_frame, text="Moving", command=open_MovingActions).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Scrolling", command=open_ScrollingActions).pack(side=tk.LEFT, padx=5)
    click_btn = tk.Button(button_frame, text="Click", command=show_clicking_window)
    click_btn.pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="History", command=show_history).pack(side=tk.LEFT, pady=5)
    tk.Button(button_frame, text="Stop All", command=stop_actions).pack(side=tk.LEFT, pady=5)

    #Power by
    powered_label = tk.Label(root, text="Powered by Chen Shen", font=("Arial", 9), fg="gray")
    powered_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
    root.protocol("WM_DELETE_WINDOW", lambda: (stop_actions(), root.destroy()))
    root.mainloop()

if __name__ == "__main__":
    main()