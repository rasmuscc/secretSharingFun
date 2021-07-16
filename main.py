import os
import random

FIELD_MOD = 10000000

def getSecret(coefs):
    return polyEval(0, coefs)

def reconstructPoly(shares):
    return NotImplemented

def polyEval(x, coefs):
    coefs.reverse()
    y = 0
    for c in range(0, len(coefs)):
        y += coefs[c] * x ** c
    return y % FIELD_MOD

def createShares(secret, n, treshold):
    # If the number of shares is less than t then we can not reconstruct the poly
    if (n < treshold):
        raise Exception

    # Get a random polynomial of degree t-1
    coefs = getRandomPoly(treshold, secret)
    print(coefs)

    # Get n shares, i.e. n points on the polynomial
    # Notice that x = 0 is a very very bad choice
    shares = list()
    for x in range(1, n + 1):
        shares.append((x, polyEval(x, coefs)))

    return shares

def getRandomPoly(treshold, secret):
    coefs = random.SystemRandom().sample(range(0, FIELD_MOD), treshold - 1)
    coefs.append(secret)
    return coefs

if __name__ == '__main__':
    print(createShares(42, 5, 3))