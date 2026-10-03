import json
import os

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen


DATA_FILE = "spotit_data.json"


class HomeScreen(Screen):

    def on_enter(self):
        self.refresh()

    def refresh(self):
        self.clear_widgets()

        root = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )

        title = Label(
            text="SpotIt",
            font_size=dp(32),
            size_hint_y=None,
            height=dp(55),
            bold=True
        )

        subtitle = Label(
            text="Find your stuff instantly",
            font_size=dp(16),
            size_hint_y=None,
            height=dp(30)
        )

        search = TextInput(
            hint_text="🔍 Search your stuff...",
            multiline=False,
            size_hint_y=None,
            height=dp(50)
        )

        search.bind(text=self.search_items)

        add_btn = Button(
            text="＋  ADD ITEM",
            size_hint_y=None,
            height=dp(55)
        )
        add_btn.bind(on_press=lambda x: self.add_item())

        need_btn = Button(
            text="🔎  I NEED IT",
            size_hint_y=None,
            height=dp(55)
        )
        need_btn.bind(on_press=lambda x: self.need_it())

        root.add_widget(title)
        root.add_widget(subtitle)
        root.add_widget(search)
        root.add_widget(add_btn)
        root.add_widget(need_btn)

        scroll = ScrollView()

        self.items_layout = GridLayout(
            cols=1,
            spacing=dp(8),
            size_hint_y=None
        )
        self.items_layout.bind(
            minimum_height=self.items_layout.setter("height")
        )

        scroll.add_widget(self.items_layout)
        root.add_widget(scroll)

        self.add_widget(root)

        self.show_items()

    def show_items(self, items=None):
        self.items_layout.clear_widgets()

        if items is None:
            items = App.get_running_app().data

        if not items:
            self.items_layout.add_widget(
                Label(
                    text="No items yet.\nTap ADD ITEM to get started.",
                    font_size=dp(18),
                    size_hint_y=None,
                    height=dp(100)
                )
            )
            return

        for item in items:
            btn = Button(
                text=f"{'★ ' if item.get('favorite') else ''}"
                     f"{item['name']}\n"
                     f"📍 {item['location']}",
                size_hint_y=None,
                height=dp(75)
            )

            btn.bind(
                on_press=lambda x, i=item:
                self.show_details(i)
            )

            self.items_layout.add_widget(btn)

    def search_items(self, instance, text):
        text = text.lower().strip()

        if not text:
            self.show_items()
            return

        results = [
            item for item in App.get_running_app().data
            if text in item["name"].lower()
            or text in item["location"].lower()
            or text in item["notes"].lower()
            or text in item["category"].lower()
        ]

        self.show_items(results)

    def add_item(self):
        self.manager.current = "add"

    def need_it(self):
        popup = Popup(
            title="I NEED IT 🔎",
            size_hint=(0.9, 0.7)
        )

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )

        search = TextInput(
            hint_text="What are you looking for?",
            multiline=False,
            size_hint_y=None,
            height=dp(50)
        )

        result = Label(
            text="Type an item name above.",
            font_size=dp(18)
        )

        def find_item(instance):
            query = search.text.lower().strip()

            matches = [
                i for i in App.get_running_app().data
                if query and query in i["name"].lower()
            ]

            if matches:
                item = matches[0]

                result.text = (
                    f"📦 {item['name']}\n\n"
                    f"📍 WHERE:\n{item['location']}\n\n"
                    f"📝 {item['notes']}"
                )
            else:
                result.text = "❌ Couldn't find that item."

        search.bind(text=find_item)

        close = Button(
            text="CLOSE",
            size_hint_y=None,
            height=dp(50)
        )
        close.bind(on_press=popup.dismiss)

        layout.add_widget(search)
        layout.add_widget(result)
        layout.add_widget(close)

        popup.content = layout
        popup.open()

    def show_details(self, item):
        popup = Popup(
            title=item["name"],
            size_hint=(0.9, 0.75)
        )

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )

        info = Label(
            text=(
                f"📍 LOCATION\n{item['location']}\n\n"
                f"🏷️ CATEGORY\n{item['category']}\n\n"
                f"📝 NOTES\n{item['notes']}\n\n"
                f"{'⭐ Favorite' if item.get('favorite') else ''}"
            ),
            font_size=dp(17)
        )

        favorite = Button(
            text="⭐ Remove Favorite"
            if item.get("favorite")
            else "☆ Add Favorite",
            size_hint_y=None,
            height=dp(50)
        )

        def toggle_favorite(instance):
            item["favorite"] = not item.get("favorite", False)
            App.get_running_app().save_data()
            popup.dismiss()
            self.refresh()

        favorite.bind(on_press=toggle_favorite)

        delete = Button(
            text="🗑️ DELETE",
            size_hint_y=None,
            height=dp(50)
        )

        def delete_item(instance):
            App.get_running_app().data.remove(item)
            App.get_running_app().save_data()
            popup.dismiss()
            self.refresh()

        delete.bind(on_press=delete_item)

        close = Button(
            text="CLOSE",
            size_hint_y=None,
            height=dp(50)
        )
        close.bind(on_press=popup.dismiss)

        layout.add_widget(info)
        layout.add_widget(favorite)
        layout.add_widget(delete)
        layout.add_widget(close)

        popup.content = layout
        popup.open()


