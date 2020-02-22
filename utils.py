
import collections
import json

class Configuration(collections.MutableMapping):

    def __init__(self, param=None):
        keys = ['alpha', 'beta', 'theta']
        self.__data = {k: None for k in keys}

        if type(param) is str:
            # TODO: read config from a file.
            pass

        if type(param) is dict:
            assert params.keys() = self.__data.keys()
            for p, v in params.items():
                self.__data[p] = v

    def __eq__(self, tgt):
        return tgt.keys() == self.__data.keys()

    def __getitem__(self, key):
        return self.__data[key]

    def keys(self):
        return self.__data.keys()

    def __len__(self):
        return len(self.__data)

    def __iter__(self):
        return iter(self.__data)

    def __delitem__(self):
        raise NotImplementedError

    def __setitem__(self, k, v):
        if k not in self.__data:
            raise KeyError(k)
        self.__data[k] = v

    def __contains__(self, k):
        return k in self.__data


    def dump(self, f):
        #json.dump(self.__data, f)
        f.write(self.dumps())

    def dumps(self):
        # TODO: make prettier format. 
        return json.dumps(self.__data)