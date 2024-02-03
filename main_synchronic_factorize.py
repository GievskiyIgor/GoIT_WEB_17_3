import time
from multiprocessing import  Pool, cpu_count


def factorize(number):
    number_list = []
    for num in range(1, number+1):
        if number % num == 0:
            number_list.append(num)
    print(f'Список чисел без остатка {number_list}')

#  Синхронний запуск
def synchronic_factorize(*numbers):  
    start = time.time()
    result = []
    for num in numbers:
        print(f'Для числа: {num}')
        for i in range(1, num+1):
            if num % i == 0:
                result.append(i)
        print(f'Список чисел, которые деляться без остатка {result}')
        result = []
    return print(f'Время работы функции {time.time() - start}')

# Багатопроцесорний запуск
def factorize_pool(*numbers):  
    start = time.time()
    print(f'Количество процессоров {cpu_count()}')
    with Pool(cpu_count()) as pool:
        for num in numbers:
            print(f'Для числа: {num}')
            pool.apply_async(factorize(num))

    pool.close()
    pool.join()
    return print(f'Время работы функции {time.time() - start}')


if __name__ == '__main__':
    print('Синхронний запуск 1:')
    synchronic_factorize(128, 255, 99999, 10651060)
    print('__sync__')
    print('Синхронний запуск 2:')
    synchronic_factorize(1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999)
    print('__***__')
    print('Бгатопроцесорний запуск 1:')
    factorize_pool(128, 255, 99999, 10651060)
    print('__pool__')
    print('Бгатопроцесорний запуск 2:')
    factorize_pool(128, 255, 99999, 10651060)
    print('__***__')
    