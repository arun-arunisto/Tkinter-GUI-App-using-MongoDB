import tkinter as tk
from PIL import ImageTk
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import random

load_dotenv()
MONOGDB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONOGDB_URI)

#removing widgets from frame
def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def fetch_db():
    db = client.recipes
    #recipe collection
    recipe_collec = db.recipes
    count_doc = recipe_collec.count_documents({})
    index = random.randint(0, count_doc-1)
    recipe = recipe_collec.find_one({"primary_key":{"$eq":index}})
    title = recipe['title']

    #ingredients
    ingre_collec = db.ingredients
    ingredient = ingre_collec.find({"recipe_key":{"$eq":index}})
    ingredients_processed_text = [str(ing["qty"])+" "+str(ing["unit"])+" "+ing['name'] for ing in ingredient]
    return title, ingredients_processed_text



bg_color = "#3d6466"

#command function
def load_frame1():
    clear_widgets(frame2)
    frame1.tkraise() #it will switch between frames
    frame1.pack_propagate(False)  # this will fix the image issues with frame
    # widgets
    # image
    logo_img = ImageTk.PhotoImage(file="RRecipe_logo.png")
    logo_widget = tk.Label(frame1, image=logo_img, bg=bg_color)
    logo_widget.image = logo_img  # this is necessary
    logo_widget.pack()

    # text label
    tk.Label(frame1,
             text="Ready for your random recipe?",
             bg=bg_color,
             fg="white",
             font=("TkMenuFont", 14)).pack()

    # button widget
    tk.Button(frame1,
              text="SHUFFLE",
              font=("TkHeadingFont", 20),
              bg="#28393a",
              fg="white",
              cursor="hand2",
              activebackground="#badee2",
              activeforeground="black",
              command=load_frame2).pack(pady=20)
def load_frame2():
    clear_widgets(frame1)
    frame2.tkraise()
    title, ingredients = fetch_db()
    #print(title,"\n",ingredients)

    #logo image
    logo_img = ImageTk.PhotoImage(file='RRecipe_logo_bottom.png')
    logo_widget = tk.Label(frame2, image=logo_img, bg=bg_color)
    logo_widget.image = logo_img
    logo_widget.pack(pady=20)

    #title
    tk.Label(
        frame2,
        text=title,
        bg=bg_color,
        fg="white",
        font=("TkHeadingFont", 20)
    ).pack(pady=25)

    #ingredients text
    for i in ingredients:
        tk.Label(
            frame2,
            text=i,
            bg="#28393a",
            fg="white",
            font=("TkMenuFont", 12)
        ).pack(fill="both")

    tk.Button(
        frame2,
        text="BACK",
        font=("TkHeadingFont",18),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activeforeground="#badee2",
        activebackground="black",
        command=load_frame1
    ).pack(pady=20)

#initializing app
root = tk.Tk()
#initializing title
root.title("Recipe Picker")
#this will place our tkinter window at center
root.eval("tk::PlaceWindow . center")

#frame
frame1 = tk.Frame(root, width=500, height=600, bg=bg_color)
frame2 = tk.Frame(root, bg=bg_color)
"""frame1.grid(row=0, column=0)
frame2.grid(row=0, column=0)"""
#the above grid method we are going to declare using for loop
for frame in (frame1, frame2):
    frame.grid(row=0, column=0, sticky="nesw")

#calling function frame1
load_frame1()

#run app
root.mainloop()