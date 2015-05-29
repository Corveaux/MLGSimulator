from browser import document
from global_holder import root
from browser import html
from upgrades import upgrades
import util
import browser

class RenderingDirective(object):
	def setup(self):
		pass
	def update(self):
		pass

class CountRenderingDirective(RenderingDirective):
	internal_containter_id=""
	resource_id=""
	def update(self):
		document[self.internal_containter_id].text=root.game.currencypool.get_string(self.resource_id)

class ResourceRenderingDirective(CountRenderingDirective):
	def __init__(self, resource_id):
		self.resource_id=resource_id
		self.internal_containter_id="SimpleTempRenderingDirective:"+self.resource_id
	def setup(self):
		container=html.DIV(Id=self.internal_containter_id, style={"color":root.game.currencypool.get_color(self.resource_id)})
		document["resources-pane"] <= container

class BuildingRenderingDirective(RenderingDirective):
	def __init__(self, controller):
		self.controller=controller
		self.resource_id=controller.building_id
		self.internal_containter_id="BuildingRenderingDirective:"+self.resource_id

	def setup(self):
		container=html.DIV()

		text_container=html.DIV(Id=self.internal_containter_id, style={"color":root.game.currencypool.get_color(self.resource_id), "font-weight":"bold"})

		table=html.TABLE()
		row=html.TR()
		buybutton=html.BUTTON()
		buybutton <= "Buy "+root.game.currencypool.get_name(self.resource_id)
		buybutton <= text_container
		buybutton.title=root.game.currencypool.get_desc(self.resource_id)
		buybutton.bind("click", self.controller.attempt_buy)
		buycell=html.TD()
		buycell <= buybutton
		row <= buycell

		sellbutton=html.BUTTON()
		sellbutton <= "Sell"
		sellbutton.bind("click", self.controller.attempt_sell)
		sellcell=html.TD()
		sellcell <= sellbutton
		row <= sellcell
		table <= row

		container <= table

		document["switchable-window-content-buildings"] <= container

	def update(self):
		document[self.internal_containter_id].text=root.game.currencypool.get_value_string(self.resource_id)

class UpgradeRenderingDirective(RenderingDirective):
	def setup(self):
		self.cache_upgrades=[-1]
		#self.update()
		
		
		#self.update()

	
	def _produce_click_handler(self, upgrade_id):
		def _internal(e):
			for k, v in upgrades[upgrade_id]["cost"].items():
				if root.game.currencypool.get_amount(k)<v:
					# browser.alert("You don't have enough "+root.game.currencypool.get_name(k)+" (need "+str(v)+")")
					return False
			for k, v in upgrades[upgrade_id]["cost"].items():
				root.game.currencypool.add_amount(k, -v)
			# print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
			root.game.upgrades.append(upgrade_id)
			self.cache_upgrades=[-1]
			# print("Added "+upgrade_id)
			# print("root.game.upgrades="+str(root.game.upgrades))
			self.update()
		# print("created a _internal for "+upgrade_id)
		return _internal

	def update(self):
		# print("Updating UpgradeRenderingDirective")
		# print("root.game.upgrades="+str(root.game.upgrades))
		# print("self.cache_upgrades="+str(self.cache_upgrades))
		if root.game.upgrades!=self.cache_upgrades:
			# print("UpgradeRenderingDirective is rerendering")
			self.cache_upgrades=root.game.upgrades
			document["switchable-window-content-upgrades"].clear()
			# print(list(upgrades.keys()))
			for upgrade in list(upgrades.keys()):
				ok=True
				for req in upgrades[upgrade].get("required",[]):
					if req not in self.cache_upgrades:
						# print("req "+req+" not satasfied for "+upgrade+", skipping")
						ok=False
				if ok:
					# print("Adding "+upgrade)
					button=html.BUTTON()
					# print("created button")
					button<=html.DIV("Buy "+upgrades[upgrade]["name"],
						style={"color":upgrades[upgrade]["color"], "font-weight":"bold"},
						title=upgrades[upgrade]["desc"])
					button<=html.DIV(util.create_cost_string(upgrades[upgrade]["cost"]))
					# print("added divs")
					if upgrade in self.cache_upgrades: button.disabled=1
					# print("disabled if reqd")
					button.bind("click", self._produce_click_handler(upgrade))
					# print("bound")
					document["switchable-window-content-upgrades"]<=button
					document["switchable-window-content-upgrades"]<=html.BR()

class Renderer(object): #DONT SERIALIZE THIS!
	def __init__(self):
		self.directives=[]

	def add_directive(self, directive):
		print("Adding directive "+str(directive))
		self.directives.append(directive)
		directive.setup()
		directive.update()

	def update(self):
		[d.update() for d in self.directives]

def _build_switch_click_callback(id):
	def _internal(e):
		document.get(selector=".switchable-window-content-selected")[0].Class="switchable-window-content"
		document["switchable-window-content-"+id].Class="switchable-window-content-selected"
	return _internal

def setup_tabs(ids):
	for id in ids:
		document["switch-pane-"+id].bind("click", _build_switch_click_callback(id))