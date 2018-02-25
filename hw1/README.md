### SuperDict

Ваша задача - написать класс, который будет расширять возможности стандартого словаря

- Класс может инициализироваться
  - путём к json-файлу с ключами: `sd = SuperDict('data.json')`. json-файл может содержать несколько строк. Если ключи в строках будут повторяться, то необходимо оставить последнее встретившееся значение 
  - путём к csv-файлу: `sd = SuperDict('data.csv')`. Первая колонка файла содержит ключ, вторая - значения. Если в строке больше двух колонок - эту строчку следует пропустить и написать сообщение об ошибке  
  - другим словарём: `my_dict = {'a':1, 'b':2}; sd = SuperDict(my_dict)`
- Должны присутствовать методы стандартного словаря: `__getitem__, clear, items, keys, values, iteritems, iterkeys, itervalues, __iter__, __eq__, __len__`
- Метод случайного поиска ключа: `SuperDict.get_random_key()`
- Метод, возвращающий длину максимального ключа
- Метод, позволяющий складывать словари: `SuperDict('data.json') + SuperDict('new_data.json')`
- Методы сохранения данных в файл: `SuperDict.to_csv('export.csv')` и `SuperDict.to_json('export.json')`
- Метод, возвращающий ключи, которые начинаются с переданного аргумента: `SuperDict.get_key_starts_from('abc')`

### FileTree

Написать функцию `file_tree(path, file_filter=None)`, которая рекурсивно обходит каталог. Если в качестве `path` передан файл, то достаточно вывести только его. Если аргумент `file_filter` не `None`, то на последнем уровне должны остаться файлы, которые заканчиваются подстрокой `file_filter`. Пример:

```Subdirectory 1:
  file11
  file12
  Sub-sub-directory 11:
    file111
    file112
Subdirectory 2:
  file21
  sub-sub-directory 21
  sub-sub-directory 22
    sub-sub-sub-directory 221
      file 2211```
