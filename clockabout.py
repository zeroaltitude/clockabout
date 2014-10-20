#!/usr/local/bin/python3

"""\
Clockabout cipher.  A word is enciphered as a product of primes in the following way:

     Let there be the first 26 primes, a = the first, b = the second, etc.
     For each character in a word, let L be its place.
     For example, "apple" has L(a) = 1, L(p) = 2, L(p) = 3, L(l) = 4, L(e) = 5.
     Let n range over the characters in a word.
     Calculate the value of a word as the product of L(n) ^ n.
     According to the order of primes:
     a = 2
     p = 53
     l = 37
     e = 11
     For example, "apple" would be 2 * 53^2 * 53^3 * 37^4 * 11^5.
     This is equal to 252452494140454456046.
     * NB: 12 because a clock has only 12 hours, therefore 43200.
     To represent this product in base 43200 (60 * 60 * 12), we'll represent each digit as a clock with a second hand.
     "apple": [0h 27m 26s] [10h 39m 2s] [0h 13m 12s] [5h 48m 47s] [0h 1m 12s] (little-endian, i.e. most significant clock last)

This cipher can therefore be decoded so long as you can correctly factor the number represented by each clock sequence.
For long words, this can be a challenging problem; however, it is made significantly easier if you realize that the only
primes you need to hunt for are the first 26.  That is the reason this problem is mathematically tractable.

"""

from draw import draw_clock


alphabet = [chr(x) for x in range(97, 123)]
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37,
          41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83,
          89, 97, 101]
inputtxt = "private message https dcdark net CEFAEDFE"

inputtxt = inputtxt.lower()
clockbase = 60 * 60 * 12


def get_clock_digits(prod):
    """base clockbase repr using xh, ym, zs"""
    crepr = ''
    struc = []
    while prod > 0:
        x = 0
        y = 0
        z = 0
        cmod = prod % clockbase
        z = cmod % 60
        y = int(((cmod - z) / 60) % 60)
        x = int((cmod - (y * 60) - z) / (60 * 60))
        crepr += "[%sh %sm %ss - %s] " % (x, y, z, cmod)
        prod = int((prod - cmod) / clockbase)
        struc.append([x, y, z])
    return {'repr': crepr, 'struc': struc}


with open("outfile.txt", 'w', encoding='utf-8') as outfile:
    for word in inputtxt.split(' '):
        # create an integer out of each word using the following scheme:
        # letter 1: n-th prime ^ 1; letter 2: m-th prime ^ 2; letter 3: l-th prime ^ 3, etc
        prod = 1
        for i in range(len(word)):
            prod *= primes[alphabet.index(word[i])] ** (i + 1)
        # determine the digits in clockbase
        clockdigits = get_clock_digits(prod)
        print('word: %s - prod: %s - clockdigits: %s' % (word, prod, clockdigits['repr']), file=outfile)
        for index, digit in enumerate(clockdigits['struc']):
            draw_clock("%s-%s" % (word, index), *digit)
