from bs4 import BeautifulSoup
import urllib2
import urlparse
import sys
import string
from nltk import word_tokenize
from nltk.corpus import stopwords
reload(sys)
sys.setdefaultencoding('utf8')
rr = open('rr2')
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
stop = set(stopwords.words('english'))
for x in d3:
#       try:
        try:
                r = urllib2.urlopen(x, timeout=30).read()
        except:
                continue
        soup = BeautifulSoup(r, "html.parser")
        if x:
                e = urlparse.urlparse(x)
        else:
                continue
        for link in soup.findAll('a'):
                print link
                if link!=None:
                        v = link.text
                        y = link.get('href')
                        if y:
                                t = urlparse.urlparse(y)
                        else:
                                continue
                        if t[0]=='':
                                y = e[0]+'://'+e[1]+y
                        v = v.rstrip(' \n\t\0')
                        v = v.lstrip(' \n\t\0')
                        for x in rr:
                                if string.find(v, x)>0:
                                        if o.has_key(v)==False:
                                                o[v] = y
                                        for e in v.lower().split():
                                                if e not in stop:
                                                        if dv.has_key(e):
                                                                dv[e] = dv[e]+1
                                                        else:
                                                                dv[e] = 1
                                                

s = open('rr8', 'w')
for x in o.keys():
        r = r+'<a href="'+o[x]+'">'+x+'</a><br>'
s.write(r)
s.close()
