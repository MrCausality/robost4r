import globals
import requests
import json
from dynamodb import DynamoDB


class Channel:

    accept = 'application/vnd.twitchtv.v5+json'
    client_id = 'sk5ok2hnx7bn2ng7xjp8bsy43oh9u2'
    response = None

    def __init__(self, _user_name, _user_id):
        self.user_name = _user_name

        if _user_id == 0:
            self.user_id = self.get_user_id()

        ddb = DynamoDB(self.user_id)

        self.token = ddb.get_token()
        self.secret = ddb.get_secret()

    def get_user_id(self):

        # TODO store the user id in the DB and try retrieving there before making a web service call

        headers = {
            'Accept': self.accept,
            'Client-ID': self.client_id,
        }

        self.response = requests.get("https://api.twitch.tv/kraken/users?login=" + self.user_name, headers=headers)

        return int(self.response.json()['users'][0]['_id'])

class Twitch:

    accept = 'application/vnd.twitchtv.v5+json'
    response = None

    def __init__(self):

        self.channel = 'https://api.twitch.tv/kraken/channels/' + str(globals.channel.user_id)

        self.headers = {
            'Accept': self.accept,
            'Authorization': 'OAuth ' + globals.channel.token,
            'Client-ID': globals.channel.client_id
        }

    def response_text(self):
        if self.response is None:
            print("no request sent yet")
        else:
            print(self.response.text)

    def title(self, title):

        self.response = requests.put(self.channel, headers=self.headers, json={'channel': {"status": title}})

    def game(self, game):

        self.response = requests.put(self.channel, headers=self.headers, json={'channel': {"game": game}})

    def get_user_id(self):

        headers = {
            'Accept': self.accept,
            'Client-ID': globals.channel.client_id,
        }

        self.response = requests.get("https://api.twitch.tv/kraken/users?login=" + globals.channel.user_name, headers=headers)

        return int(self.response.json()['users'][0]['_id'])
