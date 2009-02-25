import os
import sys


class PluginHandler:
    def __init__(self, filename):
        self.name = filename.split('.')[0] #TODO basename
        self.module = None
        self._instance = False
        self._do_import()

    def _do_import(self):
        '''Does the dirty stuff with __import__'''
        old_syspath = sys.path
        try:
            sys.path = [os.curdir, 'plugins']
            self.module = __import__(self.name, globals(), locals(), ['plugin'])
        except ImportError, e:
            print 'error loading', self.name
            print '-->', e
        finally:
            sys.path = old_syspath

    def instanciate(self):
        '''Instanciate (if not already done). 

        You shouldn't need this, but you can use it for performance tweak.

        '''
        if self._instance:
            return self._instance
        try:
            self._instance = self.module.Plugin()
        except:
            self._instance = None

        return self._instance

    def start(self):
        '''Instanciate (if necessary) and starts the plugin.
        @return False if something goes wrong, else True.
        '''
        self.instanciate()
        if not self._instance:
            return False
        try:
            self._instance.start()
        except:
            print "errore nello start di", self.name
            return False
        return True
            
    def stop(self):
        '''Stop the plugin, of course'''
        if self.active:
            self._instance.stop()

    def is_active(self):
        '''@return True if an instance exist and is started. False otherwise'''
        if not self._instance:
            return False
        return self._instance.is_active()

class PackageHandler:
    '''Abstraction over a package.
    Will be useful to work in the same way with plugins and packages.
    '''
    def __init__(self, directory):
        '''@param directory The directory containing the package'''
        self.name = directory
        self._instance = False #we are not instancing it
        self._do_import()

    def _do_import(self):
        '''Does the dirty stuff with __import__'''
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

    def instanciate(self):
        '''Instanciate (if not already done). 
        You shouldn't need this, but you can use it for performance tweak.
        '''
        if self._instance:
            return self._instance
        try:
            self._instance = self.module.plugin.Plugin()
        except:
            self._instance = None

        return self._instance

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
            self._instance.stop()

    def is_active(self):
        '''@return True if an instance exist and is started. False otherwise'''
        if not self._instance:
            return False
        return self._instance.is_active()


for root, d, f in os.walk('plugins'):
    dirs = d
    files = f
    break #SOOOO UGLY!

plugins = {}


for directory in [x for x in dirs if not x.startswith('.')]:
    try:
        mod = PackageHandler(directory)
        plugins[directory] = mod
    except Exception, e:
        print 'Exception while importing %s:\n%s' % (directory, e)

for file in [x for x in files if x.endswith('.py')]:
    try:
        mod = PluginHandler(file)
        plugins[directory] = mod
    except Exception, e:
        print 'Exception while importing %s:\n%s' % (directory, e)


for package in plugins.values():
    print package.name, package.is_active()

for package in plugins.values():
    print package.name, package.is_active(), '-->',
    package.start()
    print package.is_active(), package.module

