import json
import time
import customtkinter
import os
import pygame
import random
from PIL import Image

root = customtkinter.CTk()
root.geometry("800x500")
root.title("Pokemon GO")

pokemon = [i.removesuffix(".png") for i in os.listdir("Pokemon")]

pygame.init()
sound = pygame.mixer.Sound("bgm.mp3")
sound.set_volume(0.15)
sound.play(-1)


def update(choice=None):
    pokemon1_img = customtkinter.CTkImage(Image.open("Pokemon\\" + pokemon1.get() + ".png"),
                                          Image.open("Pokemon\\" + pokemon1.get() + ".png"),
                                          size=(256, 240))

    pokemon1_label = customtkinter.CTkLabel(root, image=pokemon1_img, text=" ")
    pokemon1_label.place(relx=0.2, rely=0.5, anchor="center")

    pokemon2_img = customtkinter.CTkImage(Image.open("Pokemon\\" + pokemon2.get() + ".png"),
                                          Image.open("Pokemon\\" + pokemon2.get() + ".png"),
                                          size=(256, 240))

    pokemon2_label = customtkinter.CTkLabel(root, image=pokemon2_img, text="")
    pokemon2_label.place(relx=0.8, rely=0.5, anchor="center")


def damage(power, level, attack_stat, stab,
           defense_stat, type_multiplier):
    if power == 0: return 0
    damage = (((2 * level / 5 + 2) * power * attack_stat / defense_stat) / 50 + 2)
    damage *= type_multiplier * stab

    return int(damage) if damage > 1 else 1


def fight():
    with open("pokemon.json", "r") as poke_data, open("moves.json", "r") as moves:
        poke_data = json.load(poke_data)
        moves = json.load(moves)
        protpok = pokemon1.get()
        opppok = pokemon2.get()
        stab1 = 1.5 if poke_data["Generation_1"][protpok]["Types"][0] in poke_data["Generation_1"][opppok][
            "Types"] else 1
        stab2 = 1.5 if poke_data["Generation_1"][opppok]["Types"][0] in poke_data["Generation_1"][protpok][
            "Types"] else 1
        pok1att, pok2att = poke_data["Generation_1"][protpok]["Base_stats"]["Attack"], \
        poke_data["Generation_1"][opppok]["Base_stats"]["Attack"]
        pok1def, pok2def = poke_data["Generation_1"][protpok]["Base_stats"]["Defense"], \
        poke_data["Generation_1"][opppok]["Base_stats"]["Defense"]

        pok1hp, pok2hp = poke_data["Generation_1"][protpok]["Base_stats"]["Hp"], \
        poke_data["Generation_1"][opppok]["Base_stats"]["Hp"]
        pok1moves = list(poke_data["Generation_1"][protpok]["Moves"])
        pok2moves = list(poke_data["Generation_1"][opppok]["Moves"])

        text_INFO.configure(font=("Cascadia Mono", 12))
        while pok1hp > 0 and pok2hp > 0 and pok1moves and pok2moves:
            move = pok1moves.pop()
            pok1damage = damage(moves[move], int(pok1lev.get()), pok1att, stab1, pok2def, 1)
            pok2hp -= pok1damage
            pygame.mixer.Sound(random.choice(["punch.mp3", "roar.mp3",
                                              "hit.wav", "sword.wav"])).play()
            text_INFO.configure(text=f"{protpok} uses {move}.\nHP of {opppok} = {pok2hp}")
            root.update()
            root.after(1000)

            if pok2hp <= 0:
                break

            move = pok2moves.pop()
            pok2damage = damage(moves[move], int(pok2lev.get()), pok2att, stab2, pok1def, 1)
            pok1hp -= pok2damage
            pygame.mixer.Sound(random.choice(["punch.mp3", "roar.mp3",
                                              "hit.wav", "sword.wav", ])).play()
            text_INFO.configure(text=f"{opppok} uses {move}.\nHP of {protpok} = {pok1hp}")
            root.update()
            root.after(1000)
        if pok2hp <= 0:
            text_INFO.configure(text=f"{protpok} wins!", font=("Cascadia Mono", 30), wraplength=200)
        elif pok1hp <= 0:
            text_INFO.configure(text=f"{opppok} wins!", font=("Cascadia Mono", 30), wraplength=200)
        elif not pok1moves or not pok2moves:
            text_INFO.configure(font=("Cascadia Mono", 30), text="DRAW!")
        root.update()

        root.after(1000)
        text_INFO.configure(text="VS", font=("Cascadia Mono", 60))

pokemon1 = customtkinter.CTkComboBox(root, corner_radius=5, font=("Cascadia Mono", 12), command=update,
                                     dropdown_font=("Cascadia Mono", 12), border_width=5, values=pokemon)
pokemon2 = customtkinter.CTkComboBox(root, corner_radius=5, font=("Cascadia Mono", 12), command=update,
                                     dropdown_font=("Cascadia Mono", 12), border_width=5, values=pokemon)
pokemon1.place(relx=0.2, rely=0.2, anchor="center")
pokemon2.place(relx=0.8, rely=0.2, anchor="center")

pok1lev = customtkinter.CTkComboBox(root, corner_radius=5, font=("Cascadia Mono", 12), command=update,
                                    dropdown_font=("Cascadia Mono", 12), border_width=5,
                                    values=[str(i + 1) for i in range(0, 100)])
pok2lev = customtkinter.CTkComboBox(root, corner_radius=5, font=("Cascadia Mono", 12), command=update,
                                    dropdown_font=("Cascadia Mono", 12), border_width=5,
                                    values=[str(i + 1) for i in range(0, 100)])
pok1lev.place(relx=0.2, rely=0.1, anchor="center")
pok2lev.place(relx=0.8, rely=0.1, anchor="center")

pokemon1_img = customtkinter.CTkImage(Image.open("Pokemon\\" + pokemon1.get() + ".png"),
                                      Image.open("Pokemon\\" + pokemon1.get() + ".png"),
                                      size=(256, 240))

pokemon1_label = customtkinter.CTkLabel(root, image=pokemon1_img, text=" ")
pokemon1_label.place(relx=0.2, rely=0.5, anchor="center")

pokemon2_img = customtkinter.CTkImage(Image.open("Pokemon\\" + pokemon2.get() + ".png"),
                                      Image.open("Pokemon\\" + pokemon2.get() + ".png"),
                                      size=(256, 240))

pokemon2_label = customtkinter.CTkLabel(root, image=pokemon2_img, text="")
pokemon2_label.place(relx=0.8, rely=0.5, anchor="center")

fight_button = customtkinter.CTkButton(root, text="FIGHT",
                                       font=("Cascadia Mono", 28),
                                       corner_radius=5,
                                       border_spacing=10,
                                       border_color="#fff",
                                       border_width=5,
                                       command=fight)
fight_button.place(relx=0.5, rely=0.8, anchor="center")

text_INFO = customtkinter.CTkLabel(root, text="VS",
                                   font=("Cascadia Mono", 60))
text_INFO.place(relx=0.5, rely=0.45, anchor="center")

root.mainloop()
