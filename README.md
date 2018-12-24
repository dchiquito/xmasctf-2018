# x-mas-ctf

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

