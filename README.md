# x-mas-ctf

# Probably Really Nice Goodies from Santa

Just reading the title, we can see a certain acronym looming: PRNG, or Pseudo-Random Number Generator. Inside the provided .zip file are two files, `flag.enc` and `Probably Really Nice Goodies from Santa.py`. The python file is relatively concise:

    import os
    
    flag = open('flag.txt').read().strip()
    
    class PRNG():
            def __init__(self):
                    self.seed = self.getseed()
                    self.iv = int(bin(self.seed)[2:].zfill(64)[0:32], 2)
                    self.key = int(bin(self.seed)[2:].zfill(64)[32:64], 2)
                    self.mask = int(bin(self.seed)[2:].zfill(64)[64:96], 2)
                    self.aux = 0
    
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
                    x = self.iv ^ self.mask
                    self.next()
                    x ^= x >> 16
                    x ^= x >> 8
                    return (x & 255)
    
    def encrypt(s):
        o=''
        for x in s:
            o += chr(ord(x) ^ p.next_byte())
        return o.encode('hex')
    
    p=PRNG()
    
    with open('flag.enc','w') as f:
        f.write(encrypt(flag))

There are three basic parts to this program: the PRNG class which seems to involve a lot of bitwise arithmetic, the encrypt method which seems to encrypt a string, the bits of code that define the flag and that uses these definitions. Let's start at the bottom and work our way up. 

    flag = open('flag.txt').read().strip()
    
    ...
    
    p=PRNG()
    
    with open('flag.enc','w') as f:
        f.write(encrypt(flag))

flag is a string variable which is simply the contents of some flag.txt. We don't have flag.txt, so it's up to us to reverse engineer the value in the flag variable. p is clearly an instance of PRNG, presumable a Pseudo-Random Number Generator. The file flag.enc is opened, then the `encrypt(s)` is called with the flag and written to flag.enc. If we can find a way reverse the encrypt function, we can apply it to the flag.enc file we were provided to find the original key.

    def encrypt(s):
        o=''
        for x in s:
            o += chr(ord(x) ^ p.next_byte())
        return o.encode('hex')

This encrypt method is pretty concise. It just loops through every character `x` in a string, calls `p.next_byte()`, and XORs them together. The XOR function (expressed in Python as the `^` operator) is reversible: if we apply `encrypt(s)` to the ciphertext, we will get the original message back. All that remains is to restore the original state of the PRNG.

    class PRNG():
            def __init__(self):
                    self.seed = self.getseed()
                    self.iv = int(bin(self.seed)[2:].zfill(64)[0:32], 2)
                    self.key = int(bin(self.seed)[2:].zfill(64)[32:64], 2)
                    self.mask = int(bin(self.seed)[2:].zfill(64)[64:96], 2)
                    self.aux = 0
    
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
                    x = self.iv ^ self.mask
                    self.next()
                    x ^= x >> 16
                    x ^= x >> 8
                    return (x & 255)

This is the heart of the problem. The first line of the constructor sets `self.seed = self.getseed()`, which uses `os.urandom(12)` to generate a random 96 bit integer. The constructor then unpacks self.seed into 3 32 bit chunks, which are put into self.iv, self.key, and self.mask. To my knowledge, there is no way for us to guess the random number provided by `os.urandom`, which uses the Operating System's random number generator. This means we have no information whatsoever about the initial values of the IV (Initial Value), Key, and Mask. As far as I can tell, self.aux is irrelevant.

