import io
import re
#import requests
import urllib
from urllib.request import urlopen
#from fake_useragent import UserAgent
import stem.process
from stem.util import term
from bs4 import BeautifulSoup

class texc(Exception): pass

class Wconnector:
	
	
	tor_process = None
	
	def __init__(self,*lurl):
		self.lurl = lurl
		self.data = []

	def fakereq(self,url):
		

		#return response.content
		html_page = urlopen(url)
		soup = BeautifulSoup(html_page, "lxml")
		self.data = list(alink.get('href') for alink in soup.findAll('a') if alink.get('href') is not "#" or alink.get('href') is not "/")
		#for link in soup.findAll('a'):
		#	linklist.append(link.get('href'))
			
			
    

	def query(self, startT = False):
		"""
		Uses pycurl to fetch a site using the proxy on the SOCKS_PORT.
		"""
		if startT == True:
			try:
				type(self).starTor()
			except Exception as texcept:
				print("Exception in tor start %s" % str(texcept.args))
		
		#output = io.BytesIO()
		try:
			if len(self.lurl) == 0: raise texc()
		except texc:
			print("Url lists cannot be blank")
		else:
			for x in self.lurl:
				self.fakereq(x)
		

	# Start an instance of Tor configured to only exit through Russia. This prints
	# Tor's bootstrap information as it starts. Note that this likely will not
	# work if you have another Tor instance running.

	@staticmethod
	def print_bootstrap_lines(line):
		if "Bootstrapped " in line:
			print(term.format(line, term.Color.BLUE))

	@classmethod
	def starTor(cls):
		SOCKS_PORT = 7000
		print(term.format("Starting Tor:\n", term.Attr.BOLD))
	

		cls.tor_process = stem.process.launch_tor_with_config(
		config = {
			'SocksPort': str(SOCKS_PORT),
			#'ExitNodes': '{ru}',
			},
		init_msg_handler = cls.print_bootstrap_lines,
		)
	
	@classmethod
	def stopTor(cls):
		print(term.format("Stopping Tor:\n", term.Attr.BOLD))
	
		if cls.tor_process is not None: cls.tor_process.kill()


		
if __name__ == '__main__':

	print('ciao')
	w = Wconnector('http://www.sloop1.com/about-neuromarketing-company/','http://www.patriziameo.it')
	t = Wconnector('http://www.sloop1.com/')
	c = Wconnector()
	
	try:
    
		print(term.format("\nChecking our endpoint:\n", term.Attr.BOLD))
		w.query(startT = True)
		t.query()
		c.query()
		
		print("w.data is %s" % w.data)
    #print(fakereq(r"http://www.sloop1.com/about-neuromarketing-company/"))
	finally:
		type(w).stopTor()  # stops tor for instance class