from lxml import html
import requests
import json
import re
from time import gmtime, strftime

offset = 318


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
	print i, "out of 380"
	
	page = requests.get('http://www.football-lineups.com/match/'+str(match)+'/' , headers=headers)

	print page.content
	
	
	#if there is no vote might crash
	#getting the table
	table = re.findall('(cellspacing=0 cellpadding=0 width=280 bgcolor=#f0f0f0><tr><td width=45% valign=top><center><b>)([\S ]+)voted',page.content)
	
	output = {}
	
	#splitting by teams
	try:
		teams = table[0][1].split('<center><b>')
	except:
		with open('url-erro.txt', 'a') as file:
			file.write(str(i)+'\t http://www.football-lineups.com/match/'+str(match)+'/\t'+strftime("%H:%M:%S", gmtime())+'\n')
		continue
		
	#working on the team lineup
	for team in teams:
		players_out = []
		
		#getting the players
		players = re.findall('<font color=tag[0-9A-Z]+>([\S]+) *([\S]*)<\/font><\/td><td>', team.replace('#','tag'))
		
		#Selecting the name or surname which is longer
		for player in players :
			if len(player[0]) > len(player[1]):
				players_out.append(player[0])
			else:
				players_out.append(player[1])
				
		#saving the players of the match in a json var
		output[re.findall('([\S]+)<\/b>', team)[0]] = players_out
		
	
	#saving the match
	with open('lineup-data/'+str(match)+'.json', 'w') as outfile:
			json.dump(output, outfile)
	
print "done!!"

