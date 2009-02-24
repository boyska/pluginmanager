import extension

class Bar:
    def __init__(self):
        print 'constructing bar'
    def do_it(self):
        print 'bar rulez'

class Xyz:
    def __init__(self):
        print 'constructing xyz'
    def do_it(self):
        print 'xyz rulez'

class Foo:
    def __init__(self, x):
        self.x = x
        self.extras = []
        extension.category_register('foo_category')


    def run(self):
        for extra in extension.get_extensions('foo_category'):
            extra.do_it()

if __name__ == '__main__':
    f = Foo(5)
    #these should be done in the plugin class
    if not extension.register('fo_category', Bar):
        print 'u-oh! the category doesn t exist'
    extension.register('foo_category', Xyz)
    f.run()
