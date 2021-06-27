import discord
import discord.member
from discord.ext import commands
import random
from time import sleep
from purgefirebase import setup,checkuser,loaddata,purchase,decreasestock,increasecredit,decreasecredit,giveitem
import asyncio
import requests
from cards import *
from datetime import datetime

#to add token read


client = commands.Bot(command_prefix='.')
client.remove_command('help')
#load data for users
CreditsData = loaddata()
#shop
shopdict = {
	"purge":10,
	"disperse":20,
	"splooge":5,
	"yo":1000
}
#loop for random event triggers
pevent = False
betlist = []
loserlist = []
pot = 0
betamount = 0
duelactive = False
duelaccept = False
duelerid = 0
contenderid = 0



def updatedata():
	global CreditsData
	CreditsData = loaddata()

@client.event
async def on_ready():
	print("Ready!")
	print(CreditsData)
	

@client.event
async def on_member_join(member):
    print(f'{member} has joined the server!')

@client.event
async def on_member_remove(member):
    print(f'{member} left the server, fucking LOSERROESKRPOSKRP')
#remember to add context for each command!

@client.command()
async def start(ctx):
	member = ctx.message.author
	if checkuser(member.id) == False:
		await ctx.send("Setting up...")
		setup(member.id)
		updatedata()	
		await ctx.send("Set-up Complete!")
	else:
		await ctx.send(f"Already completed set up for {member.name}.")
	
@client.command(aliases = ['c','cred'])
async def credits(ctx):
	authid = str(ctx.message.author.id)
	if checkuser(authid) == True:		
		credits = CreditsData[authid]["credits"]
		await ctx.send(f'{ctx.message.author.name}\'s Credits: {credits}')
	else:
		await ctx.send("You're not a registered user, Please use **.start** to register.")

@client.command()
async def shop(ctx):
	await ctx.send(f"```==================SHOP==================\n[1]{list(shopdict.keys())[0]} : {shopdict[list(shopdict.keys())[0]]} Credits\n[2]{list(shopdict.keys())[1]} : {shopdict[list(shopdict.keys())[1]]} Credits\n[3]{list(shopdict.keys())[2]} : {shopdict[list(shopdict.keys())[2]]} Credits\n[4]{list(shopdict.keys())[3]} : {shopdict[list(shopdict.keys())[3]]} Credits\n```")
	
@client.command(aliases = ['b'])
async def buy(ctx,*,itemnum):
	# check is user is registered, else prompt to start user
	authid = str(ctx.message.author.id)
	if checkuser(authid) == True:
		# get item and price
		try:
			item = list(shopdict.keys())[int(itemnum) - 1]
			itemprice = shopdict[item]
			# get user credits
			usercreds = int(CreditsData[str(ctx.message.author.id)]["credits"])
			await ctx.send("Getting item...")
			# if item > credits : send error msg, else change data loaded and patch to firebase
			if itemprice > usercreds:
				await ctx.send("NOT ENOUGH MONEY YOU POOR FUCK, TRY WINNING MORE LA")
			else:
				await ctx.send("Completing transaction...")
				usercreds -= itemprice
				CreditsData[authid]["credits"] = usercreds
				#purchase function
				purchase(authid,usercreds,item)
				updatedata()
				await ctx.send(f"Purchase complete! : {item} + 1!")
		
		except IndexError:
			await ctx.send("WTF U TRYNA BUY ITS NOT EVEN ON THE SHOP")
		except ValueError:
			await ctx.send("WHAT ARE YOU EVEN TYPING U ILLITERATE FUCK")
	else:
		await ctx.send("You're not a registered user, Please use **.start** to register.")

