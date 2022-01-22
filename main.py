from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

import elements
# from kivy.metrics import dp, sp
import api
from kivy.core.window import Window
import threading


class MainApp(MDApp):
    dialog = None
    store = JsonStore("date.json")
    api = api.Api()

    def build(self):
        # Window.size = (324, 650)
        # python main.py --size=360x740 --dpi=529
        self.load()
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file("main.kv")

    def on_start(self):
        Window.bind(on_keyboard=self.android_back_click)
        if self.api.token == "":
            self.root.current = "login"
        else:
            data = self.api.get_account("self")
            if data.get_status() == "Error code":
                self.root.current = "login"
            elif data.get_status() == "Error connect":
                self.root.current = "error_connect"
            elif data.get_status() == "Ok":
                data = data.get()
                self.root.ids.text_profile_1.text = f"id: {data['id']}\nЛогин: {data['username']}\nEmail: {data['email']}"
                self.root.ids.text_profile_2.text = f"Монеты: {data['money']}"
                self.root.ids.text_profile_3.text = f"Уровней пройдено {data['lvl']} из {data['lvls']}"
                data = self.api.get_posts()
                # self.root.ids.box.clear_widgets()
                for i in data.get():
                    self.root.ids.box.add_widget(
                        elements.OneLineListItemAligned(
                            #text=f"[font=data/Neucha.ttf][size=50]{i['title']}[/size][/font]",
                            text=f"[font=data/Neucha.ttf]{i['title']}[/font]",
                            on_release=self.open_post)
                    )

    def check_connect(self):
        data = self.api.get_account("self")
        if data.get_status() == "Error code":
            self.root.current = "login"
        elif data.get_status() == "Ok":
            data = data.get()
            self.root.ids.text_profile_11.text = f"id: {data['id']}\nЛогин: {data['username']}\nEmail: {data['email']}\nМонеты: {data['money']}"
            self.root.ids.text_profile_2.text = f"Уровней пройдено {data['lvl']} из {data['lvls']}"
            self.root.current = "main"

    def load_post(self, name):
        data = self.api.get_posts()
        slug = ""
        if data.get_status() == "Error code":
            self.root.current = "login"
        elif data.get_status() == "Error connect":
            self.root.current = "error_connect"
        elif data.get_status() == "Ok":
            for i in data.get():
                if i['title'] == name:
                    slug = i['slug']
            data = self.api.get_post(slug)
            self.root.ids.post.text = data.get()["body"]

    def open_post(self, onelinelistitem):
        name = onelinelistitem.text[onelinelistitem.text.index(']') + 1:onelinelistitem.text.index('[', 1)]
        self.root.current = "post_screen"
        self.root.ids.post.text = "Загрузка..."
        self.root.ids.post_name.title = name
        threading.Thread(target=self.load_post, args=(name, )).start()

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
                self.root.ids.text_profile_11.text = f"id: {data['id']}\nЛогин: {data['username']}\nEmail: {data['email']}\nМонеты: {data['money']}"
                self.root.ids.text_profile_2.text = f"Уровней пройдено {data['lvl']} из {data['lvls']}"
                data = self.api.get_posts()
                for i in data.get():
                    self.root.ids.box.add_widget(
                        elements.OneLineListItemAligned(
                            text=f"[font=data/Neucha.ttf]{i['title']}[/font]",
                            on_release=self.open_post)
                    )
        elif data.get_status() == "Error connect":
            self.root.ids.welcome_label.text = "Нет соединения с сервером"
        else:
            self.root.ids.welcome_label.text = "Ошибка авторизации"
        self.root.ids.spiner.active = False

    def logger(self):
        # "root", "ZX09cv87"
        self.root.ids.spiner.active = True
        threading.Thread(target=self.auth).start()

    def android_back_click(self, window, key, *largs):
        if key == 27:
            if self.root.current == "post_screen":
                self.root.current = "main"
            else:
                if not self.dialog:
                    self.dialog = MDDialog(
                        text="Хотите выйти?",
                        buttons=[
                            MDFlatButton(
                                text="Хочу",
                                theme_text_color="Custom",
                                text_color=(.59, .7, .14, 1),
                                on_press=self.to_exit
                            ),
                            MDFlatButton(
                                text="Нет",
                                theme_text_color="Custom",
                                text_color=(.59, .7, .14, 1),
                                on_press=self.to_back
                            )
                        ],
                    )
                self.dialog.open()
            return True

    def to_exit(self, inst):
        self.stop()

    def to_back(self, inst):
        self.dialog.dismiss()

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
