import rendering

resources={
	"weed":{
		"currency":"weed",
		"name":"Weed",
		"desc":"dankest of the dank",
		"color":"#00ff00",
		"allow_negative":False,
		"show_if_empty":True,
		"cap":None,
		"symbol":"fl. oz.",
		"format_string":"{:.2f}"
	},
	"noscopes":{
		"currency":"noscopes",
		"name":"Noscopes",
		"desc":"nubs uv rekt",
		"color":"#222222",
		"allow_negative":False,
		"show_if_empty":True,
		"cap":None
	}
}

from global_holder import root
def init_currency(name):
	root.game.currencypool.add_currency(**resources[name])
	root.game.renderer.add_directive(rendering.ResourceRenderingDirective(resources[name]["currency"]))

def init_all():
	[init_currency(n) for n in resources]