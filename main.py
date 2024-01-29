import tkinter as tk
import ttkbootstrap as tb
from dotenv import dotenv_values
import requests
import time

env_vars = dotenv_values('School Apps\Foodie\.env.local')
api_key = env_vars.get("API_KEY")
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
    food = entry.get()
    api_url = 'https://api.api-ninjas.com/v1/recipe?query={}'.format(food)
    response = requests.get(api_url, headers={'X-Api-Key': api_key})
    if response.status_code == requests.codes.ok:
        print(response.text)
        home.forget()
        about.pack()
    else:
        print("Error:", response.status_code, response.text)
        errorLabel.config(text="Error getting your foods. Please try again")

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

errorLabel = tb.Label(home, bootstyle="danger")
errorLabel.pack(side="left")

button = tb.Button(home, text="Search", bootstyle="success", command=search)
button.pack(pady=20)

label = tb.Label(about, text="About", font=(
    "Helvetica", 36), bootstyle="warning")
label.pack()

button = tb.Button(about, text="To Home", bootstyle="success", command=toHome)
button.pack(pady=10)

root.after(1000, show_loading_animation)

root.mainloop()