@client.command()
async def bet(ctx):
	global betlist
	global betamount
	authid = ctx.message.author.id
	if checkuser(authid) == True:
		if pevent == True:
			if ctx.message.author.id not in betlist:
				user = ctx.message.author.id
				decreasecredit(str(user),betamount)
				voice_channel = ctx.message.author.voice.channel
				members = voice_channel.members
				memberfound = False
				for member in members:
					if user == member.id:
						memberfound = True
						global pot
						
						if CreditsData[str(user)]["credits"] >= betamount:
							betlist.append(user)
							pot += betamount
							await ctx.send(f'{ctx.message.author.name} has joined the bet')
							await ctx.send(f'Pot amount: {pot}')
							break
						else:
							await ctx.send("Insufficient credits to participate in this bet")
							break
				if memberfound == False:
					await ctx.send('You are not in the voice channel')	
			else:
				await ctx.send("You have already bet")
		else:
			await ctx.send("No bet ongoing")
	else:
		await ctx.send("You're not a registered user, Please use **.start** to register.")
		



		

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! Current ping:{round(client.latency*1000)} ms.')

@client.command(aliases = ['8ball','eightball','8'])
async def _8ball(ctx,*,question):
    responses = [
		"It is certain",
		"Without a doubt",
		"Definitely",
		"Most likely",
		"Outlook good",
		"Yes!",
		"Try again",
		"Reply hazy",
		"Can't predict",
		"No!",
		"Unlikely",
		"Sources say no",
		"Very doubtful"
	]
    await ctx.send(f'{responses[random.randint(0,len(responses))-1]}')

#get list of members
#edit voice_channel to none
#tally total users disconnected
#send completion message
@client.command(aliases = ['p'])
async def purge(ctx,*,channelname):
	#get user and num of purge
	user = ctx.message.author
	if checkuser(user.id) == True:
		numofpurge = int(CreditsData[str(user.id)]["purge"])
		if numofpurge > 0:
			await ctx.send(f'PURGE COMMENCED BY {user.name}')
			#get voice channel
			try:
				voice_channel = discord.utils.get(ctx.message.guild.channels,name = f'{channelname}',type = discord.ChannelType.voice)
				members = voice_channel.members
				count = 0
				for member in members:
					await member.edit(voice_channel = None)
					count += 1
				if count == 0:
					await ctx.send('NOBODY THERE LA')
				else:
					decreasestock(str(user.id),"purge")
					await ctx.send(f'{count} Users have been purged from the voice call.')
					updatedata()
			except AttributeError:
				await ctx.send('NOBODY THERE LA')
		else:
			await ctx.send("YOU LITERALLY DONT EVEN HAVE A PURGE GO AND BUY ONE LA POOR")
	else:
		await ctx.send("You're not a registered user, Please use **.start** to register.")
#disperse function
@client.command(aliases = ['d'])
async def disperse(ctx,*,channelname):
	user = ctx.message.author
	if checkuser(user.id) == True:
		numofdisperse = int(CreditsData[str(user.id)]["disperse"])
		if numofdisperse > 0:
			#get list of members in voice call
			voice_channel = discord.utils.get(ctx.message.guild.channels,name = f'{channelname}',type = discord.ChannelType.voice)
			members = voice_channel.members
			#randomly generate number to send user to different calls
			for member in members:
				#generate number
				rannum = random.randint(0,len(ctx.guild.voice_channels)-1)
				await member.edit(voice_channel = ctx.guild.voice_channels[rannum])
			decreasestock(str(user.id),"disperse")
			await ctx.send('cumshot')
			updatedata()
		else:
			await ctx.send("YOU LTIERALLY DONT EVEN HAVE A DISPERSE GO AND BUY ONE LA POOR")
	else:
		await ctx.send("You're not a registered user, Please use **.start** to register.")
		

@client.command(aliases = ['everyonefuckingdie'])
async def randomdeath(ctx,*,channelname):
	await ctx.send('TIME TO DIE')
	channelname = channelname
	ass = True
	#connect to call
	channel = discord.utils.get(ctx.message.guild.channels,name = f'{channelname}',type = discord.ChannelType.voice)
	voice = await channel.connect()
	#play audio
	voice.play(discord.FFmpegPCMAudio('menacing.mp3'))
	voice.source = discord.PCMVolumeTransformer(voice.source)
	voice.source.volume = 0.1
	while ass:
		num1 = random.randint(0,20)
		num2 = random.randint(0,20)
		print(num1)
		print(num2)
		if voice.is_playing() == False:	
			voice.play(discord.FFmpegPCMAudio('menacing.mp3'))
			voice.source = discord.PCMVolumeTransformer(voice.source)
			voice.source.volume = 0.5
		
		if num1 == num2:
			voice.stop()
			await voice.disconnect()
			
			#get list of members in voice call
			voice_channel = discord.utils.get(ctx.message.guild.channels,name = f'{channelname}',type = discord.ChannelType.voice)
			members = voice_channel.members
			print(members)
			#randomly generate number to send user to different calls
			for member in members:
				if member.bot == False:
					#generate number
					rannum = random.randint(0,len(ctx.guild.voice_channels)-1)
					await member.edit(voice_channel = ctx.guild.voice_channels[rannum])
			await ctx.send('cumshot')
			ass = False
		else:
			sleep(1)

