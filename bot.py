# bot.py
import os
import random

import discord
from dotenv import load_dotenv

from datetime import datetime
from dateutil.tz import *

import requests
from bs4 import BeautifulSoup


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

class Player:
	name=""
	job=""
	lvl=0
	fame=0
	rank_overall=0
	def __init__(self, name):
		self.name = name
		legendsURL = 'https://maplelegends.com/ranking/all?search='
		playerURL = legendsURL + self.name 
		html_text = requests.get(playerURL).text
		soup = BeautifulSoup(html_text, 'html.parser')
		rank_table = soup.find(id='rankingTable')
		attrbs = rank_table.findAll('b')
		if len(attrbs) > 1 and int(attrbs[3].get_text()) > 0:
			findJob= rank_table.findAll('a')
			self.name = name
			self.job = str(findJob[3].get_text())
			self.lvl = int(attrbs[3].get_text())
			self.fame = int(attrbs[2].get_text())
			self.rank_overall = int(attrbs[0].get_text())
		else:
			print(self.name + " Is not a valid IGN")
	def getName(self):
		return self.name
	def getJob(self):
		return self.job
	def getLevel(self):
		return self.lvl
	def getFame(self):
		return self.fame
	def getOverallRank(self):
		return self.rank_overall
	def setName(self, name):
		self.name = name
	def setJob(self, job):
		self.job = job
	def setLevel(self, lvl):
		self.lvl = lvl
	def setFame(self, fame):
		self.fame = fame
	def setOverallRank(self, rank_overall):
		self.rank_overall = rank_overall

class EventMessageContent:
	date = ""
	time = ""
	eventType = ""
	def __init__(self, date, time, eventType):
		self.date = date
		self.time = time
		self.eventType = eventType
	def getDate(self):
		return self.date
	def getTime(self):
		return self.time
	def getHeader(self):
		if self.eventType == '!cwk':
			headerTxt = 'Its time for a CWKPQ!!! \n\nEvent: CWKPQ \nWhen: ' + self.date + ' at ' +self.time + ' UTC \n@Salty Spitoon\n \nSign up in #salty-sign-ups \nExpected Split: \n'
		elif self.eventType == '!zak':
			headerTxt = 'Its time for a Zak Run!!! \n\nEvent: Zakum Run \nWhen: ' + self.date + ' at ' +self.time + ' UTC \n@Salty Spitoon\n \nSign up in #salty-sign-ups \nExpected Split: \n'
		else:
			headerTxt = 'whoops'
		return headerTxt

class EventParty:
	numChars = 0
	maxNum = 0
	partyType = ""
	def __init__(self, maxNum, type):
		self.party = []
		self.maxNum = maxNum
		self.partyType = type
	def __init__(self, type):
		self.party = []
		self.maxNum = 6
		self.partyType = type
	def addChar(self, char):
		if self.numChars < self.maxNum and char.getLevel() > 0:
			self.party.append(char)
			self.numChars = self.numChars + 1
		else:
			print(self.partyType + " Party is Full")
	def removeChar(self, char):
		if self.numChars > 0:
			if char in self.party:
				self.party.remove(char)
				self.numChars = self.numChars - 1
			if self.numChars == 0:
				self.party = []
	def setMaxPtySize(self, maxNum):
		self.maxNum = maxNum
	def getType(self):
		return str(self.numChars)
	def getPty(self):
		return self.party
	def getMaxPty(self):
		return self.maxNum
	def printParties(self):
		partyMsg = "\n\n**" + self.partyType +" party:**\n"
		i = 1
		for char in self.party:
			partyMsg = partyMsg + str(i) + ".) " + char.getName() + ", lvl " + str(char.getLevel()) + " " + char.getJob() + "\n"
			i = i + 1
		for i in range(self.numChars, self.maxNum):
			partyMsg = partyMsg + str(i+1) + ".) \n"
		return partyMsg

