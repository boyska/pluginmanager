from plugin_base import PluginBase
import extension

class WrongFoo(PluginBase):
    implements = ('IFoo')
    def __init__(self):
        PluginBase.__init__(self)
    
    def dont_foo(self):
        print "I'm Foo and, well, I can foo-ize"

class Plugin(PluginBase):
    def __init__(self):
        PluginBase.__init__(self)

    def start(self):
        try:
            self.extensions_register()
        except ValueError:
            print "WrongFoo: I don't agree to the required interface"

    def extensions_register(self):
        extension.register('foo', WrongFoo)
