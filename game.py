import serialize, rendering, resources, browser
from global_holder import root

@serialize.register_serializable
class CurrencyPool(serialize.SimpleSerializable):
	export_vars=["amounts"]
	def __init__(self):
		self.amounts={}
		self.currencies={}

	def _add_currency(self, currency, name=None, desc="", color="#000000", allow_negative=False, show_if_empty=False, cap=None, symbol="",flags=[], data={}, format_string="{:.0f}"):
		if name==None: name=currency
		if currency not in self.currencies:
			self.currencies[currency]={
				"name":name,
				"desc":desc,
				"id":currency,
				"allow_negative":allow_negative,
				"show_if_empty":show_if_empty,
				"cap":cap,
				"color":color,
				"symbol":symbol,
				"flags":flags,
				"data":data,
				"format_string":format_string
			}

	def add_currency(self, currency, *a, **k):
		if currency not in self.currencies:
			self._add_currency(currency, *a, **k)
		if currency not in self.amounts:
			self.amounts[currency]=0

	def check_cap(self, currency):
		if self.currencies[currency]["cap"] is not None:
			if self.amounts[currency]>self.currencies[currency]["cap"]:
				self.amounts[currency]=self.currencies[currency]["cap"]

	def add_amount(self, currency, amount):
		self.add_currency(currency)
		self.amounts[currency]+=amount
		self.check_cap(currency)

	def get_amount(self, currency, must_be_int=False):
		return self.amounts[currency] if currency in self.currencies else (0 if must_be_int else None)

	def get_flags(self, currency, default=["invisible"]):
		return self.currencies[currency]["flags"] if currency in self.currencies else default

	def get_data(self, currency, default={}):
		return self.currencies[currency]["data"] if currency in self.currencies else default

	def get_desc(self, currency, default={}):
		return self.currencies[currency]["desc"] if currency in self.currencies else default

	def get_color(self, currency):
		return self.currencies[currency]["color"]

	def has_currency(self, currency):
		return currency in self.currencies

	def set_amount(self, currency, amount):
		self.add_currency(currency)
		self.amounts[currency]=amount
		self.check_cap(currency)

	def get_name(self, currency):
		return self.currencies[currency]["name"] if currency in self.currencies else "[Invalid ID]"

	def get_string(self, currency):
		if self.has_currency(currency):
			return self.currencies[currency]["name"]+": "+self.get_value_string(currency)
		else:
			return ""

	def get_value_string(self, currency):
		return self.currencies[currency]["format_string"].format(self.amounts[currency])+(" "+self.currencies[currency]["symbol"] if self.currencies[currency]["symbol"] != "" else "")

class GameComponent(serialize.SimpleSerializable):
	def tick_update(self):
		pass

class Building(GameComponent):
	building_id=""
	building_name=building_id
	building_name_plural=building_name+"s"
	desc_text=""
	color="#ffffff"
	cost={}
	def __init__(self):
		root.game.currencypool.add_currency(
			self.building_id,
			self.building_name,
			self.desc_text,
			self.color,
			False,
			False,
			None,
			self.building_name_plural,
			["building"])
		root.game.renderer.add_directive(rendering.BuildingRenderingDirective(self))

	def tick_update(self):
		if root.game.currencypool.get_amount(self.building_id)>0:
			self.tick_many(root.game.currencypool.get_amount(self.building_id))
			[self.tick_each() for x in range(root.game.currencypool.get_amount(self.building_id))]

	def attempt_buy(self, *a):
		for k, v in self.cost.items():
			if root.game.currencypool.get_amount(k)<v:
				browser.alert("You don't have enough "+root.game.currencypool.get_name(k)+" (need "+str(v)+")")
				return False
		for k, v in self.cost.items():
			root.game.currencypool.add_amount(k, -v)
		root.game.currencypool.add_amount(self.building_id, 1)

	def attempt_sell(self, *a):
		if root.game.currencypool.get_amount(self.building_id)>0:
			for k, v in self.cost.items():
				root.game.currencypool.add_amount(k, v)
			root.game.currencypool.add_amount(self.building_id, -1)

	def tick_each(self):
		pass

	def tick_many(self, count):
		pass

@serialize.register_serializable
class Game(serialize.SimpleSerializable):
	export_vars=["currencypool", "components", "upgrades"]
	def __init__(self):
		self.currencypool=CurrencyPool()
		self.components={}
		self.managers={}
		self.renderer=rendering.Renderer()
		self.upgrades=[]

	def tick_update(self):
		try:
			for component in self.components:
				self.components[component].tick_update()
			for component in self.managers:
				self.managers[component].tick_update()
			self.renderer.update()
		except BaseException as e:
			print(e)

	@property
	def noscope_chance_manual(self):
		chance=0.1
		if "aimbot" in self.upgrades: chance+=0.1
		if "multiclient" in self.upgrades: chance*=2
		return chance