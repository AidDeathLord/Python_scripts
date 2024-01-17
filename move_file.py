import shutil
import os
import time
from datetime import date


# имя файла
file = ''
# из какой папки переместить файл
path_from = ''
# куда переместить файл
path_in = ''
# через сколько дней удалить
daysToDelete = 7


today = date. today()
# перемещение файла
try:
    shutil.move(f'{path_from}\\{file}',
                f'{path_in}\\{file}')

    filename = os.path.splitext(os.path.basename(f'{path_in}\\{file}'))[0]
    os.rename(f'{path_in}\\{file}',
              f'{path_in}\\{filename}{today}.txt')
except FileNotFoundError:
    print('нет файлов')

current_time = time.time()
for dirpath, _, filenames in os.walk(path_in):
    for f in filenames:
        fileWithPath = os.path.abspath(os.path.join(dirpath, f))
        creation_time = os.path.getctime(fileWithPath)
        print("file available:", fileWithPath)
        if (current_time - creation_time) // (24 * 3600) >= daysToDelete:
            os.unlink(fileWithPath)
        else:
            continue
