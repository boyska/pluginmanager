import os
import sys


class Package:
    '''Abstraction over a package.
    Will be useful to work in the same way with plugins and packages.
    '''
    def __init__(self, directory):
        '''@param directory The directory containing the package'''
        self.name = directory
        print os.listdir(os.curdir)
        old_syspath = sys.path
        try:
            sys.path = ['.', 'plugins']
            self.module = __import__(directory, globals(), None, ['plugin']).plugin
        except Exception, e:
            print 'error when importing package', self.name
            print e
            self.module = None
        finally:
            sys.path = old_syspath
        self.instance = False #we are not instancing it

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
            print "errore nello start di", self.name
            return False
        return True
            
    def stop(self):
        if self.active:
            self.instance.stop()

    def is_active(self):
        if not self.instance:
            return False
        return self.instance.is_active()

class Plugin:
    def __init__(self, filename):
        self.name = filename.split('.')[0] #TODO basename
        self.module = None #__import__ blablabla
        old_syspath = sys.path
        try:
            sys.path = [os.curdir, 'plugins']
            self.module = __import__(self.name, globals(), locals(), [])
        except ImportError, e:
            print 'error loading', self.name
            print '-->', e
        finally:
            sys.path = old_syspath
        self.instance = False

    def instanciate(self):
        '''Instanciate (if not already done). 
        You shouldn't need this, but you can use it for performance tweak.
        '''
        if self.instance:
            return self.instance
        try:
            self.instance = self.module.Plugin()
        except:
            self.instance = None

        return self.instance

    def start(self):
        '''Instanciate (if necessary) and starts the plugin.
        @return False if something goes wrong, else True.
        '''
        self.instanciate()
        if not self.instance:
            return False
        try:
            self.instance.start()
        except:
            print "errore nello start di", self.name
            return False
        return True
            
    def stop(self):
        if self.active:
            self.instance.stop()

    def is_active(self):
        if not self.instance:
            return False
        return self.instance.is_active()


for root, d, f in os.walk('plugins'):
    dirs = d
    files = f
    break #SOOOO UGLY!

plugins = {}
print 'FILES', files


for directory in [x for x in dirs if not x.startswith('.')]:
    try:
        mod = Package(directory)
        plugins[directory] = mod
    except Exception, e:
        print 'Exception while importing %s:\n%s' % (directory, e)

for file in [x for x in files if x.endswith('.py')]:
    try:
        mod = Plugin(file)
        plugins[directory] = mod
    except Exception, e:
        print 'Exception while importing %s:\n%s' % (directory, e)


for package in plugins.values():
    print package.name, package.is_active()

for package in plugins.values():
    print package.name, package.is_active(),
    package.start()
    print package.is_active(), package.module

