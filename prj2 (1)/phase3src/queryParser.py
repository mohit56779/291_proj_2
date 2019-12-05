import re


def parseCommand(command):
    # 0. Get mode
    parsedCommand = {
        'opmode': 'brief',
        'queries': []
    }

    if command.find("output=full") != -1:
        parsedCommand['opmode'] = 'full'
        command = command.replace("output=full", "")
    else:
        command = command.replace("output=brief", "")

    # Define: AlphaNumeric
    alphanumeric = "[0-9a-zA-Z_-]"

    # Define: Date
    date = "\d{4}/\d{2}/\d{2}"
    datePrefix = "date\s*(>|>=|:|<=|<)"
    dateQueryRegex = "({0}\s*{1})".format(datePrefix, date)

    # 1. Get Date terms
    dateTerms = re.findall(dateQueryRegex, command)
    if dateTerms:
        parsedCommand['queries'] += [dateTerm[0] for dateTerm in dateTerms]
        for dateTerm in dateTerms:
            command = command.replace(dateTerm[0], "")  # remove date commands

    # Define: Email
    email = "([a-zA-Z0-9._-]+@({0}+\.)+{0}+)".format(alphanumeric)
    emailPrefix = "(from|to|cc|bcc)\s*:"
    emailQueryRegex = "({0}\s*{1})".format(emailPrefix, email)

    # 2. Get Email terms
    emailTerms = re.findall(emailQueryRegex, command)
    parsedCommand['queries'] += [query[0] for query in emailTerms]
    for email_term in emailTerms:
        command = command.replace(email_term[0], "")  # remove email commands

    # Define: Term
    term = "{0}".format(alphanumeric)
    termPrefix = "(subj|body)\s*:"
    termSuffix = "%"
    termQueryRegex = "({0}?\s*{1}+{2}?)".format(termPrefix, term, termSuffix)

    # 3. Get Term terms
    termTerms = re.findall(termQueryRegex, command)
    parsedCommand['queries'] += [query[0] for query in termTerms]
    for term in termTerms:
        command = command.replace(term[0], "")

    # 4. Post parse each component for a better search format
    parsedCommand['queries'] = \
        [parseQuery(q) for q in parsedCommand['queries']]

    # 5. Find and append Wildcarded/Non-Wildcarded Solo Terms last
    command = command.strip()
    soloTermRegex = "{0}+%?".format(alphanumeric)
    soloTerms = re.findall(soloTermRegex, command)
    for i in range(len(soloTerms)):
        soloTermTransform = {'field': 'subj/body',
                             'arg': soloTerms[i], 'wc': False}

        if soloTerms[i] and soloTerms[i][-1] == '%':
            soloTermTransform['arg'] = soloTerms[i][:-1] # remove %
            soloTermTransform['wc'] = True

        soloTerms[i] = soloTermTransform
    parsedCommand['queries'] += soloTerms

    return parsedCommand


def parseQuery(query):
    validFields = set(['date', 'subj', 'body', 'from', 'to', 'cc', 'bcc'])
    query = query.lower().replace(" ", "")  # enforce case-sensitivity
    field, arg, datePrefix, res = None, None, None, {}

    for i in range(len(query)):
        if query[i] == ':':
            field, arg = query[:i], query[i+1:]
            if field not in validFields:
                raise ValueError('Illegal query')
            elif field == 'date':
                res['field'], res['arg'], res['datePrefix'] = field, arg, ':'
            else:
                if query[-1] == '%':
                    res['wc'] = True
                    arg = arg[:-1] # remove last % wildcard
                res['field'], res['arg'], res['datePrefix'] = field, arg, None
            return res

        elif query[i] == '<':
            if query[i+1] == '=':
                field, arg, datePrefix = query[:i], query[i+2:], '<='
            else:
                field, arg, datePrefix = query[:i], query[i+1:], '<'

            if field not in validFields:
                raise ValueError('Illegal query')

            res['field'], res['arg'], res['datePrefix'] = field, arg, datePrefix
            return res

        elif query[i] == '>':
            if query[i+1] == '=':
                field, arg, datePrefix = query[:i], query[i+2:], '>='
            else:
                field, arg, datePrefix = query[:i], query[i+1:], '>'

            if field not in validFields:
                print('Illegal query')
                return

            res['field'], res['arg'], res['datePrefix'] = field, arg, datePrefix
            return res
