def get_all_keys(game_data):

		all_keys = []

		for key in game_data.keys():
			all_keys.append(key)
			if type(game_data[key]) is dict:
				all_keys = all_keys + get_all_keys(game_data[key])

		return all_keys
		
		
post = {
			'chats' : {
				'spec' : {
					'welcome' : 1,
					'advertisements' : 2,
					'reaction-roles' : 3,
					'viewer-lounge': 4,
					'viewer-bot-commands': 5,
					'funny-stuff': 6,

				}
			} 
		}
	   
print(get_all_keys(post))