
import requests
from bs4 import BeautifulSoup

playerIGN = 'akakakakakaka'
legendsURL = 'https://maplelegends.com/ranking/all?search='
playerURL = legendsURL + playerIGN 
html_text = requests.get(playerURL).text
soup = BeautifulSoup(html_text, 'html.parser')
rank_table = soup.find(id='rankingTable')
attrbs = rank_table.findAll('b')


class Player:
	name=""
	job=""
	lvl=0
	fame=0
	rank_overall=0
	def __init__(self, name, job,lvl,fame,rank_overall):
		self.name = name
		self.job = job
		self.lvl = lvl
		self.fame = fame
		self.rank_overall = rank_overall
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

if len(attrbs) > 1:
	findJob= rank_table.findAll('a')
	char = Player(str(attrbs[1].get_text()).rstrip(), str(findJob[3].get_text()), int(attrbs[3].get_text()), int(attrbs[2].get_text()), int(attrbs[0].get_text()))
else:
	print(playerIGN + " Is not a valid IGN")



