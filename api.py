import requests
from error import Error


class Api:
    def __init__(self, token=""):
        self.token = token

    def set_token(self, token):
        self.token = token

    def login(self, username, password):  # return true if get token
        try:
            url = 'http://pavellip.pythonanywhere.com/api/account/token/login'
            response = requests.post(url, data={"username": username, "password": password})
            if response.status_code == 200:
                self.token = response.json()["auth_token"]
                return Error("Ok")
            return Error("Error code")
        except requests.ConnectionError:
            return Error("Error connect")

    def get_account(self, id):  # return {'id', 'username', 'email', 'lvl', 'lvls'}
        try:
            url = 'http://pavellip.pythonanywhere.com/api/'
            head = {'Authorization': f'Token {self.token}'}
            response = requests.get(url, headers=head, params={"id": id})
            if response.status_code == 200:
                return Error("Ok", response.json())
            return Error("Error code")
        except requests.ConnectionError:
            return Error("Error connect")

    def logout(self):
        try:
            url = 'http://pavellip.pythonanywhere.com/api/account/token/logout'
            head = {'Authorization': f'Token {self.token}'}
            response = requests.post(url, headers=head)
            if response.status_code == 204:
                self.token = ""
                return Error("Ok")
            return Error("Error code")
        except requests.ConnectionError:
            return Error("Error connect")

    def get_posts(self):
        try:
            url = 'http://pavellip.pythonanywhere.com/api/pages/'
            head = {'Authorization': f'Token {self.token}'}
            response = requests.get(url, headers=head)
            if response.status_code == 200:
                return Error("Ok", response.json())
            return Error("Error code")
        except requests.ConnectionError:
            return Error("Error connect")

    def get_post(self, name):
        try:
            url = 'http://pavellip.pythonanywhere.com/api/pages/'
            head = {'Authorization': f'Token {self.token}'}
            response = requests.get(url, headers=head, params={"slug": name})
            print(response.text)
            if response.status_code == 200:
                return Error("Ok", response.json())
            return Error("Error code")
        except requests.ConnectionError:
            return Error("Error connect")
