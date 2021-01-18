import discord
import os
from discord.ext import commands
import asyncio
import re
from cogs.game import Game


class Setup(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.ctx = None

	def convert_rgb(self, color):
		color = color.lstrip('#')
		r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
		return discord.Colour.from_rgb(r, g, b)

	def is_hex(self, msg):
		return re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', msg)

	def check(self, msg):
		return msg.author == self.ctx.author


	def check_reaction(self, reaction, user):
		return user == self.ctx.author

	def check_color(self, msg):
		if check(msg):
			content = msg.content 

			if(len(content) == 6):
				content = '#' + msg.content

			return (bool(is_hex(content)) and len(content) == 7 )
		return False

	async def get_welcome_embed(self):
		title = await self.text_prompt('Please input a **title** for the welcome embed')
		description = await self.text_prompt('Please input a **description** for the welcome embed')
		
		thumbnail_check = await self.reaction_prompt('Would you like a Thumbnail for the welcome message?')
		image_check = await self.reaction_prompt('Would you like a Image for the welcome message?')

		embed = discord.Embed(title=title, description=description)
		if image_check:
			image = await self.text_prompt('Please input an **image url** for the welcome embed')
			embed.set_image(url=image)
		if thumbnail_check:
			thumbnail = await self.text_prompt('Please input a **thumbnail url** for the welcome embed')
			embed.set_thumbnail(url=thumbnail)

		return embed


	async def text_prompt(self, prompt_message):
		function = self.check

		try:
			await self.ctx.send(prompt_message)
			msg = await self.client.wait_for('message', check=function, timeout=120)
			return msg.content
		except asyncio.TimeoutError:
			self.ctx.send('You took too long to Respond! Process cancelled.')
			return None

	async def reaction_prompt(self, prompt_message):

		function = self.check_reaction

		prompt = await self.ctx.send(prompt_message)
		emoji_1 = '\U00002705'
		emoji_2 = '\U0000274C'

		await prompt.add_reaction(emoji_1)
		await prompt.add_reaction(emoji_2)

		try:
			reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=function)
			if(reaction.emoji == '\U0000274C'):
				return False
			elif(reaction.emoji == '\U00002705'):
				return True
			else:
				self.ctx.send('Invalid Response, process cancelled.')
		except asyncio.TimeoutError:
			self.ctx.send('You took too long to Respond! Process cancelled.')

	@commands.command()
	async def set_tribes(self, ctx, amount : int, players : int):
		if (players / amount) != round(players / amount):
			await ctx.send(f'Error: {players} players does not divide evenly into {amount} tribes')
		else: 
			await ctx.send(f'Creating {amount} tribes of {int(players/amount)} players')	
			for n in range(amount):
				try:
					print(n)
					await ctx.send(f'Please input a name for Tribe {n + 1}')
					name = await self.client.wait_for('message', check=check, timeout=120)
					await ctx.send(f'Please input a color for Tribe {n + 1}')
					color = await self.client.wait_for('message', check=check_color, timeout=120)

					self.tribes[name.content] = {
						'color': color.content,
						'amount': amount,
						'num_players': int(players/amount),
						'players': {}
					}

					print(self.tribes[name.content])

					await ctx.guild.create_role(name=name.content, color=convert_rgb(color.content), hoist=True)
				except asyncio.TimeoutError:
					await ctx.send('Error: took to long to respond. Process cancelled.')
					break
				else: 
					await ctx.send('Complete!')


	@commands.command()
	async def add_player(self, ctx, player : str):

		player_found = False
		member = ctx.message.guild.get_member_named(member)

		embed = discord.Embed(color=member.colour, name=member.name)
		embed.set_thumbnail(url=f'{member.avatar_url}')
		await ctx.send(embed=embed)

		prompt = await ctx.send(f'Is this the player you wish to add?')
		await bot.add_reaction(prompt, 'white_check_mark')
		await bot.add_reaction(prompt, 'x')

		try:
			reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=(self.check_reaction))
			if(reaction.emoji == 'x'):
				ctx.send('Wrong person? Try again, typing in their full Discord username and discriminator number!')
				print("Failed 1")
			elif(reaction.emoji == 'white_check_mark'):
				player_found = True
				print("Passed")
			else:
				ctx.send('Invalid Response, process cancelled.')
				print("Failed 2")

		except asyncio.TimeoutError:
			await ctx.send('')
		else:
			await ctx.send('Player Added!')
	#Unfinished, get_member_named does not work


	@commands.command()
	async def create_spec_cat(self, ctx):

		self.ctx = ctx
		server = ctx.guild
		game = Game(server.id)
		game.set_game()

		function = self.check_reaction

		trusted_spec = await self.reaction_prompt('Would you like a Trusted Spectator System?')
		vl = await self.reaction_prompt('Would you like a VL system?')

		spec_name = await self.text_prompt('Please input a **name** for the Spectator Role')
		spec_color = self.convert_rgb(await self.text_prompt('Please input a **color** for the Spectator Role'))

		trusted_spec_name = None
		trusted_spec_color = None
		trusted_spec_role = None

		if trusted_spec:
			trusted_spec_name = await self.text_prompt('Please input a **name** for the Trusted Spectator Role')
			trusted_spec_color = self.convert_rgb(await self.text_prompt('Please input a **color** for the Trusted Spectator Role'))
			trusted_spec_role = await server.create_role(name=trusted_spec_name,  colour=trusted_spec_color, hoist = True)

		spec_role  = await server.create_role(name=spec_name, colour=spec_color, hoist = True)
		category = await server.create_category("Spectators")
		await category.set_permissions(spec_role, read_messages=True, send_messages=False, connect=True, speak=True)

		channel_list = [
			'welcome',
			'advertisements',
			'reaction-roles',
			'viewer-lounge',
			'viewer-bot-commands',
			'funny-stuff',
		]

		if vl:
			channel_list.append('vl-confessionals')

		channels = []

		for channel in channel_list:
			new_channel = await server.create_text_channel(channel, category=category)
			channels.append(new_channel.id)
			if channel == 'viewer-lounge':
				await new_channel.set_permissions(spec_role, send_messages=True)

		if trusted_spec:
			new_channel = await server.create_text_channel('trusted-viewer-lounge', category=category)
			channels.append(new_channel.id)
			await new_channel.set_permissions(spec_role, read_messages=False)
			await new_channel.set_permissions(trusted_spec_role, read_messages=True, send_messages=True)

		game.set_spec_cat(channels)


	@commands.command()
	async def test_welcome(self, ctx):
		self.ctx = ctx
		await ctx.send(self.get_welcome_embed())

	@commands.command()
	async def set_welcome(self, ctx):
		self.ctx = ctx
		server = ctx.guild
		game = Game(server.id)
		game_data = game.get_game()
		print(game_data)

		embed = await self.get_welcome_embed()
		await ctx.send(embed=embed)
		welcome_set = await self.reaction_prompt('Is this embed correct?')

		if welcome_set:
			if game_data['chats']:
				game.set_welcome_embed(embed)
			else:
				await ctx.send("Error: welcome channel is either not created by the bot, or hasn't been set.")
		else:
			await ctx.send("Process cancelled.")



	@commands.command()
	async def test_gg(self, ctx):
		self.ctx = ctx
		server = ctx.guild
		game = Game(server.id)
		print(game.get_game())


	@commands.command()
	async def create_host_cat(self, ctx):
		pass


def setup(client):
	client.add_cog(Setup(client))