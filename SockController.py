import io
import os
import re
import webbrowser
import time
import random
import subprocess
#import requests
import urllib
from urllib.request import urlopen
from urllib.parse import urlparse
#from fake_useragent import UserAgent
import stem.process
from stem.util import term
from bs4 import BeautifulSoup


class texc(Exception): pass

class Wconnector:
	
	
	tor_process = None
	
	def __init__(self,lurl):
		self.lurl = lurl
		self.data = []

	def fakereq(self,url):
		

		#return response.content
		html_page = urlopen(url)
		soup = BeautifulSoup(html_page, "lxml")
		self.data = list(alink.get('href') for alink in soup.findAll('a') if alink.get('href') is not "#")
		if len(self.data) > 0:
			#check for a random url and verify if is in domain
			saddr = self.data[random.randint(1,len(self.data)-1)]
			parsed_uri = urlparse(saddr)
			domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
			print(term.format("The domain is %s" % (domain), term.Attr.BOLD))
			if domain == self.lurl:
				self.gestbrowser(saddr)
			else:
				self.fakereq(url)

		
		
		
	def gestbrowser(self,l1):
		
		timeop = random.randint(5,50)
		print("Now we process %s for time %s" % (l1,timeop))

		try:
			webbrowser.get("open -a /Applications/Google\ Chrome.app %s").open(l1)	
			time.sleep(timeop) #delay of 10 seconds
			self.fakereq(l1)
		except Exception as ex1:
			print ("Exception ex1 is %s" % (str(ex1.args)))
			self.fakereq(self.lurl)

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
			self.fakereq(self.lurl)
		

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
	w = Wconnector('http://www.sloop1.com/')
	t = Wconnector('http://www.sloop1.com/')
	#c = Wconnector()
	
	try:
    
		print(term.format("\nChecking our endpoint:\n", term.Attr.BOLD))
		w.query(startT = False)
		#t.query()
		#c.query()
		
		#print(fakereq(r"http://www.sloop1.com/about-neuromarketing-company/"))
	finally:
		type(w).stopTor()  # stops tor for instance class