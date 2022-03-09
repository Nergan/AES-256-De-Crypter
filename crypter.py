import pyAesCrypt
import time
import os

def timePrint(txt, pause=0.01):
    l1 = len(txt)
    l2 = l1 - 1
    
    for i in range(l1):
        if i != l2:
            print(txt[i], end='', flush=True)
            time.sleep(pause)
        else:
            print(txt[i], flush=True)
            
def timeInput(txt, pause=0.01):
    l1 = len(txt)
    l2 = l1 - 1
    
    for i in range(l1):
        print(txt[i], end='', flush=True)
        if i != l2:
            time.sleep(pause)
            
    return input()

# функция шифрования файла
def encryption(file, password):
    buffer_size = 512 * 1024 # размер буфера

    try:
        # шифрование
        pyAesCrypt.encryptFile(str(file),
                               str(file) + '.crp',
                               password,
                               buffer_size)
        
        os.remove(file)
        timePrint(os.path.splitext(file)[0].split('\\')[-1] + ' зашифрован')
        return True
    except:
        timePrint(os.path.splitext(file)[0].split('\\')[-1] + ' ОШИБКА')
        return False

# функция дешифровки файла
def decryption(file, password):
    buffer_size = 512 * 1024 # размер буфера

    try:
        # расшифровывание
        pyAesCrypt.decryptFile(str(file),
                               str(os.path.splitext(file)[0]),
                               password,
                               buffer_size)
        
        os.remove(file)
        timePrint(os.path.splitext(file)[0].split('\\')[-1] + ' расшифрован')
        return True
    except:
        timePrint(os.path.splitext(file)[0].split('\\')[-1] + ' ОШИБКА')
        return False

# функция сканирования директорий
def walking_by_files_dirs(dir, password, cryptFunction):
    
    res = []
    for data in os.walk(dir):
        for file in data[-1]: 
            if os.path.abspath(data[0] + '\\' + file) == os.path.abspath(__file__) and cryptFunction == encryption:
                
                cmd = timeInput('Ты хочешь зашифровать файл ЭТОЙ программы? (Y/N): ').lower()
                while cmd not in {'y', 'n'}:
                    timePrint('Неизвестная команда')
                    cmd = timeInput('Ты хочешь зашифровать файл ЭТОЙ программы? (Y/N): ').lower()
                    
                if cmd == 'n':
                    timePrint(file + ' пропущен')
                    continue
                    
            res += [cryptFunction(data[0] + '\\' + file, password)]
    
    timePrint('------------------------\nПапка ' + ('зашифрована:' if cryptFunction == encryption else 'расшифрована:') + ' успешно ' + str(res.count(True)) + ' из ' + str(len(res)) + ' файлов')

def sizeDir(dir):
    
    fileCount = 0
    for data in os.walk(dir):
        fileCount += len(data[-1])
        
    return fileCount

def act(dir, cryptFunction):
    if os.path.isfile(dir):

        if os.path.abspath(dir) == os.path.abspath(__file__) and cryptFunction == encryption:
            cmd = timeInput('Ты хочешь зашифровать файл ЭТОЙ программы? (Y/N): ').lower()
            while cmd not in {'y', 'n'}:
                timePrint('Неизвестная команда')
                cmd = timeInput('Ты хочешь зашифровать файл ЭТОЙ программы? (Y/N): ').lower()
                
            if cmd == 'n':
                return
            
        password = timeInput('Введите пароль для ' + ('шифрования: ' if cryptFunction == encryption else 'расшифровки: '))
        cryptFunction(dir, password)
            
    else:
        timePrint('Идёт расчёт времени ' + ('шифрования' if cryptFunction == encryption else 'расшифровки') + ' папки...')
        
        time = sizeDir(dir)//60
        cmd = timeInput(('Шифрование' if cryptFunction == encryption else 'Расшифровка') + ' папки составит примерно ' + str(time) + ' минут. Продолжить? (Y/N): ')
        while cmd not in {'y', 'n'}:
            timePrint('Неизвестная команда')
            cmd = timeInput(('Шифрование' if cryptFunction == encryption else 'Расшифровка') + ' папки составит примерно ' + str(time) + ' минут. Продолжить? (Y/N): ')
        
        if cmd == 'y':
            password = timeInput('Введите пароль для ' + ('шифрования: ' if cryptFunction == encryption else 'расшифровки: '))
            walking_by_files_dirs(dir, password, cryptFunction)
        else:
            timePrint('Действие отменено')

while True:
    
    mode = timeInput('Введите 0 чтобы зашифровать или 1 чтобы расшифровать: ')
    while mode not in {'0', '1'}:
        timePrint('Неверно введён режим работы программы')
        mode = timeInput('Введите 0 чтобы зашифровать или 1 чтобы расшифровать: ')
    mode = int(mode)
    
    dir = timeInput('Введите ' + ('шифруемый' if mode == 0 else 'расшифровываемый') + ' файл или папку: ')
    
    if not os.path.isfile(dir) and not os.path.isdir(dir):
        timePrint(dir + ' не найден(а)')
        continue
        
    if mode:
        act(dir, decryption)
    else:
        act(dir, encryption)