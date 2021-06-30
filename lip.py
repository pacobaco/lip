from bs4 import BeautifulSoup
import urllib
import urllib.parse
import sys
import string
from nltk import word_tokenize
from nltk.corpus import stopwords
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="lip"
)

mycursor = mydb.cursor()
rr = open('rr')
rr = rr.read()
rr = rr.split(',')
u = []
d = open('f3.txt')
d2 = d.read()
d.close()
d3 = d2.split('\n')
o = {}
g = 0
dv = {}
headlines = {}
stop = set(stopwords.words('english'))
for x in d3[:10]:
#       try:
        try:
                from urllib.request import urlopen
                r = urlopen(x,timeout=30).read()
                #print(r)
                #r = urllib2.urlopen(x, timeout=30).read()
        except:
                continue
        soup = BeautifulSoup(r, "html.parser")
        if x:
                e = urllib.parse.urlparse(x)
        else:
                continue
        for link in soup.findAll('a'):
                print(link)
                if link!=None:
                        v = link.text
                        y = link.get('href')
                        if y:
                                t = urllib.parse.urlparse(y)
                        else:
                                continue
                        if t[0]=='':
                                try:
                                    y = e[0]+'://'+e[1]+y
                                except: continue
                        v = v.rstrip(' \n\t\0')
                        v = v.lstrip(' \n\t\0')
                        mnb = v.split(' ')
                        for zz in mnb:
                                if y in headlines:
                                        headlines[y].append(zz)
                                else:
                                        headlines[y] = []
                                        headlines[y].append(zz)
                        print(mnb, y)
                        for x in rr:
                                if v.find(x)>0:
                                        if v in o==False:
                                                o[v] = y
                                        for e in v.lower().split():
                                                #print e
 #                                               if e not in stop:
                                                       #print e
                                            if e in dv:
                                                dv[e] = dv[e]+1
                                            else:
                                                dv[e] = 1
                        try:
                                from urllib.request import urlopen
                                r = urlopen(link,timeout=30).read()
                        #print(r)
                        #r = urllib2.urlopen(x, timeout=30).read()
                        except:
                                continue
                        soup = BeautifulSoup(r, "html.parser")
                        if x:
                                e = urllib.parse.urlparse(x)
                        else:
                                continue

                        img = soup.findAll('img')
                        #depending on how many images are here you will probably need to loop through img
                        for pp in img:
                                src = img.get('src')
                                title = img.get('title')
                                print(src,title)
r = ''
s = open('rr8', 'w')
for x in o.keys():
        r = r+'<a href="'+o[x]+'">'+x+'</a><br>'
s.write(r)
s.close()
print(headlines)
b=list(headlines.keys())
b.sort()
s = {}
leni = {}
for x in b:
        sql = "INSERT INTO url (url) VALUES ('"+x+"'')"
        #val = (x)
        #try:
        print(mycursor.execute(sql))

        mydb.commit()
        #except: print(sql)
        print(mycursor.rowcount, "record inserted.")

        for y in headlines[x]:


                sql = "INSERT INTO keyword (keyword) VALUES ('"+y+"'')"
#                val = (y)
                #try:
                print(mycursor.execute(sql))

                mydb.commit()
                #except: print(sql)
                print(mycursor.rowcount, "record inserted.")

                if y in s:
                        s[y].append(x)
                else:
                        s[y] = []
                        s[y].append(x)
                if y in leni:
                        leni[y]=leni[y]+1
                else:
                        leni[y]=1

print(s)
print(leni)
b=list(leni.keys())
b.sort()
mmm={}
for x in b:
        if leni[x] in mmm:
                mmm[leni[x]].append(x)
        else:
                mmm[leni[x]] = []
                mmm[leni[x]].append(x)
#print(b)
b=list(mmm.keys())
b.sort()
for x in b:
        if x not in stop and x!='':
                print(x, mmm[x])
#print(b)
