import os
from random import randint
from tkinter import ttk
import ttkbootstrap as tb
from dotenv import dotenv_values
from PIL import Image, ImageTk
from io import BytesIO
from bs4 import BeautifulSoup
from googletrans import Translator
import time
import aiohttp
import asyncio

script_dir = os.path.dirname(os.path.abspath(__file__))

icon_path = os.path.join(script_dir, "assets", "FOODIE.png")
env_path = os.path.join(script_dir, ".env")

env_vars = dotenv_values(env_path)
api_ninjas_api_key = env_vars.get("API_NINJAS_API_KEY")
wikimedia_api_key = env_vars.get("WIKI_MEDIA_API_KEY")
pexel_api_key = env_vars.get("PEXEL_API_KEY")
email = env_vars.get("EMAIL")

async def getFoodImg(search_query):
    global button

    headers = {
        'Authorization': pexel_api_key,
    }

    url = 'https://api.pexels.com/v1/search/'
    parameters = {'query': search_query}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=parameters) as response:
            if response.status == 200:
                try:
                    json_response = await response.json()
                    if json_response and 'photos' in json_response:
                        photos = json_response['photos']
                        if photos:
                            random_photo = randint(0, len(photos) - 1)
                            photo_data = photos[random_photo]
                            photo_url = photo_data['src']['landscape']
                            async with session.get(photo_url) as img_response:
                                if img_response.status == 200:
                                    img_bytes = await img_response.read()
                                    img = Image.open(BytesIO(img_bytes))
                                    img = img.resize((round(root.winfo_screenwidth()/3) - 50, 350))
                                    return ImageTk.PhotoImage(img)
                                else:
                                    print("Error downloading image:", img_response.status)
                                    return None
                        else:
                            print("No photos found in the response")
                            return None
                    else:
                        print("Invalid JSON response format")
                        return None
                except Exception as e:
                    button.config(text= "Search", state= "active")
                    root.update_idletasks()
                    print("Error parsing JSON:", e)
                    return None
            else:
                print("Not found:", response.status)
                return None

async def getFoodDesc(search_query):
    global button

    language_code = 'en'
    number_of_results = 1
    headers = {
        'Authorization': "Bearer {}".format(wikimedia_api_key),
        'User-Agent': 'Foodie (' + email + ')'
    }

    base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
    endpoint = '/search/page'
    url = base_url + language_code + endpoint
    parameters = {'q': search_query, 'limit': number_of_results}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=parameters) as response:
            if response.status == 200:
                try:
                    json_response = await response.json()
                    if json_response.get("pages"):
                        first_page = json_response["pages"][0]
                        if first_page.get("excerpt"):
                            try:
                                soup = BeautifulSoup(first_page["excerpt"], 'html.parser')
                                soupText = soup.get_text()
                                translator = Translator()
                                translated_text = translator.translate(soupText, src='auto', dest='en').text
                                return translated_text
                            except Exception as e:
                                print("Not Found:", e)
                                return None
                        else:
                            return "No excerpt available"
                    else:
                        return "No pages found"
                except Exception as e:
                    button.config(text= "Search", state= "active")
                    root.update_idletasks()
                    print("Error parsing JSON:", e)
                    return "Error parsing JSON"
            else:
                print("Error:", response.status)
                return "Error getting food description"

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
    foods_canvas.forget()
    scrollbar.forget()
    root.geometry("600x800")
    root.update_idletasks()
    home.pack()


async def search():
    global button, toHome

    button.config(text="Searching", state="disabled")
    root.update_idletasks()
    food = entry.get()
    api_url = 'https://api.api-ninjas.com/v1/recipe?query={}'.format(food)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(api_url, headers={'X-Api-Key': api_ninjas_api_key}) as response:
                if response.status == 200:
                    res = await response.json()
                    if res:
                        foodSearch = tb.Label(foods, text="Search results for " + food + " ...", font=("Helvetica", 24), bootstyle="light")
                        foodSearch.grid(row=1, column=0, columnspan=3)
                        toHomeBtn = tb.Button(foods, text="To Home", bootstyle="success", command=toHome)
                        toHomeBtn.grid(row=1, column=2)
                        for i, food in enumerate(res):
                            foodFrame = tb.Frame(foods, width=300, height=300, relief="sunken", borderwidth=2, bootstyle="light")
                            foodImgRes = await getFoodImg(food["title"])
                            foodImg = tb.Label(foodFrame, image=foodImgRes)
                            foodImg.pack()
                            foodImg.image = foodImgRes
                            foodTitle = tb.Label(foodFrame, text=food["title"], font=("Helvetica", 20), bootstyle="light, inverse")
                            foodTitle.pack()
                            subFoodDescText = await getFoodDesc(food["title"])
                            subFoodDescText = subFoodDescText[:42] + "..."
                            subFoodDesc = tb.Label(foodFrame, text=subFoodDescText, font=("Helvetica", 12), bootstyle="light, inverse", wraplength=300)
                            subFoodDesc.pack()
                            # button = tb.Button(foodFrame, text="To Home", bootstyle="success", command=toHome)
                            # button.pack(pady=10)
                            foodFrame.grid(padx=10, pady=10, row=(i//3) + 5, column=(i%3), sticky="nsew")
                        home.forget()
                        root.state('zoomed')
                        foods_canvas.pack(side="left", fill="both", expand=True)
                        scrollbar.pack(side="right", fill="y")
                    else:
                        errorLabel.config(text="No results found")
                        button.config(text= "Search", state= "active")
                        root.update_idletasks()
                else:
                    print("Error:", response.status)
                    errorLabel.config(text="Error getting your food now. Please try again later")
                    button.config(text= "Search", state= "active")
                    root.update_idletasks()
        except Exception as e:
            print("Exception:", e)
            errorLabel.config(text="An error occurred while searching. Please try again.")
        finally:
            button.config(text="Search", state="active")
            root.update_idletasks()

root = tb.Window(title="Foodie", themename="darkly", iconphoto=icon_path)
# root.geometry("%dx%d" % (root.winfo_screenwidth(), root.winfo_screenheight()))
root.geometry("800x800")
root.place_window_center()

home = tb.Frame(root)
foods_canvas = tb.Canvas(root)

scrollbar = ttk.Scrollbar(root, orient="vertical", command=foods_canvas.yview)

foods_canvas.configure(yscrollcommand=scrollbar.set)

foods = tb.Frame(foods_canvas)
foods_canvas.create_window((0, 0), window=foods, anchor="nw")

def update_scroll_region(event):
    foods_canvas.configure(scrollregion=foods_canvas.bbox("all"))

# home page
home.pack()
image = tb.PhotoImage(file=icon_path)
label = tb.Label(home, image=image)
label.pack()

label2 = tb.Label(home, text="What would you like to prepare today?", justify="center", font=(
    "Helvetica", 20), wraplength=400, bootstyle="light")
label2.pack(pady=20)

entry = tb.Entry(home, width=50, bootstyle="warning")
entry.pack()

errorLabel = tb.Label(home, bootstyle="danger")
errorLabel.pack()

button = tb.Button(home, text="Search", bootstyle="warning", padding=(40, 20), command=lambda: asyncio.run(search()))
button.pack(pady=20)

# foods page
# foodFrame = tb.Frame(foods, width=300, height=300)
# foodTitle = tb.Label(foodFrame, font=(
#     "Helvetica", 36), bootstyle="warning")
# foodTitle.pack()

# button = tb.Button(foodFrame, text="To Home", bootstyle="success", command=toHome)
# button.pack(pady=10)

root.after(1000, show_loading_animation)

foods.bind("<Configure>", update_scroll_region)

root.mainloop()