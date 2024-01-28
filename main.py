import tkinter as tk
from ttkbootstrap.constants import *
import ttkbootstrap as tb

root = tb.Window(title="Foodie", themename="superhero", iconphoto="School Apps/Foodie/assets/food.ico")
root.geometry("%dx%d" % (root.winfo_screenwidth(), root.winfo_screenheight()))

root.mainloop()