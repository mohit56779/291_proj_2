import re
from subprocess import Popen
from glob import glob


    
## index building code
   
def buildIndexFromPhase2():
    commands = ["cat ../recs.txt | sort -u | perl ../break.pl | db_load -T -t hash -c dupsort=1 re.idx",                                                         "cat ../terms.txt | sort -u | perl ../break.pl | db_load -T -t btree -c dupsort=1 te.idx",
               "cat ../emails.txt | sort -u | perl ../break.pl | db_load -T -t btree -c dupsort=1 em.idx",
               "cat ../dates.txt | sort -u | perl ../break.pl | db_load -T -t btree -c dupsort=1 da.idx"]
    for cmd in commands:
        p = Popen(cmd, shell = True)

def buildIndexFromMain():
    commands = ["cat recs.txt | sort -u | perl break.pl | db_load -T -t hash -c dupsort=1 ./_temp_/re.idx",                                                      "cat terms.txt | sort -u | perl break.pl | db_load -T -t btree -c dupsort=1 ./_temp_/te.idx",
               "cat emails.txt | sort -u | perl break.pl | db_load -T -t btree -c dupsort=1 ./_temp_/em.idx",
               "cat dates.txt | sort -u | perl break.pl | db_load -T -t btree -c dupsort=1 ./_temp_/da.idx"]
    for cmd in commands:
        p = Popen(cmd, shell = True)


def genIndex():
    mode = input("\nWhere is this program being run from? <m-->Main function/p-->Phase 2 Function>: ")
    try:
        response = input("\nBuilding index files... WARNING!! All index files in the current directory will be deleted. Proceed? <y/n>: ")
        if response == "y":
            
            if mode == "m":
                Popen("rm -f ./_temp_/*.idx", shell = True)
                buildIndexFromMain()
            else:
                Popen("rm -f *.idx", shell = True)
                buildIndexFromPhase2()

            print("\nAll files have been prepped and indexes have been built successfully!")
        elif response == "n":
            quit()
    except IOError as io:
        print("\nThe file %s does not exist within the current Directory. Please ensure the file exists and try again" %filename)
    except OSError as os:
        print("\nOne or more of the specified files do not exist within the current Directory. Please ensure that all the files exist and try again")
    


            


if __name__ == '__main__':
    # xmlParser.parseXml()
    genIndex()
    
    