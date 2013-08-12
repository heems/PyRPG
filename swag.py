#use xxx as damage value and then sub it out later for actual enemy damage
import xml.etree.ElementTree as ET
class Swag:
	def __init__(self):
		self.tree = ET.parse('data.xml')
		self.root = self.tree.getroot()
	def parseAttacks(self):	
		attacks = {}
		for attack in self.root:
			for enemy in attack:
				name = enemy.get('name') 
				text = enemy.text
				attacks[name] = text
		return attacks