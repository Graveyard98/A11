import requests
import discord
from discord.ext import commands
import json
import random
import asyncio
import webserver
from webserver import keep_alive
import os
import datetime
import json
import time
owner_id = 961825579127164999

server_id = 1144851716580315146

channel_id = 648044573536550922

start = False  #False

prefix = "T!"

def read_json(filename):
    with open(f"database/{filename}.json", "r") as file:
        data = json.load(file)
    return data


def write_json(data, filename):
    with open(f"database/{filename}.json", "w") as file:
        json.dump(data, file, indent=4)
        file.close()
 
 
 
TIGER = commands.Bot(command_prefix=prefix, help_command=None, )
Token = os.environ['Token']

start_time = datetime.datetime.utcnow()
db = {"on_off": False, "channel": None, "guild":None, "msg": None, "botid":None, "count":0}
keep_alive()
ccounts = {"n":0}
#write_json(db, "adb")
db = read_json("adb")
#https://discord.com/api/v10/channels/{channel_id}/messages/{message_id
header = {"authorization":Token}
rr= requests.get("https://discord.com/api/v9/channels/1144851716580315149/messages/1149528356031827978", headers=header)
print(rr.text)


def button_click(token,channelid,guildid, messageid):
    header = {
    'authorization': token
    }
    time.sleep(5)
    r = requests.get(f"https://discord.com/channels/{guildid}/{channelid}/{messageid}", headers = header)
    info = [json.loads(r.text)]
#    print(info[0])

    data = {
    "type": 3,
    "guild_id":str(guildid),
    "channel_id": channelid,
    "message_id": info[0]['id'],
    "session_id": 'fadg',
    "application_id": db["botid"],
    "data": {
    "component_type": 2,
    "custom_id": info[0]['components'][0]['components'][int(random.choice([0,1,2]))]['custom_id'] 
    }
    }
    r = requests.post('https://discord.com/api/v9/interactions',headers = header , json = data)
    print(r)
    return r.status_code



async def sender():
	guild = TIGER.get_guild(int(db["guild"]))
	channel =guild.get_channel(int(db["channel"]))
	while db["on_off"]:
		await asyncio.sleep(10)
		if not db["on_off"] == False:
			await channel.send(db["msg"])
			num = random.choice([30, 31,32,33,34,35,36,37,38,39,40,41,42,43,44,45])
			print(num)
			await asyncio.sleep(num*60)
		
		

db["on_off"] = start

@TIGER.event
async def on_ready():
	print(f"BOT IS READY !\n name: {TIGER.user}\n I'd: {TIGER.user.id}\n Coded by: † ƬiᎶᏋR#1234 ( TIGER CODEZ ! )\n ")
	guild = TIGER.get_guild(int(server_id))
	channel = guild.get_channel(int(channel_id))
	m = await channel.fetch_message(1149528356031827978)

	print(m.components)
	if start == False:
		print("CARD GRABBING IS STOPED.")
	elif guild == None:
		print("SERVER NOT FOUND PLEASE CHECK ID AND TRY AGAIN.")
	elif channel == None:
		print("Channel NOT FOUND PLEASE CHECK ID AND TRY AGAIN.")
	else:
		db["channel"] = channel_id
		db["guild"] = server_id
		db["on_off"] = start
		write_json(db, "adb")
	if db["on_off"] == True:
		os.system("clear")
		print(f"CARDS GRABBER IS STARTED.\n SERVER NAME: {guild.name}\n CHANNEL NAME: {channel.name}")
		await sender()



#@TIGER.command()
#async def start(ctx):
#	if db["on_off"] == True:
#		await ctx.reply("> Bot has started already !")
#	else:
#		db["channel"] = ctx.channel.id
#		db["guild"] = ctx.guild.id
#		db["on_off"] = True
#		write_json(db, "adb")
#		await ctx.reply("> Bot has started successfully !")
#		await sender()

@TIGER.event
async def on_message(message):
	try:
		if str(message.author.id) == str(owner_id):
			await TIGER.process_commands(message)
		else:
			pass#rint("command was not awaited by owner !")
	except:
		pass
	if db["on_off"] == True:
		if str(message.author.id)== db["botid"]:
			if f"{TIGER.user.mention} is dropping" in message.content:
				x =button_click(token=Token, channelid= message.channel.id, guildid=message.guild.id, messageid=message.id)
				if x == 204:
					now = datetime.datetime.utcnow()  
					delta = now - start_time
					hours, remainder = divmod(int(delta.total_seconds()), 3600)
					minutes, seconds = divmod(remainder, 60)
					days, hours = divmod(hours, 24)
					if days:
						time_format = "**{d}** days, **{h}** hours, **{m}** minutes, and **{s}** seconds."
					else:
						time_format = "**{h}** hours, **{m}** minutes, and **{s}** seconds."
					uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)
					ccounts["n"] += 1
					print(f"> Successfully grabbed card !\n total cards grabbed: **{ccounts['n']}** \nIn: {uptime_stamp}")
#					await message.reply(f"> Successfully grabbed card !\n total cards grabbed: **{db['count']}** \nIn: {uptime_stamp}")
				else:
					print("> Failed to grabbed card !")
#					await message.reply("> Failed to grabbed card !")

@TIGER.command()
async def help(ctx):
	await ctx.reply(f"**CARDS GRABBER**\n`Coded by`: **† ƬiᎶᏋR#1234**\n \n `commands`: \n1: `{prefix}start` - start the bot. \n2: `{prefix}stop` - stop the bot. \n3: `{prefix}ping` - shows bot ping. \n4: `{prefix}uptime` - shows bot uptime. \n5: `{prefix}grabbed_info` - shows total grabbed cards and time.")

@TIGER.command()
async def ping(ctx):
    latency = round(TIGER.latency * 1000, 2)
    await ctx.send(f"Pong! Latency: {latency}ms")

@TIGER.command()
async def uptime(ctx):
	now = datetime.datetime.utcnow()  
	delta = now - start_time
	hours, remainder = divmod(int(delta.total_seconds()), 3600)
	minutes, seconds = divmod(remainder, 60)
	days, hours = divmod(hours, 24)
	if days:
		time_format = "**{d}** days, **{h}** hours, **{m}** minutes, and **{s}** seconds."
	else:
		time_format = "**{h}** hours, **{m}** minutes, and **{s}** seconds."
	uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)
	await ctx.reply(uptime_stamp)

@TIGER.command()
async def grabbed_info(ctx):
	now = datetime.datetime.utcnow()  
	delta = now - start_time
	hours, remainder = divmod(int(delta.total_seconds()), 3600)
	minutes, seconds = divmod(remainder, 60)
	days, hours = divmod(hours, 24)
	if days:
		time_format = "**{d}** days, **{h}** hours, **{m}** minutes, and **{s}** seconds."
	else:
		time_format = "**{h}** hours, **{m}** minutes, and **{s}** seconds."
	uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)
	await ctx.reply(f"**GRABBED INFO**\n> total cards grabbed {ccounts['n']} in {uptime_stamp}.")

#@TIGER.command()
#async def stop(ctx):
#	if db["on_off"] == False:
#		await ctx.reply("> Bot is stopped already !")
#	else:
#		db["channel"] = None
#		db["guild"] = None
#		db["on_off"] = False
#		write_json(db, "adb")
#		await ctx.reply("> Bot has stopped successfully !")


#Coded by: † ƬiᎶᏋR#1234 ( TIGER CODEZ !)
TIGER.run(Token)