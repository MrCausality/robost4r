import requests

clientId = "sk5ok2hnx7bn2ng7xjp8bsy43oh9u2"

r = requests.get("https://api.twitch.tv/kraken/oauth2/authorize?client_id=" + clientId + "&redirect_uri=http://localhost&response_type=token&scope=channel_editor")

print(r.text)