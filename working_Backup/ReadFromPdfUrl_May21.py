# -*- coding: utf-8 -*-
"""
Created on Thu May 21 10:33:16 2020

@author: ajaybkumar
"""


# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 15:37:54 2020

@author: ajaybkumar
"""
import sys
from tika import parser
import re
import requests 
from bs4 import BeautifulSoup 
import cx_Oracle
import pandas as pd

#output handler for blob
def OutputTypeHandler(cursor, name, defaultType, size, precision, scale):
    if defaultType == cx_Oracle.CLOB:
        return cursor.var(cx_Oracle.LONG_STRING, arraysize=cursor.arraysize)
    if defaultType == cx_Oracle.BLOB:
        return cursor.var(cx_Oracle.LONG_BINARY, arraysize=cursor.arraysize)

#Database Connection
dsn_tns = cx_Oracle.makedsn('10.118.62.195', '1521', 'db1') # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
conn = cx_Oracle.connect(user='product_ors', password='pr0duct_ors', dsn=dsn_tns) # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'
conn.outputtypehandler = OutputTypeHandler
c = conn.cursor()

print ("Opened database successfully")

file = str(sys.argv[1])

# Parse data from file
file_data = parser.from_file(file)

# Get files text content
text = file_data['content']
#print(text)

DellUrl = re.findall('https://[\n]|\S+|[\n]', text)
#print(DellUrl)

s=""
for item in DellUrl:    
  s += item.replace("\n","")
#print("stin", s)

httpind = s.find('http')
#print("index at", httpind)

url=s[httpind:]
print("updated url",url)


#extracting code beautifulsoup for html parser
def readwebdata(): 
    # the target we want to open     
    #url='https://www.flipkart.com/dell-vostro-14-3000-core-i5-8th-gen-8-gb-1-tb-hdd-linux-2-gb-graphics-vos-3480-laptop/p/itmf1a0a2f37df6d'
    
    #open with GET method 
    resp=requests.get(url) 
    #print(resp)
      
    #http_respone 200 means OK status 
    if resp.status_code==200: 
        #print("Successfully opened the web page") 
             
        # we need a parser,Python built-in HTML parser is enough .
        soup=BeautifulSoup(resp.content,'html.parser')  
        
        Specifications = soup.find(class_="_2RngUh")
  
        ExtractSpecName = Specifications.find_all(class_="_3-wDH3 col col-3-12") 
        #print(ExtractSpecName)
        
        NameList = [word.get_text() for word in ExtractSpecName]
        #print(NameList)
        
        ExtractSpecValue = Specifications.find_all(class_="_2k4JXJ col col-9-12") 
        #print(ExtractSpecValue)
        
        ValueList = [word.get_text() for word in ExtractSpecValue]
        #print(ValueList)
        
        dict = {'name': NameList, 'value': ValueList}  
        
        df=pd.DataFrame(dict) 
        #print(df)
                
        INTRCTID=sys.argv[2]
        
        for index, row in df.iterrows():
            if index < 1:
                print("skip this")
            else:
                c.execute("INSERT INTO Additional_Features (FEATURE_NAME,FEATURE_VALUE,INTERACTION_ID) VALUES (:ID,:VAL,:INTR)", ID = row['name'],VAL = row['value'],INTR=INTRCTID)
                print(row['name'], row['value'])

        conn.commit();
        c.close()
readwebdata()