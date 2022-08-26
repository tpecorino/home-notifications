import tkinter as tk
from db import DBConnection

db = DBConnection()


def subscribe(event):
    entity_id = listbox_unsubscribed_entities.get(tk.ANCHOR)

    if entity_id:
        entity = db.fetch_entity_by_name(entity_id)
        print("HERE", entity)
        db.update_entity(entity_id, 1)
        listbox_unsubscribed_entities.delete(tk.ANCHOR)
        listbox_subscribed_entities.insert(entity.id - 1, entity_id)
        print("Subscribed", entity_id)


def unsubscribe(event):
    entity_id = listbox_subscribed_entities.get(tk.ANCHOR)

    if entity_id:
        db.update_entity(entity_id, 0)
        entity = db.fetch_entity_by_name(entity_id)
        listbox_subscribed_entities.delete(tk.ANCHOR)
        listbox_unsubscribed_entities.insert(entity.id - 1, entity_id)
        print("Unsubscribed", entity_id)


def add_entities(home_entities):
    for entity in home_entities:
        if entity.is_subscribed:
            listbox_subscribed_entities.insert(tk.END, entity.name)
        else:
            listbox_unsubscribed_entities.insert(tk.END, entity.name)


window = tk.Tk()

frame_entities_container = tk.Frame(window)
frame_entities_container.columnconfigure([0, 1, 2], minsize=100, weight=1)
frame_entities_container.rowconfigure(0, minsize=100, weight=1)
frame_entities_container.pack(fill=tk.BOTH, side=tk.TOP)

frame_unsubscribed = tk.Frame(frame_entities_container)
frame_unsubscribed.grid(row=0, column=0, sticky="nsew")
listbox_unsubscribed_entities = tk.Listbox(frame_unsubscribed, width=50, height=50)
listbox_unsubscribed_entities.pack(side=tk.LEFT, fill=tk.BOTH)

# Subscribe/Unsubscribe buttons
frame_btn_group = tk.Frame(frame_entities_container)
frame_btn_group.grid(row=0, column=1, sticky="ew")

btn_subscribe = tk.Button(frame_btn_group, text=">")
btn_subscribe.pack(pady=10)
btn_subscribe.bind("<Button-1>", subscribe)

btn_unsubscribe = tk.Button(frame_btn_group, text="<")
btn_unsubscribe.pack()
btn_unsubscribe.bind("<Button-1>", unsubscribe)

frame_subscribed = tk.Frame(frame_entities_container)
frame_subscribed.grid(row=0, column=2, sticky="nsew")
listbox_subscribed_entities = tk.Listbox(frame_subscribed, width=50)
listbox_subscribed_entities.pack(side=tk.RIGHT, fill=tk.BOTH)

scrollbar = tk.Scrollbar(frame_unsubscribed)
scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

listbox_unsubscribed_entities.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox_unsubscribed_entities.yview)


def init(home_entities):
    for entity in home_entities:
        if entity.is_subscribed:
            listbox_subscribed_entities.insert(tk.END, entity.name)
        else:
            listbox_unsubscribed_entities.insert(tk.END, entity.name)

    window.mainloop()
