# Message Generator

import os
import random

from datetime import datetime
from dateutil.tz import *

import requests
from bs4 import BeautifulSoup


local = tzlocal()
now = datetime.now()
now = now.replace(tzinfo = local)
# Handles the Local Timezone Information
readable_event_date_local = (now).strftime('%a, %b %d %Y %I:%M:%S %p')
local_time = '\n \n' + 'Local Time:  ' + readable_event_date_local +'\n'
# Handles the Server Timezone Information
utc = tzutc()
utc_now = now.astimezone(utc)
readable_event_date_server = (utc_now).strftime('%a, %b %d %Y %I:%M:%S %p')
server_time = 'Server Time: ' + readable_event_date_server
response = local_time + server_time

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
		if self.eventType == 'cwk':
			headerTxt = 'Its time for a CWKPQ!!! \n\nEvent: CWKPQ \nWhen: ' + self.date + ' at ' +self.time + ' UTC \n@Salty Spitoon\n \nSign up in #salty-sign-ups \nExpected Split: \n'
		elif self.eventType == 'zak':
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


# playerIGN = 'MattTheSair'
# legendsURL = 'https://maplelegends.com/ranking/all?search='
# playerURL = legendsURL + playerIGN 
# html_text = requests.get(playerURL).text
# soup = BeautifulSoup(html_text, 'html.parser')
# rank_table = soup.find(id='rankingTable')
# attrbs = rank_table.findAll('b')
# if len(attrbs) > 1:
# 	findJob= rank_table.findAll('a')
# 	char = Player(str(attrbs[1].get_text()).rstrip(), str(findJob[3].get_text()), int(attrbs[3].get_text()), int(attrbs[2].get_text()), int(attrbs[0].get_text()))
# 	response = char.getName() + " is a " + "Level " + str(char.getLevel()) + " " + char.getJob()
# else:
# 	response = playerIGN + " Is not a valid IGN"	

day = (datetime.now()).strftime("%x")
eventTime = (datetime.now()).strftime("%X")
event = 'cwk'
evnt = EventMessageContent(day, eventTime, event)
# ptyRanged = EventParty(6, "Ranged")
# ptyCleave = EventParty(4, "Cleave")
# ptyBuyer = EventParty(3, "Buyer")

# partyListRanged = ['innerbloom', 'BoBoArcher', 'Tricks', 'Winterein', 'SwordSlap']
# for memRange in partyListRanged:
# 	ptyRanged.addChar(Player(memRange))
# 	print(memRange + " added to ranged party")
# partyListCleave = ['TinyIce', 'Getzu', 'Neofang', 'Duckys']
# for memCleave in partyListCleave:
# 	ptyCleave.addChar(Player(memCleave))
# 	print(memCleave + " added to cleave party")

eventMsgDone = Event(evnt, 3)
partyListRanged = ['innerbloom', 'BoBoArcher', 'Tricks', 'Winterein', 'SwordSlap']
for memRange in partyListRanged:
	eventMsgDone.addExpeditionMember(Player(memRange), "Ranged")
	print(memRange + " added to ranged party")
# eventMsgDone.addExpeditionMember(Player(partyListRanged[0]), "Ranged")
# print(partyListRanged[0] + " added to ranged party")

# eventMsgDone.addParty(ptyRanged)
# eventMsgDone.addParty(ptyCleave)
# eventMsgDone.addParty(ptyBuyer)
eventMsgDone.printEvent()
eventMsgDone.charRemove(partyListRanged[0])
eventMsgDone.printEvent()
# char = Player("asdffsdfasdfdffsfsffsfs")
# pty.addChar(char)
# pty.printPty()