def searchGeneric(key, cursor, searchByPrefixWildcard=False):
    """ 
    given a key (x-y:ID) and a db cursor, return a set of all matching IDs
    """
    if searchByPrefixWildcard:
        return searchWithWildcard(key, cursor)
    return searchNoWildcard(key, cursor)


def searchNoWildcard(key, cursor):
    """ 
    given a key returns all ids 
    """
    IDs = set()
    iterator = cursor.first()
    while iterator and iterator[0].decode("utf-8") != key:
        iterator = cursor.next()

    if iterator != None:
        while iterator and iterator[0].decode("utf-8") == key:
            IDs.add(iterator[1].decode("utf-8"))
            iterator = cursor.next()
    return IDs


def searchWithWildcard(key, cursor):
    """ 
    behaves like searchInTerm but with prefix wildcard matching, and with one key
    """
    IDs = set()
    iterator = cursor.first()
    while iterator and not iterator[0].decode("utf-8").startswith(key):
        iterator = cursor.next()

    if iterator != None:
        while iterator and iterator[0].decode("utf-8").startswith(key):
            IDs.add(iterator[1].decode("utf-8"))
            iterator = cursor.next()
    return IDs
