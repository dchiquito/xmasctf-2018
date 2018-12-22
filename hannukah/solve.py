from Crypto.Util.number import isPrime
from random import getrandbits

real_pubkey = 577080346122592746450960451960811644036616146551114466727848435471345510503600476295033089858879506008659314011731832530327234404538741244932419600335200164601269385608667547863884257092161720382751699219503255979447796158029804610763137212345011761551677964560842758022253563721669200186956359020683979540809

real_ct = 66888784942083126019153811303159234927089875142104191133776750131159613684832139811204509826271372659492496969532819836891353636503721323922652625216288408158698171649305982910480306402937468863367546112783793370786163668258764837887181566893024918981141432949849964495587061024927468880779183895047695332465


def genKey(k):

	while True:
		r=getrandbits(k)
		while(r%2):
			r=getrandbits(k)
		p =  3 * r**2 +  2 * r + 7331
		q = 17 * r**2 + 18 * r + 1339
		n = p * q

		if(isPrime(p) and isPrime(q)):
			print(r)
			print("hehehehehehe")
			return (p,q) , n

def encrypt(m,pubkey):

	c=m**2 % pubkey
	return c

def keyForR(r):
	p = (3 * r**2 + 2 * r + 7331)
	q = (17 * r**2 + 18 * r + 1339)
	return (p,q,p*q)

def findKey(n):
	minr = 0
	maxr = 2**257
	r = (minr + maxr) / 2
	guess = keyForR(r)[2]
	while guess != n:
		if guess < n:
			minr = r
		else:
			maxr = r
		r = (minr + maxr) / 2
		guess = keyForR(r)[2]
	return r

def gcd(a, b):
	"""Return greatest common divisor using Euclid's Algorithm."""
	while b:      
		a, b = b, a % b
	return a

def lcm(a, b):
	"""Return lowest common multiple."""
	return a * b // gcd(a, b)

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

def decrypt(ct,p,q):
	tot = lcm(p-1,q-1)
	#tot = (p-1)*(q-1)
	print "tot", tot
	d = modinv(2,tot)
	print "d", d
	m = pow(ct, d, p*q)
	return m

r = findKey(real_pubkey)
p,q,n = keyForR(r)

print "p",p
print isPrime(p)
print "q",q
print isPrime(q)
print "n",p*q

print decrypt(real_ct, p, q)







