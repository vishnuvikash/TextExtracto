pdf_name_list=['1.pdf','2.pdf','3.pdf','4.pdf','5.pdf','6.pdf','7.pdf']

import PyPDF2

'''
pdf_file=open('7.pdf','rb')

read_pdf=PyPDF2.PdfFileReader(pdf_file)
nPages=read_pdf.getNumPages()
page=read_pdf.getPage(21)#have to write a loop over here.
page_content=page.extractText()
page_content
'''

import re

#gives line by line output of the extracted Data
def get_pdf_content_lines(pdf_file_path):
        with open(pdf_file_path,'rb') as f:
               pdf_reader = PyPDF2.PdfFileReader(f)
               for page in pdf_reader.pages: 
                   for line in page.extractText().splitlines():
                       yield line

#the text contains all extracted information
count=0
text=''
for i in pdf_name_list:
        for line in get_pdf_content_lines(i):
           text+=line
           a="@"
           text+=a
        count+=1
        text=text[:-16]
        text=text.replace("Date / Time@Incident Number@Location@Nature@Incident ORI@","")
        text=text.replace("NORMAN POLICE DEPARTMENT@Daily Incident Summary (Public)@","")
        text=text.replace("Daily Incident Summary (Public)@NORMAN POLICE DEPARTMENT@","")

#all Incidents first row column values are found using regex and added thorn in front of it
#in order to identify each column

Incidents=re.findall(r'\d/\d{2}/\d{4}\s\d{1,2}:\d{2}',text)
for i in Incidents:
        if i in text:
               y='þ'
               y+=i
               text=text.replace(i,y)

# with similar column values þ is some time is added more than once, removing those þ's with #single þ
countP=re.findall(r'þ*þ',text)

               
for i in countP:
        if i in text:
        	text=text.replace(i,'þ')
		

countA=re.findall(r'@*@',text)
               
for i in countA:
        if i in text:
               text=text.replace(i,'@')
#removing the first þ so that now all the values within þ relates to each Incident information
text=text[1:]


#print(text)

#spliting by þ and storing each Incident info in seperate row of list

incident_info1=text.split('þ')
print(len(incident_info1))
incident_info=[i for i in incident_info1 if len(i)!=0]
print(len(incident_info))
#getting list of rows which is l here 
# intentionally added @ so that we can seperate each field from others and #identify null spaces 
count=0
count1=0
l=[]
temp1=[]
for i in incident_info:
        c=re.findall(r'@',i)
        i=i[:-1]
        temp=i.split('@')
        count=len(temp)
        #temp1=[]
        if(count==3):
               temp1=[count1+1,temp[0],' ',' ',temp[1],temp[2]]
        elif(count==5):
               temp1=[count1+1,temp[0],temp[1],temp[2],temp[3],temp[4]]
        elif(count==6):
               join=temp[2]+temp[3]
               temp1=[count1+1,temp[0],temp[1],join,temp[4],temp[5]]
        l.insert(count1,temp1)
        count1+=1

for i in l:
	print(i)
#       
'''
for i in l:
        print(i)
'''        