class Event:
	msgHeader = ""
	numParties = 0
	numParticipants = 0
	def __init__(self, msgHeader, numParties):
		self.msgHeader = msgHeader
		self.parties = []
		self.numParties = numParties
		partyTypes = ['Attacker','Ranged','Cleave','Buyer']
		if numParties == 3:
			for i in range(0, self.numParties):
				newParty = EventParty(partyTypes[i+1])
				self.parties.append(newParty)
		elif numParties == 2:
			newParty = EventParty(partyTypes[0])
			self.parties.append(newParty)
			newParty = EventParty(partyTypes[3])
			self.parties.append(newParty)
		else:
			newParty = EventParty(partyTypes[0])
			self.parties.append(newParty)
	def addParty(self, pty):
		self.parties.append(pty)
		self.numParticipants = self.numParticipants + pty.getMaxPty
		self.printPtys()
	def addExpeditionMember(self, char, ptyType):
		if self.numParties > 1:
			if ptyType == "Attacker":
				if len(self.parties[0].getPty()) < self.parties[0].getMaxPty():
					self.parties[0].addChar(char)
				else:
					print("Party is Full")											# DM person trying to join via discord here
			elif ptyType == "Ranged":
				if len(self.parties[0].getPty()) < self.parties[0].getMaxPty():
					self.parties[0].addChar(char)
				else:
					print("Party is Full")											# DM person trying to join via discord here
			elif ptyType == "Cleave":
				if len(self.parties[1].getPty()) < self.parties[1].getMaxPty():
					self.parties[1].addChar(char)
				else:
					print("Party is Full")											# DM person trying to join via discord here
			elif ptyType == "Buyer":
				if len(self.parties[2].getPty()) < self.parties[2].getMaxPty():
					self.parties[2].addChar(char)
				else:
					print("Party is Full")											# DM person trying to join via discord here
	def partyRemove(self, pty):
		if pty in self.parties:
			self.parties.remove(pty)
	def charRemove(self, charIGN):
		for party in self.parties:
			for char in party.getPty():
				if char.getName() == charIGN:
					party.removeChar(char)
					print(char.getName() + " removed")
	def printEvent(self):
		eventMsg = self.msgHeader.getHeader()
		for x in self.parties:
			eventMsg = eventMsg + x.printParties() 
		return eventMsg
	def printPtys(self):
		for x in self.parties:
			x.printParties()



@client.event
async def on_message(message):
	if message.author == client.user:
		return
	parsedMessage = message.content.split(" ")
	if parsedMessage[0] == '!run':
		response = 'The format for generating an event is as follows:\n'
		response = response + ' !eventType date{in format: YYYY/MM/DD} time{for UTC in 24HR format: HH:MM} #Range #Cleave #buyers'
	elif parsedMessage[0] == '!cwk' and len(parsedMessage) == 6:
		# response = parsedMessage[0] + ' selected for ' + parsedMessage[1] + ' at ' + parsedMessage[2] + ' with ' + str(parsedMessage[3]) + ' ranged attackers, ' + str(parsedMessage[4]) + ' cleave attackers, and ' + str(parsedMessage[4]) + ' buyers'
		numParties = 0
		for x in range(3, 6):
			if int(parsedMessage[x]) > 0:
				numParties = numParties + 1
		evnt = EventMessageContent(parsedMessage[1], parsedMessage[2], parsedMessage[0])
		partyStats = [parsedMessage[3], parsedMessage[4], parsedMessage[5]]
		eventGenerate = Event(evnt, numParties)
		eventGenerate.
		response = eventGenerate.printEvent()
	elif parsedMessage[0] == '!zak' and len(parsedMessage) == 6:
		# response = parsedMessage[0] + ' selected for ' + parsedMessage[1] + ' at ' + parsedMessage[2] + ' with ' + str(parsedMessage[3]) + ' ranged attackers, ' + str(parsedMessage[4]) + ' cleave attackers, and ' + str(parsedMessage[4]) + ' buyers'
		numParties = 0
		for x in range(3, 6):
			if int(parsedMessage[x]) > 0:
				numParties = numParties + 1
		evnt = EventMessageContent(parsedMessage[1], parsedMessage[2], parsedMessage[0])
		eventGenerate = Event(evnt, numParties)
		response = eventGenerate.printEvent()
	elif parsedMessage[0] == '!time':
		# Handles the Server Timezone Information
		utc = tzutc()
		now = datetime.now()
		utc_now = now.astimezone(utc)
		readable_event_date_server = (utc_now).strftime('%A, %b %d %Y %I:%M:%S %p')
		server_time = 'Server Time: ' + readable_event_date_server
		response = server_time
	elif parsedMessage[0] == '!lvl':
		playerIGN = str(parsedMessage[1])
		legendsURL = 'https://maplelegends.com/ranking/all?search='
		playerURL = legendsURL + playerIGN 
		html_text = requests.get(playerURL).text
		soup = BeautifulSoup(html_text, 'html.parser')
		rank_table = soup.find(id='rankingTable')
		attrbs = rank_table.findAll('b')
		if len(attrbs) > 1:
			findJob= rank_table.findAll('a')
			char = Player(str(attrbs[1].get_text()).rstrip(), str(findJob[3].get_text()), int(attrbs[3].get_text()), int(attrbs[2].get_text()), int(attrbs[0].get_text()))
			response = char.getName() + " is a " + "Level " + str(char.getLevel()) + " " + char.getJob()
		else:
			response = playerIGN + " Is not a valid IGN"		
	else:
		response = 'Valid commands: !lvl, !time, !cwk, !zak \nFor format of Event Commands, type !run' 
	await message.channel.send(response)

client.run(TOKEN)
