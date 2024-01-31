import os
from random import randint
import ttkbootstrap as tb
from dotenv import dotenv_values
from PIL import Image, ImageTk
from io import BytesIO
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
                    photos = json_response.get('photos', [])
                    if photos:
                        randomPhotoIndex = randint(0, len(photos) - 1)
                        randomPhotoUrl = photos[randomPhotoIndex]['src']['landscape']
                        image_response = await session.get(randomPhotoUrl)
                        image_data = await image_response.read()
                        img = Image.open(BytesIO(image_data))
                        img = img.resize((300, 300))
                        return ImageTk.PhotoImage(image=img)
                    else:
                        return "No photos found"
                except Exception as e:
                    print("Error parsing JSON:", e)
                    return "Error parsing JSON"
            else:
                print("Error:", response.status)
                return "Error getting image"

async def getFoodDesc(search_query):
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
                            return first_page["excerpt"]
                        else:
                            return "No excerpt available"
                    else:
                        return "No pages found"
                except Exception as e:
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
    foods.forget()
    home.pack()


async def search():
    global button

    button.config(text="Searching", default="disabled")
    food = entry.get()
    api_url = 'https://api.api-ninjas.com/v1/recipe?query={}'.format(food)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(api_url, headers={'X-Api-Key': api_ninjas_api_key}) as response:
                if response.status == 200:
                    res = await response.json()
                    if res:
                        for i, food in enumerate(res):
                            foodFrame = tb.Frame(foods, width=300, height=300, bootstyle="light", padding=40)
                            foodImgRes = await getFoodImg(food["title"])
                            foodImg = tb.Label(foodFrame, image=foodImgRes)
                            foodImg.pack()
                            foodTitle = tb.Label(foodFrame, text=food["title"], font=("Helvetica", 20), bootstyle="light, inverse")
                            foodTitle.pack()
                            subFoodDescText = await getFoodDesc(food["title"])
                            subFoodDesc = tb.Label(foodFrame, text=subFoodDescText, font=("Helvetica", 12), bootstyle="light, inverse", wraplength=300)
                            subFoodDesc.pack()
                            button = tb.Button(foodFrame, text="To Home", bootstyle="success", command=toHome)
                            button.pack(pady=10)
                            foodFrame.grid(padx=10, pady=10, row=i//3, column=i%3, sticky="nsew")
                        home.forget()
                        root.geometry("%dx%d" % (root.winfo_screenwidth(), root.winfo_screenheight()))
                        foods.pack()
                    else:
                        errorLabel.config(text="No results found")
                        button.config(text= "Search", default= "active")
                else:
                    print("Error:", response.status)
                    errorLabel.config(text="Error getting your foods. Please try again")
                    button.config(text= "Search", default= "active")
        except Exception as e:
            print("Exception:", e)
            errorLabel.config(text="An error occurred while searching. Please try again.")
        finally:
            button.config(text="Search", default="active")

root = tb.Window(title="Foodie", themename="darkly", iconphoto=icon_path)
# root.geometry("%dx%d" % (root.winfo_screenwidth(), root.winfo_screenheight()))
root.geometry("600x800")
root.place_window_center()

home = tb.Frame(root)
foods = tb.Frame(root)

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

root.mainloop()
