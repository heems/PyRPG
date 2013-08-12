class Item:
	def __init__(self, name, cost, canEquip):
		self.name = name
		self.cost = cost
		self.canEquip = canEquip
	def __str__(self):
		return "%s : $%d " % (self.name, self.cost)
	def __repr__(self):
		return "%s : $%d " % (self.name, self.cost)

class Weapon(Item):
	def __init__(self, atk, name, cost):
		Item.__init__(self, name, cost, True)
		self.atk = atk

class Pot(Item):
	def __init__(self, heal, name, cost):
		Item.__init__(self, name, cost, False)
		self.heal = heal

class Armor(Item):
	def __init__(self, defense, name, cost):
		Item.__init__(self, name, cost, True)
		self.defense = defense

health = Pot(5, 'sandwich', 3)
sword = Weapon(10, 'sword', 5)
pocketsand = Weapon(15, 'pocket sand', 10)
fedora = Armor(10, 'steel fedora', 20)

store = {
	health.name : health, 
	sword.name : sword, 
	pocketsand.name : pocketsand,
	fedora.name : fedora,
}