import sys
from md5 import md5

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def _getStrings(length=10):
	for a in alphabet:
		if length <= 1:
			yield a
		else:
			for b in _getStrings(length-1):
				yield a+b

def findCaptcha(cap):
	for c in _getStrings():
		if md5(c).hexdigest()[:5] == cap:
			return c

def handleClient(client):
	cap = client.read("Give a string X such that md5[^=]*=([0-9a-f]{5})\.").group(1)
	client.write(findCaptcha(cap))
	

if __name__ == "__main__":
	if len(sys.argv) > 1:
		print findCaptcha(sys.argv[1])
	else:
		print findCaptcha(raw_input("captcha> "))

