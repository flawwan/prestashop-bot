import requests
from pyquery import PyQuery as pq
import re
import time
import random
import sys

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.37 (KHTML, like Gecko) Chrome/58.0.3030.110 Safari/537.37',
}

visited = []
def check_eggs(url, stop=False, quick=False):
	if url in visited:
		return
	else:
		visited.append(url)

	time.sleep(random.randint(1,1200)/1000.0)

	r = requests.get(url)
	
	p = pq(r.text)

	scriptvars =  p("script").text()
		
	if "eaHiddenObjectLink" in r.text or "hidden-object-icon" in r.text or "HiddenObjectLink" in r.text:
		eggs = re.findall('var eaHiddenObjectLink = (.*?);\s*', scriptvars, re.M)
		print "Found egg: " + str(eggs[0])
	else:
		#print "No eggs found on url: " + url
		pass
	category = p("input[name=id_category]").attr("value")
	n = p("input[name=n]").attr("value")
	
	if quick:
		return

	if category and not stop: #show all items and check
		all_url = url + "?id_category=" + str(category) + "&n=" + str(n)
		#print "Showing all items on page: " + all_url
		check_eggs(all_url, True)
	else:
		#Check items on page
		for item in p(".ajax_block_product"):
			visit_item_url = p(item)("a").attr("href")
		
		#	print "Bot will now check item: " + visit_item_url
			check_eggs(visit_item_url, True)


url = sys.argv[1]
r = requests.get(url)

links = []

p = pq(r.text)

#Scrape links
for a in p("a"):
	link = p(a).attr("href") 
	#Try to filter out false positives
	if link not in links and "/cart?add" not in link and sys.argv[1] in link:
		links.append(link)

#Check each link for eggs
i = 0	
for url in (links):
	print str(i) + " of " + str(len(links))
	check_eggs(url)	
	i+=1
