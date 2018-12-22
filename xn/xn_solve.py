from subprocess import *
import time, re
import numpy


def query(i):
	proc = Popen("nc 199.247.6.180 16000", shell=True, stdin=PIPE, stdout=PIPE)
	proc.stdin.write(str(i))
	time.sleep(0.5)
	proc.stdin.write("-1")
	resp = proc.stdout.read()
	pattern = re.compile("The output is. ([0-9]+)")
	match = pattern.search(resp)
	proc.kill()
	return int(match.group(1))

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

L = 36
Q = 1705110751

def genC(x):
	c  = [1] * L
	n = 1
	for i in range(0, L):
		c[i] = n
		#n = (x*n) % Q
		n = x*n
	return c

def fmt(m,a):
	for i in range(0,L):
		print m[i],a[i]
	print

def sub(c1,c2):
	c = [1] * L
	for i in range(0, L):
		#c[i] = (c1[i] - c2[i] + Q) % Q
		c[i] = c1[i] - c2[i]
	return c

def mul(c1,x):
	c = [1] * L
	for i in range(0, L):
		#c[i] = (c1[i] * x)%Q)
		c[i] = c1[i] * x
	return c

def div(c1,x):
	c = [1] * L
	for i in range(0, L):
		c[i] = c1[i] / x
	return c

def evaluate(a, x):
	s = 0
	n = 1
	for i in range(0,L):
		s = (s + a[i]*n) % Q
		n = (n * x) % Q
		#s = s + a[i]*n
		#n = n*x
	return s

def initM():
	m = []
	for i in range(0,L):
		m.append(genC(i))
	return m

def solveRow(m, a, ri, debug=False):
	d = m[ri][ri]
	if debug: print "fixing by",d
	m[ri] = div(m[ri],d)
	if debug: print "(just confirming)",d,"*",modinv(d,Q),"=",(d*modinv(d,Q))%Q
	if debug: print a[ri],"*",modinv(d,Q),"=",(a[ri]*modinv(d,Q))%Q
	a[ri] = (a[ri] * modinv(d, Q))%Q
	#a[ri] = a[ri] / d
	for i in range(0,L):
		if i == ri:
			continue
		if debug: print a[i],"-",a[ri],"*",m[i][ri]
		if debug: print m[i],"-",m[ri],"*",m[i][ri]
		a[i] = (a[i] - a[ri]*m[i][ri])%Q
		m[i] = sub(m[i], mul(m[ri],m[i][ri]))
	return m, a

def solve(m,a,debug=False):
	for i in range(0,L):
		m,a = solveRow(m,a,i,debug)
		if debug:fmt(m,a)
	
	for i in range(0,L):
		a[i] = a[i] % Q
	return m,a

m = initM()
#a = []
#for i in range(0,L):
#	a.append(query(i))
a = [125, 3458, 26558034, 183077483, 25466948, 100036253, 177661991, 306510532, 955557732, 948964581, 1614362586, 454886101, 1267078167, 1550438605, 768330970, 75008836, 1531423755, 37398348, 387921097, 502576854, 1532146839, 1643094778, 929464975, 349767757, 1071157180, 988814302, 231351349, 248138464, 833888087, 1186527016, 822804383, 1467706597, 1580221121, 464257682, 277202332, 357607855, 34823892, 1220259545, 1365269281, 1474828342, 1853079, 412935064, 642963738, 1642262229, 54955869, 1448343961, 1140482158, 67155253, 1060955137, 945678178][:L]
print a

#fmt(m,a)
m,a = solve(m,a)
fmt(m,a)

s = ""
for o in a:
	s = chr(o) + s
print s







