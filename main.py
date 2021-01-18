import discord
import os
from discord.ext import commands
from setuptools import setup, find_packages

client = commands.Bot(command_prefix = '-')

@client.event
async def on_ready():
	print('Hello XTRON, I am fully operational')

@client.command()
async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}')
	print(f'Loaded {extension}.py')

@client.command()
async def unload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')
	print(f'Unloaded {extension}.py')

@client.command()
async def reload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')
	client.load_extension(f'cogs.{extension}')
	print(f'Reloaded {extension}.py')

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

client.run('Token')
