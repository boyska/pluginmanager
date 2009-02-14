import plug


class Bar:
    def __init__(self):
        print 'constructing bar'
    def do_it(self):
        print 'bar rulez'

class BarComponent(plug.Component):
    implements = (('Extra',))
    constructor = Bar

class Xyz:
    def __init__(self):
        print 'constructing xyz'
        pass
    def do_it(self):
        print 'xyz rulez'

class XyzOmponent(plug.Component):
    implements = (('Extra', ))
    constructor = Xyz


class Foo:
    extern = plug.ExtensionPoint('Extra')
    
    def __init__(self, x):
        self.x = x
        self.extras = []


    def run(self):
        print 'E', self.extern
        print 'E0', self.extern[0]

        for i in self.extern:
            self.extras.append(i.constructor())

        print self.extras
        for i in self.extras:
            i.do_it()
    


if __name__ == '__main__':
    f = Foo(5)
    f.run()
