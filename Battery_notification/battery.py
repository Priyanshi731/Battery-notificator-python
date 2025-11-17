# pip install psutil
# import psutil

# battery = psutil.sensors_battery()
# plugged = battery.power_plugged
# percent = battery.percent

# if percent <= 30 and plugged!=True:

#     # pip install py-notifier
#     # pip install win10toast
#     from pynotifier import Notification

#     Notification(
#         title="Battery Low",
#         description=str(percent) + "% Battery remain!!",
#         duration=5,  # Duration in seconds

#     ).send()


# import psutil
# from win10toast import ToastNotifier

# battery = psutil.sensors_battery()
# plugged = battery.power_plugged
# percent = battery.percent

# if percent <= 30 and not plugged:
#     toaster = ToastNotifier()
#     toaster.show_toast(
#         "Battery Low ⚠️",
#         f"{percent}% Battery remaining! Please plug in your charger.",
#         duration=10,  # seconds
#     )
# else:
#     print(f"Battery is {percent}% and charging status is {plugged}")
# import psutil
# import tkinter as tk
# from tkinter import messagebox
# from win10toast import ToastNotifier


# # -------------------- Backend Function --------------------
# def check_battery():
#     battery = psutil.sensors_battery()
#     percent = battery.percent
#     plugged = battery.power_plugged

#     # Update label text in GUI
#     status_label.config(text=f"Battery: {percent}% | Plugged In: {plugged}")

#     # If low battery, show notification and popup
#     if percent <= 30 and not plugged:
#         toaster = ToastNotifier()
#         toaster.show_toast(
#             "Battery Low ⚠️",
#             f"{percent}% Battery remaining! Please plug in your charger.",
#             duration=10,
#         )
#         messagebox.showwarning("Battery Alert", f"Battery Low: {percent}%")

#     # Run this check again every 60 seconds (60000 ms)
#     root.after(60000, check_battery)


# # -------------------- Frontend (Tkinter GUI) --------------------
# root = tk.Tk()
# root.title("Battery Notificator")
# root.geometry("400x200")
# root.config(bg="#eaf2f8")

# title_label = tk.Label(
#     root, text="🔋 Battery Notificator", font=("Arial", 16, "bold"), bg="#eaf2f8"
# )
# title_label.pack(pady=10)

# status_label = tk.Label(
#     root, text="Checking battery...", font=("Arial", 12), bg="#eaf2f8"
# )
# status_label.pack(pady=10)

# check_button = tk.Button(
#     root,
#     text="Check Battery Now",
#     command=check_battery,
#     bg="#58d68d",
#     font=("Arial", 12),
# )
# check_button.pack(pady=10)

# # Initial call
# check_battery()

# root.mainloop()
import psutil
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar, Style
from win10toast import ToastNotifier
import threading


# -------------------- Backend Function --------------------
# # -------------------- DEMO MODE --------------------
# demo_mode = True          # True = simulate battery for demo
# simulated_percent = 25    # Battery percentage for demo
# simulated_plugged = False # Charging status for demo
def check_battery():
    battery = psutil.sensors_battery()
    percent = battery.percent
    plugged = battery.power_plugged

    # Update label text in GUI
    status_label.config(text=f"Battery: {percent}% | Plugged In: {plugged}")
    progress["value"] = percent

    # Color logic based on battery level
    if percent <= 30:
        progress_style.configure(
            "green.Horizontal.TProgressbar", foreground="red", background="red"
        )
    elif percent <= 70:
        progress_style.configure(
            "green.Horizontal.TProgressbar", foreground="orange", background="orange"
        )
    else:
        progress_style.configure(
            "green.Horizontal.TProgressbar", foreground="green", background="green"
        )

    # If low battery, show notification
    if percent <= 30 and not plugged:
        toaster = ToastNotifier()
        toaster.show_toast(
            "Battery Low ⚠",
            f"{percent}% Battery remaining! Please plug in your charger.",
            duration=10,
        )
        messagebox.showwarning("Battery Alert", f"Battery Low: {percent}%")

    # Schedule next check
    root.after(60000, lambda: threading.Thread(target=check_battery).start())


# -------------------- GUI Enhancements --------------------
def animate_title():
    current_color = title_label.cget("fg")
    next_color = "#2ecc71" if current_color == "#1f618d" else "#1f618d"
    title_label.config(fg=next_color)
    root.after(700, animate_title)  # repeat animation every 0.7s


def on_hover(event):
    check_button.config(bg="#27ae60", fg="white")


def on_leave(event):
    check_button.config(bg="#58d68d", fg="black")


# -------------------- Frontend (Tkinter GUI) --------------------
root = tk.Tk()
root.title("Battery Notificator ⚡")
root.geometry("420x260")  # initial size
root.resizable(True, True)  # allow resizing
root.state("zoomed")  # start maximized (optional)
root.minsize(420, 260)  # minimum size

# Gradient background effect
canvas = tk.Canvas(root)
canvas.pack(fill="both", expand=True)


def draw_gradient(event=None):
    canvas.delete("all")  # clear previous gradient
    height = canvas.winfo_height()
    width = canvas.winfo_width()
    for i in range(height):
        r = 234 - i // 2
        g = 242 - i // 3
        b = 248
        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(0, i, width, i, fill=color)


# Draw gradient initially and on resize
canvas.bind("<Configure>", draw_gradient)

# Main Frame
frame = tk.Frame(root, bg="#eaf2f8")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Title Label with animation
title_label = tk.Label(
    frame,
    text="🔋 Battery Notificator",
    font=("Helvetica", 18, "bold"),
    fg="#1f618d",
    bg="#eaf2f8",
)
title_label.pack(pady=10)
animate_title()

# Battery Status Label
status_label = tk.Label(
    frame, text="Checking battery...", font=("Arial", 13), bg="#eaf2f8", fg="#424949"
)
status_label.pack(pady=10)

# Battery Progress Bar
progress_style = Style()
progress_style.configure("green.Horizontal.TProgressbar", thickness=20)
progress = Progressbar(frame, style="green.Horizontal.TProgressbar", length=250)
progress.pack(pady=10)

# Button with hover effect
check_button = tk.Button(
    frame,
    text="Check Battery Now",
    command=lambda: threading.Thread(target=check_battery).start(),
    bg="#58d68d",
    font=("Arial", 12, "bold"),
    relief="flat",
    width=18,
    pady=5,
)
check_button.pack(pady=10)
check_button.bind("<Enter>", on_hover)
check_button.bind("<Leave>", on_leave)

# Initial check
threading.Thread(target=check_battery).start()

root.mainloop()
