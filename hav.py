from bs4 import BeautifulSoup
import urllib
import urllib.parse
import sys
import string
#from nltk import word_tokenize
#from nltk.corpus import stopwords
#reload(sys)
#sys.setdefaultencoding('utf8')
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
#stop = set(stopwords.words('english'))
for x in d3:
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
        for y in headlines[x]:
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
        print(x, mmm[x])
print(b)

                        v = v.lstrip(' \n\t\0')
                        for x in rr:
                                if string.find(v, x)>0:
                                        if o.has_key(v)==False:
                                                o[v] = y
                                        for e in v.lower().split():
                                                #print e
 #                                               if e not in stop:
                                                       #print e
                                            if dv.has_key(e):
                                                dv[e] = dv[e]+1
                                            else:
                                                dv[e] = 1
r = ''
s = open('rr8', 'w')
for x in o.keys():
        r = r+'<a href="'+o[x]+'">'+x+'</a><br>'
s.write(r)
s.close()
