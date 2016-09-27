class Service:
    """
    Service singleton implementation.

    """

    def __new__(cls, **kw):
        try:
            return cls._instance
        except AttributeError as e:
            cls._instance = super().__new__(cls)
        return cls._instance
