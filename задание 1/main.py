#  Перевод заданных чисел в другие системы счисления.


def get_parts (number: str):                                #  По заданию требуется работать с дробными числами,
    integral_part, fractional_part = '0', '0'               #  эта функция возвращает информацию о том, дробное ли число,
    number = str(number)                                    #  и его целую и дробную части.
    is_fraction = bool(number.count('.'))
    dot_position = number.find('.')
    match is_fraction:
        case True:
            integral_part = number[:dot_position]
            fractional_part = '0' + number[dot_position:]
        case False:
            integral_part, fractional_part = number, '0'
    return integral_part, fractional_part, is_fraction


#  Первый этап. Перевод числа в десятичную систему счисления для последующих преобразований.

#  Метод перевода:
#  Сначала число разбивается на разряды. Единицы - разряд 0, десятки - 1 и т. д.
#  Разряды после запятой идут на убывание: десятые - разряд -1, сотые - -2 и т. д.
#  Потом для каждого разряда производятся вычисления по формуле "число * основание ** разряд"
#  В процессе результаты полученные для целой части складываются,
#  результаты для дробной части складываются и записываются после запятой.


def from_any_to_dec(number: str, base_from: int) -> str:

    if base_from == 10:                  #  Оптимизируем)
        return number
    
    def digit_to_int(digit: str) -> int:  #  Данная функция определяет значение цифр 
        symbols = '0123456789ABCDEF'      #  в системах счисления с основанием больше 10.
        number = symbols.find(digit)
        return number

    #  Перевод целой части.

    integral_part, fractional_part, is_fraction = get_parts(number)
    place = len(integral_part) - 1
    value = 0
    result = ''
    for digit in integral_part:
        value = value + digit_to_int(digit) * base_from ** place
        place -= 1
    result = str(value)

    #  Перевод дробной части, если она есть.

    if is_fraction:
        value = 0
        dot_position = fractional_part.find('.')
        for digit in fractional_part[dot_position + 1:]:
            value = value + digit_to_int(digit) * base_from ** place
            place -= 1
        result = result + '.' + str(value)[dot_position + 1:]
    return result


#  Второй этап. Перевод числа из десятичной системы счисления необходимую.

#  Метод перевода:
#  Целая часть числа в десятичной системе делится на основание системы, в которую нужно перевести число.
#  Остаток от деления записывается, а целая часть, получившаяся в результате, снова делится.
#  Остатки записываются в обратном порядке. Процесс повторяется, пока в целой части чиса не останется ноль.
#  Дробная часть числа умножается на основание системы, в которую необходимо перевести число.
#  Целая часть результата записывается, дробная - снова умножается, числа записываются в естественном порядке
#  Процесс повторяется, пока в результате умножения не получится целое число, не станет ясно,
#  что дробь переодична или пока не будет достигнута необходимая точность.

def from_dec_to_any(number: str, base_to: int) -> str:

    if base_to == 10:                       # Снова оптимизируем)
        return number

    def int_to_digit(integer: int) -> str:  #  Данная функция определяет запись числа 
        symbols = '0123456789ABCDEF'        #  в системах счисления с основанием больше 10.
        digit = symbols[integer]
        return digit
        

    # Перевод целой части.

    integral_part, fractional_part, is_fraction = get_parts(number)
    result = ''
    while int(integral_part) != 0:
        result = int_to_digit(int(integral_part) % base_to) + result
        integral_part = int(integral_part) // base_to
    
    #  Перевод дробной части, если она есть.

    if is_fraction:
        result += '.'
        frac_part_of_frac = fractional_part
        while float(frac_part_of_frac) != 0.0:
            if len(result) > 20:
                break
            fractional_part = float(fractional_part) * base_to            
            int_part_of_frac, frac_part_of_frac, is_fraction = get_parts(fractional_part)
            result += int_to_digit(int(int_part_of_frac))
            fractional_part = frac_part_of_frac
    return result



# Функция перевода чисел из системы в систему, которая позволяет избежать громозких записей.

def from_any_to_any(number: str, base_from: int, base_to: set):     #  В качестве каждого аргумента можно передать любое количество значений.
    base_to = sorted(base_to)                                       #  Компульсивная сортировка)

    print('Число ', number, '(' + str(base_from) + '-ная система) в других системах счисления:')

    X_dec = (from_any_to_dec(number, base_from))                     #  Перевод в десятичную систему для последующего использования.
    
    for item in base_to:                                             #  Всё обёрнуто в цикл, чтобы не плодить одинаковые строки.
        if base_from == item:                                        #  Компульсивная проверка ради оптимизации)
            continue
        result = from_dec_to_any(X_dec, item)                        #  Перевод полученного десятичного значения в нужные системы.
        print('c основанием ' + str(item) + ':', result)
    print('\n')


# Задание переменных, вызов функций.


def main():

    numbers = {'110011.001' : 2, '24.4' : 8, '125.375' : 10, 'DA.3' : 16}  #  Задание значений можно оформить через input,
    base_to = {2, 8, 10, 16}                                               #  и получить калькулятор для массового перевода чисел.

    for number in numbers.keys():
        from_any_to_any(number, numbers.get(number), base_to)
    

if __name__ == '__main__':
    main()

#  Вот и всё, теперь ни ячейки памяти, ни коды процессора не страшны.
