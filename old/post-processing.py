import glob
import json
import os.path

players_files = glob.glob ( '/home/roc/workspace/fifa-db-players/players-data/*' )

for p in players_files:
	#load player info
	with open(p) as data_file:    
		player_info = json.load(data_file)
	
	club_id = str(player_info["club"])
	club_path = '/home/roc/workspace/fifa-db-players/club-data/'+club_id+'.json'
	
	club_info = {}
	#file exists
	if os.path.exists(club_path):
		#load info
		with open(club_path) as data_file:    
			club_info = json.load(data_file)

	club_info[player_info["id"]] = player_info

	#save file
	with open(club_path, 'w') as outfile:
		json.dump(club_info, outfile)
	
