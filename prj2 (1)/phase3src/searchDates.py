def rangeSearchDates(dateQueryObj, cursor):
    """ 
    given a date range or equality returns a list of ids
    """
    IDs = set()

    if dateQueryObj['datePrefix'] == '<':
        rangeBound = cursor.set_range(str.encode(dateQueryObj['arg']))
        iterator = cursor.first()

        while iterator and iterator[0] != rangeBound[0]:
            IDs.add(iterator[1].decode("utf-8"))
            iterator = cursor.next()

    elif dateQueryObj['datePrefix'] == '>':
        iterator = cursor.set_range(str.encode(dateQueryObj['arg']))

        while iterator:
            if iterator[0].decode("utf-8") != dateQueryObj['arg']:
                IDs.add(iterator[1].decode("utf-8"))
            iterator = cursor.next()

    return IDs
