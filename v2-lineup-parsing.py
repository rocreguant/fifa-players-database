import requests
import json
import re
from time import gmtime, strftime
import unicodedata


offset = 354


#idea info: http://www.gregreda.com/2015/02/15/web-scraping-finding-the-api/

#i don't think this is working properly
#for some reason changes all special characters to A
def remove_accents(s):
	return unicodedata.normalize('NFKD', s).encode('ascii','ignore')



def get_lineup(match):
	#To convert it i used the following external help:
	#http://curl.trillworks.com/
	#from : http://www.football-lineups.com/match/231269/
	
	################
	# getting the teams
	headers = {'User-Agent': 'Mozilla/4.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	page = requests.get('http://www.football-lineups.com/match/'+match+'/' , headers=headers)
	teams = re.findall('title\>([.\- A-Za-z0-9]+)La Liga',remove_accents(page.text[:400]))[0]
	teams = teams.split(' vs ')
	lineup = {}
	
	################
	# getting the players
	
	
	cookies = {
		  '_ga': 'GA1.2.1689489604.1474738067',
		  'PHPSESSID': 'd3ommvr4fccp4qvf4kofcqk9k7',
	    '_gat': '1',
	}

	headers = {
		  'Host': 'www.football-lineups.com',
		  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0',
		  'Accept': '*/*',
		  'Accept-Language': 'en-US,en;q=0.5',
		  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		  'X-Requested-With': 'XMLHttpRequest',
		  'Referer': 'http://www.football-lineups.com/match/'+match+'/',
		  'Connection': 'keep-alive',
		  'Cache-Control': 'max-age=0',
	}

	data = 'f='+match+'&w=670&h=194&m=8&i=0&mn=0'


	r = requests.post('http://www.football-lineups.com/ajax/get_lnp.php', headers=headers, cookies=cookies, data=data)

	t = remove_accents(r.text)
	sp = t.split('<script>')[2]
	ps = sp.split('document.getElementById') # starts at 1
	first = True
	c = 0
	players = {}
	for p in ps: #iterating through all players
		if first:
			first = False
			continue
		
		#getting in a way the id
		_id = re.findall('[a-zA-Z0-9]+j([0-9]{1,2})\'\)',p)
		if not _id:
			continue
		#get name
		
		name = re.findall('title=\"([a-zA-Z0-9\s,\-.\(\)]+)\"',p)[0]
		position = re.findall('class=\"([a-zA-Z]{4})\"',p)[0]
		player = {"name":name, "position":position}
		c +=1
		players[_id[0]] = player
		if c  == 11:
			lineup[teams[0]] = players
			#c = 0
			players = {}
	lineup[teams[1]] = players
	
	return lineup


headers = {'User-Agent': 'Mozilla/4.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
page = requests.get('http://www.football-lineups.com/tourn/La_Liga_2015-2016/fixture/' , headers=headers)

#TODO check if the server returned a page or said that was overloaded

matches = re.findall('<td align=center width=50 ><a  href="/match/([0-9]+)/"',page.content)

i = 0
for match in matches:
	i+=1
	
	#added offset continuity
	if i < offset:
		continue
	print i, "out of 380 ", match

	output = get_lineup(str(match))
	
	#saving the match
	with open('lineup-data2/'+str(match)+'.json', 'w') as outfile:
			json.dump(output, outfile)


print "done!!"
