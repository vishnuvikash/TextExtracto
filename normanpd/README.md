**Assignment-Activity Police Report Extraction**

In this assignment I have extracted information from a scraped file and add it to an SQLite database. The Scraped files are downloaded from http://normanpd.normanok.gov/content/daily-activity page which has data related to Norman Police Depatment Daily Activity Reports Listing in it. The webpage has three types of arrests, incidents and case summaries. We have to just download the Incident Summary files as part of the Assignment and save them locally.	

------------------------------------------------------------------------------------------------
Task 1: DOWNLOAD DATA (INCIDENT SUMMARY FILES)
	For downloading the data I have used the urllib.request package, it does return a byte object which I have decoded in 'utf-8'. For getting the url links of all the Incident Summaries files present on the webpage, I have used regular expression r'/file[\w|%|/|\-|]+Incident.*\.pdf' which identifies the urls startinfg with '/file followed by a combination of [a-z][A-Z][0-9],%,/,-followed by Incident and which is followed by any kind of characters.

A sample url is of the form https://normanpd.normanok.gov/filebrowser_download/657/2017-02-27%20Daily%20Incident%20Summary.pdf 

I have obtained the urls from the page and downloaded the files using the urllib.request.urlretrieve() funtion passing these urls. I have locally saved the downloaded pdfs.

-------------------------------------------------------------------------------------------------
TASK 2: EXTRACT  DATA 
	I have the downloaded pdfs and have to extract the valuable data from pdfs. Each pdf has five columns in which data is hidden. For Extracting the information from the pdf I have used the PyPDF2.PdfFileReader package, the package includes function for identifying the number of pages and iterating over the pages line by line and also for extracting page content. The extracted page content is in the form of string which has many unwanted characters.

Sample-few lines of extracted content
 
	 \nDate / Time\nIncident Number\nLocation\nNature\nIncident ORI\n/27/2017 0:03\n 2017-00014012'\n 'W STATE HWY 9 HWY \n I35 NB ON RAMP \n108A RAMP Traffic Stop OK0140200\n

For all the seven pages from urls, we have starting of the each pdf with starting 16 characters this  Date / Time\nIncident Number\nLocation\nNature\nIncident ORI\n, so I have tried to remove it by using simple string index operations i.e x=x[:-16], similarly at the end of final page in pdf files, the we have time stamp which we have the 

I have replaced the Date / Time@Incident Number@Location@Nature@Incident ORI@ and NORMAN POLICE DEPARTMENT@Daily Incident Summary (Public)@ and Daily Incident Summary (Public)@NORMAN POLICE DEPARTMENT@  with the null char as it is not valuabel info.

I have inserted thorn chatacters in front every date occurence using the regular expressions, the thorn char helps in disitnguishing the information rows in the table.

I have searched for the possibility of occurences of contionus þ characters and replaced all such conditions with single char of þ.

countP=re.findall(r'þ*þ',text)

               
for i in countP:
        if i in text:
        	text=text.replace(i,'þ')

 incident_info1=text.split('þ')
        # print(len(incident_info1))
    incident_info=[i for i in incident_info1 if len(i)!=0]

Still even after replacing the mulitple occurences of thorn with single thorn there are few cases, so above two lines solves the problem by delting the list values caused due to these extra thorns. 



 count=0
    count1=0
    l=[]
    temp1=[]
    for i in incident_info:
        c=re.findall(r'@',i)
        i=i[:-1]
        temp=i.split('@')
        count=len(temp)
            # temp1=[]
        if(count==3): 
            temp1=[count1+1,temp[0],' ',' ',temp[1],temp[2]]
        elif(count==5):
            temp1=[count1+1,temp[0],temp[1],temp[2],temp[3],temp[4]]
        elif(count==6):
            join=temp[2]+temp[3]
            temp1=[count1+1,temp[0],temp[1],join,temp[4],temp[5]]
        l.insert(count1,temp1)
        count1+=1

Basically 3 types of row entries were there during extraction: 

type1- all column values are there- values in row are five
type2- the third colum value was so large that it has taken 2 lines thus while retrieving -we get 6 values in a row
type3- null values in column2 and column3 and these spaces occupied by col4 and col5 values

the above for loop code is effeciently written to solve these 3 types.

Finally after removing the generalised error, strings from the text have been split on the basis of 'þ' ans stored them in a list. The list has some empty entries which were deleted later. Used the list values here to generate lists of fixed type.

The lists that we obtained initially are not exactly rows in each pdf as the pdf have null spaces and also occupying dual lines, so I have written generalised code for tackling all the three scenarios after spltting.

After run through the generlised code I was able to generate lists  and return them.

