
import collections
import json
import datetime

class Configuration(collections.MutableMapping):

    def __init__(self, id=None, param=None):
        keys = [
            'nrollouts']

        self.__data = {k: None for k in keys}
        self.__data['id'] = id
        self.__data['date'] = str(datetime.datetime.now())

        if type(param) is str:
            # TODO: read config from a file.
            with open(param, 'r') as f:
                line = f.readline()
                while line:
                    line = line.split(':')
                    line = [x.strip() for x in line]
                    if line[0] in self.__data.keys():
                        self.__data[line[0]] = line[1]
                    line = f.readline()

        if type(param) is dict:
            assert params.keys() == self.__data.keys()
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

    def __repr__(self):
        return 'Parameter configuration ID: {} configured at {}'.format(
            str(self.__data['id']), str(self.__data['date'])
        )

    def __str__(self):
        return ('Parameters configuration: \n  ' + 
                '\n  '.join(['{}: {}'.format(key, val) 
                for key, val in self.__data.items()]))

    def dump(self, f):
        #json.dump(self.__data, f)
        f.write(self.dumps())

    def dumps(self):
        # TODO: make prettier format. 
        return json.dumps(self.__data)