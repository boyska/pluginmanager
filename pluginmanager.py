'''Handles plugin importing'''
import os
import sys


class PluginHandler:
    '''Abstraction over a plugin.
    
    Given a filename, will import it and allows to control it.

    '''
    def __init__(self, filename):
        '''constructor'''
        self.name = filename.split('.')[0] #TODO basename
        self.module = None
        self._instance = None
        self._do_import()

    def _do_import(self):
        '''Does the dirty stuff with __import__'''
        old_syspath = sys.path
        try:
            sys.path = [os.curdir, 'plugins']
            self.module = __import__(self.name, globals(), locals(), ['plugin'])
        except ImportError, reason:
            print 'error loading', self.name
            print '-->', reason
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
        except Exception:
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
        except Exception:
            print "errore nello start di", self.name
            return False
        return True
            
    def stop(self):
        '''Stop the plugin, of course'''
        if self._instance and self.is_active():
            self._instance.stop()

    def is_active(self):
        '''@return True if an instance exist and is started. False otherwise'''
        if not self._instance:
            return False
        return self._instance.is_active()


class PackageResource:
    def __init__(self, base_dir, directory):
        self.path = directory #'''Path to the package'''
        self.base_path = base_dir
        self._resources = [] #Ope ned resources

    def _get_resource_path(self, relative_path):
        '''get the path to the required resource.
        @return the path if it exists or an empty string otherwise'''
        abs_path = os.path.join(self.base_path, self.path, relative_path)
        if os.path.exists(abs_path):
            return abs_path
        return ''

    #TODO: context manager
    def get_resource(self, relative_path):
        '''Opens a file.
        @param relative_path A path starting from the package dir
        @return a file object opening relative_path if it is possible, or None.
        '''
        file_path = self._get_resource_path(relative_path)
        if not file_path:
            return None
        try:
            f = open(file_path)
        except IOError:
            return None
        else:
            self._resources.append(f)
            return f
    
    def close_resource(self, resource):
        '''Close a file.
        @param resource A resource returned by get_resource
        @return 
        '''
        try:
            self._resources.remove(resource)
            resource.close()
        except IOError:
            return False

        return True

    def close(self):
        '''everything. to be called when the plugin is stopped'''
        for resource in self._resources:
            self._resources.remove(resource) #TODO: check if this is buggy
            resource.close()
            

class PackageHandler:
    '''Abstraction over a plugin.
    
    Given a directory, will import the plugin.py file inside it and allows to control it.
    It will provide the plugin several utilities to work on the package

    '''
    def __init__(self, base_dir, directory):
        '''@param directory The directory containing the package'''
        self.name = directory
        self.directory = directory
        self.base_dir = base_dir
        self._instance = None #we are not instancing it

        self.module = None
        self._do_import()

    def _do_import(self):
        '''Does the dirty stuff with __import__'''
        old_syspath = sys.path
        try:
            sys.path = ['.', self.base_dir]
            self.module = __import__(self.directory, globals(), None, ['plugin'])
            self.module = self.module.plugin
        except Exception, reason:
            print 'error when importing package', self.name
            print reason
            self.module = None
        finally:
            sys.path = old_syspath

    def instanciate(self):
        '''Instanciate (if not already done). 
        You shouldn't need this, but you can use it for performance tweak.
        '''
        if self._instance is not None:
            return self._instance
        try:
            self._instance = self.module.Plugin()
        except Exception:
            self._instance = None
        else:
            self._instance.resource = PackageResource(self.base_dir, self.directory)
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
        except Exception:
            print "errore nello start di", self.name
            return False
        return True
            
    def stop(self):
        '''If active, stop the plugin'''
        if self.is_active():
            self._instance.stop()
            self._instance.resource.close()

    def is_active(self):
        '''@return True if an instance exist and is started. False otherwise'''
        if not self._instance:
            return False
        return self._instance.is_active()


class PluginManager:
    '''Scan directories and manage plugins loading/unloading/control'''
    def __init__(self):
        self._plugins = {} #'name': Plugin/Package
    
    def scan_directory(self, dir_):
        '''Find plugins and packages inside dir_'''
        dirs = files = []
        for root, directories, files in os.walk(dir_):
            dirs = directories
            files = files
            break #sooo ugly
        
        for directory in [x for x in dirs if not x.startswith('.')]:
            try:
                mod = PackageHandler(dir_, directory)
                self._plugins[mod.name] = mod
            except Exception, reason:
                print 'Exception while importing %s:\n%s' % (directory, reason)
        
        for filename in [x for x in files if x.endswith('.py')]:
            try:
                mod = PluginHandler(filename)
                self._plugins[mod.name] = mod
            except Exception, reason:
                print 'Exception while importing %s:\n%s' % (filename, reason)
    
    def plugin_start(self, name):
        '''Starts a plugin.
        @param name The name of the plugin. See plugin_base.PluginBase.name.
        '''
        if not name in self._plugins:
            return False
        self._plugins[name].start()
        return True
    
    def plugin_stop(self, name):
        '''Stops a plugin.
        @param name The name of the plugin. See plugin_base.PluginBase.name.
        '''
        if not name in self._plugins:
            return False
        self._plugins[name].stop()
        return True

    def plugin_is_active(self, name):
        '''Check if a plugin is active.
        @param name The name of the plugin. See plugin_base.PluginBase.name.
        @return True if loaded and active, else False.
        '''
        if not name in self._plugins:
            return False
        self._plugins[name].is_active()
        return True
    
    def get_plugins(self):
        return self._plugins.keys()
