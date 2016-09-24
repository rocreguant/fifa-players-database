from lxml import html
import requests
import json
import re

offset = 336

# On the first version I'm going to pharse the most direct and influential skills
# since they seem to be a combination of the rest and i'm interested in a quick solution

for i in range(343):
	if i+offset > 344:
		break
	page = requests.get('http://www.futhead.com/15/career-mode/players/all/all/all/all/all/all/all/all/all/rating/cards/?page='+str(i+offset))
	tree = html.fromstring(page.content)
	xpath_link_players = "//*[contains(concat(' ', @class, ' '), ' player-page-listing ')]/div//a/@href"
	list_link_players = tree.xpath(xpath_link_players)
	for player_link in list_link_players:
		page = requests.get('http://www.futhead.com/'+player_link)
		tree = html.fromstring(page.content)
		abilities = {
			"pac"  : re.findall('[0-9]*',tree.xpath("//*[contains(concat(' ', @class, ' '), ' playercard-attr playercard-attr1 ')]/text()")[0])[0],
			"sho"  : re.findall('[0-9]*',tree.xpath("//*[contains(concat(' ', @class, ' '), ' playercard-attr playercard-attr2 ')]/text()")[0])[0],
			"pas"  : re.findall('[0-9]*',tree.xpath("//*[contains(concat(' ', @class, ' '), ' playercard-attr playercard-attr3 ')]/text()")[0])[0],
			"dri"  : re.findall('[0-9]*',tree.xpath("//*[contains(concat(' ', @class, ' '), ' playercard-attr playercard-attr4 ')]/text()")[0])[0],
			"deff" : re.findall('[0-9]*',tree.xpath("//*[contains(concat(' ', @class, ' '), ' playercard-attr playercard-attr5 ')]/text()")[0])[0],
			"phy"  : re.findall('[0-9]*',tree.xpath("//*[contains(concat(' ', @class, ' '), ' playercard-attr playercard-attr6 ')]/text()")[0])[0]
		}
		
		try:
			club = re.search('data-club="([0-9]+)"',page.content).group(1)
		except:
			club = -1
		
		player_data = {
			"id" 		: str.split(player_link,'/')[4],
			"name"	: str.split(player_link,'/')[5],
			"rating": re.search('data-player-rating="([0-9]+)"',page.content).group(1),
			"club"	: club,
			"nation": re.search('data-nation="([0-9]+)"',page.content).group(1),
			"heigh"	: re.search('<tr><td>Height</td><td>([0-9]+)cm',page.content).group(1),
			"age"		: re.search('<tr><td>Age</td><td>([0-9]+)',page.content).group(1),
			"Weak-Foot"	: re.search('<tr><td>Weak Foot</td><td>([a-zA-Z]+)',page.content).group(1),
			"potential"	: re.search('class="playercard-potential">Potential: ([0-9]+)',page.content).group(1),
			"position"	: re.search('data-position-original="([A-Z]+)"',page.content).group(1),
			"abilities" : abilities,
			"Skill-Moves" : re.search('<tr><td>Skill Moves</td><td>([0-9]+)',page.content).group(1),
			"Attack-Workrate"	: re.search('<tr><td>Attack Workrate</td><td>([a-zA-Z]+)',page.content).group(1),
			"Defensive-Workrate"	: re.search('<tr><td>Defensive Workrate</td><td>([a-zA-Z]+)',page.content).group(1)

		}
		
		with open('players-data/'+str.split(player_link,'/')[4]+'.json', 'w') as outfile:
			json.dump(player_data, outfile)
	print i+offset
	
print "done!!!"
