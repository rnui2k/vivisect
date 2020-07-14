try:
    import cPickle as pickle
except ImportError:
    import pickle

import vivisect


vivsig_cpickle = 'VIV'.ljust(8,'\x00')

if isinstance(vivsig_cpickle, str):
    vivsig_cpickle = vivsig_cpickle.encode('utf-8')

def saveWorkspaceChanges(vw, filename):
    elist = vw.exportWorkspaceChanges()
    if len(elist):
        f = open(filename, 'ab')
        pickle.dump(elist, f, protocol=2)
        f.close()

def saveWorkspace(vw, filename):
    events = vw.exportWorkspace()
    vivEventsToFile(filename, events)

def vivEventsAppendFile(filename, events):
    f = open(filename, 'ab')
    # Mime type for the basic workspace
    pickle.dump(events, f, protocol=2)
    f.close()

def vivEventsToFile(filename, events):
    f = open(filename, 'wb')
    # Mime type for the basic workspace
    f.write(vivsig_cpickle)
    pickle.dump(events, f, protocol=2)
    f.close()

def vivEventsFromFile(filename):
    f = open(filename, "rb")
    vivsig = f.read(8)

    # check for various viv serial formats
    if vivsig == vivsig_cpickle:
        pass

    else: # FIXME legacy file format.... ( eventually remove )
        f.seek(0)

    events = []
    # Incremental changes are saved to the file by appending more pickled
    # lists of exported events
    while True:
        try:
            events.extend( pickle.load(f) )
        except EOFError as  e:
            break
        except pickle.UnpicklingError as  e:
            print(e)
            raise vivisect.InvalidWorkspace(filename, "invalid workspace file")

    f.close()

    # FIXME - diagnostics to hunt msgpack unsave values
    #for event in events:
        #import msgpack
        #try:
            #msgpack.dumps(event)
        #except Exception as  e:
            #print('Unsafe Event: %d %r' % event)

    return events

def loadWorkspace(vw, filename):
    events = vivEventsFromFile(filename)
    vw.importWorkspace(events)
    return

