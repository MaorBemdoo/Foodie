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


def search():
    home.forget()
    about.pack()

root = tb.Window(title="Foodie", themename="darkly", iconphoto="School Apps/Foodie/assets/food.ico")
root.geometry("%dx%d" % (root.winfo_screenwidth(), root.winfo_screenheight()))
root.place_window_center()

home = tb.Frame(root)
about = tb.Frame(root)

home.pack()
image = tb.PhotoImage(file="School Apps/Foodie/assets/food.ico")
label = tb.Label(home, image=image)
label.pack()

label2 = tb.Label(home, text="Search for a food to see details on how to prepare it", font=(
    "Helvetica", 24), bootstyle="warning")
label2.pack(pady=20)

entry = tb.Entry(home, width=50, bootstyle="warning")
entry.pack()

button = tb.Button(home, text="Search", bootstyle="success", command=search)
button.pack(pady=20)

label = tb.Label(about, text="About", font=(
    "Helvetica", 36), bootstyle="warning")
label.pack()

button = tb.Button(about, text="To Home", bootstyle="success", command=toHome)
button.pack(pady=10)

root.after(1000, show_loading_animation)

root.mainloop()
