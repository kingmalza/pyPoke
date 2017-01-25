import io
import requests
import urllib
from fake_useragent import UserAgent
import stem.process
from stem.util import term

class texc(Exception): pass
class Wconnector:
	
	SOCKS_PORT = 7000
	tor_process = None
	
	def __init__(self,*lurl):
		self.lurl = lurl

	def fakereq(self):
		#ua = UserAgent()
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
		proxies = {
			"http": "localhost",
			"https": "localhost",
		}    
    
		response = requests.get(url, headers=headers, proxies=proxies)
		return response.content
    

	def query(self, startT = False):
		"""
		Uses pycurl to fetch a site using the proxy on the SOCKS_PORT.
		"""
		if startT == True and type(self).tor_process not is None:
			try:
				starTor()
			except Exception as texcept:
				print("Exception in tor start %s" % str(texcept.args))
		
		#output = io.BytesIO()
		try:
			if len(self.lurl) == 0: raise texc()
		except texc:
			print("Url lists cannot be blank")
		else:
			for x in self.lurl:
				#then call fakereq
				print (x)
		

	# Start an instance of Tor configured to only exit through Russia. This prints
	# Tor's bootstrap information as it starts. Note that this likely will not
	# work if you have another Tor instance running.

	@staticmethod
	def print_bootstrap_lines(line):
		if "Bootstrapped " in line:
			print(term.format(line, term.Color.BLUE))

	@classmethod
	def starTor(cls):
		print(term.format("Starting Tor:\n", term.Attr.BOLD))
	

		cls.tor_process = stem.process.launch_tor_with_config(
		config = {
			'SocksPort': str(SOCKS_PORT),
			#'ExitNodes': '{ru}',
			},
		init_msg_handler = print_bootstrap_lines,
		)
	
	@classmethod
	def stopTor(cls):
		print(term.format("Stopping Tor:\n", term.Attr.BOLD))
	
		if cls.tor_process is not None: cls.tor_process.kill()


		
if __name__ == '___main__':

	w = Wconnector('http://www.sloop1.com/about-neuromarketing-company/','http://www.patriziameo.it')
	t = Wconnector('http://www.sloop1.com/')
	c = Wconnector()
	
	try:
    
		print(term.format("\nChecking our endpoint:\n", term.Attr.BOLD))
		w.query()
		t.query()
		c.query()
    #print(fakereq(r"http://www.sloop1.com/about-neuromarketing-company/"))
	finally:
		type(w).stopTor()  # stops tor for instance class