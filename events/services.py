def split_date(string_date, date_format="{:%Y-%m-%d}"):
    """
    Transforma a data em YYYY-MM-DD em uma tupla de três valores para
    utilizar na visão de eventos de um determinado dia.
    """
    return tuple([int(i) for i in date_format.format(string_date)])
