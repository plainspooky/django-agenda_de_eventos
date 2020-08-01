def split_str_date(date_as_string):
    """
    Transforma a data em 'YYYY-MM-DD' em uma tupla de três valores para
    utilizar na visão de eventos de um determinado dia.
    """
    year, month, day, *__ = date_as_string.split("-")
    return year, month, day
