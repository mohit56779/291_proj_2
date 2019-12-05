import re

def parseXml():
    inp = input('Please input the name of the .xml in the format <filename.xml> to build: ')
    # opening the file to read in 'r' mode
    file = open(inp)
    # creating and opening files to write in 'w' mode
    file1 = open('terms.txt','w')
    file2 = open('emails.txt','w')
    file3 = open('dates.txt','w')
    file4 = open('recs.txt','w')    
    
    start = False
    end = False
    
    lines = [] 
    
    for line in file:
     
        r1= line.find("<mail>")
        r2 = line.find("</mail>")
        if r1!= -1:
            start = True
        if r2 != -1:
            end = True
        if start == True:
            lines.append(line)
        if end == True:
            process(lines)
            lines = []
            start = False
            end = False
            
def process(lines):
    # creating and opening files to write in 'w' mode
    file1 = open('terms.txt','a')
    file2 = open('emails.txt','a')
    file3 = open('dates.txt','a')
    file4 = open('recs.txt','a')    
   
    mail = ""
    for line in lines:
        mail = mail+ line
    
    # getting the row of the email
    row = re.findall('<row>(.*?)</row>', mail)[0]
    
    # getting subj and body strings (contains /ns) for file1
    subj = re.findall('<subj>(.*?)</subj>', mail,re.DOTALL)
    if len(subj)>0:
        subj = str(subj[0])
    else:
        subj =''
        
    body = re.findall('<body>(.*?)</body>', mail,re.DOTALL)
    
    if len(body)>0:
        body = str(body[0])
    else:
        body = ''
    # getting from field of the email for file2
    from_email = re.findall('<from>(.*?)</from>', mail,re.DOTALL)
    
    # getting to field of the email for file2
    to = re.findall('<to>(.*?)</to>', mail,re.DOTALL)

    # getting cc field of the email for file2    
    cc = re.findall('<cc>(.*?)</cc>', mail,re.DOTALL)
    
    # getting bcc field of the email for file2    
    bcc = re.findall('<bcc>(.*?)</bcc>', mail,re.DOTALL)
    
    # getting date field of the email for file3
    date = re.findall('<date>(.*?)</date>', mail,re.DOTALL)
    
    # using re to split subj and body into words (whitespace,\n) , add these checks (',', . , ; , !, ?)
    #print(subj,body)
    
    subj = re.findall(r"[0-9a-zA-Z_-]+",subj)
    body = re.findall(r"[0-9a-zA-Z_-]+",body)
    
    
    # writing on file1
    for word in subj:
        # here check if the word is as per requirement and convert to lowercase
        if len(word.strip())>2 and re.match('[0-9a-zA-Z_-]',word) and word!= 'amp' and word!= 'apos' and word!= 'quot':
    
            file1.write('s-' + word.lower() +":" + row + '\n')
  
    for word in body:
        #check again
        if len(word.strip())>2 and re.match('[0-9a-zA-Z_-]',word)and word!= 'amp' and word!= 'apos' and word!= 'quot':
           
            file1.write('b-' + word.lower() +":" + row + '\n')
            
    # writing in file2
   
    if len(from_email)>0 and from_email[0] != '':
        split_list = from_email[0].split(',')
        for item in split_list:

            file2.write('from-' + item.lower() + ":" + row + "\n")
            
    if len(to)>0 and to[0] != '':
        split_list = to[0].split(',')
        for item in split_list:
            file2.write('to-' + item.lower() + ":" + row + "\n")            
        
    if len(cc)>0 and cc[0] != '':
        split_list = cc[0].split(',')
        for item in split_list:
            file2.write('cc-' + item.lower() + ":" + row + "\n") 
            
    if len(bcc)>0 and bcc[0] != '':
        split_list = bcc[0].split(',')
        for item in split_list:
            file2.write('bcc-' + item.lower() + ":" + row + "\n") 
            
            
    # writing in file3
    if len(date)>0:
        file3.write(date[0] + ":" + row + "\n")
    # writing in file4
    file4.write(row+ ":" +  mail)
    
if __name__ == "__main__":
    parseXml()
    
    
   
