def extend(cls):
    """Add fucntion to class"""
    def _decorator(f):
        setattr(cls, f.__name__, f)
    return _decorator