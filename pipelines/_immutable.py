# Ref: https://www.python.org/dev/peps/pep-0351/

def freeze(obj):
    try:
        hash(obj)
        return obj
    except TypeError:
        freezer = getattr(obj, '__freeze__', None)
        if freezer:
            return freezer()
        raise TypeError('object is not freezable')


class imdict(dict):
    def __hash__(self):
        return id(self)

    def _immutable(self, *args, **kws):
        raise TypeError('object is immutable')

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    update = _immutable
    setdefault = _immutable
    pop = _immutable
    popitem = _immutable


class xdict(dict):
    def __freeze__(self):
        return imdict(self)
