import os 

def see_default():
	print(os.getcwd())
	with open(os.getcwd()+'/skins/default.txt', 'r', encoding="utf8") as f:
		return f.read()
