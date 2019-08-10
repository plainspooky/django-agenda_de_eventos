def split_date(string_date):
    """Transforma a data em YYYY-MM-DD em uma tupla de três valores para
    utilizar na visão de eventos de um determinado dia."""
    for value in string_date.split("-"):
        yield int(value)
