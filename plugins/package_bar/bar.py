import extension

class Bar:
    print 'bar is parsed'
    def __init__(self):
        print 'bar is running'
    def bar(self):
        print 'bar will bar'
        print ' # extension can be extended! ;)'
        for extra in extension.get_extensions('foo'):
            try:
                print 'foo', extra
                extra.do_foo()
            except Exception, reason:
                print 'NW', extra, reason

