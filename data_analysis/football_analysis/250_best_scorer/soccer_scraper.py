# import
import requests
from bs4 import BeautifulSoup

# function
def del_empty(value, cond, array):
	if value != cond:
		array.append(value)
	else:
		pass

def create_soup(content, parser):
	return BeautifulSoup(content, parser)


def fetch_data(soup, players_info, type='odd'):
	for info in soup.find_all(class_=type):
		# name & club:
		name_info = []
		for name in info.find_all('a'):
			del_empty(name.get_text(),'',name_info)

		players_info['name'].append(name_info[0])
		players_info['club'].append(name_info[1])

		# nationality and league
		nat_and_league = []
		for nat in info.find_all('img'):
			del_empty(nat['title'],[],nat_and_league)
			
		players_info['nationality'].append(nat_and_league[1])	
		players_info['league'].append(nat_and_league[-1])

		# age - matchs played - goals - assists - total
		goals = []
		for age in  info.find_all(class_='zentriert'):
			del_empty(age.get_text(),'',goals)

		players_info['age'].append(goals[1])
		players_info['match_played'].append(goals[2])
		players_info['goals'].append(goals[-3])
		players_info['assists'].append(goals[-2])
		players_info['total'].append(goals[-1])


#Test
# URL = 'https://www.transfermarkt.com/statistik/topscorer'

# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}

# page = requests.get(URL, headers=headers)

# soup =create_soup(page.content, 'html.parser')


# players_info = {
# 	'name': [],
# 	'club': [],
# 	'age': [],
# 	'league': [],
# 	'nationality': [],
# 	'match_played': [],
# 	'goals': [],
# 	'assists': [],
# 	'total': [],
# }


# fetch_data(soup, players_info, 'odd')
# fetch_data(soup, players_info, 'even')
# print(players_info)


 







