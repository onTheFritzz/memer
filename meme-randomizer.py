import random, json, time, os
from random import choice
from datetime import datetime as dt

def jLoad(fileName):
	with open(fileName, 'r') as r:
		return json.load(r)

def getValue(jFile, key):
	try:
		jk = jFile[key]
		return jk
	except:
		raise ValueError(f'"{key}" is prolly not a valid key')

def getRandomMemes(number):
	articleBlock = f'# All Ur Meemz R Belog to Uz\nLast Updated {dt.now().strftime("%m.%d.%Y-%H:%M:%S")}<br>All credits to ebaumsworld.com\n\n'
	for x in range(number + 1):
		# Generate random number provided it has not been used before
		try:
			articleNo = choice([i for i in range(1, len(memeFiles) + 1) if i not in j['memes-used']])
			j['memes-used'].append(articleNo)
		
		except IndexError:
			j['memes-used'] = []

		# After meme index number has been generated, add to 'do not use' list

		with open(memerConfig, 'w') as w:
			json.dump(j, w) # Dump new list, including current random, 'do not use' number

		folder = memeFiles[articleNo].split('.json')[0] # Folder of article number that was picked at random
		folderFileArticle = f'{walkDir}\\{folder}\\{memeFiles[articleNo]}' # Full file path of randomly selected meme article

		article = jLoad(folderFileArticle)
		header = getValue(article, 'header')
		titlesImages = getValue(article, 'titles-images')

		gototop = '<a href="#link0">GO TO TOP</a>'
		previous = f'<a href="#link{x}">GO TO PREVIOUS</a>'
		sourceLink = f'<a href="https://www.ebaumsworld.com/pictures/-/{folder}/">Original Article <b>with</b> Ads</a>'

		articleBlock += f'## <a href="#link{x+1}" id="link{x}">{header}</a>\n'

		for ti in titlesImages:
			title, image = ti[0], ti[1]
			articleBlock += f'{title}\n<img src="{image}">\n\n'
		
		print(f'Writing article {x}')
		articleBlock += f'\n{sourceLink}\n\n{gototop}\n\n{previous}\n\n'
		with open('README.MD', 'a', encoding='utf-8') as a:
			a.write(articleBlock)
		articleBlock = ''

memerConfig = 'memer-config.json'
walkDir = './all-files' #f'{os.environ["USERPROFILE"]}\\Desktop\\files' # Location of article jsons

with open('README.md', 'w') as w: # Generate file if doesn't exist or clear file from previous run
	w.write('')

j = jLoad(memerConfig)
memeFiles = [] # List of all meme json files
for root, dirs, files in os.walk(walkDir):
	if len(files) == 1: # Do not include files in parent directory
		memeFiles.append(files[0])

getRandomMemes(10)