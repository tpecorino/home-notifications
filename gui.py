import tkinter as tk
from tkinter import ttk


class GUI:
    def __init__(self, db):
        self.db = db
        self.window = tk.Tk()
        self.tabControl = ttk.Notebook(self.window)
        self.entities_tab = tk.Frame(self.tabControl)
        self.settings_tab = tk.Frame(self.tabControl)
        self.frame_entities_container = tk.Frame(self.entities_tab)
        self.frame_subscribed = tk.Frame(self.frame_entities_container)
        self.frame_unsubscribed = tk.Frame(self.frame_entities_container)
        self.frame_btn_group = tk.Frame(self.frame_entities_container)
        self.btn_subscribe = tk.Button(self.frame_btn_group, text=">")
        self.btn_unsubscribe = tk.Button(self.frame_btn_group, text="<")
        self.subscribed_label = tk.Label(self.frame_subscribed, text="Subscribed")
        self.unsubscribed_label = tk.Label(self.frame_unsubscribed, text="Unsubscribed")
        self.listbox_subscribed_entities = tk.Listbox(self.frame_subscribed, width=50)
        self.listbox_unsubscribed_entities = tk.Listbox(self.frame_unsubscribed, width=50, height=50)
        self.scrollbar = tk.Scrollbar(self.frame_unsubscribed)

    def setup_layout(self):
        self.window.title("Home Assistant Notifications")
        self.tabControl.add(self.entities_tab, text="Subscriber")
        self.tabControl.add(self.settings_tab, text="Settings")
        self.tabControl.pack(expand=1, fill="x")

        # Entities container
        self.frame_entities_container.columnconfigure([0, 1, 2], minsize=100, weight=1)
        self.frame_entities_container.rowconfigure(0, minsize=100, weight=1)
        self.frame_entities_container.pack(fill=tk.BOTH, side=tk.TOP)

        self.frame_subscribed.grid(row=0, column=2, sticky="nsew")
        self.frame_unsubscribed.grid(row=0, column=0, sticky="nsew")
        self.unsubscribed_label.pack()
        self.subscribed_label.pack()

        self.listbox_subscribed_entities.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.listbox_unsubscribed_entities.pack(side=tk.LEFT, fill=tk.BOTH)

        # Subscribe/Unsubscribe buttons
        self.frame_btn_group.grid(row=0, column=1, sticky="ew")
        self.btn_subscribe.pack(pady=10)
        self.btn_unsubscribe.pack()
        self.btn_subscribe.bind("<Button-1>", self.subscribe)
        self.btn_unsubscribe.bind("<Button-1>", self.unsubscribe)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.listbox_unsubscribed_entities.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox_unsubscribed_entities.yview)

    def subscribe(self, event):
        entity_id = self.listbox_unsubscribed_entities.get(tk.ANCHOR)

        if entity_id:
            entity = self.db.fetch_entity_by_name(entity_id)
            print("HERE", entity)
            self.db.update_entity(entity_id, 1)
            self.listbox_unsubscribed_entities.delete(tk.ANCHOR)
            self.listbox_subscribed_entities.insert(entity.id - 1, entity_id)
            print("Subscribed", entity_id)

    def unsubscribe(self, event):
        entity_id = self.listbox_subscribed_entities.get(tk.ANCHOR)

        if entity_id:
            self.db.update_entity(entity_id, 0)
            entity = self.db.fetch_entity_by_name(entity_id)
            self.listbox_subscribed_entities.delete(tk.ANCHOR)
            self.listbox_unsubscribed_entities.insert(entity.id - 1, entity_id)
            print("Unsubscribed", entity_id)

    def add_entities(self, home_entities):
        for entity in home_entities:
            if entity.is_subscribed:
                self.listbox_subscribed_entities.insert(tk.END, entity.name)
            else:
                self.listbox_unsubscribed_entities.insert(tk.END, entity.name)

    def init(self):
        print("GUI Init")

        self.setup_layout()

        home_entities = self.db.fetch_entities()

        for entity in home_entities:
            if entity.is_subscribed:
                self.listbox_subscribed_entities.insert(tk.END, entity.name)
            else:
                self.listbox_unsubscribed_entities.insert(tk.END, entity.name)

        self.window.mainloop()
