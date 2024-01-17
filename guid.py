import winreg
import pprint
# import shutil

select_server = ''
# эта строка ищется в файле 1cv8strt.pfl
# нам нужна инфа со след строки
ANCHOR = '{"S","http://srv1c/ib/ws"}'
GUID_LEN = 45
GUID_LEN_1C = 36


def get_user_info(server: str):
    def get_path_to_roaming():
        try:
            user_path = path + '\\' + user_guid + '\\fdeploy'
            user_directs = winreg.OpenKeyEx(remote_comp_location, user_path)
            directs = winreg.QueryInfoKey(user_directs)
            # получаем количество локальных папок пользователя
            directs_number = directs[0]

            for direct_num in range(directs_number):
                direct = winreg.EnumKey(user_directs, direct_num)
                direct_path = user_path + '\\' + direct
                key = winreg.OpenKeyEx(remote_comp_location, direct_path)
                a = winreg.QueryValueEx(key, 'PathEffective')
                path_to_roaming = a[0]
                if 'Roaming' in path_to_roaming:
                    path_to_cache = path_to_roaming + '\\1C\\1cv8'
                    return path_to_cache
                else:
                    continue
        except FileNotFoundError:
            print('error roaming')

    def get_user_name():
        try:
            # дополняем путь, для получения имени пользователя
            user_path = path + '\\' + user_guid
            # получаем ключ для доступа в папку пользователя в реестре
            user_directs = winreg.OpenKeyEx(remote_comp_location, user_path)
            # получаем информацию из нужного ключа
            key_info = winreg.QueryValueEx(user_directs, 'ProfileImagePath')
            path_to_user = key_info[0]
            # приводим к нужному виду
            split_user_path = path_to_user.split('\\')
            return split_user_path[2]
        except FileNotFoundError:
            print('error user')

    result = []
    location = winreg.HKEY_LOCAL_MACHINE
    path = r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList'
    # get access to the registry of a remote computer
    remote_comp_location = winreg.ConnectRegistry(server, location)
    # link to registry key profile list
    profile_list = winreg.OpenKeyEx(remote_comp_location, path)
    # get the number of users
    profiles = winreg.QueryInfoKey(profile_list)
    users_number = profiles[0]
    print(f'количество пользователей: {users_number}')
    for profile_num in range(users_number):
        # получаем гуид каждого пользователя в реестре
        user_guid = winreg.EnumKey(profile_list, profile_num)
        # нам нужны гуиды клиентов, они определенной длинны
        if len(user_guid) == GUID_LEN:
            # result.append(get_path_to_roaming())
            result.append([get_user_name(), get_path_to_roaming()])
    return result


def main():
    def find_line():
        try:
            path_to_file = path + '\\1cv8strt.pfl'
            try:
                file = open(path_to_file, 'r')
                lines = file.readlines()
                for index, line in enumerate(lines):
                    if ANCHOR in line:
                        necessary_line = (lines[index + 1])
                        return {user: necessary_line[6:-4]}
                else:
                    return {user: path_to_file}
            except PermissionError:
                return {user: 'нет доступа'}
        except FileNotFoundError:
            return {user: 'файл не найден'}

    result = []
    users_info = get_user_info(select_server)
    for user, path in users_info:
        result.append(find_line())

    my_file = open(f'C:\\ibases\\{select_server}.txt', 'w+')
    for line in result:
        my_file.write(f'{str(line)}\n')
    my_file.close()



if __name__ == '__main__':
    main()
