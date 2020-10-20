import bot
import soccer_scraper

# initialize my output file
players_info = {
	'name': [],
	'club': [],
	'age': [],
	'league': [],
	'nationality': [],
	'match_played': [],
	'goals': [],
	'assists': [],
	'total': [],
}

# Go to the tabe we need to scrape
bot = bot.TopScorrerBot()
bot.go_to_site()
bot.scroll_down()

# navigate through the page
for page in range(1000):
	page_source = bot.driver.page_source
	soup = soccer_scraper.create_soup(page_source, 'html.parser')
	# scrape the table 
	soccer_scraper.fetch_data(soup, players_info, 'odd')
	soccer_scraper.fetch_data(soup, players_info, 'even') 
	# go to the next page
	bot.mv_across_page()
	# break the loop at the end of the page
	if bot.end == True:
		break
	else:
		pass


# save the file
import json
with open('../data/250_best_scorer.json', 'w') as json_file:
	json.dump(players_info, json_file)


