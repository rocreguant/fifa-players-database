import requests
import json
import re
from time import gmtime, strftime
import unicodedata

#i don't think this is working properly
#for some reason changes all special characters to A
def remove_accents(s):
	return unicodedata.normalize('NFKD', s).encode('ascii','ignore')



def get_lineup(match):
	#To convert it i used the following external help:
	#http://curl.trillworks.com/
	#from : http://www.football-lineups.com/match/231269/
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

	h = remove_accents(r.text)#unicodedata.normalize('NFKD', unicode(r.text, 'utf8'))
	
	aux = re.findall('class="[A-Za-z]+"\s title="(.+)"\s href="\/footba',h)[0]
	print re.findall('class="[A-Za-z]+"\s+title="([\w\s]*)"',aux)


print get_lineup('231269')



#first step getting all the players
#class="[A-Za-z]+"\s title="(.+)"\s href="\/footba

#getting the names
#class="[A-Za-z]+"\s+title="([\w\s]*)"

