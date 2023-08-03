import os


DIR_PATH = '/home/mssql/data/'
FILE_TO_COMPARE = '/home/admin/compare_file.txt'

NUM = 100000000000

EMAIL = 'in@kompromiss.ru'


def open_file(path: str) -> dict:
    result = dict()
    with open(path) as file:
        for line in file:
            key, value = line.split()
            result[key] = value
    return result


def get_files_size(path: str) -> dict:
    list_of_files = os.listdir(path)
    result = dict()
    for elem in list_of_files:
        size = os.path.getsize(f'{DIR_PATH}{elem}')
        result[elem] = size
    return result


def check_compare_file():
    if not os.path.exists(FILE_TO_COMPARE):
        with open(FILE_TO_COMPARE, 'x'):
            pass


def main():
    check_compare_file()

    size_to_compare = open_file(FILE_TO_COMPARE)
    new_size = get_files_size(DIR_PATH)

    new_info = ''
    result = ''
    for key in new_size.keys():
        new_info = new_info + f'{key} {new_size.get(key)}\n'
        if key in size_to_compare:
            if new_size.get(key) // NUM > int(size_to_compare.get(key)) // NUM:
                result = result + new_info

    if result != '':
        os.system(f'mail -s "sql" {EMAIL} <<< "{result}"')

    info = open(FILE_TO_COMPARE, 'w')
    info.writelines(new_info)
    info.close()


if __name__ == '__main__':
    main()