class AddScreen(Screen):

    def on_enter(self):
        self.build()

    def build(self):
        self.clear_widgets()

        root = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )

        title = Label(
            text="➕ Add Item",
            font_size=dp(28),
            bold=True,
            size_hint_y=None,
            height=dp(55)
        )

        self.name = TextInput(
            hint_text="Item name (e.g. Passport)",
            multiline=False,
            size_hint_y=None,
            height=dp(50)
        )

        self.location = TextInput(
            hint_text="Where is it? (e.g. Bedroom cupboard, 2nd shelf)",
            multiline=False,
            size_hint_y=None,
            height=dp(50)
        )

        self.category = TextInput(
            hint_text="Category (e.g. Documents)",
            multiline=False,
            size_hint_y=None,
            height=dp(50)
        )

        self.notes = TextInput(
            hint_text="Notes",
            size_hint_y=None,
            height=dp(100)
        )

        save = Button(
            text="💾 SAVE ITEM",
            size_hint_y=None,
            height=dp(55)
        )
        save.bind(on_press=self.save_item)

        back = Button(
            text="← BACK",
            size_hint_y=None,
            height=dp(50)
        )
        back.bind(
            on_press=lambda x:
            setattr(self.manager, "current", "home")
        )

        root.add_widget(title)
        root.add_widget(self.name)
        root.add_widget(self.location)
        root.add_widget(self.category)
        root.add_widget(self.notes)
        root.add_widget(save)
        root.add_widget(back)

        self.add_widget(root)

    def save_item(self, instance):
        name = self.name.text.strip()
        location = self.location.text.strip()

        if not name or not location:
            Popup(
                title="Missing information",
                content=Label(
                    text="Please enter the item name and location."
                ),
                size_hint=(0.8, 0.3)
            ).open()
            return

        item = {
            "name": name,
            "location": location,
            "category": self.category.text.strip() or "Other",
            "notes": self.notes.text.strip(),
            "favorite": False
        }

        App.get_running_app().data.append(item)
        App.get_running_app().save_data()

        self.manager.current = "home"


class SpotItApp(App):

    def build(self):
        self.title = "SpotIt"

        self.data = self.load_data()

        manager = ScreenManager()

        manager.add_widget(
            HomeScreen(name="home")
        )

        manager.add_widget(
            AddScreen(name="add")
        )

        return manager

    def load_data(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r") as file:
                    return json.load(file)
        except Exception:
            pass

        return []

    def save_data(self):
        try:
            with open(DATA_FILE, "w") as file:
                json.dump(
                    self.data,
                    file,
                    indent=4
                )
        except Exception:
            pass


if __name__ == "__main__":
    SpotItApp().run()
