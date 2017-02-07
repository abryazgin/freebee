import models


class MetaModelFactory(type):
    def __getattr__(self, item):
        return getattr(models, item)


class ModelFactory(metaclass=MetaModelFactory):
    def __getattr__(self):
        pass
