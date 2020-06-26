# -*- coding: utf-8 -*-
"""
Created on Tue May 12 14:34:37 2020

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
# from urllib.request import urlopen
# from nltk.tokenize import sent_tokenize
# import nltk
import cx_Oracle
import pandas as pd
from urlextract import URLExtract
#scrapy

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

def Find(string): 
    # findall() has been used  
    # with valid conditions for urls in string 
    extractor = URLExtract()
    for url in extractor.gen_urls(string):
        print(url)
    #     return url 
    #url = re.findall(r'(https?://\S+)', string)
    # url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[.$-_@.&+]|[!*\(\),\n]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string) 
    #url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string,re.MULTILINE) 
    return url 

file = str(sys.argv[1])

# Parse data from file
file_data = parser.from_file(file)

# Get files text content
text = file_data['content']
#print(text)

#print("Urls: ", Find(text))

DellUrl = Find(text)
print(DellUrl)


#extracting code beautifulsoup for html parser
def readwebdata(): 
    # the target we want to open     
    url='https://www.flipkart.com/dell-vostro-14-3000-core-i5-8th-gen-8-gb-1-tb-hdd-linux-2-gb-graphics-vos-3480-laptop/p/itmf1a0a2f37df6d'
    
    #open with GET method 
    resp=requests.get(url) 
    #print(resp)
      
    #http_respone 200 means OK status 
    if resp.status_code==200: 
        #print("Successfully opened the web page") 
        #print("The news are as follow :-\n") 
      
        # we need a parser,Python built-in HTML parser is enough .
        
        soup=BeautifulSoup(resp.content,'html.parser')  
        dir(soup)
        #print(soup)
        
        # for element in soup.find_all(class_=True):
        #     elm=element['class']
        #     try:
        #           if soup.find('div',class_=elm).text == "General":
        #               print(elm)
        #     except:
        #         pass
        
        # test = soup.find(text="General")
        # print("test",test)
            
           
        
        ############
        Specifications = soup.find(class_="_2RngUh")
        
               
        #As there are multiple sections we can use this to select particular section
        #Specifications = soup.find_all('div', {'class': '_2RngUh'})[4]
        #print("test",Specifications)
        # l=Specifications.descendants
        # print("printing",l)
        
        # for i in l:
        #     print("printing descendants",i)
        
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
        # #print(df)
        
               
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