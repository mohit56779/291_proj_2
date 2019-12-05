import re


def processRecord(output, opmode):
    opmode = opmode.mode

    if opmode == 'brief':

        row = re.findall('<row>(.*?)</row>', str(output))[0]
        subj = re.findall('<subj>(.*?)</subj>', str(output))[0]

        print("**************************")

        print("row:" + row)
        print("subj:" + subj)
    else:

        row = re.findall('<row>(.*?)</row>', str(output))[0]
        date = re.findall('<date>(.*?)</date>', str(output))[0]
        from_ = re.findall('<from>(.*?)</from>', str(output))[0]
        to = re.findall('<to>(.*?)</to>', str(output))[0]
        cc = re.findall('<cc>(.*?)</cc>', str(output))[0]
        bcc = re.findall('<bcc>(.*?)</bcc>', str(output))[0]
        subj = re.findall('<subj>(.*?)</subj>', str(output))[0]
        body = re.findall('<body>(.*?)</body>', str(output))[0]

        # replacing xml characters
        body = body.replace("&#10;", "\n")
        body = body.replace("&lt;", "<")
        body = body.replace("&gt;", ">")
        body = body.replace("&amp;", "&")
        body = body.replace("&apos;", "'")
        body = body.replace('&quot;', '"')

        print("*************************\n")

        print("row:" + row)
        print("date:" + date)
        print("subj:" + subj)
        print("from:" + from_)
        print("to:" + to)
        print("cc:" + cc)
        print("bcc:" + bcc)
        print("body:" + body)
