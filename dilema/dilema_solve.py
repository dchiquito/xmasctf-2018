from time import sleep
import captcha
from nccli import NC


def readRange(client):
	range_match = client.read("Given a random function defined in range \((-?[0-9]+), (-?[0-9]+)\) find the global maximum of the function")
	return int(range_match.group(1)), int(range_match.group(2))

def queryRange(client, x):
	client.write("1")
	sleep(0.25)
	client.write(str(x))
	return float(client.read(" = (-?[0-9]*\.[0-9]*)").group(1))

def narrowRange(client, mi, ma, step=1):
	max_x = ma
	max_y = queryRange(client, ma)
	x = mi
	while x < ma:
		y = queryRange(client, x)
		print x,y
		if y > max_y:
			max_y = y
			max_x = x
		x += step
	return max_x

def solve(client, global_max):
	client.write("2")
	sleep(0.5)
	client.write(str(global_max))
	return client.read("X-MAS{[^}]*}").group(0)

if __name__ == "__main__":
	client = NC("nc 199.247.6.180 14001", False) # Set to True for debugging
	print "Handling captcha"
	captcha.handleClient(client)
	mi, ma = readRange(client)
	print "Searching", mi, ma
	peak = narrowRange(client, mi, ma, 1)
	print "Peak found at", peak
	peak = narrowRange(client, peak-1, peak+1, 0.1)
	print "Peak found at", peak
	peak = narrowRange(client, peak-0.1, peak+0.1, 0.01)
	print "Peak found at", peak
	peak = narrowRange(client, peak-0.01, peak+0.01, 0.001)
	print "Peak found at", peak
	peak = narrowRange(client, peak-0.001, peak+0.001, 0.0001)
	print "Peak found at", peak
	global_max = queryRange(client,peak)
	print "Global max:",global_max
	flag = solve(client, global_max)
	print flag