Let's continue reading with `next_byte()`. First x is set to the XOR of IV and Mask. `self.next()` is then called, which presumably changes the state of the PRNG so that the next call to `next_byte()` returns a different value. The last few lines basically XOR different bits of X with itself, like this example with a random x:

    x is a 32 bit integer

   |               |               |               |               |
    1 1 0 1 1 1 0 0 0 0 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 1 1 0 1 1
   |     8 bits    |     8 bits    |     8 bits    |     8 bits    |

    x ^= x >> 16
    which is the same as:
    x = x ^ (x >> 16)

   x
   |               |               |               |               |
    1 1 0 1 1 1 0 0 0 0 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 1 1 0 1 1
   |               |               |               |               |
   x >> 16
   |               |               |               |               |
   |               |                1 1 0 1 1 1 0 0 0 0 1 0 0 0 1 0
   |               |               |               |               |
   x ^ x >> 16
   |               |               |               |               |
    1 1 0 1 1 1 0 0 0 0 1 0 0 0 1 0 1 1 0 0 0 0 0 1 0 0 1 1 1 0 0 1
   |  irrelevant   |  irrelevant   |               |               |


   x ^= x >> 8
   x
   |               |               |               |               |
    1 1 0 1 1 1 0 0 0 0 1 0 0 0 1 0 1 1 0 0 0 0 0 1 0 0 1 1 1 0 0 1
   |  irrelevant   |  irrelevant   |               |               |
   x >> 8
   |               |               |               |               |
                    1 1 0 1 1 1 0 0 0 0 1 0 0 0 1 0 1 1 0 0 0 0 0 1
   |               |  irrelevant   |  irrelevant   |               |
   x ^ x >> 8
   |               |               |               |               |
    1 1 0 1 1 1 0 0 1 1 1 1 1 1 1 0 1 1 1 0 0 0 1 1 1 1 1 1 1 0 0 0
   |  irrelevant   |  irrelevant   |  irrelevant   |               |
   
   I have been marking bytes as irrelevant, because the last step is to AND x with 255, which has a convenient value in binary:
   
   return x & 255
   x
   |               |               |               |               |
    1 1 0 1 1 1 0 0 1 1 1 1 1 1 1 0 1 1 1 0 0 0 1 1 1 1 1 1 1 0 0 0
   |               |               |               |               |
   255
   |               |               |               |               |
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1
   |               |               |               |               |
   x ^ 255
   |               |               |               |               |
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 0 0 0
   |               |               |               |               |
 
Essentially, x is folded into itself to reduce it from a 32 bit int to an 8 bit byte. I explicitly went through this process because it will be done again in `parity(x)`. 

OK, back to the `next()` function:

            def parity(self,x):
                    x ^= x >> 16
                    x ^= x >> 8
                    x ^= x>> 4
                    x ^= x>> 2
                    x ^= x>> 1
                    return x & 1
   
            ... 
    
            def LFSR(self):
                    return self.iv >> 1 | (self.parity(self.iv&self.key) << 32)
    
            def next(self):
                    self.aux, self.iv = self.iv, self.LFSR()
    
