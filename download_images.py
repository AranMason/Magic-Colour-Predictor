import urllib.request as urllib
import json
import os
import time
import random

print("Opening JSON Data")

def isValidCard(card):
	return 'token' not in type_line 	and \
		'emblem' not in type_line 		and \
		'planeswalker' not in type_line and \
		'scheme' not in type_line		and \
		card['lang'] == 'en' 			and \
		'/' not in card['name'] 		and \
		not card['promo']
		# card['border_color'] is 'black'

with open('scryfall-all-cards.json', encoding='utf-8') as json_file:
	data = json.load(json_file)

	print("JSON Data Loaded")

	# print(data[0]['image_uris']['art_crop'])
	# print(data[2]['color_identity'])

	length = len(data)

	# print( length + " cards found!")

	for card in data:

		#print("Downloaded {progress} of {length}".format(length=length, progress=))

		type_line = card['type_line'].lower()

		# Only Black Border cards, We don't use art from emblems, tokens, planeswalkers, split cards pr Promos.
		if isValidCard(card):

			card_color = card['color_identity']


			if(len(card_color) < 1):
				card_color = "colorless"
			elif (len(card_color) == 1):
				card_color = card_color[0]
			else:
				card_color = 'multi'

			# We don't deal in multi-colour cards
			if card_color is not 'multi':

				# Randomly assign the card as test or training data
				# rng = random.randint(0, 5)
				test = 'test'
				# if rng > 4:
				# 	test = 'validate'

				# for color_id in card_color_id:

				image_uri = card['image_uris']['art_crop']

				directory = 'mtg/{test}/{folder}'.format(folder=card_color, test=test)

				if not os.path.exists(directory):
					os.mkdir(directory)

				file_name = "{card_name} - {multiverse_id}".format(card_name=card['name'], multiverse_id=card['id'])

				card_file_name = "{folder}/{card_name}.jpg".format(card_name=file_name, folder=directory)

				if not os.path.isfile(card_file_name):
					print("Downloading: " + card['name'] + " - " + card['id'])
					# Add a small delay to respect Scryfalls rate limiting requests.
					time.sleep(0.2)
					image = urllib.urlretrieve(image_uri, card_file_name)
					print("Download Complete")