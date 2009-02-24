import os

for root, d, files in os.walk('.'):
    dirs = d
    break #SOOOO UGLY!

plugins = {}

class Package:
	'''Abstraction over a package.
	Will be useful to work in the same way with plugins and packages.
	'''
	def __init__(self, directory):
		'''@param directory The directory containing the package'''
		self.name = directory
		self.module = __import__(directory, globals(), None, ['plugin'])
		self.instance = None #we are not instancing it

	def instanciate(self):
		'''Instanciate (if not already done). 
		You shouldn't need this, but you can use it for performance tweak.
		'''
		if self.instance:
			return self.instance
		try:
			self.instance = self.module.plugin.Plugin()
		except:
			self.instance = None

		return self.instance

	def start(self):
		'''Instanciate (if necessary) and starts the plugin.
		@return False if something goes wrong, else True.
		'''
		inst = self.instanciate()
		if not inst:
			return False
		try:
			inst.start()
		except:
			return False
		return True
				
	def stop(self):
		if self.active:
			self.instance.stop()
	
	def is_active(self):
		if not self.instance:
			return False
		return True
		return self.instance.active


for directory in [x for x in dirs if not x.startswith('.')]:
    print 'D', directory
    
    try:
        #mod = __import__(directory, globals(), None, ['plugin'])
        mod = Package(directory)
    except Exception, e:
        print 'Exception while importing %s:\n%s' % (directory, e)

    plugins[directory] = mod

for package in plugins.values():
	print package.name, package.is_active()

