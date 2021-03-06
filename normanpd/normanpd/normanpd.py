#!/usr/bin/env  python
# -*- coding: utf-8 -*-
import PyPDF2
import urllib.request
import re

def fetchincidents():
    u="http://normanpd.normanok.gov/content/daily-activity"
    ui="http://normanpd.normanok.gov/"
    response = urllib.request.urlopen(u)
    data = response.read()      # a `bytes` object
    text = data.decode('utf-8')
    x=re.findall(r'/file[\w|%|/|\-|]+Incident.*\.pdf',text)
    urls=[]# contains the downloadable pdf links
    count=0
    for i in x:
        y=''
        y=ui+i
        urls.insert(count,y)
        count+=1
        
    pdf_name_list=['1.pdf','2.pdf','3.pdf','4.pdf','5.pdf','6.pdf','7.pdf']

               # localUrl='/home/vishnu/Desktop/normanpd/'
    count=0
        # Downloads the pdfs in the directory
    for i in pdf_name_list:
        urllib.request.urlretrieve(urls[count],i)
        count+=1

def extractincidents():
    pdf_name_list=['1.pdf','2.pdf','3.pdf','4.pdf','5.pdf','6.pdf','7.pdf']
    
    # gives line by line output of the extracted Data
    def get_pdf_content_lines(pdf_file_path):
        with open(pdf_file_path,'rb') as f:
            pdf_reader = PyPDF2.PdfFileReader(f)
            for page in pdf_reader.pages:
                for line in page.extractText().splitlines():
                    yield line

        # the text contains all extracted information
    count=0
    text=''
    for i in pdf_name_list:
        for line in get_pdf_content_lines(i):
            text+=line
            a="@" #intentionally added for identifying the each column values which usage is used later part
            text+=a
        count+=1
        text=text[:-16] #for removing the timestamp present on each pdf on the last page
        text=text.replace("Date / Time@Incident Number@Location@Nature@Incident ORI@","")# replacing the starting row of each pdf
        text=text.replace("NORMAN POLICE DEPARTMENT@Daily Incident Summary (Public)@","")#replacing the last line of first page of each pdf
        text=text.replace("Daily Incident Summary (Public)@NORMAN POLICE DEPARTMENT@","")#some pdfs have the last line of first page in diff fashion

        # all Incidents first row column values are found using regex and added thorn in       front of it
        # in order to identify each row

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
        # removing the first þ so that now all the values within þ relates to each Incident information
    text=text[1:]
        # print(text)

        # spliting by þ and storing each Incident info in seperate row of list
	#even though after removing extra thorns still there were few cases below two lines solves the problem
    incident_info1=text.split('þ')
        # print(len(incident_info1))
    incident_info=[i for i in incident_info1 if len(i)!=0]
        # print(len(incident_info))
        # getting list of rows which is l here
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
            # temp1=[] code for solving basically 3 type of rows possible in pdfs and data extraction from each of them
        if(count==3): 
            temp1=[count1+1,temp[0],' ',' ',temp[1],temp[2]]
        elif(count==5):
            temp1=[count1+1,temp[0],temp[1],temp[2],temp[3],temp[4]]
        elif(count==6):
            join=temp[2]+temp[3]
            temp1=[count1+1,temp[0],temp[1],join,temp[4],temp[5]]
        l.insert(count1,temp1)
        count1+=1

    return l


def createdb():
    import sqlite3
    conn=sqlite3.connect('normanpd.db',timeout=15)
    print("Database created and opened succesfully")
    c = conn.cursor()
    c.execute('''CREATE TABLE incidents
               (id INT PRIMARY KEY NOT NULL,
               number TEXT,
               date_time TEXT,
               location TEXT,
               nature TEXT,
               ORI TEXT);''')
    conn.commit()
    conn.close()


def populatedb(tup_incidents):
    import sqlite3
    conn = sqlite3.connect('normanpd.db',timeout=60)
    print('Connected to the Database Successfully')
    c=conn.cursor()
    c.executemany('INSERT INTO incidents VALUES (?,?,?,?,?,?)',tup_incidents)
    print("Database populated succesfuly!!!")
    conn.commit()
    conn.close()

def status(db):
    import sqlite3
    conn=sqlite3.connect(db,timeout=30)
    print('Connected succesfully to the Database')
    c=conn.cursor()
    c.execute("SELECT COUNT(*) FROM incidents")
    total_row_count=c.fetchone()[0]
    print('\nThe total number of rows in incidents table are {0}\n\n'.format(total_row_count))
    print('Random Five rows from normanpd.db database:\n')
    c.execute("SELECT * FROM incidents ORDER BY RANDOM() LIMIT 5;")
    for row in c.fetchall():
        print(row)
    
    conn.commit()
    conn.close()
