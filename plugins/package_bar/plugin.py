import extension
from plugin_base import PluginBase
import bar

class Plugin(PluginBase):
    def __init__(self):
        PluginBase.__init__(self)
        pass
    def extensions_register(self):
        print bar.Bar
        extension.register('bar_category', bar.Bar)
