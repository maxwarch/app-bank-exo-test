class Singleton(type):
    _instance = None  # This is an attribute of the class

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
            return cls._instance
        name = cls.__name__

        if cls._instance is not None:
            return cls._instance

        raise RuntimeError(
            f"{name} already created. use {name}.get() to get the {name} instance."
        )

    def get(cls):
        return cls._instance