@client.command(aliases = ['rp','someonedie'])
async def randompurge(ctx,*,amount):
	purgelist = [
	" you have been chosen to PERISHSIEJHROSEIRJF",
	" committed death",
	" is our lucky winner",
	" die time",
	"  死了咯",
	" has been purged from the call."
	]
	channelname = ctx.message.author.voice.channel.name
	#validate if user has enough credits
	usercred = CreditsData[f'{ctx.message.author.id}']['credits']
	if int(usercred) >= int(amount):
		if int(amount) < 0:
			await ctx.send("WHY TF WOULD U BET NEGATIVE MONEY IDIOT") 
		else:
			global betamount
			global betlist
			global pot
			global pevent
			global loserlist
			pot = int(amount)
			if pevent == False:																																
				pevent = True
							
				betamount = int(amount)
				decreasecredit(str(ctx.message.author.id),betamount)
				async def innerpurge(purgelist,channelname):
					await ctx.send('TIME TO DIE')
					#connect to call
					channel = discord.utils.get(ctx.message.guild.channels,name = f'{channelname}',type = discord.ChannelType.voice)
					voice = await channel.connect()
					#play audio
					voice.play(discord.FFmpegPCMAudio('silverscrapes.mp3'))
					voice.source = discord.PCMVolumeTransformer(voice.source)
					voice.source.volume = 0.1
					sleep(14.5)
					voice.stop()
					await voice.disconnect()
					members = []
					for user in betlist:
						members.append(discord.utils.get(ctx.message.guild.members,id = user))
						print(members)
					bot = True
					while bot == True:
						randomuser = members[random.randint(0,len(members)-1)]
						if randomuser.bot == False:
							await randomuser.edit(voice_channel = None)
							await ctx.send(f'{randomuser.name}{purgelist[random.randint(0,len(purgelist)-1)]}')
							bot = False
							betlist.remove(randomuser.id)
							loserlist.append(randomuser.id)
				
				await ctx.send("20 seconds till random purge event")
				await asyncio.sleep(20)
				betlist.append(ctx.message.author.id)
				if pot > 0 and len(betlist) > 1:
					while len(betlist) != 1:
						await innerpurge(purgelist,channelname)
					#give pot to winner
					winner = betlist[0]
					name = discord.utils.get(ctx.message.guild.members,id = winner)
					increasecredit(str(winner),pot)
					await ctx.send(f'{name} has won {pot} from the bet!')
					for userid in loserlist:
						name = discord.utils.get(ctx.message.guild.members,id = userid)
						await ctx.send(f'{name} fucking lost the bet FUCKING TRASH')	
					pevent = False
					pot = 0
					betlist = []
					betamount = 0	
					loserlist = []		
				elif len(betlist) == 1:
					await ctx.send("lmao nobody want bet with u")
				else:
					await ctx.send("error with event, event stopped")
			else:
				await ctx.send("AN EVENT IS ALRAWEDY HAPPENIUGSENOISNG")
	else:
		await ctx.send("YOURE TOO BROKE TO EVEN BET")
	updatedata()
	

@client.command(aliases = ['s','splooge','coom'])
async def cum(ctx):
	user = ctx.message.author
	numofcum = int(CreditsData[str(user.id)]["splooge"])
	if numofcum > 0:
		#connect to call
		channel = ctx.message.author.voice.channel
		voice = await channel.connect()
		#play audio
		voice.play(discord.FFmpegPCMAudio('splooge.mp3'))
		voice.source = discord.PCMVolumeTransformer(voice.source)
		voice.source.volume = 0.3
		await ctx.send("SPLOOGED")
		
		#leave call
		sleep(15)
		await voice.disconnect()
		decreasestock(str(user.id),"splooge")
	else:
		await ctx.send("NO SPLOOGE FOR U OWADLAP:LD:ALSD")

	updatedata()

