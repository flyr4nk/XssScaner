# coding: utf8
 
import sys
import os
from time import time
import urlparse
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import urllib2


def writestr(arg):
    f=open(r'c:\all\log.txt','a')
    f.write(arg+'\n')
    f.close()


class mybrowser():
     def __init__(self):
             self.user_agent = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2) Gecko/20100124 Firefox/3.6 (Swiftfox)'
 
             self.application = QApplication([])
             self.webpage = QWebPage()
             self.webpage.userAgentForUrl = lambda url: self.user_agent
             self.webframe = self.webpage.currentFrame()
    
             self.webpage.javaScriptAlert = self._alert
             # self.webpage.javaScriptConfirm = lambda frame, message: raw_input('==Confirm== (y/n): %s' % message) == 'y'
             # self.webpage.javaScriptConsoleMessage = lambda string1, int1, string2: sys.stdout.write('==Message==: %s %d %s\n' % (string1, int1, string2))
             # self.webpage.javaScriptPrompt = lambda frame, message, defaultValue, result: raw_input('==Prompt== %s:' % message) or False
             self.url =''
             self._load_status = 'init'
             self.webpage.connect(self.webpage,SIGNAL('loadFinished(bool)'),self._onLoadFinished)
             self.webpage.connect(self.webpage,SIGNAL('loadStarted()'),self._onLoadStarted)
 
     def load(self, url):
            self.url=url
            self.webframe.load(QUrl(url))
            self.wait_load()
	


 
     def html(self):
         return unicode(self.webframe.toHtml())
 
     def wait_load(self, least = 0, most = 10):
          start = time()
          while (self._load_status == 'start' and time() - start < most) or time() - start < least:
                self.application.processEvents()
 
     def _onLoadFinished(self, status):
          if status:
              self._load_status = 'end'
 
     def _onLoadStarted(self):
            self._load_status = 'start'
 
     def _alert(self, frame, message):
             if u'1'==unicode(message):
                 print 'xss'
                 #writestr(self.url)


     def close(self):
         """Close Browser instance and release resources."""  
         if self.webpage:
                del self.webpage

         self.application.exit()  
  

if __name__=='__main__':
   try:
     browser=mybrowser()
#     print sys.argv[1]
     cmd =  urllib2.unquote(sys.argv[1])
     browser.load(cmd)
     browser.close()
   except Exception:
            browser.close()


