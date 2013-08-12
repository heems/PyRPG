from random import randint
import sys
from items import *
from swag import Swag #swag is an xml parser since the file name parser is taken

invalid = ['???', 'what?', 'sorry I cant do that',]

###############################LOAD VARIABLES#########################################
parser = Swag()
attacks = parser.parseAttacks()
###############################CLASSES################################################

class Character:
	def __init__(self, level):
		self.name = ""
		self.health = 1
		self.health_max = 1
		self.level = level
	def do_damage(self, enemy, damage):
		enemy.health -= damage
		if enemy == p:
			if self.name in attacks:
				print attacks[self.name]
			print "you take %s damage and are now at %d health" % (damage, enemy.health)
		else:
			print "the enemy takes %s damage. now its at %d health" % (damage, enemy.health)
		return enemy.health <= 0
	def calcDamage(self, max, defense):
		r = randint(max/2, max) - defense
		if r > 0:
			return r
		else:
			return 0


class Enemy(Character):
	def __init__(self, name, level):
		Character.__init__(self, level)
		self.name = name
		self.health = level
	def attack(self):
		self.do_damage(p, self.calcDamage(self.level, randint(0,self.level/4)))

class Player(Character):
	def __init__(self):
		Character.__init__(self, 3)
		self.state = 'normal'
		self.health = 10
		self.health_max = 10
		self.baseatk = 3
		self.basedef = 1
		self.atkBoost = 0
		self.defBoost = 0
		self.money = 100
		self.exp = 0
		self.maxexp = 2
		self.inv = {}
		self.equipped = {}
	def quit(self):
		sys.exit("you suck")
	def help(self):
		print currCommands.keys()
	def status(self): 
		print "health: %d/%d \tmoney: %d exp: %d/%d level: %d" % (self.health, self.health_max, self.money, self.exp, self.maxexp, self.level)
	def explore(self):
		recharge()
		print "you go forward in the dungeon\n"
		roll = randint(0,10)
		if roll < 2:
			print "nothing interesting happens"
			if self.health < self.health_max:
				self.health += 1
		elif roll < 4:
			merchant()
		elif roll < 11:
			self.enemy = makeEnemy()
			self.state = 'combat'
			print 'aw shit, you run into a level %d %s' % (self.enemy.level, self.enemy.name)
	def attack(self):
		d = self.calcDamage(self.baseatk + self.atkBoost, self.basedef + self.defBoost)
		if self.do_damage(self.enemy, d):
			print 'you win nice'
			self.getExp()
			self.state = 'normal'
		else:
			self.enemy.attack()
	def inventory(self):
		print "you check your pockets and find\n"
		print ', '.join(self.inv)
	def equip(self):
		toEquip = raw_input("what would you like to equip?\t")
		if toEquip in self.inv and self.inv[toEquip].canEquip == True:
			self.equipped[toEquip] = self.inv[toEquip]
			del self.inv[toEquip]
			print self.equipped
			print self.inv
			self.updateBody()
		else:
			print "you can't equip that"
	def updateBody(self):
		for item in self.equipped:
			if isinstance(item, Weapon):
				self.atkBoost += item.atk
				print "atk is now %d" % (self.baseatk + self.atkBoost)
	def use(self):
		toUse = raw_input("what would you like to use?\t")
		if toUse in self.inv and self.inv[toUse].canEquip == False:
			self.health += self.inv[toUse].heal
			del self.inv[toUse]
			if self.health > self.health_max:
				self.health = self.health_max
			print self.inv
			print self.health
		else:
			print "you can't use that"
	def getExp(self):
		self.exp += self.enemy.level
		self.money += randint(self.enemy.level/2, self.enemy.level)
		if self.exp >= self.maxexp:
			overflow = self.exp - self.maxexp
			self.maxexp *= 1.25
			self.exp = overflow
			self.levelup()
	def levelup(self):
		self.level += 1
		print "YOU LEVEL UP!\n"
		print "what would you like to level up? (1) atk (2) def (3) health"
		choice = raw_input("-> ")
		if choice == '1':
			self.baseatk += 2
		elif choice == '2':
			self.basedef += 2
		elif choice == '3':
			self.health_max += 3
		else:
			print "... ok you dont get anything."
		self.health = self.health_max

def makeEnemy():
	l = p.level
	r = randint(l/2, l) - 1
	if l > len(enemies):
		r = len(enemies) - 1
	return enemies[r]

def recharge():
	for enemy in enemies:
		enemy.health = enemy.level
def merchant():
	print "you meet a traveling salesman\n"
	print "you are carrying %d dollars" % (p.money)
	print "\nthe store is carrying this stuff with these prices"
	print str(store.values()).strip('[]')
	tobuy = raw_input("\nWhat would you like to buy? (enter \'n\' for nothing): ")
	if tobuy == 'n':
		print "ok get out of my store\n\n"
		return
	while tobuy not in store:
		print "we dont have that"
		tobuy = raw_input("would you like anything else?\t")
	if tobuy in p.inv:
		print "you have that already"
	elif store[tobuy].cost <= p.money:
		p.money -= store[tobuy].cost
		p.inv[tobuy] = store[tobuy]
		print "thanks for the business"
	else:
		print "YOU'RE TOO POOR TO AFFORD THAT STOP WASTING MY TIME!"
		print "the merchant slaps you for 2 damage"
		p.health -= 2

###############################COMMAND LISTS############################################
normCommands = {
	'quit': Player.quit,
	'help': Player.help,
	'status': Player.status,
	'inventory': Player.inventory,
	'explore': Player.explore,
	'equip' : Player.equip,
	'use' : Player.use,
}

combCommands = {
	#'flee' : Player.flee,
	'attack' : Player.attack,
	'help': Player.help,	
}

commands = {
	'normal' : normCommands,
	'combat' : combCommands,
}

###############################ENEMIES############################################
magikarp = Enemy('magikarp', 1)
cupcake = Enemy('cupcake', 2)
goat = Enemy('goat', 3)
lgoat = Enemy('large goat', 4)
rlgoat = Enemy('really large goat', 5)
stapler = Enemy('angry stapler', 6)
bruce = Enemy('bruce lee', 9)
neckbeard = Enemy('large neckbeard', 9)
boss_man = Enemy('boss', 20)
enemies = [magikarp, cupcake, goat, lgoat, rlgoat, stapler, bruce, neckbeard,]

###############################GAME LOOP################################################


p = Player()
p.name = raw_input("What is your name?\t")
print "type help to get a list of commands"
while(p.health > 0):
	currCommands = commands[p.state]
	line = raw_input("> ")
	args = line.split()
	if len(args) > 0:
		commandFound = False
		for c in currCommands.keys():
			#if the first couple letters of input match the first couple letters of command
			if args[0] == c[:len(args[0])]:
				currCommands[c](p)
				commandFound = True
				break
		if not commandFound:
			print invalid[randint(0,2)]
	print "\n\n---------------------------------------------------------------------\n\n"			
sys.exit("you died...\nRIP IN PIECE")