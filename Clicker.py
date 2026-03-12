import tkinter as tk
import pyautogui
import threading
import time
import os

def main():
    root = tk.Tk()
    root.title("Clicker")

    window_width = 380
    window_height = 110
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    count_var = tk.StringVar(value="9999")
    status_var = tk.StringVar(value="Status: Idle")
    remaining_var = tk.StringVar(value="")

    # Status label sits directly above buttons
    status_frame = tk.Frame(root)
    status_frame.pack(pady=(6, 0))
    tk.Label(status_frame, textvariable=status_var).pack(side=tk.LEFT, padx=(0, 10))
    tk.Label(status_frame, textvariable=remaining_var).pack(side=tk.LEFT)

    count_lock = threading.Lock()
    action_lock = threading.Lock()

    history_list = []
    history_window = [None]
    history_listbox = [None]
    moving_window = [None]
    scrolling_window = [None]
    clicking_window = [None]
    running = [False]

    # Per-action sleep interval vars (seconds)
    move_sleep_var = tk.StringVar(value="5")
    scroll_sleep_var = tk.StringVar(value="5")
    click_sleep_var = tk.StringVar(value="5")

    def _make_count_row(win, sleep_var):
        """Add 'All counts' + sleep into a popup window."""
        count_frame = tk.Frame(win)
        count_frame.pack(pady=(4, 0))
        tk.Label(count_frame, text="All counts:").pack(side=tk.LEFT)
        tk.Entry(count_frame, textvariable=count_var, width=7).pack(side=tk.LEFT, padx=2)
        tk.Label(count_frame, text="Sleep (s):").pack(side=tk.LEFT, padx=(6, 0))
        tk.Entry(count_frame, textvariable=sleep_var, width=5).pack(side=tk.LEFT, padx=2)

        def on_count_change(*args):
            remaining_var.set("")
        count_var.trace_add("write", on_count_change)

    def show_clicking_window():
        if clicking_window[0] and tk.Toplevel.winfo_exists(clicking_window[0]):
            clicking_window[0].deiconify()
            clicking_window[0].lift()
            update_clicking_position()
            return
        win = tk.Toplevel(root)
        win.title("Clicking")
        win.geometry("310x110")
        win.resizable(False, False)
        _make_count_row(win, click_sleep_var)
        tk.Button(win, text="Click", command=start_ClickingActions).pack(pady=6)
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
        win.title("Moving")
        win.geometry("310x110")
        win.resizable(False, False)
        _make_count_row(win, move_sleep_var)
        tk.Button(win, text="Move", command=start_MovingActions).pack(pady=6)
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
        win.title("Scrolling")
        win.geometry("310x110")
        win.resizable(False, False)
        _make_count_row(win, scroll_sleep_var)
        tk.Button(win, text="Scroll", command=start_ScrollingActions).pack(pady=6)
        def on_close():
            win.after(2000, win.withdraw)
        win.protocol("WM_DELETE_WINDOW", on_close)
        scrolling_window[0] = win
        win.transient(root)
        win.attributes("-topmost", True)
        update_scrolling_position()
        root.bind("<Configure>", update_scrolling_position)

    def update_clicking_position(event=None):
        if clicking_window[0] and tk.Toplevel.winfo_exists(clicking_window[0]):
            btn = action_btn
            btn_x = btn.winfo_rootx()
            btn_y = btn.winfo_rooty()
            btn_h = btn.winfo_height()
            clicking_window[0].geometry(f"+{btn_x}+{btn_y + btn_h + 10}")

    def update_scrolling_position(event=None):
        if scrolling_window[0] and tk.Toplevel.winfo_exists(scrolling_window[0]):
            root_x = root.winfo_x()
            root_y = root.winfo_y()
            scrolling_window[0].geometry(f"+{root_x}+{root_y - 150}")

    def update_moving_position(event=None):
        if moving_window[0] and tk.Toplevel.winfo_exists(moving_window[0]):
            root_x = root.winfo_x()
            root_y = root.winfo_y()
            moving_window[0].geometry(f"+{root_x - 320}+{root_y}")

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

    def move_loop(count, sleep_s):
        with action_lock:
            for i in range(count):
                if not running[0]:
                    break
                pyautogui.moveRel(-50, 0)
                pyautogui.moveRel(50, 0)
                remaining = count - i - 1
                with count_lock:
                    remaining_var.set(f"Remaining: {remaining}")
                time.sleep(sleep_s)
            running[0] = False
            status_var.set("Status: Idle")
            remaining_var.set("")
            log_action("Move", count)

    def scroll_loop(count, sleep_s):
        with action_lock:
            for i in range(count):
                if not running[0]:
                    break
                pyautogui.scroll(50)
                pyautogui.scroll(-50)
                remaining = count - i - 1
                with count_lock:
                    remaining_var.set(f"Remaining: {remaining}")
                time.sleep(sleep_s)
            running[0] = False
            status_var.set("Status: Idle")
            remaining_var.set("")
            log_action("Scroll", count)

    def click_loop(count, sleep_s):
        with action_lock:
            for i in range(count):
                if not running[0]:
                    break
                pyautogui.click()
                remaining = count - i - 1
                with count_lock:
                    remaining_var.set(f"Remaining: {remaining}")
                time.sleep(sleep_s)
            running[0] = False
            status_var.set("Status: Idle")
            remaining_var.set("")
            log_action("Click", count)

    def open_MovingActions():
        if moving_window[0] and tk.Toplevel.winfo_exists(moving_window[0]) and moving_window[0].state() == "normal":
            moving_window[0].withdraw()
        else:
            show_moving_window()

    def open_ScrollingActions():
        if scrolling_window[0] and tk.Toplevel.winfo_exists(scrolling_window[0]) and scrolling_window[0].state() == "normal":
            scrolling_window[0].withdraw()
        else:
            show_scrolling_window()

    def stop_actions():
        running[0] = False
        remaining_var.set("")
        status_var.set("Status: Idle")
        for win in [history_window[0], moving_window[0], scrolling_window[0], clicking_window[0]]:
            if win and tk.Toplevel.winfo_exists(win):
                win.withdraw()

    def start_MovingActions():
        if action_lock.locked():
            status_var.set("Status: Busy, stop first")
            return
        stop_actions()
        time.sleep(0.1)
        status_var.set("Status: Moving")
        try:
            count = int(count_var.get())
        except ValueError:
            count = 10
        try:
            sleep_s = float(move_sleep_var.get())
        except ValueError:
            sleep_s = 5.0
        running[0] = True
        threading.Thread(target=move_loop, args=(count, sleep_s), daemon=True).start()

    def start_ScrollingActions():
        if action_lock.locked():
            status_var.set("Status: Busy, stop first")
            return
        stop_actions()
        time.sleep(0.1)
        status_var.set("Status: Scrolling")
        try:
            count = int(count_var.get())
        except ValueError:
            count = 10
        try:
            sleep_s = float(scroll_sleep_var.get())
        except ValueError:
            sleep_s = 5.0
        running[0] = True
        threading.Thread(target=scroll_loop, args=(count, sleep_s), daemon=True).start()

    def start_ClickingActions():
        if action_lock.locked():
            status_var.set("Status: Busy, stop first")
            return
        stop_actions()
        time.sleep(1)
        status_var.set("Status: Clicking")
        try:
            count = int(count_var.get())
        except ValueError:
            count = 10
        try:
            sleep_s = float(click_sleep_var.get())
        except ValueError:
            sleep_s = 5.0
        running[0] = True
        threading.Thread(target=click_loop, args=(count, sleep_s), daemon=True).start()

    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)

    def show_action_menu(event):
        action_menu.tk_popup(event.x_root, event.y_root)

    action_menu = tk.Menu(button_frame, tearoff=0)
    action_menu.add_command(label="Moving", command=open_MovingActions)
    action_menu.add_command(label="Scrolling", command=open_ScrollingActions)
    action_menu.add_command(label="Clicking", command=show_clicking_window)

    action_btn = tk.Button(button_frame, text="Action")
    action_btn.pack(side=tk.LEFT, padx=5)
    action_btn.bind("<Button-1>", show_action_menu)

    def show_port_menu(event):
        port_menu.tk_popup(event.x_root, event.y_root)

    def switch_port(port):
        os.system(f"dispsel switch {port}")

    port_menu = tk.Menu(button_frame, tearoff=0)
    port_menu.add_command(label="HDMI1", command=lambda: switch_port("hdmi1"))
    port_menu.add_command(label="HDMI2", command=lambda: switch_port("hdmi2"))
    port_menu.add_command(label="DP", command=lambda: switch_port("dp"))

    port_btn = tk.Button(button_frame, text="Port Switch")
    port_btn.pack(side=tk.LEFT, padx=5)
    port_btn.bind("<Button-1>", show_port_menu)

    tk.Button(button_frame, text="History", command=show_history).pack(side=tk.LEFT, pady=5)
    tk.Button(button_frame, text="Stop All", command=stop_actions).pack(side=tk.LEFT, pady=5)

    powered_label = tk.Label(root, text="Powered by Chen Shen", font=("Arial", 9), fg="gray")
    powered_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
    root.protocol("WM_DELETE_WINDOW", lambda: (stop_actions(), root.destroy()))
    root.mainloop()

if __name__ == "__main__":
    main()