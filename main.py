from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.card import MDCard
from kivymd.uix.list import OneLineListItem

import elements
# from kivy.metrics import dp, sp
import api
# from kivy.core.window import Window
import threading

class MainApp(MDApp):
    def build(self):
        # Window.size = (324, 650)
        # python main.py --size=360x740 --dpi=529
        self.store = JsonStore("date.json")
        self.api = api.Api()
        self.load()
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file("main.kv")

    def on_start(self):
        if self.api.token == "":
            self.root.current = "login"
        else:
            data = self.api.get_account("self")
            if data.get_status() != "Ok":
                self.root.current = "login"
            else:
                data = data.get()
                self.root.ids.text_profile.text = f"id: {data['id']}\nЛогин: {data['username']}\nEmail: {data['email']}\nУровней пройдено {data['lvl']} из {data['lvls']}"
                data = self.api.get_posts()
                #self.root.ids.box.clear_widgets()
                for i in data.get():
                    #print(i["title"])
                    self.root.ids.box.add_widget(
                        OneLineListItem(text=i["title"], theme_text_color="Custom", text_color=(.59, .7, .14, 1))
                    )



    def auth(self):
        data = self.api.login(self.root.ids.user.text, self.root.ids.password.text)
        if data.get_status() == "Ok":
            self.save()
            self.root.ids.welcome_label.text = "Успешно авторизовались"
            self.root.current = "main"
            data = self.api.get_account("self")
            if data.get_status() != "Ok":
                self.root.current = "login"
            else:
                data = data.get()
                self.root.ids.text_profile.text = f"id: {data['id']}\nЛогин: {data['username']}\nEmail: {data['email']}\nУровней пройдено {data['lvl']} из {data['lvls']}"
        elif data.get_status() == "Error connect":
            self.root.ids.welcome_label.text = "Нет соединения с сервером"
        else:
            self.root.ids.welcome_label.text = "Ошибка авторизации"
        self.root.ids.spiner.active = False

    def logger(self):
        # "root", "ZX09cv87"
        self.root.ids.spiner.active = True
        threading.Thread(target=self.auth).start()

    def load(self):
        try:
            self.api.token = self.store.get('profile')['token']
        except KeyError:
            pass

    def save(self):
        self.store.put('profile', token=self.api.token)


if __name__ == '__main__':
    app = MainApp()
    app.run()
