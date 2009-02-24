import extension
import bar

class Plugin:
	def __init__(self):
		pass
	def extensions_register(self):
		print bar.Bar
		extension.register('bar_category', bar.Bar)
