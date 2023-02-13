import scrapy, logging, datetime, time, json, os
from scrapy.crawler import CrawlerProcess
from git import Repo

now = datetime.datetime.now().strftime("%m/%d/%Y-%H:%M:%S")

def fusRoDah():
	try:
		repo = Repo('./')
		repo.git.add(update=True) # Fus ## Add
		repo.index.commit(now) # Roh ## Commit
		origin = repo.remote(name='origin')
		origin.push() # Dah ## Push
	except:
		print('Error') # Fus Roh Duh.
		pass

class baumerSpider(scrapy.Spider):
	def __init__(self):
		self.start_urls = ['https://www.ebaumsworld.com']
		logging.getLogger('scrapy').propagate = False
		self.header = f'# All ur Memes R belog to Uz<br>\nLast updated: {now}\n<br>\nAll credits to ebaumsworld.com'
		self.urlPageStart = 1
		self.urlPageEnd = 6 # Get memes from page 1 through this number
		self.articleCounter = 0 # Counter designation for each article/meme dump
		self.sleepBetweenArticles = 30
		self.outputHtml = 'FRONTPAGES-README.MD'#f'Article {self.urlPageStart}-{self.urlPageEnd}.md'

		try:
			os.remove(self.outputHtml)
		
		except:
			pass
		
		finally:
			with open(self.outputHtml, 'a+') as w: 
				w.write(self.header)

	def sleeper(self, seconds, note=''):
		for sec in range(seconds):
			print(f'Sleeping {sec}/{seconds} (sec/s)...', flush=False, end='\r')
			time.sleep(1)
	
	def jMaker(self, j):
		jFileName = j['article-number']
		if not os.path.exists(jFileName):
			os.makedirs(jFileName)

		fileOut = f'./{jFileName}/{jFileName}.json'
		with open(fileOut, "w") as wf:
			json.dump(j, wf)

	def parse(self, response): # Get all front page article in start urls
		urlSuffix = '/?page=' # Page url suffix
		for page in range(self.urlPageStart, self.urlPageEnd):
			pageUrl = f'{self.start_urls[0]}{urlSuffix}{page}'
			print(pageUrl)
			yield scrapy.Request(pageUrl, callback=self.recursiveParse) # Recursively parse each page

	def recursiveParse(self, response): # Get links for any list item in 'Featured' front page
		for url in response.xpath('//div[@class="featureFeedDetails"]//a/@href').getall():
			if url.startswith('https://gaming.ebaumsworld.com'): # Exclude gaming articles which are categorized under 'pictures'
				pass

			elif 'pictures' in url:
				yield scrapy.Request(f'{self.start_urls[0]}{url}', callback=self.getMemes)

	def getMemes(self, response):
		self.articleCounter += 1 # Crawling a successful link, up article counter.
		headerXpath = '//*[@id="detailPage"]/header/h1/text()' # Xpath for article header
		memeXpath = '//img[@class="galleryListImage"]/@src' # Xpath for meme images
		titleXpath = '//li[@class="galleryListItem"]/text()' # Xpath for meme titles
		
		articleHeader = response.xpath(headerXpath).get()
		memes = [meme.get() for meme in response.xpath(memeXpath)]
		titles = []
		
		for title in response.xpath(titleXpath): # Get each title text
			title = title.get().strip()
			if title != '': # Discard extraneous empty values that get scraped
				titles.append(title)
		
		memeBlock = list(zip(titles, memes)) # Generate 2D array and associate meme images with title

		nextNumber = self.articleCounter + 1 # Markdown link to next article/meme collection
		previousNumber = self.articleCounter - 1
		html = f'## <a href="#linky{nextNumber}" id="linky{self.articleCounter}">{articleHeader}</a><br>\n\n'

		for title, meme in memeBlock:
			html += f'<span style="font-size:4em">{title}</span><br><img src="{meme}" style="width:100%"><br>\n\n'
		html += f'<a href="#linky{previousNumber}">GO TO PREVIOUS</a>\n\n'	
		html += f'<a href="{response.url}">Source URL <b>with</b> Ads</a>\n\n'
		html += '<a href="#linky1">GO TO TOP</a>\n'

		j = {
			'article-number': response.url.split('/')[-2],
			'header': articleHeader,
			'titles-images': memeBlock
		}
		
		#self.jMaker(j)
		#print(response.url.split('/')[-2])

		print(f'{self.articleCounter} - Scraped ...{response.url[-50:-1]} successfully.')
		with open(self.outputHtml, 'a+', encoding='utf-8') as w:
			w.write(html)
		self.sleeper(self.sleepBetweenArticles)

if __name__ == "__main__":
	#process = CrawlerProcess()
	#process.crawl(baumerSpider)
	#process.start()
	fusRoDah()