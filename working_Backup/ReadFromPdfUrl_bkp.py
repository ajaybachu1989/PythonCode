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
#scrapy

#output handler for blob
def OutputTypeHandler(cursor, name, defaultType, size, precision, scale):
    if defaultType == cx_Oracle.CLOB:
        return cursor.var(cx_Oracle.LONG_STRING, arraysize=cursor.arraysize)
    if defaultType == cx_Oracle.BLOB:
        return cursor.var(cx_Oracle.LONG_BINARY, arraysize=cursor.arraysize)



dsn_tns = cx_Oracle.makedsn('10.118.62.195', '1521', 'db1') # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
conn = cx_Oracle.connect(user='product_ors', password='pr0duct_ors', dsn=dsn_tns) # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'
conn.outputtypehandler = OutputTypeHandler
c = conn.cursor()


print ("Opened database successfully")

def Find(string): 
    # findall() has been used  
    # with valid conditions for urls in string 
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[.$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string) 
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

#NLTK to tokenize words
#page = urlopen('https://www.flipkart.com/dell-inspiron-5000-core-i5-8th-gen-8-gb-1-tb-hdd-512-gb-ssd-windows-10-home-2-graphics-5584-laptop/p/itm75586b0f7d7f1?pid=COMFKYHFGW9GXYDH&lid=LSTCOMFKYHFGW9GXYDH4HH2WF&marketplace=FLIPKART&srno=s_1_2&otracker=AS_QueryStore_OrganicAutoSuggest_1_2_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_2_na_na_ps&fm=SEARCH&iid=d5b40251-1a6a-485d-bb51-8914cb70234d.COMFKYHFGW9GXYDH.SEARCH&ppt=sp&ppn=sp&ssid=phv630wx1c0000001587038307308&qH=40034c3bbcbbd998').read()
#print(page)#returns text with html tags
#tokens = nltk.word_tokenize(page)

##############33
#return clear text without any word qualifiers
#raw = BeautifulSoup(page).get_text()
#print(raw)
#tokens = nltk.word_tokenize(raw)
##################3

#rawtext = nltk.clean_html(page)

#print(rawtext)

# response = urlopen('https://www.facebook.com/')
# html = response.read()
# print(html)





#extracting code beautifulsoup for html parser
def readwebdata(): 
    # the target we want to open     
    url='https://www.flipkart.com/dell-inspiron-5000-core-i5-8th-gen-8-gb-1-tb-hdd-512-gb-ssd-windows-10-home-2-graphics-5584-laptop/p/itm75586b0f7d7f1'
    #url='https://www.ebay.com/itm/Dell-Red-Laptop-Tablet-Inspiron-11-Model-Great-Condition/264709572782?hash=item3da1eb88ae:g:nKMAAOSwAi1dHul5'
    #https://www.geeksforgeeks.org/reading-selected-webpage-content-using-python-web-scraping/  
    #open with GET method 
    resp=requests.get(url) 
    #print(resp)
      
    #http_respone 200 means OK status 
    if resp.status_code==200: 
        print("Successfully opened the web page") 
        print("The news are as follow :-\n") 
      
        # we need a parser,Python built-in HTML parser is enough .
        
        soup=BeautifulSoup(resp.content,'html.parser')  
        #print(soup)
        
        ############
        Specifications = soup.find(class_="_2RngUh")
        #print(Specifications)
        
        ExtractSpecName = Specifications.find_all(class_="_3-wDH3 col col-3-12") 
        #print(ExtractSpecName)
        
        NameList = [word.get_text() for word in ExtractSpecName]
        #print(NameList)
        
        ExtractSpecValue = Specifications.find_all(class_="_2k4JXJ col col-9-12") 
        #print(ExtractSpecValue)
        
        ValueList = [word.get_text() for word in ExtractSpecValue]
        #print(ValueList)
        
        # for i in range(1, len(NameList)): 
        #     #c.execute("insert into Additional_Features(FEATURE_NAME,FEATURE_VALUE) values (:1, :1)", NameList[i])
        #     c.execute("INSERT INTO Additional_Features (FEATURE_NAME) VALUES (:ID)", ID = NameList[i])
        #     #c.execute("update Additional_Features set FEATURE_VALUE = :VAL  where FEATURE_NAME = :NAME",(ValueList[i],NameList[i]))
        #     #print(NameList[i])
            
        # for i in range(1, len(NameList)): 
        #     #c.execute("insert into Additional_Features(FEATURE_NAME,FEATURE_VALUE) values (:1, :1)", NameList[i])
        #     #c.execute("INSERT INTO Additional_Features (FEATURE_NAME) VALUES (:ID)", ID = NameList[i])
        #     c.execute("update Additional_Features set FEATURE_VALUE = :VAL  where FEATURE_NAME = :NAME",(ValueList[i],NameList[i]))
        #     print(ValueList[i])
            
        
        ##############
        ################
        # proxies_table = soup.find(class_='_3ENrHu')
        # proxies = []
        # for row in proxies_table.tbody.find_all('tr'):
        #     proxies.append('{},{}'.format(row.find_all('td')[0].string, row.find_all('td')[1].string))
        
        # print(proxies)
        
        dict = {'name': NameList, 'value': ValueList}  
        
        df=pd.DataFrame(dict) 
        #print(df)
        
        # for i in range(len(df)) : 
        #     print(df.loc[i, "name"], df.loc[i, "value"]) 
        
        # for index,rows in df.iterrows():
        #     c.execute("""update result SET Pay_Agent = ? WHERE SEND_AGENT = ?""",df['PAY_AGENT'][index],df['SEND_AGENT'][index])
        # index+=1
        
        INTRCTID=sys.argv[2]
        
        for index, row in df.iterrows():
            #c.executemany("insert into Additional_Features(FEATURE_NAME,FEATURE_VALUE) values (:name, :value)", row['name'], row['value'])
            if index < 1:
                print("skip this")
            else:
                c.execute("INSERT INTO Additional_Features (FEATURE_NAME,FEATURE_VALUE,INTERACTION_ID) VALUES (:ID,:VAL,:INTR)", ID = row['name'],VAL = row['value'],INTR=INTRCTID)
                print(row['name'], row['value'])
            
            
        
        #################
        
        
            
        
        
        
        
        
        
        

        #print(soup.text)
        #text= soup.find_all(text=True)
        
        #print(set([t.parent.name for t in text]))
#         blacklist = [
# 	'[document]',
# 	'noscript',
# 	'header',
# 	'html',
# 	'meta',
# 	'head', 
# 	'input'
# 	# there may be more elements you don't want, such as "style", etc.
# ]
#         output=''
#         for t in text:
#             if t.parent.name not in blacklist:
#                 output+= '{} '.format(t)
#         #print(output)        
        
#         tokens = nltk.word_tokenize(output)
        #print(tokens)
        #print(text)#returns text with text qualifiers''
        #print([type(item) for item in list(soup.children)])
        #soup=BeautifulSoup(resp.content,'html5lib')  #above and this working as same
        
        #print(soup.prettify())
        #print(soup.head)
  
        # l is the list which contains all the text i.e news  
        #l=soup.find("ul",{"class":"searchNews"}) 
        #print(soup.find_all("product"))
      
        #now we want to print only the text part of the anchor. 
        #find all the elements of a, i.e anchor 
              #for i in l.findAll("a"):

    # else: 
        # print("Error") 
        conn.commit();
        c.close()
readwebdata()




