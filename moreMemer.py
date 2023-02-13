from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent

class moreMemes():
	def __init__(self):
		print('init')
		ua = UserAgent() # In order to *juke* out bot detectors on crypto websites
		userAgent = ua.random
		options = webdriver.ChromeOptions()
		options.add_experimental_option("excludeSwitches", ["enable-logging"]) # Silence Selenium's default "Getting default [bluetooth] adapter failed" error.
		options.add_argument(f'user-agent={userAgent}') # Establish a cloaked user agent
		
		self.headless = True
		if self.headless == True:
			options.add_argument("--headless")
		
		self.driver = webdriver.Chrome(options=options) # Main selenium browser instance
		self.baseUrl = 'https://topfiftymemes.com/'

	def getFiftyMemes(self): # An External function to return output
		self.driver.get(self.baseUrl)
			
		block = '//div[@class="css-ocbxeg"]'
		print('searching...')
		WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, block)))
		block = self.driver.find_element(By.XPATH, block).text
		print(block)

if __name__ == "__main__":
	mm = moreMemes()
	mm.getFiftyMemes()