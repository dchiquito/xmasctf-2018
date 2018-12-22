
from nccli import NC
import captcha
from urllib2 import urlopen
import re

def readSequence(client):
	return client.read("\\[([^\\]]+)\\]").group(1).replace(" ", "").split(",")

def lookupSequence(seq):
	page = urlopen("https://oeis.org/search?q=" + "%2C".join(seq))
	raw_html = page.read()
	pattern = re.compile("<tt>[^<]*<b[^<]*</b>, (-?[0-9]+),")
	match = pattern.search(raw_html)
	return match.group(1)


if __name__ == "__main__":
	client = NC("nc 199.247.6.180 14003", False)
	captcha.handleClient(client)
	for i in range(0,25):
		seq = readSequence(client)
		print "Sequence",seq
		next_up = lookupSequence(seq)
		print "Next up",next_up
		client.write(next_up)
	print client.readline()
	print client.readline()
	print client.readline()
	print client.readline()

