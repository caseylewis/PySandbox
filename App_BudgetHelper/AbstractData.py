from abc import abstractmethod


class AbstractObjCommonKeys:
    NAME = 'Name'


class AbstractKeys:
    @property
    @abstractmethod
    def NAME(self):
        pass

    @property
    @abstractmethod
    def all_keys(self):
        pass

    @property
    @abstractmethod
    def required_keys(self):
        pass


class AbstractIndices:
    @property
    @abstractmethod
    def NAME(self):
        pass

    @property
    @abstractmethod
    def all_indices(self):
        pass


class AbstractDictBasedDataObject(dict):
    @property
    @abstractmethod
    def keys(self):
        pass

    @property
    @abstractmethod
    def object_name(self):
        pass

    @property
    @abstractmethod
    def idxs(self):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        # CHECK FOR ALL REQUIRED KEYS
        for key in self.keys.required_keys:
            if key not in kwargs.keys():
                raise MissingKeyError(key)

        self.default_values()

    @abstractmethod
    def default_values(self):
        pass

    def copy_from(self, copy_object):
        for key, value in copy_object.items():
            self[key] = value


class MissingKeyError(Exception):
    def __init__(self, key):
        self._key = key
        super().__init__("Missing Key Error: [{}]".format(self._key))


# if __name__ == '__main__':
#     return
