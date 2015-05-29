import game, serialize
from global_holder import root

class WeedFarm(game.Building):
	building_id="weedfarm"
	building_name="Weed Farm"
	building_name_plural=building_name+"s"
	desc_text="A far m to get danker (+0.05 weed/s)"
	color="#00aa00"
	cost={"weed":10}
	def tick_many(self, count):
		root.game.currencypool.add_amount("weed", count*0.005)

class DankTurret(game.Building):
	building_id="dankturret"
	building_name="DankTurret"
	building_name_plural=building_name+"s"
	desc_text="Noscopes Nubs for noscopes (-0.05 weed/s, +0.025 noscopes/s)"
	color="#222222"
	cost={"noscopes":2}
	def tick_many(self, count):
		root.game.currencypool.add_amount("weed", -count*0.005)
		root.game.currencypool.add_amount("noscopes", count*0.0025)