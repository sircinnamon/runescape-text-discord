import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import json
import os
import logging
import runescape_text as runescape
import tempfile

CMD_PREFIX = "rs:"
BOT_DESCRIPTION = """How to use:

Prefix your message with "rs:" followed by any of the normal modifiers in runescape! I'll send you back an image showing the chat message.

Only one colour and one animation will be applied, obviously.
Modifiers:
	Colours:
		yellow
		white
		cyan
		red
		green
		purple
		flash1
		flash2
		flash3
		glow1
		glow2
		glow3
	Animations:
		scroll
		slide
		wave (:wave: is an emoji so try :wave1:)
		wave2
		shake
"""
client = Bot(CMD_PREFIX, description=BOT_DESCRIPTION)

@client.listen('on_ready')
async def on_ready():
	print('Logged in as {} <{}>'.format(client.user.name, client.user.id))
	print('------')
	print("Current servers:")
	for server in client.guilds:
		print("* {} ({})".format(server.name,server.id))
	print('------')
	logging.info("Logged in successfully")
	await client.change_presence(activity=discord.Game(name='Runescape'))

@client.command(hidden=True, aliases=[""])
async def runescapify(ctx):
	content = ctx.message.clean_content
	content = content.replace(CMD_PREFIX+" ","",1)
	content = content.replace("wave1:", "wave:") # Custom override to avoid emoji
	img = runescape.parse_string(content)
	filename = ""
	fileobj = None
	if(len(img)==1):
		fileobj = tempfile.NamedTemporaryFile(suffix=".png",prefix="runescape-")
		filename = fileobj.name
		logging.info("Saving png for {} at {}".format(ctx.message.id, filename))
		runescape.single_frame_save(img[0], file=fileobj.file)
		fileobj.file.flush()
	else:
		fileobj = tempfile.NamedTemporaryFile(suffix=".gif",prefix="runescape-")
		filename = fileobj.name
		logging.info("Saving gif for {} at {}".format(ctx.message.id, filename))
		runescape.multi_frame_save(img, file=fileobj.file)
		fileobj.file.flush()
	fileobj.file.seek(0)
	await ctx.send(file=discord.File(fileobj.file, filename=filename))

@client.event
async def on_message(msg):
	if msg.content.startswith("{}{}".format(CMD_PREFIX, "help")):
		pass
	elif msg.content.startswith(CMD_PREFIX):
		# Add a space to trigger runescapify
		msg.content = msg.content.replace(CMD_PREFIX, CMD_PREFIX+" ", 1)
	elif msg.content.startswith("`"+CMD_PREFIX):
		msg.content = msg.content[1:-1]
		msg.content = msg.content.replace(CMD_PREFIX, CMD_PREFIX+" ", 1)

	await(client.process_commands(msg))
		# await runescapify(ctx)


keys = {
	"discord_token": None
}
with open(".keyfile") as f:
	keys = json.load(f)
if('DISCORD_TOKEN' in os.environ and os.environ['DISCORD_TOKEN']!=None):
	keys["discord_token"] = os.environ['DISCORD_TOKEN']
if("discord_token" not in keys):
	token = input("You must specify the discord bot token: ")
	keys["discord_token"] = token

logging.basicConfig(filename="logs/bot.log",format="(%(asctime)s) %(levelname)s:%(message)s",level=logging.INFO)
logging.info("Logging configured.")
client.run(keys["discord_token"])