import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time 
import numpy as np

# bot 
class search_bot():

	def __init__(self):
		options = webdriver.ChromeOptions()
		options.add_argument('--ignore-certificate-errors')
		options.add_argument('--incognito')
		# options.add_argument('--headless') # without opening a browser window
		self.driver = webdriver.Chrome(options=options)
		self.players_not_found = []	

	def go_to_site(self):
		self.driver.get('https://fbref.com')
		time.sleep(2)

	def seek_player(self, player):
		name = self.driver.find_element_by_xpath('//*[@id="header"]/div[3]/form/div/div/input[2]')
		name.send_keys(player)
		try:
			bouton = self.driver.find_element_by_xpath('//*[@id="header"]/div[3]/form/div/div/div/div[1]/div[2]/div/div/span[2]/strong/em[1]')
		except:
			bouton = self.driver.find_element_by_xpath('//*[@id="header"]/div[3]/form/input[1]')
		bouton.click()
		time.sleep(2)
		link = self.driver.find_element_by_link_text('2019-2020')
		link.click()


	def collect_info(self, categories):

		# initialize Bs for scrapping
		page_source = self.driver.page_source
		soup = BeautifulSoup(page_source, 'html.parser')

		table = 'min_width sortable stats_table shade_zero now_sortable'

		try:
			table = soup.find(class_=table).tbody
		except :
			table = soup.find(class_=table +' sliding_cols').tbody

		# select the ligne - with a filtering on the spacer rows
		for row in table.find_all('tr'):
			if row.get('class') == None and row.get('data-row') != None: 
				# True -> player on the bench / False -> player on the field
				if row.find(attrs={'data-stat':'bench_explain'}) != None:
					for cat in categories.keys():
						pass
				else:
					for cat in categories.keys():
						value = row.find(attrs={'data-stat':cat})
						if cat in ('date','round','opponent'):
							categories[cat].append(value.find('a').get_text())
						else:
							try:
								categories[cat].append(value.get_text())
							except:
								categories[cat].append(np.NaN)
			else:
				pass
		return categories


# Create the list of the best scorrer
def players_name(n):
	df = pd.read_json('../data/250_best_scorer.json')
	df.sort_values('goals', ascending=False, inplace=True)
	player_name = list(df['name'][:n])
	return player_name

# create the scrapper function
def run_scrapper(players, keys, players_database):
	for i,name in enumerate(players):
		player_info = {key:[] for key in keys}
		# a. seek the player
		try:
			bot.seek_player(name)
		except:
			bot.players_not_found.append(name)
			print(f'player not found :{name}')

		# b. collect player's stat
		try:
			player_info = bot.collect_info(player_info)
			print(f'{name}: data collect!')
		except AttributeError:
			bot.players_not_found.append(name)
			print(f'player not found :{name}')

		# c. add it to the database
		player_info = pd.DataFrame(player_info)
		player_info['name'] = name
		players_database = pd.concat([players_database,player_info], axis=0, sort=False)

		#d. save the database afterevery 10 players
		if i % 10 == 0:
			print(f'save : {i+1}/250')
			players_database.to_csv('../data/players_database.csv', index=False)

	players_database.to_csv('../data/players_database.csv', index=False)
	return bot.players_not_found


### ___ Main PGRM ___ ###

start = time.time()
# 1. Create the outpout dataframe
keys = ['date', 'comp', 'round','opponent','minutes', 'goals', 'assists', 'shots_total', 'shots_on_target', 
		'crosses','fouled', 'pens_made', 'pens_att', 'xg','npxg', 'xa']
players_database = pd.DataFrame({key:[] for key in keys})

# 2. Choose the players and initialize the bot
bot = search_bot()
bot.go_to_site()
players = players_name(250)
# 3. Run the main loop
players_not_found = run_scrapper(players, keys, players_database)
print(players_not_found)
print(time.time() - start)

