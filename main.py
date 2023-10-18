import requests
import discord
from discord.ext import commands
import json
import random
import asyncio
import time
import os
import webserver
from webserver import keep_alive
token =os.environ['Token'] 


server_id =   648031568756998155

channel_id = 648044573536550922

start = True #False



TIGER = commands.Bot(command_prefix="T!", help_command=None)



db = {"on_off": False, "channel": None, "guild":None, "msg": "Kd", "botid":"646937666251915264", "count":0}

db["on_off"] = start

#@TIGER.event
#async def on_ready():
#	print(" bot is ready")

header = {
    'authorization': token
    }
r = requests.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=15", headers = header)
msg_id = 1150754582629204068
info = json.loads(r.text)
for y in info:
	if int(y["id"]) == msg_id:
		print(y)
#print(json.loads(r.text)[0]["id"])



def button_click(token,channelid,guildid, msg_id):
    header = {
    'authorization': token
    }
    time.sleep(5)
    r = requests.get(f"https://discord.com/api/v9/channels/{channelid}/messages?limit=50", headers = header)
    info = json.loads(r.text)
    for y in info:
    	if int(y["id"]) == msg_id:
#    print(info[0])
		    data = {
		    "type": 3,
		    "guild_id":str(guildid),
		    "channel_id": channelid,
		    "message_id": y['id'],
		    "session_id": 'fadg',
		    "application_id": db["botid"],
		    "data": {
		    "component_type": 2,
		    "custom_id": y['components'][0]['components'][int(random.choice([0,1,2]))]['custom_id'] 
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
		



@TIGER.event
async def on_ready():
	print(f"BOT IS READY !\n name: {TIGER.user}\n I'd: {TIGER.user.id}\n Coded by: † ƬiᎶᏋR#1234 ( TIGER CODEZ ! )\n ")
	guild = TIGER.get_guild(int(server_id))
	channel = guild.get_channel(int(channel_id))
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
#		write_json(db, "adb")
	if db["on_off"] == True:
		os.system("clear")
		print(f"CARDS GRABBER IS STARTED.\n SERVER NAME: {guild.name}\n CHANNEL NAME: {channel.name}")
		await sender()

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
				x =button_click(token=token, channelid= message.channel.id, guildid=message.guild.id, msg_id=message.id)
				if x == 204:
					print(f"> Successfully grabbed card")
				else:
					print("> Failed to grabbed card !")
					
keep_alive()
TIGER.run(token)