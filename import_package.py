import os

for root, d, files in os.walk('.'):
    dirs = d
    break #SOOOO UGLY!

plugins = {}
for directory in [x for x in dirs if not x.startswith('.')]:
    print 'D', directory
    
    try:
        mod = __import__(directory, globals(), None, ['plugin'])
    except Exception, e:
        print 'Exception while importing %s:\n%s' % (directory, e)

    plugins[directory] = mod

print plugins

