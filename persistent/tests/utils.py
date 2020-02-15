
class TrivialJar(object):
    """
    Jar that only supports registering objects so ``_p_changed``
    can be tested.
    """

    def register(self, ob):
        """Does nothing"""

class ResettingJar(object):
    """Testing stub for _p_jar attribute.
    """
    def __init__(self):
        from persistent import PickleCache # XXX stub it!
        from persistent.interfaces import IPersistentDataManager
        from zope.interface import directlyProvides
        self.cache = self._cache = PickleCache(self)
        self.oid = 1
        self.registered = {}
        directlyProvides(self, IPersistentDataManager)

    def add(self, obj):
        import struct
        obj._p_oid = struct.pack(">Q", self.oid)
        self.oid += 1
        obj._p_jar = self
        self.cache[obj._p_oid] = obj


    # the following methods must be implemented to be a jar

    def setstate(self, obj):
        # Trivial setstate() implementation that just re-initializes
        # the object.  This isn't what setstate() is supposed to do,
        # but it suffices for the tests.
        obj.__class__.__init__(obj)

class RememberingJar(object):
    """Testing stub for _p_jar attribute.
    """
    def __init__(self):
        from persistent import PickleCache # XXX stub it!
        self.cache = PickleCache(self)
        self.oid = 1
        self.registered = {}

    def add(self, obj):
        import struct
        obj._p_oid = struct.pack(">Q", self.oid)
        self.oid += 1
        obj._p_jar = self
        self.cache[obj._p_oid] = obj
        # Remember object's state for later.
        self.obj = obj
        self.remembered = obj.__getstate__()


    def fake_commit(self):
        self.remembered = self.obj.__getstate__()
        self.obj._p_changed = 0

    # the following methods must be implemented to be a jar

    def register(self, obj):
        self.registered[obj] = 1

    def setstate(self, obj):
        # Trivial setstate() implementation that resets the object's
        # state as of the time it was added to the jar.
        # This isn't what setstate() is supposed to do,
        # but it suffices for the tests.
        obj.__setstate__(self.remembered)
