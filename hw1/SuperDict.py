import csv
import random
import json

class SuperDict(dict):
    def __init__(self, arg, field_names=['key', 'value']):
        if isinstance(arg, dict):
            for key in arg:
                self[key] = arg[key]
        elif isinstance(arg, str):
            if arg.endswith('.json'):
                with open(arg, 'r') as input:
                    data = json.load(input)
                    for key in data:
                        self[key] = data[key]
            elif arg.endswith('.csv'):
                with open(arg, newline='') as input:
                    reader = csv.DictReader(input)
                    for row in reader:
                        if len(row) > 2:
                            print('wrong .csv file!')
                        else:
                            self[row[field_names[0]]] = row[field_names[1]]

    def to_json(self, file_name='data.json'):
        with open(file_name, 'w') as File:
            json.dump(self, File)

    def to_csv(self, file_name='data.csv', field_names=['key', 'value']):
        with open(file_name, 'w') as File:
            writer = csv.DictWriter(File, delimiter=',', fieldnames=field_names)
            writer.writeheader()
            for key in self:
                writer.writerow({field_names[0]: key, field_names[1]: self[key]})
    
    '''
    методы items, keys и values реализованы как в python2: сначала генерится список значений, затем возвращается

    iteritems, iterkeys и itervalues вызывают соответственно items, keys и values родительского класса через метод super()

    методы __getitem__, clear, __iter__, __eq__, __len__ есть у родителя
    '''

    def items(self):
        return list(self.iteritems())
    
    def keys(self):
        return list(self.iterkeys())
    
    def values(self):
        return list(self.itervalues())

    def iteritems(self):
        return super(SuperDict, self).items()

    def iterkeys(self):
        return super(SuperDict, self).keys()

    def itervalues(self):
        return super(SuperDict, self).values()

    def get_random_key(self):
        keys = self.keys()
        index = random.randrange(len(keys))
        return keys[index]

    def get_key_starts_from(self, begin):
        keys = self.keys()
        return [key for key in keys if key.startswith(begin)]
    
    def __add__(self, other):
        for key in other:
            self[key] = other[key]
        return self

    def len_of_max_key(self):
        return len(max(self.keys()))

init1 = {'a':1, 'b':2, 'bc':3, 'abcd':4, 'abcde':5} 
init2 = {'a':314, 'sphere': 271828, 'BD-11':2018}
sd_1 = SuperDict(init1)
sd_1.to_csv('data.csv')
sd_1.to_json('data.json')
sd_2 = SuperDict('data.csv') + SuperDict('data.json') + SuperDict(init2)
print('keys:', end=' ')
print(sd_2.keys())
print('keys starts from \'b\':', end=' ')
print(sd_2.get_key_starts_from('b'))
print('len of max key:', end=' ')
print(sd_2.len_of_max_key())
print('random key:', end=' ')
print(sd_2.get_random_key())