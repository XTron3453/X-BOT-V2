import discord
import os
from discord.ext import commands
import asyncio
import re
from cogs.game import Game

class Events(commands.Cog):
	def __init__(self, client):
		self.client = client


	@commands.Cog.listener()
	async def on_member_join(self, member):
		print(member)
		game = Game(member.guild.id)

		if 'welcome' in game.get_all_keys() and game.get_welcome_embed():
			await self.client.get_channel(game.get_welcome_channel()).send(embed=(game.get_welcome_embed()))






def setup(client):
	client.add_cog(Events(client))
