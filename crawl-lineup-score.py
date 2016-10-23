#initial page:
# http://www.11v11.com/competitions/premier-league/2016/matches/
#380 matches

from lxml import html
import requests
import json
import re
from time import gmtime, strftime

offset = 0


headers = {'User-Agent': 'Mozilla/4.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
page = requests.get('http://www.11v11.com/competitions/premier-league/2016/matches/' , headers=headers)

#TODO check if the server returned a page or said that was overloaded

matches = re.findall('href=\"\/matches\/([a-z\-0-9]+)/',page.content)

#remove duplicates in the list
matches = list(set(matches))


i = 0
for match in matches:
	i+=1
	
	#added offset continuity
	if i < offset:
		continue
	print i, "out of 380"
	
	match_name = re.findall('([\-a-z]+)[0-9]',match)[0][:-1]
	print match #manchester-united-v-watford-02-march-2016-317118
	
	page = requests.get('http://www.11v11.com/matches/'+march , headers=headers)
	#get score
	#compute difference of score
	#get starting lineup
	
	
	
	
	
