from html.parser import HTMLParser
from urllib import parse
from urllib.request import urlopen
from queue import Queue
from domain_name import *
def write_file(base_url):
	f=open('thenewboston.txt','w')
	f.write(base_url)
	f.close()
base_url='https://thenewboston.com/'
page_url='https://thenewboston.com/'
write_file(base_url)
class Linkfinder(HTMLParser):
	def __init__(self,page_url,base_url):
		super().__init__()
		self.page_url=page_url
		self.base_url=base_url
		self.links=[]
		
	def handle_starttag(self,tag,attrs):
		
		if tag=='a':
			for attribute,value in attrs:
				if attribute=='href':
					url=parse.urljoin(self.page_url,value)
					#print(url)
					x=len(url.split('/'))-2
					if x<=5:
						self.links.append(url)
	def page_links(self):
		return self.links


q=Queue()
visited=set()
q.put(base_url)
visited.add(base_url)
v=set()
while not q.empty():
	s=q.get()
	try:
		response=urlopen(s)
		html_byte=response.read()
		html_string=html_byte.decode('utf-8')
		#print(html_string)
		finder=Linkfinder(s,base_url)
		finder.feed(html_string)
		x=finder.page_links()
		f=open('thenewboston.txt','a')
		for i in x:
			domain_name=get_domain_name(i)
			if domain_name not in s:
				continue
			elif i not in visited:
				q.put(i)
				visited.add(i)
				f.write(i+'\n')
	except:
		print('sorry')
