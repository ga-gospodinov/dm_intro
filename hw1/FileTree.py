import os

def file_tree(Path, file_filter=None, num_of_space=0):
    for element in os.listdir(Path):
        NewPath = Path + '/' + element
        if os.path.isdir(NewPath):
            print(num_of_space * '\t' + element)
            file_tree(NewPath, file_filter, num_of_space=(num_of_space + 1))
        elif file_filter == None or element.endswith(file_filter):
            print(num_of_space * '\t' + element)


Path = input('enter dir: ')
Filter = input('enter filter: ')
file_tree(Path, Filter)