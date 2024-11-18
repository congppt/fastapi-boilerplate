def extend(cls):
    """Add fucntion to non-builtin class"""
    def _decorator(f):
        setattr(cls, f.__name__, f)
    return _decorator