`next()` simply sets self.iv to `LFSR()` (and also sets self.aux, but this appears to be irrelevant). `LFSR()` ([Linear-Feedback Shift Register](https://en.wikipedia.org/wiki/Linear-feedback_shift_register)) does some interesting bitwise arithmetic. `parity(x)` is used to employ a similar folding algorithm to the one used above to collapse (IV AND Key) into a single bit. IV is then shifted to the right one bit, then that parity bit is inserted on the far left of the IV. The resulting value is the new IV.

PRNG has a lot of technical things going on, so lets sum up what we know about it. Only the IV ever actually changes; Key and Mask both remain constant. Mask XOR IV is used to garble up the IV before it is used as the next random byte. Key XOR IV is used to garble up the IV before the parity bit is calculated, and IV is shifted to the right by one bit to make room for the parity bit.

This is pretty difficult. We need to determine three different random 32 bit integers before we have any chance of decrypting our flag. Once we have the initial state of the PRNG, we will be set. Unfortunately, the only information we have about the initial state is the encrypted flag:

ab38abdef046216128f8ea76ccfcd38a4a8649802e95f817a2fc945dc04a966d502ef1e31d0a2d

Fortunately, we do know one more thing: the first six characters of the flag. All X-Mas CTF flags are formatted like this: `X-MAS{...}` (which can be hex encoded into `582d4d41537b...7d`). Considering only the very first byte, before any of the shifting occurs, we know that `0x58 XOR collapse_to_8_bits(IV XOR MASK) = 0xab`. Because of how XOR's algebraic properties (`X XOR X = 0`, `X XOR 0 = X`, and `X XOR Y = Y XOR X`), we also know that `collapse_to_8_bits(IV XOR MASK) = 0x58 XOR 0xab = 0xf3`. I am going to handwave my hands around some algebra and assert that `collapse_to_8_bits(IV XOR MASK) = collapse_to_8_bits(IV) XOR collapse_to_8_bits(MASK)`. This allows us to reduce the 32 bit value of MASK to an 8 bit value, MASK8: `MASK8 = collapse_to_8_bits(MASK)`. This ultimately gives us:

    collapse_to_8_bits(IV) XOR MASK8 = 0xf3

Now we stand a chance at determining MASK8.


# Santa's List

Logging into the server, we see the following prompt:

    Ho, ho, ho and welcome back!
    Your list for this year:
    
    Sarah - Nice
    Bob - Nice
    Eve - Naughty
    Galf - 25898466163a90f42702135d867da28e83bdfb8e65cd8e63b2a55912dcfc7cf27dc90ea3b7704e322c71a0ca94dbb082c4ed60d8f047cd97799b199371dff074f7cfb65fe720a091d89b0a517e42f2698d069a7187f5eb5b852078ca88ba1a0f1c7fa66435df4eeadce529799e95e258ad45813c778633c3d1f9f3375f8097d8
    Alice - Nice
    Johnny - Naughty
    
    [1] Encrypt
    [2] Decrypt
    [3] Exit

Exploring the options, we have the ability to:

1. Encrypt an arbitrary string. This gives us a large integer.
2. Decrypt an integer. This also gives us a large integer.
3. Exit. Not very interesting.

Clearly, "Galf" has an interesting Naughty/Nice value. It appears to be a hex encoded value. Unfortunately it does not decode to a string, and it unpacks to a very large integer. Decrypting this integer gives the result `Ho, ho ho, no...`. Note that opening the server again will give Galf a different value.

Along with the nc server, we were given `santas_list.zip`. This archive contains one file, `list.py`. Reading this file, it is clearly the same one running on the server. `list.py` basically:

* Generates a random RSA key
* Opens the file `flag.txt`, encrypts it, converts it to hex, and displays it in the opening message
* Listens for user input
  * When encrypting, it simply converts the text to hex, converts that to a long, and encrypts it. However, it also adds the numerical plaintext to the list `used`.
  * When decrypting, it first checks that the value isn't the encrypted flag (which is why we were unable to decrypt it previously). After decrypting, it also checks that `message % previous != 0` for every previous in the list `used`. This will be important later.

So we have access to an encrypted flag (C = M<sup>e</sup> (mod N)), an RSA encrypt function (X<sup>e</sup> (mod N)), and an RSA decrypt function that doesn't allow us to decrypt `C` directly. There is an attack called [Blinding](https://en.wikipedia.org/wiki/Blinding_(cryptography)) which allows us to modify the ciphertext, decrypt that modified value, then un-modify it. Basically, we need an arbitrary message `S` which we will encrypt (S<sup>e</sup> (mod N)), then multiply it by the ciphertext (CS<sup>e</sup> = M<sup>e</sup>S<sup>e</sup> = MS<sup>e</sup> (mod N)), decrypt that ((MS<sup>e</sup>)<sup>d</sup> ≅ MS (mod N)), then divide by `S` to get the original `M`. Note that we can't necessarily use normal integer division because of modular arithmetic. Instead, we must calculate the modular inverse of `S (mod N)` and multiply by that. 

However, the modulo check in the decrypt step blocks this plan. If we encrypt `S` using the Encrypt function, it will be recorded in `used`. When we try to multiply the ciphertext by the encrypted `S` and decrypt that, it will notice that the result is divisible by `S` and block our decryption attempt. We need a way to avoid this check. If we can find a way to encrypt `S` without using the Encrypt function, we will be able to use Decrypt.

The RSA encrypt function is simply M<sup>e</sup> (mod N). By running `list.py` and adding some debug statements, we can determine that `e` is 65537, a very common value. Unfortunately, it appears that N is randomized every time `list.py` is run, so we will have to find a way to determine it using only what we can get out of the prompt. Let's do some number theory:

RSA encryption:

x<sup>e</sup> ≅ C<sub>x</sub> (mod N)

x<sup>e</sup> = C<sub>x</sub> + kN (for some value of k)

x<sup>e</sup> - C<sub>x</sub> = kN

y<sup>e</sup> - C<sub>y</sub> = jN (same equation, but different value for x)

Note that the Greatest Common Denominator (GCD) of kN and jN is N. For reasonably small values of `x` and `y`, we can use [Euclid's Algorithm](https://en.wikipedia.org/wiki/Greatest_common_divisor#Using_Euclid's_algorithm) to determine N in a reasonable amount of time. 

Practically speaking, the smallest values of `x` and `y` I could easily find were 33 and 35, which correspond to characters '!' and '#'. We can Encrypt these strings using the prompt, then calculate `N` using the following code:

    cx = Encrypt('!') # 33
    cy = Encrypt('#') # 35
    kn = (33 ** 65537) - cx
    jn = (35 ** 65537) - cy
    N = gcd(kn, jn)

Now that we know `N`, we can encrypt anything we want without using the server. We will now pick an arbitrary `S` (I used `N/2`), then use the above blinding attack to decrypt the encrypted ciphertext. See `/santaslist/santaslist_solve.py` for my solution.

# Santa's List 2.0

Reading the source provided in Santa's List 2.0, the only difference is that there is a limit of 5 requests to the server. Fortunately, our previous solution only requires 3 requests: 2 for encrypting '!' and '#', and 1 for decrypting the modified ciphertext. See the above solution.

# A Weird List of Sequences

Logging into the server, we are at once confronted with a captcha prompt:

    CAPTCHA!!!
    Give a string X such that md5(X).hexdigest()[:5]=48e5a.

Ironically this seems very difficult for a human to do, but trivial for a computer `¯\_(ツ)_/¯`

I wrote up a script that hashes random strings until the last 5 digits of the hash matches a given value. See sequences/captcha.py. It reliably finds a match within 10 seconds, which is fast enough.

Now that we are passed the "captcha", we get to the actual problem:

    Hello, litlle one! This time the challenge is very random!
    You will be asked 25 questions where you are given the first 30 terms of a random integer sequence and you will have to determine the next term of that sequence!
    Let's start!
    
    Question number 1!
    Here's the sequence:
    [0, 0, 1, 0, 2, 2, 2, 4, 6, 7, 8, 13, 15, 21, 25, 30, 39, 50, 58, 74, 89, 105, 129, 156, 185, 221, 264, 309, 366, 433]
    input an integer:

I have no idea what this series is. Fortunately, I have heard of a site called [OEIS](https://oeis.org/). The On-Line Encyclopedia of Integer Sequences is a huge repository of lists of numbers. Pasting the given series in to the search bar, we discover that this is the "Number of partitions of n such that there is exactly one part which occurs twice, while all other parts occur only once", and the next value is `505`. We plug in this value into the server and get this:

    Good job, next question!
    
    Question number 2!
    Here's the sequence:
    [1, 1, 2, 3, 5, 7, 0, 4, 0, 8, 9, 1, 0, 2, 3, 0, 0, 0, 0, 6, 0, 0, 1, 1, 2, 0, 5, 7, 0, 0]
    input an integer:

Clearly this is going to be tedious. We could probably do this manually 25 times, but I have had problems in past CTFs with `nc` connections timing out prematurely. Instead, we will use Python's `urllib2` to query the OEIS and scrape the page data to determine the next value in the sequence. This is the function I wrote to accomplish this:

    def lookupSequence(seq):
        page = urlopen("https://oeis.org/search?q=" + "%2C".join(seq))
        raw_html = page.read()
        pattern = re.compile("<tt>[^<]*<b[^<]*</b>, (-?[0-9]+),")
        match = pattern.search(raw_html)
        return match.group(1)

To make the automation process cleaner, I also wrote sequences/nccli.py to provide the NC class, which serves as a simple wrapper around the `nc` command. This allows my script to directly interface with the server.

See sequences/sequences\_solve.py for the final solution script.

