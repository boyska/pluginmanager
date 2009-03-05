import pluginmanager
import extension
from interfaces.bar import IBar

class DoThings:
    def __init__(self):
        extension.category_register('bar', IBar)
        extension.category_register('xyz')
        extension.category_register('magic')
    
    def do_x(self):
        for extra in extension.get_extensions('bar'):
            try:
                print 'bar', extra
                extra.bar()
            except:
                print 'NW', extra

things = DoThings()
plugin_manager = pluginmanager.PluginManager()
plugin_manager.scan_directory('plugins')
for plug in plugin_manager.get_plugins():
    plugin_manager.plugin_start(plug)
things.do_x()

