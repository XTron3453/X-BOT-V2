import discord
import os
from discord.ext import commands
import asyncio
import re
import pymongo
from pymongo import MongoClient

class Game(commands.Cog):
	def __init__(self, server_id):
		self.server = server_id
		self.ctx = None
		self.connection = MongoClient("mongodb+srv://XTRON:KurokoSh%21ra1@x-bot.z3s0i.mongodb.net/test?authSource=admin&replicaSet=atlas-d6sk26-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")
		self.database = self.connection['X-BOTV2']
		self.collection = self.database['Game Data']

	def get_game_as_keys(self):
		def get_all_keys(game_data):
			all_keys = []

			for key in game_data.keys():
				all_keys.append(key)
				if type(game_data[key]) is dict:
					all_keys = all_keys + get_all_keys(game_data[key])

			return all_keys
		return get_all_keys(self.get_game())



	def get_game(self):
		return self.collection.find_one({"_id": self.server})

	def set_game(self):
		if self.collection.find_one({"_id": self.server}):
			post = {
				'chats': {},
				'tribes': {}
			}

			self.collection.update({'_id': self.server}, {'$set': post}, upsert=True)

	def set_spec_cat(self, channels):
		post = {
			'chats' : {
				'spec' : {
					'welcome' : channels[0],
					'advertisements' : channels[1],
					'reaction-roles' : channels[2],
					'viewer-lounge': channels[3],
					'viewer-bot-commands': channels[4],
					'funny-stuff': channels[5],

				}
			} 
		}

		if 'trusted-viwer-lounge' in channels and 'vl-confessionals' in channels:
			post['chats']['specs']['vl-confessionals'] = channels[6]
			post['chats']['specs']['trusted-viwer-lounge'] = channels[7]

		elif 'vl-confessionals' in channels:
			post['chats']['specs']['vl-confessionals'] = channels[6]

		elif 'trusted-viwer-lounge' in channels:
			post['chats']['specs']['trusted-viwer-lounge'] = channels[6]
		else:
			pass

		self.collection.update({'_id': self.server}, {'$set': post}, upsert=True)

	def set_welcome_embed(self, embed):
		print(embed.to_dict())
		post = {
			'welcome_embed': embed.to_dict()
		}
		self.collection.update({'_id': self.server}, {'$set': post}, upsert=True)

	def get_welcome_channel(self):
		return self.collection['chats']['specs']['welcome']

	def get_welcome_embed(self):
		return self.collection['welcome_embed']



def setup(client):
	client.add_cog(Game(client))