@client.command(aliases = ["r"])
async def reyna(ctx):
	user = ctx.message.author
	#connect to call
	channel = ctx.message.author.voice.channel
	voice = await channel.connect()
	#play audio
	voice.play(discord.FFmpegPCMAudio('iLSHoWBriemStonTrUPOWA.mp3'))
	voice.source = discord.PCMVolumeTransformer(voice.source)
	voice.source.volume = 1
	await ctx.send("brimstone")
	
	#leave call
	sleep(5)
	await voice.disconnect()



@client.command(aliases = ['yoe','y'])
async def yo(ctx):
	#get user
	user = ctx.message.author
	numofyo = int(CreditsData[str(user.id)]["yo"])
	if numofyo > 0:
		#connect to call
		channel = ctx.message.author.voice.channel
		members = channel.members
		syafiq = discord.utils.get(ctx.message.guild.members, id = 264778312969224192)
		if syafiq in members:
			voice = await channel.connect()
			#play audio
			voice.play(discord.FFmpegPCMAudio('yo.mp3'))
			voice.source = discord.PCMVolumeTransformer(voice.source)
			voice.source.volume = 0.1
			sleep(12)
			await ctx.send("yoe")
			await syafiq.edit(voice_channel = None)
			await voice.disconnect()
			decreasestock(user.id,"yo")
		else:
			await ctx.send("SYAFIQ NOT INCALLLLLLLL")
	else:
		await ctx.send("NO YO FOR UUUUUUUUUUUUUUUUUUUUUU")
	updatedata()

@client.command(aliases =['h'])
async def help(ctx):
	await ctx.send(
		"```**		HELP LIST FOR PURGE BOT 		**\n\
			**Commands**\n\
			test\n\
				```\
		"
	)

@client.command(aliases = ['i'])
async def inventory(ctx):
	#get user id
	user = ctx.message.author.id
	#get inventory
	disperse = int(CreditsData[str(user)]["disperse"])
	purge = int(CreditsData[str(user)]["purge"])
	splooge = int(CreditsData[str(user)]["splooge"])
	yo = int(CreditsData[str(user)]["yo"])
	#print info
	await ctx.send(f"```\
	INVENTORY\n\
	=======================\n\
	Disperse = {disperse}\n\
	Purge = {purge}\n\
	Splooge = {splooge}\n\
	Yo = {yo}\n\
	=======================```")
	


@client.command()
async def refresh(ctx):
	await ctx.send("Updating data please wait...")
	updatedata()
	await ctx.send("Done!")

