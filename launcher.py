import tkinter as tk
from tkinter import filedialog, PhotoImage, messagebox
import subprocess
import os
import sys
import json
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = "config.json"
DEFAULT_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "mc console")

#subfunctions or wtv their called

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return {"game_dir": DEFAULT_DIR, "dark_mode": True}

def save_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
def launch_game():
    game_dir = config["game_dir"]
    exe_path = os.path.join(game_dir, "Minecraft.Client.exe")
    if os.path.exists(exe_path):
        save_username()
        subprocess.Popen([exe_path], cwd=game_dir)
        status_label.config(text="Opening Game...")
        root.after(3000, lambda: status_label.config(text=""))
    else:
        status_label.config(text="Game Not Found! Check The Set File Path.")

def save_username():
    name = username_entry.get().strip()
    if name:
        username_file = os.path.join(config["game_dir"], "username.txt")
        with open(username_file, "w") as f:
            f.write(name)

def browse():
    folder = filedialog.askdirectory()
    if folder:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder)
        config["game_dir"] = folder
        save_config()
        status_label.config(text="Path saved!")

def on_path_change(event):
    config["game_dir"] = path_entry.get()
    save_config()

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    config["dark_mode"] = dark_mode
    save_config()
    if dark_mode:
        bg, fg, entry_bg = "#1e1e1e", "#ffffff", "#2d2d2d"
    else:
        bg, fg, entry_bg = "#f0f0f0", "#000000", "#ffffff"
    root.configure(bg=bg)
    username_label.configure(bg=bg, fg=fg)
    game_label.configure(bg=bg, fg=fg)
    game_hint_label.configure(bg=bg, fg=fg)
    status_label.configure(bg=bg, fg=fg)
    path_frame.configure(bg=bg)
    username_entry.configure(bg=entry_bg, fg=fg)
    path_entry.configure(bg=entry_bg, fg=fg)
    launch_btn.configure(bg=bg, fg=fg)
    browse_btn.configure(bg=bg, fg=fg)
    theme_btn.configure(bg=bg, fg=fg)
def show_about():
    tk.messagebox.showinfo("About", "LEMS Launcher v1.0\nMade by WafflzOwO\nGithub:https://github.com/WafflzOwO")

#=not functions lmao

config = load_config()
dark_mode = not config.get("dark_mode", True)

root = tk.Tk()
icon = PhotoImage(file=os.path.join(BASE_DIR, "assets", "icon.png"))
root.iconphoto(True, icon)
root.title("LEMS Launcher For Minecraft Legacy")
root.geometry("500x300")
root.resizable(False, False)

menubar = tk.Menu(root)
settings_menu = tk.Menu(menubar, tearoff=0)
settings_menu.add_command(label="Toggle Theme", command=toggle_theme)
settings_menu.add_separator()
menubar.add_cascade(label="Settings", menu=settings_menu)
menubar.add_command(label="About", command=show_about)
root.config(menu=menubar)

username_label = tk.Label(root, text="Username:")
username_label.pack(pady=(20, 2))

username_entry = tk.Entry(root, width=35)
username_entry.pack()

saved_username_file = os.path.join(config["game_dir"], "username.txt")
if os.path.exists(saved_username_file):
    with open(saved_username_file, "r") as f:
        username_entry.insert(0, f.read().strip())

game_label = tk.Label(root, text="Game folder:")
game_label.pack(pady=(15, 2))

path_frame = tk.Frame(root)
path_frame.pack()

path_entry = tk.Entry(path_frame, width=35)
path_entry.insert(0, config["game_dir"])
path_entry.pack(side=tk.LEFT)
path_entry.bind("<FocusOut>", on_path_change)

browse_btn = tk.Button(path_frame, text="Browse", command=browse)
browse_btn.pack(side=tk.LEFT, padx=5)

game_hint_label = tk.Label(root, text="^^(Directory Containing The Minecraft Files)^^\n\
Not Sure What This Means?: https://github.com/WafflzOwO")
game_hint_label.pack(pady=(5, 2))

launch_btn = tk.Button(root, text="▶  Play", command=launch_game, width=6, height=1)
launch_btn.pack(pady=10)

theme_btn = tk.Button(root, text="Toggle Theme☀/⭐", command=toggle_theme)
theme_btn.pack(pady=5)

status_label = tk.Label(root, text="")
status_label.pack()

toggle_theme()

root.mainloop()
