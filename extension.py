_registry = {} #'CategoryName': ['list', 'of', 'components']
_classes = {} #'ComponentName': <class 'Component'>
_instances = {} #'ComponentName': <Component object>

def category_register(category):
    '''Add a category to the registry'''
    _registry[category] = []

def register(category, cls):
    '''Register cls as an Extension for category. 
    If the category doesn't exist, it creates it(but returns False).
    It doesn't instanciate that class immediately
    @return False if the category didn't exist. Probably you made a mistake, True otherwise.
    '''
    class_name = _get_class_name(cls)
    _classes[class_name] = cls

    try:
        _registry[category].append(class_name)
    except KeyError:
        category_register(category)
        _registry[category].append(class_name)
        return False #check this: probably that category doesn't exist (or it's not well-declared)
    
    return True
    #note: we shouldn't immediately instanciate it

def get_extensions(category):
    '''return a list of ready-to-use extension instances'''
    return [_instance_of(class_name) for class_name in _registry[category]]

def get_default(category)::
	'''return ONE extension instance. It will be chosen with preferences'''
	#put here your choosing logic (preferences)
	available = get_extensions(category)
	if available:
		return available[0] #that's just a test: you should choose better
	return None

def _instance_of(class_name):
    '''Given a class name, will return a ready-to-use instance. 
    Every "trick" (hey, only if necessary), will be done here.
    '''
    if class_name in _instances:
        return _instances[class_name]

    instance = _classes[class_name]()
    _instances[class_name] = instance
    return instance

def _get_class_name(cls):
    '''Returns the full name of a class: module.class
    For instances, call get_full_name(self.__class__)'''
    return '.'.join([cls.__module__, cls.__name__])

