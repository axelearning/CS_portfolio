from selenium import webdriver
from time import sleep


# selenium bot
class TopScorrerBot():
	def __init__(self):
		options = webdriver.ChromeOptions()
		options.add_argument('--ignore-certificate-errors')
		options.add_argument('--incognito')
		# options.add_argument('--headless') # without opening a browser window
		self.driver = webdriver.Chrome(options=options)
		self.end = False


	def go_to_site(self):
		self.driver.get('https://www.transfermarkt.com/statistik/topscorer')
		sleep(10)
		
	def mv_across_page(self):
		try:
			next_page = self.driver.find_element_by_xpath('//*[@id="yw2"]/li[13]')
			next_page.click()
			sleep(5)
			
		except :
			self.end = True

	def scroll_down(self):
		next_page = self.driver.find_element_by_xpath('//*[@id="yw2"]/li[13]')
		next_page.click()




# # test
# bot = TopScorrerBot()
# bot.go_to_site()
# bot.scroll_down()
# for page in range(12):
# 	bot.mv_across_page()