--------------------------------------------------------------------------

TASK-3 
 CREATING DB

I have created the incidents table in  sqlite Database with the specified schema i.e conn=sqlite3.connect('normanpd.db',timeout=15) and timeout element is very important in the avoiding bugs scuch as Database locks.

Steps for Creating Sample DB

import sqlite3
conn=sqlite3.connect('normanpd.db',timeout=15)
c=conn.cursor()
c.execute('''CREATE TABLE incidents
               (id INT PRIMARY KEY NOT NULL,
               number TEXT,
               date_time TEXT,
               location TEXT,
               nature TEXT,
               ORI TEXT);''')
	for passing the schema
conn.commit()-for commiting any changes
conn.close()-closing the connection


p---------------------------------------------------------------------
Task 4  Populating the Database 

The data is populated in the database by passing the lists which were extracted from pdfs.
I have used c.executemany('INSERT INTO incidents VALUES (?,?,?,?,?,?)',tup_incidents) for concurrently populating the database and here the tup_incidents is tuple form of Incidents

Problems Faced: Database was got locked some times during the testing stage due to which I have used timeout attrubute as well in the connection.
------------------------------------------------------------------------
TASK 5 Status of DB

For the status of Db the total number of rows after storing all the values from the pdfs is printed followed by random five rows which changes dynamically whenver the command is executed.

For the row count -c.execute("SELECT COUNT(*) FROM incidents")
    		   total_row_count=c.fetchone()[0]   is being used

For printing Random rows -c.execute("SELECT * FROM incidents ORDER BY RANDOM() LIMIT 5;")
			    for row in c.fetchall():
				print(row)



**OUTPUT**(PACKAGING and making the project locally testable )

vishnu@vishnu-Inspiron-5537:~/Desktop/normanpd$ virtualenv -p python3.6 venv
Running virtualenv with interpreter /usr/bin/python3.6
Using base prefix '/usr'
New python executable in /home/vishnu/Desktop/normanpd/venv/bin/python3.6
Also creating executable in /home/vishnu/Desktop/normanpd/venv/bin/python
Installing setuptools, pip, wheel...done.
vishnu@vishnu-Inspiron-5537:~/Desktop/normanpd$ source venv/bin/activate
(venv) vishnu@vishnu-Inspiron-5537:~/Desktop/normanpd$ pip3 install PyPDF2
Collecting PyPDF2
Installing collected packages: PyPDF2
Successfully installed PyPDF2-1.26.0
(venv) vishnu@vishnu-Inspiron-5537:~/Desktop/normanpd$ python3 main.py
Database created and opened succesfully
Connected to the Database Successfully
Database populated succesfuly!!!
Connected succesfully to the Database

The total number of rows in incidents table are 2433


Random Five rows from normanpd.db database:

(193, '2/27/2017 14:11', '2017-00014141', '35.21155955~-97.4363668333333', 'Traffic Stop', 'OK0140200')
(797, '2/25/2017 12:14', '2017-00002118', '1111 24TH AVE SW', 'Back Pain', '14005')
(1264, '2/24/2017 17:56', '2017-00013480', '-1 1423 REBECCA LN', 'Hit and Run', 'OK0140200')
(2078, '2/22/2017 23:30', '2017-00012962', '1300 STEAMBOAT WAY', 'Disturbance/Domestic', 'OK0140200')
(448, '2/26/2017 8:33', '2017-00002803', '401 W IMHOFF RD', 'Stand By EMS', 'EMSSTAT')
(venv) vishnu@vishnu-Inspiron-5537:~/Desktop/normanpd$ pip3 install --editable .
Obtaining file:///home/vishnu/Desktop/normanpd
Installing collected packages: Activity-Police-Report-Extraction
  Running setup.py develop for Activity-Police-Report-Extraction
Successfully installed Activity-Police-Report-Extraction
(venv) vishnu@vishnu-Inspiron-5537:~/Desktop/normanpd$ deactivatevishnu@vishnu-Inspiron-5537:~/Desktop/normanpd$ 


>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
REQUIRED:

DEPENDENCIES:
PyPDF2-pip install PyPDF2 for installing PyPDF2

VERSION:
PYTHON VERSION 3.6 preferred ,any version above PY(3.0) have to work.


<REFERENCES:>
Police DataURL-http://normanpd.normanok.gov/content/daily
PYPDF2-https://pythonhosted.org/PyPDF2/PdfFileReader.html
SQLITE3 with Python: https://docs.python.org/2/library/sqlite3.html
python-https://docs.python.org/3/
urllib-https://docs.python.org/3/howto/urllib2.html
urllib-http://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

