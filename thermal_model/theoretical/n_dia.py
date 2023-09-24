def day_number(dia, mes):
    """
    Calculate the n-th day of the year.

    Parameters:
    - dia (int): The chosen day (1-31).
    - mes (int): The chosen month (1-12).

    Returns:
    - day_number (int): The n-th day of the year.
    """
    dias_por_mes = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    day_number = sum(dias_por_mes[:mes]) + dia
    return day_number

if __name__ == '__main__':
    print(day_number(12, 2))
