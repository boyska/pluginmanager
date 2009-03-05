from plugin_base import PluginBase
import extension

class Foo(PluginBase):
    def __init__(self):
        PluginBase.__init__(self)
    
    def do_foo(self):
        print "I'm Foo and, well, I can foo-ize"

class Plugin(PluginBase):
    def __init__(self):
        PluginBase.__init__(self)

    def start(self):
        self.extensions_register()

    def extensions_register(self):
        extension.register('foo', Foo)
