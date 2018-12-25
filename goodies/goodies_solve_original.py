#
# This file was my original solution. I did a lot more messing around and guesswork to obtain the flag. See goodies_solve.py for a much cleaner solution that matches up with the writeup.
#


import os

flag = open('flag.txt').read().strip()

class PRNG():
	def __init__(self):
		self.seed = self.getseed()
		#self.iv = int(bin(self.seed)[2:].zfill(64)[0:32], 2)
		# I had to tune this manually until it worked. Started at the end and worked backwards.
		self.iv =   int('00011100'+'10011110'+'11001110'+'01110101'+'11110001'+'00000000'+'00000000'+'00000000'+'01000100',2)
		#self.key = int(bin(self.seed)[2:].zfill(64)[32:64], 2)
		self.key =  int('00000000',2)
		#self.mask = int(bin(self.seed)[2:].zfill(64)[64:96], 2)
		self.mask = int('10110111',2)
		self.aux = 0
		print("intializing ",self.iv, self.key, self.mask, self.aux)

	def parity(self,x):
		x ^= x >> 16
		x ^= x >> 8
		x ^= x>> 4
		x ^= x>> 2
		x ^= x>> 1
		return x & 1
	
	def getseed(self):
		return int(os.urandom(12).encode('hex'), 16)
	
	def LFSR(self):
		return self.iv >> 1 | (self.parity(self.iv&self.key) << 32)
	
	def next(self):
		self.aux, self.iv = self.iv, self.LFSR()
	
	def next_byte(self):
		#print "iv\t\t",format(self.iv, 'b').zfill(32)
		#x = self.iv ^ self.mask
		x = self.iv & 0xffffffff
		self.next()
		x ^= x >> 16
		x ^= x >> 8
		#print "x\t",format(x&255, 'b').zfill(8)
		return (x & 255)

def encrypt(s):
	o=''
	for x in s:
		o += chr(ord(x) ^ p.next_byte())
	return o.encode('hex')
def demask(s):
	o=''
	for x in s:
		o += chr(ord(x) ^ p.mask)
	return o

p = PRNG()
enc = demask(open('flag_og.enc').read().strip().decode('hex'))
print(enc)
dec = encrypt(enc).decode('hex')
print(dec)
guess = "X-MAS{67812345678123456781234567812345}"
for i in range(0,len(dec)):
	# To be an ascii character, it must be in range [32..127], so the highest bit is always 0
	# also we know the first 6 bytes are 'X-MAS{' so that narrows down the initial value and lets us determine the mask
	print dec[i],"\t",guess[i],"\t",format(ord(dec[i]), 'b').zfill(8), "\t", ((i-1)%8)+1
print dec

if False:
	p=PRNG()

	with open('flag.enc','w') as f:
		f.write(encrypt(flag))
