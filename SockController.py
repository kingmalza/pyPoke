import io
import pycurl
import requests
import urllib
from fake_useragent import UserAgent

import stem.process

from stem.util import term

SOCKS_PORT = 7000

def fakereq(url):
    #ua = UserAgent()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    proxies = {
        "http": "localhost",
        "https": "localhost",
    }    
    
    response = requests.get(url, headers=headers, proxies=proxies)
    return response.content
    

def query(url):
    """
    Uses pycurl to fetch a site using the proxy on the SOCKS_PORT.
    """

    output = io.BytesIO()

    query = pycurl.Curl()
    query.setopt(pycurl.URL, url)
    query.setopt(pycurl.PROXY, 'localhost')
    query.setopt(pycurl.PROXYPORT, SOCKS_PORT)
    query.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)
    query.setopt(pycurl.WRITEFUNCTION, output.write)

    try:
        query.perform()
        return output.getvalue()
    except pycurl.error as exc:
        return "Unable to reach %s (%s)" % (url, exc)


# Start an instance of Tor configured to only exit through Russia. This prints
# Tor's bootstrap information as it starts. Note that this likely will not
# work if you have another Tor instance running.

def print_bootstrap_lines(line):
    if "Bootstrapped " in line:
        print(term.format(line, term.Color.BLUE))


print(term.format("Starting Tor:\n", term.Attr.BOLD))

tor_process = stem.process.launch_tor_with_config(
    config = {
        'SocksPort': str(SOCKS_PORT),
        #'ExitNodes': '{ru}',
        },
    init_msg_handler = print_bootstrap_lines,
)

try:
    
    print(term.format("\nChecking our endpoint:\n", term.Attr.BOLD))
    print(term.format(query(r"http://www.sloop1.com/about-neuromarketing-company/"), term.Color.BLUE))
    #print(fakereq(r"http://www.sloop1.com/about-neuromarketing-company/"))
finally:
    tor_process.kill()  # stops tor