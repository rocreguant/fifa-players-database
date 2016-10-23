import glob
import json
import os.path

matches = glob.glob ( '/home/roc/workspace/fifa-db-players/lineup-data2/*' )

for match in matches:
	#load player info
	with open(match) as data_file:
		match_info = json.load(data_file)
		d = []
		for key, value in match_info.iteritems():
			if key == 'Espanyol de Barcelona ': k ='Espanol'
			elif key == 'Rayo Vallecano': k ='Vallecano'
			elif key == 'Rayo Vallecano ': k ='Vallecano'
			elif key == 'Celta Vigo': k ='Celta'
			elif key == 'Atletico Madrid ': k ='Ath Madrid'
			elif key == 'Atletico Madrid': k ='Ath Madrid'
			elif key == 'Athletic Club': k ='Ath Bilbao'
			elif key == 'Athletic Club ': k ='Ath Bilbao'
			elif key == 'Real Sociedad': k ='Sociedad'
			else: k = key
			d.append(k)


	#save file
	with open('/home/roc/workspace/fifa-db-players/lineup-data3/'+d[0]+'-'+d[1]+'.json', 'w') as outfile:
		json.dump(match_info, outfile)
	
