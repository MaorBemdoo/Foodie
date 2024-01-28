import tkinter as tk
import ttkbootstrap as tb
import time

def show_loading_animation():
    loading_window = tb.Toplevel(root)
    loading_window.title("Loading")

    progress_bar = tb.Progressbar(loading_window, mode='indeterminate')
    progress_bar.pack(padx=10, pady=20)

    progress_bar.start()

    time.sleep(3)

    progress_bar.stop()

    loading_window.destroy()

def toHome():
    about.forget()
    home.pack()


def toAbout():
    home.forget()
    about.pack()

root = tb.Window(title="Foodie", themename="superhero", iconphoto="School Apps/Foodie/assets/food.ico")
root.geometry("%dx%d" % (root.winfo_screenwidth(), root.winfo_screenheight()))

home = tb.Frame(root)
about = tb.Frame(root)

home.pack()
label = tb.Label(home, text="Home", font=(
    "Helvetica", 36), bootstyle="warning")
label.pack()

button = tb.Button(home, text="To About", bootstyle="success", command=toAbout)
button.pack(pady=10)

label = tb.Label(about, text="About", font=(
    "Helvetica", 36), bootstyle="warning")
label.pack()

button = tb.Button(about, text="To Home", bootstyle="success", command=toHome)
button.pack(pady=10)

root.after(1000, show_loading_animation)

root.mainloop()
