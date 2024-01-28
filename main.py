import tkinter as tk
from ttkbootstrap.constants import *
import ttkbootstrap as tb

root = tb.Window(title="Foodie", themename="superhero", iconphoto="School Apps/Foodie/assets/food.ico")
root.geometry("%dx%d" % (root.winfo_screenwidth(), root.winfo_screenheight()))

home = tb.Frame(root)
about = tb.Frame(root)


def toHome():
    about.forget()
    home.pack()


def toAbout():
    home.forget()
    about.pack()


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

root.mainloop()