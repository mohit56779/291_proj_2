import difflib
import xmlParser
import time
def main():
    inp = input("Make sure to run phase1 with the xml file you wish to test before testing for correctness.\nThe test uses difflib to test differences and time to test speed.\n\nType 1 to test for 10 entries correctness and 2 to test for 1k entries correctness\nand type 3 to test for speed: ")
    if inp == str(1):
        test_10()
    elif inp == str(2):
        test_1k()
    elif inp == str(3):
        test_speed()
        
def test_speed():
    inp = input("type the number of times you wanna multiple 10.xml (enteries = 10 times that): ")
    
    content = open('10.xml').read()
    
    file = open('file.xml', 'w+')
    
    for i in range(0,int(inp)):
        file.write(content)
        
    start = time.time()
    print("Type 'file.xml' below to test")
    xmlParser.main()
    end = time.time()
    
    print("time taken to parse xml : " + str(end - start))
        
    
    
    
    
        
def test_10():   
    # testing dates.txt
    print('testing dates')
    
    inp = 'dates.txt'
    inp2 = 'result-10-dates.txt'
    
    text1 = open(inp).readlines()
    text2 = open(inp2).readlines()  
    
    for line in difflib.unified_diff(text1, text2):
        print(line) 
        
    
    print('testing terms.txt')    
    inp = 'terms.txt'
    inp2 = 'result-10-terms.txt'
    
    text1 = open(inp).readlines()
    text2 = open(inp2).readlines()  
    
    for line in difflib.unified_diff(text1, text2):
        print(line)     
        
        
        
    print('testing recs.txt')   
    inp = 'recs.txt'
    inp2 = 'result-10-recs.txt'
    
    text1 = open(inp).readlines()
    text2 = open(inp2).readlines()  
    
    for line in difflib.unified_diff(text1, text2):
        print(line)  
    
    print('testing emails.txt')   
    inp = 'emails.txt'
    inp2 = 'result-10-emails.txt'
    
    text1 = open(inp).readlines()
    text2 = open(inp2).readlines()  
    
    for line in difflib.unified_diff(text1, text2):
        print(line) 
        
def test_1k():   
    # testing dates.txt
    print('testing dates')
    
    inp = 'dates.txt'
    inp2 = 'result-1k-dates.txt'
    
    text1 = open(inp).readlines()
    text2 = open(inp2).readlines()  
    
    for line in difflib.unified_diff(text1, text2):
        print(line) 
        
    
    print('testing terms.txt')    
    inp = 'terms.txt'
    inp2 = 'result-1k-terms.txt'
    
    text1 = open(inp).readlines()
    text2 = open(inp2).readlines()  
    
    for line in difflib.unified_diff(text1, text2):
        print(line)
    print('testing recs.txt')   
    inp = 'recs.txt'
    inp2 = 'result-1k-recs.txt'
    
    text1 = open(inp).readlines()
    text2 = open(inp2).readlines()  
    
    for line in difflib.unified_diff(text1, text2):
        print(line)  
        
    print('testing emails.txt')   
    inp = 'emails.txt'
    inp2 = 'result-1k-emails.txt'
    
    text1 = open(inp).readlines()
    text2 = open(inp2).readlines()  
    
    for line in difflib.unified_diff(text1, text2):
        print(line)     
       
 
    
        
  
        
 
main()
