class Service:
    """
    Service singleton implementation.

    """

    @classmethod
    def factory(cls, **kwargs):
        return super().__new__(cls)

    def __new__(cls, **kw):
        try:
            return cls._instance
        except AttributeError as e:
            cls._instance = cls.factory(**kw)
        return cls._instance
