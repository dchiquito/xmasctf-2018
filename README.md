# x-mas-ctf

# A Weird List of Sequences
Logging into the server, we are at once confronted with a captcha prompt:
> CAPTCHA!!!
> Give a string X such that md5(X).hexdigest()[:5]=48e5a.

Ironically this seems very difficult for a human to do, but trivial for a computer ¯\\_(ツ)_/¯
I wrote up a script that hashes random strings until the last 5 digits of the hash matches a given value. See sequences/captcha.py. It reliably finds a match within 10 seconds, which is fast enough.
Now that we are passed the "captcha", we get to the actual problem:

> Hello, litlle one! This time the challenge is very random!
> You will be asked 25 questions where you are given the first 30 terms of a random integer sequence and you will have to determine the next term of that sequence!
> Let's start!
> 
> Question number 1!
> Here's the sequence:
> [0, 0, 1, 0, 2, 2, 2, 4, 6, 7, 8, 13, 15, 21, 25, 30, 39, 50, 58, 74, 89, 105, 129, 156, 185, 221, 264, 309, 366, 433]
> input an integer:

