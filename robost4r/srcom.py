import urllib
import requests

class srcom:

	api_url = "http://www.speedrun.com/api/v1/"
	
	#def __init__(self):
                
	
	def get(self, endpoint, paras):
		uri = self.api_url + endpoint
		response = requests.get(uri, params=paras)
		if response.status_code == 404:
			print(response.status_code)
		if len(response.json()) > 1:
			return response.json()["data"][0]
		else:
			return response.json()["data"]

	def get_user_name(self,id):
		user = self.get("users/" + id,"none")
		return user['names']['international']

	def get_user_id(self,user):
		url = 'users/' + user
		user = self.get(url,"none")
		return user['id']


	def get_game_name(self,id):
		game = self.get("games/" + id,"none")
		return game['names']['international']
		
	def get_game_id(self,name):
		game = (self.get('games', {"name": name}))#[0]
		return game['id']

	##needs category still
	def get_lb(self,name):
		id = self.get_game_id(name)
		game = (self.get('games/'+ id + '/records', "none"))
		game_name = self.get_game_name(id)
		game_released = self.get('games/' + id, 'none')['released']
		records = ['Game: ' + game_name + '(' + str(game_released) + ')']
		for i in range(3):
			users = game["runs"][i]['run']['players']
			for j in range(len(users)):
				player_id = game["runs"][i]['run']['players'][j]['id']
				#print(game["runs"][i]['run']['players'][j]['id'])
			player_name = self.get_user_name(player_id)
			place = game["runs"][i]['place']
			time = game["runs"][i]['run']['times']['primary']
			time_format = self.convert_time(time)
			record = str(place) + ' ' + player_name + ' ' + time_format
			records.append(record)
		return ' | '.join(map(str,records))

		

	def convert_time(self,time):
			for char in time:
				if char == 'M' or char == 'H':
					time = time.replace(char, ':')
				if char == 'P' or char == 'T' or char == 'S':
					time = time.replace(char, '')
			if time.count(':') < 2:
				time = ":" + time
			time2 = time.split(":")
			for i in range (0,len(time2)):
				if not time2[i]:
					time2[i] = "00"
				while len(time2[i]) < 2:
					time2[i] = "0" + time2[i]
			time3 = ""
			for i in range(0,len(time2)-1):
				time3 = time3 + time2[i] + ":"
			time3 = time3 + time2[-1]
			return time3

	def get_pb(self,player):
		player_id = self.get_user_id(player)
		pbs = get("users/" + player_id + "/personal-bests","none")
		for pb in pbs:
			print(pb)
			print()
