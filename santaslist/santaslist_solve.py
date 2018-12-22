#!/usr/bin/python3
from Crypto.PublicKey import RSA
from Crypto.Util.number import *
import codecs

def encrypt(m):
    return pow(m, rsa.e, rsa.n)


def decrypt(c):
    return pow(c, rsa.d, rsa.n)

def gcd(x, y):
   while(y): 
       x, y = y, x % y 
   return x

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

s = ord("!") # 33
r = ord("#") # 35
se = int(input("Encrypted '!' > ").strip())
re = int(input("Encrypted '#' > ").strip())
ss = (s ** 65537) - se
rr = (r ** 65537) - re
n = gcd(ss,rr)
print("Found N:", n)

ct = int(input("Hex code > ").strip(), 16)
print(ct)
print("Decrypt this:")
print(ct * pow(n//2,65537,n))
salted = int(input("Decrypted value > "))
plaintext = salted * modinv(n//2, n) % n
print(plaintext)
hextext = hex(plaintext)[2:]
print(hextext)
if len(hextext)%2 == 1:
    hextext = "0"+hextext
print(hextext)
flg = codecs.decode(hextext, "hex")
print(flg)

