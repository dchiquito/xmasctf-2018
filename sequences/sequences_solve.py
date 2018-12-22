
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
		#seq = ['88', '169', '286', '484', '598', '682', '808', '844', '897', '961', '1339', '1573', '1599', '1878', '1986', '2266', '2488', '2626', '2662', '2743', '2938', '3193', '3289', '3751', '3887', '4084', '4444', '4642', '4738', '4804']
		print "Sequence",seq
		next_up = lookupSequence(seq)
		print "Next up",next_up
		client.write(next_up)
	print client.readline()
	print client.readline()
	print client.readline()
	print client.readline()

