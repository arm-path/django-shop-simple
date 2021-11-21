# Функция - Проверяет на целочисленный тип данных.
def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False