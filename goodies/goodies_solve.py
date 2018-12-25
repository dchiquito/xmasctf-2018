
flag_enc_hex = open('flag.enc').read().strip()

flag_enc = flag_enc_hex.decode("hex")
flag_initial = "X-MAS{"
flag_initial_hex = flag_initial.encode("hex")

flag_xor = ""
for i in range(0,len(flag_initial)):
    flag_xor += chr(ord(flag_initial[i]) ^ ord(flag_enc[i]))


print flag_enc_hex[:12] + " ^ " + "X-MAS{".encode("hex")[2:] + " = " + flag_xor.encode("hex")[2:]



class PRNG():
    def __init__(self):
        print "Using manually determined values for IV and MASK:"
        print "IV = 0x44"
        print "MASK = 0xb7"
        self.iv = int("44", 16)
        self.mask8 = int("b7", 16)

    # Parity bit is the most significant bit of the next byte of ciphertext
    def parity(self, next_cipher_byte):
        return ((next_cipher_byte >> 7) ^ 1) & 1

    # Linear-Feedback Shift Register inserts the parity bit on the left of the IV, after shifting IV 1 bit to the right to make room for it
    def LFSR(self, next_cipher_byte):
        return self.iv >> 1 | (self.parity(next_cipher_byte) << 7)

    # Advances the state of the PRNG
    def next(self, next_cipher_byte):
        self.iv = self.LFSR(next_cipher_byte)

    # Get's the next byte of the pseudo-random number stream
    def next_byte(self, next_cipher_byte):
        x = self.iv
        x ^= x >> 16
        x ^= x >> 8
	x &= 255
	x ^= self.mask8
        self.next(next_cipher_byte)
        return x

# Decrypts a string s
def decrypt(s):
    o=''
    for i in range(0,len(s)-1):
        o += chr(ord(s[i]) ^ p.next_byte(ord(s[i+1])))
    # decrypt one last character with an empty next_cipher_byte to get the last character of ciphertext
    o += chr(ord(s[-1]) ^ p.next_byte(0))
    return o

p=PRNG()

print decrypt(flag_enc_hex.decode("hex"))

