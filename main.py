from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
# from kivymd.uix.list import MDList

import elements
# from kivy.metrics import dp, sp
import api
from kivy.core.window import Window
import threading
from requests import ConnectionError

class MainApp(MDApp):
    dialog = None
    store = JsonStore("date.json")
    api = api.Api()

    def build(self):
        # Window.size = (324, 650)
        # python main.py --size=360x740 --dpi=529
        self.theme_cls.theme_style = "Dark"  # Light
        self.load()
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file("main.kv")

    def on_start(self):
        Window.bind(on_keyboard=self.android_back_click)
        if self.api.token == "":
            self.root.current = "login"
        else:
            self.get_info()

    def get_info(self):
        try:
            data = self.api.get_account("self")
            self.root.ids.text_profile_1.text = f"id: {data['id']}\nЛогин: {data['username']}\nEmail: {data['email']}"
            self.root.ids.text_profile_2.text = f"Монеты: {data['money']}"
            self.root.ids.text_profile_3.text = f"Уровней пройдено {data['lvl']} из {data['lvls']}"
            try:
                data = self.api.get_posts()
                self.root.current = "main"
                for i in data:
                    self.root.ids.box.add_widget(
                        elements.OneLineListItemAligned(
                        # text=f"[font=data/Neucha.ttf][size=50]{i['title']}[/size][/font]",
                        text=f"[font=data/Neucha.ttf]{i['title']}[/font]",
                        on_release=self.open_post)
                        )
            except ConnectionError:
                self.root.current = "error_connect"
            except Exception:
                self.root.current = "login"
        except ConnectionError:
            self.root.current = "error_connect"
        except Exception:
            self.root.current = "login"

    def check_connect(self):
        self.get_info()

    def load_post(self, name):
        try:
            data = self.api.get_posts()
            slug = ""
            for i in data:
                if i['title'] == name:
                    slug = i['slug']
            try:
                data = self.api.get_post(slug)
                self.root.ids.post.text = data["body"]
            except ConnectionError:
                self.root.current = "error_connect"
            except Exception:
                self.root.current = "login"
        except ConnectionError:
            self.root.current = "error_connect"
        except Exception:
            self.root.current = "login"

    def open_post(self, onelinelistitem):
        name = onelinelistitem.text[onelinelistitem.text.index(']') + 1:onelinelistitem.text.index('[', 1)]
        self.root.current = "post_screen"
        self.root.ids.post.text = "Загрузка..."
        self.root.ids.post_name.title = name
        threading.Thread(target=self.load_post, args=(name,)).start()

    def get_gift(self):
        try:
            data = self.api.get_gift()
            if data == 1:
                self.root.ids.text_gift.text = "Удачной игры! +1 монетка"
                try:
                    data = self.api.get_account("self")
                    self.root.ids.text_profile_2.text = f"Монеты: {data['money']}"
                except ConnectionError:
                    self.root.current = "error_connect"
                except Exception:
                    self.root.current = "login"
            elif data == 2:
                self.root.ids.text_gift.text = "Повезло, получаешь пожелания хорошего дня"
            else:
                self.root.ids.text_gift.text = "Еще рано, подожди"
        except ConnectionError:
            self.root.current = "error_connect"
        except Exception:
            self.root.current = "login"

    def auth(self):
        try:
            data = self.api.login(self.root.ids.user.text, self.root.ids.password.text)
            self.save()
            self.root.ids.welcome_label.text = "Успешно авторизовались"
            try:
                data = self.api.get_account("self")
                self.root.ids.text_profile_1.text = f"id: {data['id']}\nЛогин: {data['username']}\nEmail: {data['email']}"
                self.root.ids.text_profile_2.text = f"Монеты: {data['money']}"
                self.root.ids.text_profile_3.text = f"Уровней пройдено {data['lvl']} из {data['lvls']}"
                try:
                    data = self.api.get_posts()
                    self.root.current = "main"
                    for i in data.get():
                        self.root.ids.box.add_widget(
                            elements.OneLineListItemAligned(
                                text=f"[font=data/Neucha.ttf]{i['title']}[/font]",
                                on_release=self.open_post)
                        )
                except ConnectionError:
                    self.root.current = "error_connect"
                except Exception:
                    self.root.current = "login"
            except ConnectionError:
                self.root.current = "login"
            except Exception:
                self.root.current = "login"
        except ConnectionError:
            self.root.ids.welcome_label.text = "Нет соединения с сервером"
        except Exception:
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
                        text="[font=data/Neucha.ttf]Хотите выйти?[/font]",
                        buttons=[
                            MDFlatButton(
                                text="Хочу",
                                theme_text_color="Custom",
                                text_color=(.59, .7, .14, 1),
                                font_name='data/Neucha.ttf',
                                on_press=self.to_exit
                            ),
                            MDFlatButton(
                                text="Нет",
                                theme_text_color="Custom",
                                text_color=(.59, .7, .14, 1),
                                font_name='data/Neucha.ttf',
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

    def change_theme(self):
        if self.theme_cls.theme_style == "Dark":
            self.theme_cls.theme_style = "Light"
        else:
            self.theme_cls.theme_style = "Dark"
        self.save()

    def auth_exit(self):
        self.api.logout()
        self.root.current = "login"
        self.api.token = ""
        self.save()

    def load(self):
        try:
            self.api.token = self.store.get('profile')['token']
        except KeyError:
            pass
        try:
            self.theme_cls.theme_style = self.store.get('profile')['theme']
        except KeyError:
            pass

    def save(self):
        self.store.put('profile', token=self.api.token, theme=self.theme_cls.theme_style)


if __name__ == '__main__':
    app = MainApp()
    app.run()
