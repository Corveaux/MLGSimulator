from global_holder import root
def create_cost_string(cost):
	string=""
	for k,v in cost.items():
		string+=str(v)+" "+root.game.currencypool.get_name(k)+" & "
	string=string[:-3]
	return string