@client.command()
async def duel(ctx,*,member):
	#wait for approve
	global duelactive
	duelactive = True
	global duelerid
	dueler = ctx.message.author.name
	duelerid = ctx.message.author.id
	global contenderid
	contender = discord.utils.get(ctx.message.guild.members, name = member)
	if contender != None:
		await ctx.send(f"10 Seconds till duel with {contender}")
		contenderid = contender.id
		
	else:
		await ctx.send("The person you're trying to duel with doesnt exist :(")	
		return
	await asyncio.sleep(10)
	global duelaccept
	if duelaccept == True:
		#generate a reward: Either credits or item
		prizelist = ["100","200","500","purge","disperse","splooge","yo"]
		prize = prizelist[random.randint(0,len(prizelist)-1)]
		#countdown
		duelerwins = 0
		contenderwins = 0
		round = 1
		while duelerwins != 2 and contenderwins != 2:
			#request for new deck
			deckdata = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
			deckid = deckdata.json()["deck_id"]
			count = 5
			message = await ctx.send(f"Countdown to duel! : {count}")
			while count != 0:
				await asyncio.sleep(1)
				count -= 1
				await message.edit(content = f"Countdown to duel! : {count}")
			await ctx.send(f"DUEL DUEL DUEL DUEL DUEL DUEL DUEL")
			#draw cards
			carddata = requests.get(f"https://deckofcardsapi.com/api/deck/{deckid}/draw/?count=2")
			carddata = carddata.json()
			duelercard = cardmaker(carddata,0)
			contendercard = cardmaker(carddata,1)
			#embed pictures, round, names and prize
			embed = discord.Embed(title=f"Round {round}", colour=discord.Colour(0xf45a20), url="https://discordapp.com", timestamp=datetime.now())
			embed.set_image(url=duelercard.image)
			embed.set_thumbnail(url="https://cdn3.iconfinder.com/data/icons/casino-and-gambling-icons/470/Aces-2-512.png")
			embed.set_author(name="PurgeBOT", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
			embed.set_footer(text=f"Duel between {dueler} and {contender}", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
			embed.add_field(name="🤔", value=f"Prize:{prize}")
			embed.add_field(name=f"SCORE:{dueler}({duelerwins}) : {contender}({contenderwins})", value=f"{dueler} Cards:", inline=True)

			embed2 = discord.Embed(title=f"Round {round}", colour=discord.Colour(0xf45a20), url="https://discordapp.com", timestamp=datetime.now())
			embed2.set_image(url=contendercard.image)
			embed2.set_thumbnail(url="https://cdn3.iconfinder.com/data/icons/casino-and-gambling-icons/470/Aces-2-512.png")
			embed2.set_author(name="PurgeBOT", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
			embed2.set_footer(text=f"Duel between {dueler} and {contender}", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
			embed2.add_field(name="🤔", value=f"Prize:{prize}")
			embed2.add_field(name=f"SCORE:{dueler}({duelerwins}) : {contender}({contenderwins})", value=f"{contender} Cards:", inline=True)

			await ctx.send(embed=embed)
			await ctx.send(embed=embed2)
			if duelercard.totalvalue > contendercard.totalvalue:
				duelerwins += 1 
				await ctx.send(f'{dueler} is the winner for round {round}!')
			else:
				contenderwins += 1
				await ctx.send(f'{contender} is the winner for round {round}!')
			round += 1
		#embed into message the winner, cards and prize
		if duelerwins == 2:
			usercreds = int(CreditsData[duelerid]["credits"])
			await ctx.send(f'{dueler} is the winner of the duel!')
			#give prize 
			giveitem(duelerid,usercreds,prize)

		else:
			await ctx.send(f'{contender} is the winner of the duel!')
			usercreds = int(CreditsData[contenderid]["credits"])
			await ctx.send(f'{dueler} is the winner of the duel!')
			#give prize 
			giveitem(contenderid,usercreds,prize)

		updatedata
		#update winner prizes
	elif contender != None and duelaccept == False:
		await ctx.send("Contender did not accept the duel.")
	duelaccept = False

@client.command()
async def accept(ctx):
	author = ctx.message.author.id
	if duelactive == True and author != duelerid and author == contenderid:
		global duelaccept
		duelaccept = True
		await ctx.send("Duel accepted!")
	elif duelactive == False:
		await ctx.send("No duel to accept")
	elif author == duelerid:
		await ctx.send("WHY WOULD YOU ACCEPT YOUR OWN BET STUPID")
	elif author != contenderid:
		await ctx.send("NOT BETITNVI WITH U RIGHT")

@client.command()
async def reallyah(ctx):
	#connect to call
	channel = ctx.message.author.voice.channel
	voice = await channel.connect()
	#play audio
	voice.play(discord.FFmpegPCMAudio('discordbot\\reallyah.mp3'))
	voice.source = discord.PCMVolumeTransformer(voice.source)
	voice.source.volume = 0.3

	
	#leave call
	sleep(10)
	await voice.disconnect()

@client.command()
async def startQuotes(ctx):
	while True:
		timer = 0
		while(timer != 60000):
			timer+=1
			print(timer)
		if timer== 60000:
			#get quotes
			quotes = requests.get("https://type.fit/api/quotes").json()
			#random quote
			value = random.randint(0,len(quotes))
			print(type(quotes))
			print(value)
			message = quotes[value]["text"] + " - " + quotes[value]["author"]
			timer = 0
			await ctx.send(message)


client.run(TOKEN)
