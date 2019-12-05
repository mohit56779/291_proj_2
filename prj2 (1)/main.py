import sys
import time
import re
from bsddb3 import db
from phase1src.xmlParser import parseXml
from phase2src.indicesGen import genIndex
from phase3src.queryParser import parseCommand
from phase3src.searchGeneric import searchGeneric
from phase3src.searchDates import rangeSearchDates
from phase3src.processRecord import processRecord


if sys.version[:5] != '3.5.2':  # Safety first
    print('\n***')
    print('Warning: you are using a python version the lab machines are not')
    print('Your version is:', sys.version[:5])
    print('***\n')


class BDB:
    def __init__(self, idxFilePath):
        self.db = db.DB()

        # auto-connect
        self.db.open(idxFilePath)
        self.cursor = self.db.cursor()

    def disconnect(self):
        self.db.close()
        self.cursor.close()


class currModeTracker:
    def __init__(self):
        self.mode = "brief"


def interface(currMode):
    print("\nEnter 'exit' to leave program")
    rawInputStr = input('Query: ')  # uncomment before commits

    if rawInputStr.lower().strip() == "exit":
        print("exiting...\n")
        sys.exit(0)
    elif rawInputStr.lower().strip() == "output=full":
        currMode.mode = "full"
        return "None"
    elif rawInputStr.lower().strip() == "output=brief":
        currMode.mode = "brief"
        return "None"
    else:
        return parseCommand(rawInputStr)


def driver(currMode):
    # 1) Open db connections from generated indices folder
    datesDB = BDB('./_temp_/da.idx')
    emailDB = BDB('./_temp_/em.idx')
    recsDB = BDB('./_temp_/re.idx')
    termsDB = BDB('./_temp_/te.idx')

    # 2) Get raw queries
    parsedCommand = interface(currMode)
    if parsedCommand == "None":
        return

    # 3) Search
    if not parsedCommand['queries']:
        raise ValueError("No valid command found")

    resultIDs, setsIntersected = set(), 0
    for query in parsedCommand['queries']:
        subIDs, key, withWildCard = set(), None, False

        # Terms
        if query['field'] in ['subj', 'body', 'subj/body']:
            if 'wc' in query and query['wc']:
                withWildCard = True

            if query['field'] == 'subj/body':
                subIDs = searchGeneric(
                    "s-" + query['arg'], termsDB.cursor, withWildCard)
                subIDs = subIDs.union(searchGeneric(
                    "b-" + query['arg'], termsDB.cursor, withWildCard))
            else:
                if query['field'] == 'subj':
                    key = "s-" + query['arg']
                elif query['field'] == 'body':
                    key = "b-" + query['arg']
                subIDs = searchGeneric(key, termsDB.cursor, withWildCard)

        # Dates
        if query['field'] == 'date':
            if query['datePrefix'] == ':':
                subIDs = searchGeneric(query['arg'], datesDB.cursor)
            elif query['datePrefix'] in ['<=', '>=']:
                # find equality first
                subIDs = searchGeneric(query['arg'], datesDB.cursor)
                query['datePrefix'] = '<' if query['datePrefix'] == '<=' else '>'
                # then range search
                subIDs = subIDs.union(
                    rangeSearchDates(query, datesDB.cursor))
            else:  # >, <
                subIDs = rangeSearchDates(query, datesDB.cursor)

        # Emails
        if query['field'] in ['from', 'to', 'cc', 'bcc']:
            subIDs = searchGeneric(
                query['field'] + "-" + query['arg'], emailDB.cursor)

        # Finally, intersect with the result ID set (AND logic policy)
        if setsIntersected < 1:
            resultIDs = subIDs
            setsIntersected += 1
        else:
            resultIDs = resultIDs.intersection(subIDs)
            if not resultIDs:  # if any two sets have no intersection break
                resultIDs = set()
                break
            setsIntersected += 1

    # 4) Format Print Output
    for i in resultIDs:
        record = recsDB.db.get(str.encode(i.strip()))
        processRecord(record, currMode)
    print("Found {0} records".format(len(resultIDs)))

    # 5) Close db connections
    datesDB.disconnect()
    emailDB.disconnect()
    recsDB.disconnect()
    termsDB.disconnect()


if __name__ == "__main__":
    parseXml()
    genIndex()
    time.sleep(2)

    currMode = currModeTracker()

    while True:
        try:
            driver(currMode)
        except ValueError as e:
            print(e)
