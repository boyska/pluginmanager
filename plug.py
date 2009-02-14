'''plug.py: implementation of emesene2 component architecture

Meta-plugin API inspired in trac component architecture.
Features less magic behavior and more awesomeness.

This is RFC code, and as such, I've documented implementation details 
extensively. Enjoy

Meant to extend the GUI and run all the code in the main loop - that means,
this is not thread safe in any way. This is not a problem for external
plugins, since the calls are made from the extension point, but these points
can't be defined and run in a thread. [Strictly speaking the GIL allows doing
that dirty stuff between threads but I'll assume that nobody with SVN access
is stupid enough to do such things]
In short, don't use this with e3.

We tried to avoid metaclasses and magic behavior and failed.
State is global, the three variables below.
Components are singletons because otherwise extension points wouldn't work.

There are two steps to initialize a component. Just to leave it clear:
-ComponentMeta.__new__ does *class* initialization, such as adding to the
 clases dict and registering to each interface
-Component.__new__ does *instance* initialization. It handles singletons,
 returning either a new instance or a saved one. It also calls the
 original class __init__

The metaclass __new__ is run after the class block is parsed, while the other
two are run when the object is instantiated.
'''

# Association of interfaces to a list of class names:
#  {<Interface identifier>: ['Component', ...], ...}
registry = {}
# trac equivalent: ComponentMeta._registry (dict)

# Association of class names to class objects
#  {'ClassName': <class 'Component'>, ...}
classes = {}
# trac equivalent: ComponentMeta._components (list)

# Association of class names to instance objects:
#  {'Component': <Component object at 0x...>, ...}
instances = {}
# trac equivalent: ComponentManager().components (dict)


def get_full_name(cls):
    '''Returns the full name of a class: module.class
    For instances, call get_full_name(self.__class__)'''
    return '.'.join([cls.__module__, cls.__name__])


class Interface(object):
    '''Base class for interfaces.
    
    This isn't really required. The registry keys above could be subclasses of
    Interface (with documented methods), strings (for informally specified
    interfaces, e.g. preliminary sketching or debug), or anything with an id()
    That being said, I believe using subclasses is the way to go, otherwise we
    would suffer of the same shortcomings as string exceptions.
    '''
    def __init__(self):
        print dir(self)
        print get_full_name(self)

class ComponentMeta(type):
    '''Meta class for components

    Provides some of the magic behavior of components:
    - Adds the class to the global dict "classes",
    - Registers it with the implemented interfaces ("registry")
    - Moves the __init__ method to __user_init__ (see Component.__new__)
    '''

    def __new__(cls, name, bases, d):
        print "ComponentMeta.__new__(): ",

        d['__user_init__'] = d.get('__init__', lambda x: None)
        d['__init__'] = lambda x: None

        new_class = type.__new__(cls, name, bases, d)

        full_name = get_full_name(new_class)
        print full_name
        print "bases",bases

        if name == 'Component':
            return new_class
        
        classes[full_name] = new_class
        
        for interface in d.get('implements', ()):
            print "Appending", full_name, "to", interface
            registry.setdefault(interface, []).append(full_name)
        
        return new_class
    

class Component(object):
    '''Base class for components
    
    The __new__ method handles singleton behavior.
    Any __init__ is moved to __user_init__ by the metaclass, so that it is
    only called when the instance is new.
    '''

    __metaclass__ = ComponentMeta

    # A tuple or list of interface identifiers
    implements=()

    def __new__(cls, *args, **kwargs):
        full_name = get_full_name(cls)

        print "Component.__new__() ", full_name,

        self = instances.get(full_name)
        if self is None:
            self = super(Component, cls).__new__(cls, *args, **kwargs)
            print "first instance"
            instances[full_name] = self
            self.__user_init__()
        else:
            print "returning old instance"
            
        return self

class ExtensionPoint(property):
    '''A property that returns a list of instances of components
    implementing an interface.'''

    def __init__(self, interface):
        property.__init__(self, self.fget)
        self.interface = interface

    def fget(self, component):
        print 'ExtensionPoint.fget: ', registry[self.interface]
        return [classes[x]() for x in registry[self.interface]]

class ExtensionPoint(property):
    '''A property that returns a list of instances of components
    implementing an interface.'''

    def __init__(self, interface):
        property.__init__(self, self.fget)
        self.interface = interface

    def fget(self, component):
        print 'ExtensionPoint.fget: ', registry[self.interface]
        return [classes[x]() for x in registry[self.interface]]


