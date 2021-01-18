import discord
import os
from discord.ext import commands
import asyncio

class Example(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def alliance(self):
		print('Hello XTRON, I am fully operational')

def setup(client):
	client.add_cog(Example(client))


