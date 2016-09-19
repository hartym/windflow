class Service:
    def __new__(cls):
        try:
            return cls._instance
        except AttributeError as e:
            cls._instance = super().__new__(cls)
        return cls._instance
