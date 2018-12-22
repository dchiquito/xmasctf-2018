# x-mas-ctf

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

