import requests
import json
import re

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
page = requests.get('http://www.football-lineups.com/tourn/La_Liga_2015-2016/fixture/' , headers=headers)


matches = re.findall('<td align=center width=50 ><a  href="/match/([0-9]+)/"',page.content)

for match in matches:
	page = requests.get('http://www.football-lineups.com/match/'+str(match)+'/' , headers=headers)
