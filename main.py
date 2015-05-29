import browser
import browser.timer
print=browser.console.log
print("Loading...")

import global_holder
global_holder.init()
from global_holder import root

import serialize
from browser import document

serialize.init()
import game
import rendering
import example_buildings
import resources
import json
import traceback
import random

from browser.local_storage import storage as local_storage

root.game=game.Game()
resources.init_all()
root.game.managers["weedfarm"]=example_buildings.WeedFarm()
root.game.managers["dankturret"]=example_buildings.DankTurret()
root.game.renderer.add_directive(rendering.UpgradeRenderingDirective())

browser.timer.set_interval(root.game.tick_update, 100)

def on_acquire_click(e):
	root.game.currencypool.add_amount("weed", 1)
	if random.random()<root.game.noscope_chance_manual:
		root.game.currencypool.add_amount("noscopes", 1)

document["cheat_add_weedfarm"].bind("click", lambda e:root.game.currencypool.add_amount("weedfarm", 1))
document["acquire_weed"].bind("click", on_acquire_click)

def save_session(e):
	try:
		save=serialize.save(root.game)
		print(save)
		local_storage["save"]=json.dumps(save)
	except BaseException as e: traceback.print_exc()
def load_session(e):
	try:
		data=json.loads(local_storage["save"])
		print(data)
		root.game=serialize.load(data, root.game)
	except BaseException as e: traceback.print_exc()
document["save_session"].bind("click", save_session)
document["load_session"].bind("click", load_session)
rendering.setup_tabs(("buildings", "upgrades"))

del document["loading_memo"]