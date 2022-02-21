import requests


class Api:
    def __init__(self, token=""):
        self.token = token

    def set_token(self, token):
        self.token = token

    def login(self, username, password):  # return true if get token
        url = 'http://pavellip.pythonanywhere.com/api/v1/account/token/login'
        response = requests.post(url, data={"username": username, "password": password})
        if response.status_code == 200:
            self.token = response.json()["auth_token"]
            return True
        raise Exception

    def get_account(self, id):  # return {'id', 'username', 'email', 'lvl', 'lvls'}
        url = 'http://pavellip.pythonanywhere.com/api/v1/'
        head = {'Authorization': f'Token {self.token}'}
        response = requests.get(url, headers=head, params={"id": id})
        if response.status_code == 200:
            return response.json()
        raise Exception

    def logout(self):
        url = 'http://pavellip.pythonanywhere.com/api/v1/account/token/logout'
        head = {'Authorization': f'Token {self.token}'}
        response = requests.post(url, headers=head)
        if response.status_code == 204:
            self.token = ""
            return True
        raise Exception

    def get_posts(self):
        url = 'http://pavellip.pythonanywhere.com/api/v1/pages/'
        head = {'Authorization': f'Token {self.token}'}
        response = requests.get(url, headers=head)
        if response.status_code == 200:
            return response.json()
        raise Exception

    def get_post(self, name):
        url = 'http://pavellip.pythonanywhere.com/api/v1/pages/'
        head = {'Authorization': f'Token {self.token}'}
        response = requests.get(url, headers=head, params={"slug": name})
        if response.status_code == 200:
            return response.json()
        raise "ErrorCode"

    def get_gift(self):
        url = 'http://pavellip.pythonanywhere.com/api/v1/gift/'
        head = {'Authorization': f'Token {self.token}'}
        response = requests.get(url, headers=head)
        if response.status_code == 200:
            return response.json()["gift"]
        raise "ErrorCode"
